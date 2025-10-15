"""Validate command - validate swarm configurations."""

from pathlib import Path
from typing import List, Tuple

from ..models import Initiative, Status
from ..core import validate_initiative
from ..utils import Colors, extract_initiative_ids, find_initiative_directory


def validate_swarm(swarm_file: Path, base_path: Path = Path(".")) -> Tuple[List[Initiative], int, int]:
    """Validate all initiatives in a swarm configuration.
    
    Args:
        swarm_file: Path to swarm YAML file
        base_path: Base path to search from
        
    Returns:
        Tuple of (initiatives, blocking_errors, warnings)
    """
    print(f"🔍 Validating swarm readiness...")
    print(f"   Swarm config: {swarm_file}")
    print()

    # Extract initiative IDs
    initiative_ids = extract_initiative_ids(swarm_file)

    if not initiative_ids:
        print(f"{Colors.YELLOW}⚠️  Warning: No initiatives found in swarm config{Colors.NC}")
        print("   Looking for patterns like 'Initiative 0003' or '0004-backend-api'")
        return [], 0, 1

    print(f"Found {len(initiative_ids)} initiative(s): {', '.join(initiative_ids)}")
    print()

    initiatives = []
    blocking_errors = 0
    warnings = 0

    for init_id in initiative_ids:
        # Find directory
        directory = find_initiative_directory(init_id, base_path)

        if directory is None:
            print(f"{Colors.RED}❌ Initiative {init_id} directory not found{Colors.NC}")
            blocking_errors += 1
            continue

        # Validate initiative
        initiative = validate_initiative(directory)
        initiatives.append(initiative)

        # Print status
        _print_initiative_status(initiative)

        # Count errors and warnings
        if initiative.status == Status.BLOCKED:
            blocking_errors += len(initiative.issues)
        elif initiative.status == Status.WARNING:
            warnings += len(initiative.warnings)

    # Check bidirectional swarm-task binding
    print()
    binding_errors, binding_warnings = _check_swarm_binding(swarm_file, initiatives, base_path)
    blocking_errors += binding_errors
    warnings += binding_warnings

    return initiatives, blocking_errors, warnings


def print_summary(initiatives: List[Initiative], blocking_errors: int, warnings: int, swarm_file: Path) -> int:
    """Print validation summary.
    
    Args:
        initiatives: List of validated initiatives
        blocking_errors: Number of blocking errors
        warnings: Number of warnings
        swarm_file: Path to swarm file
        
    Returns:
        Exit code (0 for success, 1 for blocked)
    """
    ready_count = sum(1 for i in initiatives if i.status == Status.READY)

    print()
    print("=" * 50)
    print(f"{Colors.BOLD}VALIDATION SUMMARY{Colors.NC}")
    print("=" * 50)
    print(f"✅ Ready initiatives: {ready_count}")
    print(f"❌ Blocking errors: {blocking_errors}")
    print(f"⚠️  Warnings: {warnings}")
    print()

    if blocking_errors > 0:
        print(f"{Colors.RED}❌ BLOCKED: Fix blocking issues before starting swarm{Colors.NC}")
        print()
        print("Common fixes:")
        print("  1. Generate missing tasks:")
        print("     claude (then use /aipo-create-tasks)")
        print("  2. Create initiative directory and files")
        print("  3. Verify initiatives exist in ai-project/initiatives/")
        return 1
    else:
        print(f"{Colors.GREEN}✅ All checks passed! Safe to start swarm.{Colors.NC}")
        print()
        print("Start swarm with:")
        print(f"  claude-swarm start {swarm_file} --background")
        return 0


def _check_swarm_binding(swarm_file: Path, initiatives: List[Initiative], base_path: Path) -> Tuple[int, int]:
    """Check bidirectional binding between swarm file and tasks.prd files.
    
    Args:
        swarm_file: Path to swarm YAML file
        initiatives: List of initiatives found in swarm
        base_path: Base path to search from
        
    Returns:
        Tuple of (errors, warnings)
    """
    print(f"{Colors.BOLD}🔗 Checking Swarm-Task Binding{Colors.NC}")
    
    errors = 0
    warnings = 0
    swarm_name = swarm_file.name
    
    # Get all initiatives in the project
    initiatives_dir = base_path / "ai-project" / "initiatives"
    if not initiatives_dir.exists():
        print(f"{Colors.YELLOW}⚠️  Skipping binding check: initiatives directory not found{Colors.NC}")
        return 0, 1
    
    # Check 1: Initiatives in swarm should have Swarm field in tasks.prd
    print()
    print("Direction 1: Swarm → Tasks")
    for init in initiatives:
        task_file = init.directory / "tasks.prd"
        if task_file.exists():
            content = task_file.read_text()
            if f"**Swarm**: {swarm_name}" in content:
                print(f"{Colors.GREEN}  ✓{Colors.NC} {init.directory_name} references {swarm_name}")
            elif "**Swarm**:" in content:
                # Has Swarm field but different file
                import re
                match = re.search(r'\*\*Swarm\*\*:\s*(\S+)', content)
                if match:
                    other_swarm = match.group(1)
                    print(f"{Colors.YELLOW}  ⚠{Colors.NC}  {init.directory_name} references different swarm: {other_swarm}")
                    warnings += 1
            else:
                print(f"{Colors.YELLOW}  ⚠{Colors.NC}  {init.directory_name} missing Swarm field")
                warnings += 1
        else:
            print(f"{Colors.RED}  ✗{Colors.NC} {init.directory_name} tasks.prd not found")
            errors += 1
    
    # Check 2: Initiatives with this Swarm field should be in the swarm config
    print()
    print("Direction 2: Tasks → Swarm")
    swarm_initiative_names = {i.directory_name for i in initiatives}
    
    for init_dir in initiatives_dir.iterdir():
        if init_dir.is_dir() and init_dir.name.startswith(tuple('0123456789')):
            task_file = init_dir / "tasks.prd"
            if task_file.exists():
                content = task_file.read_text()
                if f"**Swarm**: {swarm_name}" in content:
                    if init_dir.name in swarm_initiative_names:
                        print(f"{Colors.GREEN}  ✓{Colors.NC} {init_dir.name} is in {swarm_name}")
                    else:
                        print(f"{Colors.RED}  ✗{Colors.NC} {init_dir.name} references {swarm_name} but not in swarm config")
                        errors += 1
    
    print()
    if errors == 0 and warnings == 0:
        print(f"{Colors.GREEN}✅ Bidirectional binding OK{Colors.NC}")
    elif errors > 0:
        print(f"{Colors.RED}❌ Binding errors found: {errors}{Colors.NC}")
    else:
        print(f"{Colors.YELLOW}⚠️  Binding warnings: {warnings}{Colors.NC}")
    
    return errors, warnings


def _print_initiative_status(initiative: Initiative) -> None:
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

