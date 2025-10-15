"""Check command - check a single initiative."""

from pathlib import Path

from ..core import validate_initiative
from ..models import Status
from ..utils import Colors


def check_initiative(directory: Path) -> int:
    """Check a single initiative directory.
    
    Args:
        directory: Path to initiative directory
        
    Returns:
        Exit code (0 for ready, 1 for blocked)
    """
    if not directory.exists():
        print(f"{Colors.RED}❌ Error: Directory not found: {directory}{Colors.NC}")
        return 1

    if not directory.is_dir():
        print(f"{Colors.RED}❌ Error: Not a directory: {directory}{Colors.NC}")
        return 1

    initiative = validate_initiative(directory)
    _print_initiative_status(initiative)

    if initiative.status == Status.BLOCKED:
        return 1
    return 0


def _print_initiative_status(initiative) -> None:
    """Print the status of an initiative.
    
    Args:
        initiative: Initiative to print
    """
    # Format task info
    if initiative.completed_count > 0:
        task_info = f"{initiative.completed_count}/{initiative.task_count} tasks completed"
    else:
        task_info = f"{initiative.task_count} tasks"

    if initiative.status == Status.READY:
        print(f"{Colors.GREEN}✅ {initiative.name} ready ({task_info}){Colors.NC}")
    elif initiative.status == Status.WARNING:
        print(f"{Colors.YELLOW}⚠️  {initiative.name} ({task_info}){Colors.NC}")
        for warning in initiative.warnings:
            print(f"   {Colors.YELLOW}Warning: {warning}{Colors.NC}")
    elif initiative.status == Status.BLOCKED:
        print(f"{Colors.RED}❌ {initiative.name} BLOCKED{Colors.NC}")
        for issue in initiative.issues:
            print(f"   {Colors.RED}Issue: {issue}{Colors.NC}")

