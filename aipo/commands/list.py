"""List command - list all initiatives."""

from pathlib import Path

from ..core import get_all_initiatives
from ..models import Status
from ..utils import Colors


def list_initiatives(base_path: Path = Path(".")) -> int:
    """List all initiatives in the project.
    
    Args:
        base_path: Base path to search from
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    initiatives_dir = base_path / "ai-project" / "initiatives"

    if not initiatives_dir.exists():
        print(f"{Colors.RED}❌ Error: Initiatives directory not found{Colors.NC}")
        print(f"   Looking for: {initiatives_dir}")
        return 1

    initiatives = get_all_initiatives(base_path)

    if not initiatives:
        print("No initiatives found")
        return 0

    print(f"{Colors.BOLD}Initiatives:{Colors.NC}")
    print()

    for initiative in initiatives:
        # Determine status emoji
        if initiative.status == Status.READY:
            emoji = "✅"
        elif initiative.status == Status.WARNING:
            emoji = "⚠️ "
        else:
            emoji = "❌"

        # Format task info
        if initiative.task_count == 0:
            tasks_info = "(no tasks)"
        elif initiative.completed_count > 0:
            tasks_info = f"({initiative.completed_count}/{initiative.task_count} tasks)"
        else:
            tasks_info = f"({initiative.task_count} tasks)"

        print(f"  {emoji} {initiative.name} {tasks_info}")

    return 0

