"""Utility functions for AI Project Orchestrator."""

import re
from pathlib import Path
from typing import List, Dict


class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    NC = '\033[0m'  # No Color

    @classmethod
    def disable(cls):
        """Disable colors for non-TTY output."""
        cls.RED = cls.GREEN = cls.YELLOW = cls.BLUE = cls.BOLD = cls.DIM = cls.NC = ''


def create_progress_bar(completed: int, total: int, width: int = 20) -> str:
    """Create a visual progress bar.
    
    Args:
        completed: Number of completed items
        total: Total number of items
        width: Width of the progress bar in characters
        
    Returns:
        String representation of the progress bar
    """
    if total == 0:
        return "[" + " " * width + "]"
    
    filled = int(width * completed / total)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}]"


def extract_tasks(tasks_file: Path) -> List[Dict]:
    """Extract task list from tasks.prd file.
    
    Args:
        tasks_file: Path to tasks.prd file
        
    Returns:
        List of task dictionaries with id, title, status, and group
    """
    content = tasks_file.read_text()
    tasks = []
    
    # Find all task entries
    task_pattern = re.compile(r'^- \[([x ])\] (TASK-\d+):\s*(.+)$', re.MULTILINE)
    
    # Track current group
    current_group = 0
    group_pattern = re.compile(r'^## Task Group (\d+):', re.MULTILINE)
    
    # Build a map of line numbers to groups
    line_to_group = {}
    lines = content.split('\n')
    for i, line in enumerate(lines):
        group_match = group_pattern.match(line)
        if group_match:
            current_group = int(group_match.group(1))
        line_to_group[i] = current_group
    
    # Find tasks
    for match in task_pattern.finditer(content):
        checkbox, task_id, title = match.groups()
        status = 'completed' if checkbox == 'x' else 'pending'
        
        # Find which line this task is on
        line_num = content[:match.start()].count('\n')
        group = line_to_group.get(line_num, 0)
        
        # Check if it's marked as in progress (heuristic: look for common markers)
        task_line_start = match.start()
        context = content[task_line_start:task_line_start+200]
        if '(in progress)' in context.lower() or '🔄' in context:
            status = 'in_progress'
        
        tasks.append({
            'id': task_id,
            'title': title.strip(),
            'status': status,
            'group': group
        })
    
    return tasks


def extract_initiative_ids(swarm_file: Path) -> List[str]:
    """Extract initiative IDs from swarm YAML file.
    
    Looks for patterns like:
    - "Initiative 0003"
    - "0004-backend-api"
    
    Args:
        swarm_file: Path to swarm YAML file
        
    Returns:
        Sorted list of initiative IDs
    """
    content = swarm_file.read_text()

    # Find patterns like "Initiative 0003" or "initiative 0003"
    pattern1 = re.findall(r'[Ii]nitiative\s+(\d{4})', content)

    # Find patterns like "0004-backend-api" in paths or descriptions
    pattern2 = re.findall(r'\b(\d{4})-[a-z][a-z0-9-]*', content)

    # Combine and deduplicate
    all_ids = set(pattern1 + pattern2)

    return sorted(list(all_ids))


def find_initiative_directory(initiative_id: str, base_path: Path) -> Path | None:
    """Find the directory for an initiative ID.
    
    Args:
        initiative_id: The initiative ID (e.g., "0001")
        base_path: Base path to search from
        
    Returns:
        Path to initiative directory or None if not found
    """
    initiatives_dir = base_path / "ai-project" / "initiatives"

    if not initiatives_dir.exists():
        return None

    # Look for directories matching the pattern NNNN-*
    for directory in initiatives_dir.iterdir():
        if directory.is_dir() and directory.name.startswith(f"{initiative_id}-"):
            return directory

    return None


def format_time_estimate(hours: float) -> str:
    """Format time estimate in human-readable format.
    
    Args:
        hours: Number of hours
        
    Returns:
        Formatted string (e.g., "2h", "1d 4h", "2w 3d")
    """
    if hours < 1:
        return f"{int(hours * 60)}m"
    elif hours < 24:
        return f"{hours:.1f}h"
    elif hours < 168:  # Less than a week
        days = hours / 8  # Assuming 8-hour workdays
        return f"{days:.1f}d"
    else:
        weeks = hours / 40  # Assuming 40-hour workweek
        return f"{weeks:.1f}w"

