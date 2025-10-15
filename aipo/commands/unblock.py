"""Unblock command - analyze and suggest unblocking actions."""

from pathlib import Path
from ..core import get_all_initiatives, categorize_initiatives
from ..utils import Colors


def unblock_command(base_path: Path = Path(".")) -> int:
    """Analyze dependencies and suggest unblocking actions.
    
    Args:
        base_path: Base path to search from
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    initiatives_dir = base_path / "ai-project" / "initiatives"
    
    if not initiatives_dir.exists():
        print(f"{Colors.RED}❌ Error: ai-project/initiatives/ not found{Colors.NC}")
        print(f"{Colors.YELLOW}💡 Run /aipo-create-project first{Colors.NC}")
        return 1
    
    # Get all initiatives
    initiatives = get_all_initiatives(base_path)
    
    if not initiatives:
        print(f"{Colors.YELLOW}⚠️  No initiatives found{Colors.NC}")
        return 0
    
    # Categorize initiatives
    active, completed, not_started, cancelled = categorize_initiatives(initiatives)
    
    # Analyze blocking relationships
    print(f"{Colors.BOLD}🔓 Dependency Analysis{Colors.NC}")
    print()
    
    # Find blocked initiatives
    blocked_initiatives = []
    for init in not_started + active:
        if init.dependencies:
            blocking_deps = []
            for dep_id in init.dependencies:
                dep = next((i for i in initiatives if i.id == dep_id), None)
                if not dep:
                    blocking_deps.append(f"{dep_id} (NOT FOUND)")
                elif not dep.is_completed:
                    status_str = "completed" if dep.is_completed else ("active" if dep.is_active else "not started")
                    blocking_deps.append(f"{dep_id} ({status_str})")
            
            if blocking_deps:
                blocked_initiatives.append((init, blocking_deps))
    
    if not blocked_initiatives:
        print(f"{Colors.GREEN}✅ No blocked initiatives - all dependencies are met!{Colors.NC}")
        print()
        
        # Show ready initiatives
        ready = [i for i in not_started if not i.dependencies]
        if ready:
            print(f"{Colors.BOLD}Ready to start ({len(ready)}):{Colors.NC}")
            for init in ready:
                print(f"  • {init.directory.name}")
                print(f"    {init.completed_count}/{init.task_count} tasks, ~{init.estimated_hours}h")
            print()
        
        return 0
    
    # Show blocked initiatives
    print(f"{Colors.RED}🔒 Blocked Initiatives ({len(blocked_initiatives)}):{Colors.NC}")
    print()
    
    for init, blocking_deps in blocked_initiatives:
        print(f"{Colors.BOLD}{init.directory.name}{Colors.NC}")
        status_str = "completed" if init.is_completed else ("active" if init.is_active else "not started")
        print(f"  Status: {status_str}")
        print(f"  Progress: {init.completed_count}/{init.task_count} tasks")
        print(f"  Blocked by:")
        for dep in blocking_deps:
            print(f"    ❌ {dep}")
        print()
    
    # Suggest actions
    print(f"{Colors.BOLD}💡 Suggested Actions:{Colors.NC}")
    print()
    
    # Find initiatives that are blocking others and need attention
    blocking_initiatives = set()
    for _, blocking_deps in blocked_initiatives:
        for dep in blocking_deps:
            dep_id = dep.split()[0]  # Extract ID before status
            blocking_initiatives.add(dep_id)
    
    active_blocking = [i for i in active if i.id in blocking_initiatives]
    not_started_blocking = [i for i in not_started if i.id in blocking_initiatives]
    
    if active_blocking:
        print(f"{Colors.YELLOW}📋 Active initiatives blocking others:{Colors.NC}")
        for init in active_blocking:
            print(f"  • {init.directory.name} ({init.completed_count}/{init.task_count} tasks)")
            print(f"    → Continue with: /aipo-start-task {init.directory.name}")
        print()
    
    if not_started_blocking:
        print(f"{Colors.YELLOW}🚀 Not started initiatives blocking others:{Colors.NC}")
        for init in not_started_blocking:
            # Check if this initiative is itself blocked
            is_blocked = any(i.id == init.id for i, _ in blocked_initiatives)
            if is_blocked:
                print(f"  • {init.directory.name} (also blocked by dependencies)")
            else:
                print(f"  • {init.directory.name} (ready to start)")
                print(f"    → Start with: /aipo-start-task {init.directory.name}")
        print()
    
    # Show dependency chain
    if blocked_initiatives:
        print(f"{Colors.BOLD}📊 Dependency Chain:{Colors.NC}")
        print()
        _print_dependency_tree(initiatives, completed, active, not_started)
    
    return 1 if blocked_initiatives else 0


def _print_dependency_tree(initiatives, completed, active, not_started):
    """Print a visual dependency tree."""
    
    # Start with completed initiatives (unblocking)
    if completed:
        print(f"{Colors.GREEN}✓ Completed (unblocking):{Colors.NC}")
        for init in completed:
            print(f"  ✓ {init.id}: {init.directory.name}")
        print()
    
    # Then active (in progress)
    if active:
        print(f"{Colors.YELLOW}⧗ Active:{Colors.NC}")
        for init in active:
            deps_str = f" [depends: {', '.join(init.dependencies)}]" if init.dependencies else ""
            print(f"  ⧗ {init.id}: {init.directory.name}{deps_str}")
        print()
    
    # Then not started
    if not_started:
        print(f"{Colors.BLUE}○ Not Started:{Colors.NC}")
        for init in not_started:
            deps = init.dependencies
            if deps:
                # Check which dependencies are met
                met_deps = []
                unmet_deps = []
                for dep_id in deps:
                    dep = next((i for i in initiatives if i.id == dep_id), None)
                    if dep and dep.is_completed:
                        met_deps.append(dep_id)
                    else:
                        unmet_deps.append(dep_id)
                
                deps_str = ""
                if met_deps:
                    deps_str += f" [✓ {', '.join(met_deps)}]"
                if unmet_deps:
                    deps_str += f" [❌ {', '.join(unmet_deps)}]"
                
                print(f"  ○ {init.id}: {init.directory.name}{deps_str}")
            else:
                print(f"  ○ {init.id}: {init.directory.name} [ready]")
        print()

