"""Next command - intelligently suggest next task to work on."""

from pathlib import Path
from typing import Optional, List, Tuple

from ..core import get_all_initiatives, categorize_initiatives
from ..models import Initiative, Task
from ..utils import Colors, extract_tasks


def next_command(
    base_path: Path = Path("."),
    show_all: bool = False,
    initiative_dir: Optional[str] = None,
    agent: Optional[str] = None,
    agent_initiatives: Optional[str] = None
) -> int:
    """Intelligently suggest next task to work on.
    
    Args:
        base_path: Base path to search from
        show_all: Whether to show next task for each active initiative
        initiative_dir: Specific initiative directory to check
        agent: Agent name (for swarm coordination)
        agent_initiatives: Comma-separated list of initiative dirs assigned to agent
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Handle agent mode (for swarm coordination)
    if agent:
        return _next_for_agent(base_path, agent, agent_initiatives)
    
    # Get all initiatives
    initiatives = get_all_initiatives(base_path)
    
    if not initiatives:
        print(f"{Colors.RED}❌ No initiatives found{Colors.NC}")
        return 1
    
    if initiative_dir:
        # Find specific initiative
        initiative = next((i for i in initiatives if i.directory.name == initiative_dir), None)
        if not initiative:
            print(f"{Colors.RED}❌ Initiative not found: {initiative_dir}{Colors.NC}")
            return 1
        
        next_task = _get_next_task_for_initiative(initiative, initiatives)
        if next_task:
            _print_next_task(initiative, next_task)
            return 0
        else:
            print(f"{Colors.YELLOW}⚠️  No available tasks for {initiative.name}{Colors.NC}")
            return 1
    
    # Categorize initiatives
    active, completed, not_started, cancelled = categorize_initiatives(initiatives)
    
    if show_all:
        # Show next task for each active initiative
        if not active:
            print(f"{Colors.YELLOW}⚠️  No active initiatives{Colors.NC}")
            if not_started:
                print()
                print(f"{Colors.BOLD}Not started initiatives:{Colors.NC}")
                for init in not_started[:3]:
                    if init.task_count == 0:
                        print(f"  • {init.name}: Run /aipo-create-tasks {init.directory.name}")
                    else:
                        print(f"  • {init.name}: Run /start-task {init.directory.name} TASK-001")
            return 1
        
        print(f"{Colors.BOLD}📋 Next Tasks for Active Initiatives:{Colors.NC}")
        print()
        
        for initiative in active:
            next_task = _get_next_task_for_initiative(initiative, initiatives)
            if next_task:
                _print_next_task(initiative, next_task, compact=True)
            else:
                print(f"  {Colors.GREEN}✓{Colors.NC} {initiative.name}: All tasks complete!")
            print()
        
        return 0
    
    # Single next task recommendation
    print(f"{Colors.BOLD}🎯 Next Recommended Task:{Colors.NC}")
    print()
    
    # Priority order:
    # 1. Active initiatives with pending tasks
    # 2. Not started initiatives with generated tasks
    # 3. Not started initiatives without tasks
    
    candidates = []
    
    # Check active initiatives
    for initiative in active:
        next_task = _get_next_task_for_initiative(initiative, initiatives)
        if next_task:
            # Calculate priority score
            # - Lower completion % = higher priority
            # - Consider dependencies
            priority = 100 - initiative.progress_percentage
            candidates.append((priority, initiative, next_task))
    
    if candidates:
        # Sort by priority (highest first)
        candidates.sort(key=lambda x: x[0], reverse=True)
        priority, initiative, next_task = candidates[0]
        
        _print_next_task(initiative, next_task)
        
        # Show alternatives if any
        if len(candidates) > 1:
            print()
            print(f"{Colors.BOLD}Other options:{Colors.NC}")
            for _, alt_init, alt_task in candidates[1:3]:  # Show up to 2 more
                print(f"  • {alt_init.name}: {alt_task.id} - {alt_task.title}")
        
        return 0
    
    # No active tasks, suggest starting a new initiative
    if not_started:
        initiative = not_started[0]
        print(f"All active initiatives are blocked or complete.")
        print()
        print(f"Start next initiative: {Colors.BOLD}{initiative.name}{Colors.NC}")
        if initiative.task_count == 0:
            print(f"Command: {Colors.GREEN}/aipo-create-tasks {initiative.directory.name}{Colors.NC}")
        else:
            print(f"Command: {Colors.GREEN}/start-task {initiative.directory.name} TASK-001{Colors.NC}")
        return 0
    
    # Everything is complete!
    print(f"{Colors.GREEN}🎉 All initiatives complete!{Colors.NC}")
    return 0


def _get_next_task_for_initiative(initiative: Initiative, all_initiatives: List[Initiative]) -> Optional[Task]:
    """Get the next available task for an initiative.
    
    Args:
        initiative: Initiative to check
        all_initiatives: All initiatives (for dependency checking)
        
    Returns:
        Next Task object or None
    """
    if not initiative.is_active:
        return None
    
    tasks_file = initiative.directory / "tasks.prd"
    if not tasks_file.exists():
        return None
    
    tasks_data = extract_tasks(tasks_file)
    if not tasks_data:
        return None
    
    # Convert to Task objects
    tasks = [
        Task(
            id=t['id'],
            title=t['title'],
            status=t['status'],
            group=t.get('group', 0)
        )
        for t in tasks_data
    ]
    
    # Find current group (highest group with completed or in-progress tasks)
    current_group = max(
        (t.group for t in tasks if t.is_completed or t.is_in_progress),
        default=0
    )
    
    # Check if current group is complete
    current_group_tasks = [t for t in tasks if t.group == current_group]
    current_group_complete = all(t.is_completed for t in current_group_tasks)
    
    # If current group is complete, move to next group
    if current_group_complete:
        # Check if dependencies for next group are satisfied
        next_group = current_group + 1
        next_group_tasks = [t for t in tasks if t.group == next_group]
        
        if next_group_tasks:
            # Dependencies satisfied, use next group
            current_group = next_group
        else:
            # No more tasks
            return None
    
    # Find first pending task in current group
    pending_tasks = [
        t for t in tasks
        if t.group == current_group and t.is_pending
    ]
    
    return pending_tasks[0] if pending_tasks else None


def _next_for_agent(base_path: Path, agent: str, agent_initiatives: Optional[str]) -> int:
    """Get next task for a specific agent in swarm mode.
    
    Reads agent assignments from tasks.prd files (Agent: field).
    
    Args:
        base_path: Base path to search from
        agent: Agent name
        agent_initiatives: Comma-separated list of initiative dirs (optional, deprecated)
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Get all initiatives
    all_initiatives = get_all_initiatives(base_path)
    
    if not all_initiatives:
        print(f"{agent}: No initiatives found")
        return 1
    
    # Find all tasks assigned to this agent across all initiatives
    agent_tasks = []
    
    for initiative in all_initiatives:
        if not initiative.is_active:
            continue
            
        tasks_file = initiative.directory / "tasks.prd"
        if not tasks_file.exists():
            continue
        
        # Read tasks and find those assigned to this agent
        tasks_data = extract_tasks(tasks_file)
        if not tasks_data:
            continue
        
        # Convert to Task objects and filter by agent assignment
        for task_data in tasks_data:
            task = Task(
                id=task_data['id'],
                title=task_data['title'],
                status=task_data['status'],
                group=task_data.get('group', 0)
            )
            
            # Check if task is assigned to this agent
            task_agent = _extract_agent_from_task(tasks_file, task.id)
            if task_agent == agent and task.is_pending:
                # Add to candidates with priority
                # Priority: group number (lower first), then task number
                priority = (task.group, int(task.id.split('-')[1]))
                agent_tasks.append((priority, initiative, task))
    
    if not agent_tasks:
        print(f"{agent}: All assigned tasks complete")
        return 0
    
    # Sort by priority (lowest group first, then task number)
    agent_tasks.sort(key=lambda x: x[0])
    _, initiative, task = agent_tasks[0]
    
    # Output format for coordinator
    print(f"{agent}: /start-task {initiative.directory.name} {task.id}")
    
    return 0


def _extract_agent_from_task(tasks_file: Path, task_id: str) -> Optional[str]:
    """Extract agent assignment from a task in tasks.prd.
    
    Args:
        tasks_file: Path to tasks.prd
        task_id: Task ID to find
        
    Returns:
        Agent name or None
    """
    try:
        content = tasks_file.read_text()
        lines = content.split('\n')
        
        # Find the task line
        in_task = False
        for i, line in enumerate(lines):
            if task_id in line and line.strip().startswith('-'):
                in_task = True
                continue
            
            if in_task:
                # Look for Agent: field
                if line.strip().startswith('- Agent:'):
                    agent = line.split(':', 1)[1].strip()
                    return agent
                # Stop if we hit another task or section
                elif line.strip().startswith('- [') or line.strip().startswith('##'):
                    break
        
        return None
    except Exception:
        return None


def _print_next_task(initiative: Initiative, task: Task, compact: bool = False) -> None:
    """Print next task recommendation.
    
    Args:
        initiative: Initiative containing the task
        task: Task to print
        compact: Whether to use compact format
    """
    if compact:
        print(f"  {Colors.GREEN}→{Colors.NC} {initiative.name}")
        print(f"    {task.id}: {task.title}")
        print(f"    Command: {Colors.GREEN}/start-task {initiative.directory.name} {task.id}{Colors.NC}")
    else:
        print(f"Initiative: {Colors.BOLD}{initiative.name}{Colors.NC}")
        print(f"Progress: {initiative.completed_count}/{initiative.task_count} ({initiative.progress_percentage:.0f}%)")
        print()
        print(f"Next Task: {Colors.BOLD}{task.id}{Colors.NC}")
        print(f"Title: {task.title}")
        print(f"Group: {task.group}")
        print()
        print(f"Command: {Colors.GREEN}/start-task {initiative.directory.name} {task.id}{Colors.NC}")

