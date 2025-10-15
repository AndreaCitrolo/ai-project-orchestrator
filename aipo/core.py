"""Core validation and analysis functions."""

import re
from pathlib import Path
from typing import List, Tuple

from .models import Initiative, Status


def validate_initiative(directory: Path) -> Initiative:
    """Validate a single initiative directory.
    
    Args:
        directory: Path to initiative directory
        
    Returns:
        Initiative object with validation results
    """
    name = directory.name
    init_id = name.split('-')[0]

    initiative = Initiative(
        id=init_id,
        name=name,
        directory=directory,
        status=Status.READY
    )

    # Check for required files
    description_file = directory / "description.prd"
    tasks_file = directory / "tasks.prd"

    if not description_file.exists():
        initiative.issues.append("Missing description.prd")
        initiative.status = Status.BLOCKED

    if not tasks_file.exists():
        initiative.issues.append("Missing tasks.prd")
        initiative.status = Status.BLOCKED
        return initiative

    # Validate tasks.prd content
    tasks_content = tasks_file.read_text()

    # Validate new format structure
    if "**ID**:" not in tasks_content:
        initiative.warnings.append("tasks.prd missing metadata section (**ID**:)")
        if initiative.status == Status.READY:
            initiative.status = Status.WARNING

    if "## Summary" not in tasks_content:
        initiative.warnings.append("tasks.prd missing Summary section")
        if initiative.status == Status.READY:
            initiative.status = Status.WARNING

    # Extract metadata
    _extract_initiative_metadata(initiative, tasks_content)

    # Check for [START: ] and [END: ] markers and extract timestamps
    start_match = re.search(r'\[START:\s*([^\]]*)\]', tasks_content)
    end_match = re.search(r'\[END:\s*([^\]]*)\]', tasks_content)
    
    if start_match:
        initiative.started_at = start_match.group(1).strip() or None
    elif initiative.completed_count > 0:
        # Only warn if tasks are completed but no START marker
        initiative.warnings.append("tasks.prd missing [START: ] marker but has completed tasks")
        if initiative.status == Status.READY:
            initiative.status = Status.WARNING
    
    if end_match:
        initiative.ended_at = end_match.group(1).strip() or None

    # Count all tasks: both pending [ ] and completed [x]
    all_task_matches = re.findall(r'^- \[[x ]\] TASK-\d+', tasks_content, re.MULTILINE)
    initiative.task_count = len(all_task_matches)

    # Count completed tasks
    completed_matches = re.findall(r'^- \[x\] TASK-\d+', tasks_content, re.MULTILINE)
    initiative.completed_count = len(completed_matches)

    if initiative.task_count == 0:
        initiative.issues.append("tasks.prd exists but has no tasks defined")
        initiative.status = Status.BLOCKED

    # Check status from Summary section
    status_match = re.search(r'\*\*Status\*\*:\s*([^\n]+)', tasks_content)
    if status_match:
        initiative.summary_status = status_match.group(1).strip()
        summary_status = initiative.summary_status.lower()
        
        # Check for cancelled status - BLOCKING
        if "cancelled" in summary_status:
            initiative.issues.append("Initiative is marked as cancelled")
            initiative.status = Status.BLOCKED
        
        # Check for completed status - BLOCKING (completed initiatives shouldn't be in swarm)
        if "completed" in summary_status:
            initiative.issues.append("Initiative already completed - remove from swarm")
            initiative.status = Status.BLOCKED

    # Check coherence between tasks and Summary status
    if initiative.task_count > 0:
        pending_count = initiative.task_count - initiative.completed_count

        # All tasks completed but Summary not marked as completed
        if pending_count == 0:
            if status_match and "completed" not in status_match.group(1).lower():
                initiative.warnings.append(
                    f"All {initiative.task_count} tasks completed but Summary status not marked as Completed"
                )
                if initiative.status == Status.READY:
                    initiative.status = Status.WARNING
        
        # Has completed tasks but Summary says "not started"
        if initiative.completed_count > 0 and status_match:
            if "not started" in status_match.group(1).lower():
                initiative.warnings.append(
                    f"Has {initiative.completed_count}/{initiative.task_count} completed tasks but Summary says 'Not started'"
                )
                if initiative.status == Status.READY:
                    initiative.status = Status.WARNING

    # Warnings for large initiatives
    if initiative.task_count > 50:
        initiative.warnings.append(f"Large number of tasks ({initiative.task_count})")
        if initiative.status == Status.READY:
            initiative.status = Status.WARNING

    return initiative


def _extract_initiative_metadata(initiative: Initiative, content: str) -> None:
    """Extract metadata from tasks.prd content.
    
    Args:
        initiative: Initiative object to populate
        content: Content of tasks.prd file
    """
    # Extract dependencies
    deps_match = re.search(r'\*\*Dependencies\*\*:\s*([^\n]+)', content)
    if deps_match:
        deps_text = deps_match.group(1).strip()
        if deps_text.lower() != 'none':
            # Parse comma-separated list of dependencies
            initiative.dependencies = [d.strip() for d in deps_text.split(',')]
    
    # Extract target date
    date_match = re.search(r'\*\*Target Date\*\*:\s*([^\n]+)', content)
    if date_match:
        initiative.target_date = date_match.group(1).strip()
    
    # Extract estimated hours
    hours_match = re.search(r'\*\*Estimated Hours\*\*:\s*(\d+)', content)
    if hours_match:
        initiative.estimated_hours = int(hours_match.group(1))


def get_all_initiatives(base_path: Path = Path(".")) -> List[Initiative]:
    """Get all initiatives in the project.
    
    Args:
        base_path: Base path to search from
        
    Returns:
        List of Initiative objects
    """
    initiatives_dir = base_path / "ai-project" / "initiatives"

    if not initiatives_dir.exists():
        return []

    directories = sorted([
        d for d in initiatives_dir.iterdir()
        if d.is_dir() and d.name[0].isdigit()
    ])

    return [validate_initiative(d) for d in directories]


def categorize_initiatives(initiatives: List[Initiative]) -> Tuple[List[Initiative], List[Initiative], List[Initiative], List[Initiative]]:
    """Categorize initiatives by their status.
    
    Args:
        initiatives: List of Initiative objects
        
    Returns:
        Tuple of (active, completed, not_started, cancelled) initiative lists
    """
    active = []
    completed = []
    not_started = []
    cancelled = []
    
    for initiative in initiatives:
        if initiative.is_cancelled:
            cancelled.append(initiative)
        elif initiative.is_completed:
            completed.append(initiative)
        elif initiative.is_active:
            active.append(initiative)
        else:
            not_started.append(initiative)
    
    return active, completed, not_started, cancelled

