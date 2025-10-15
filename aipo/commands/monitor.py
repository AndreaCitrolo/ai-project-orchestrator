"""Monitor command - deterministic status checking without LLM."""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

from ..core import get_all_initiatives, categorize_initiatives
from ..utils import Colors, create_progress_bar, extract_tasks


def monitor_swarm(base_path: Path = Path("."), show_tasks: bool = False, interactive: bool = False) -> int:
    """Monitor current swarm status deterministically without LLM.
    
    Args:
        base_path: Base path to search from
        show_tasks: Whether to show detailed task information
        interactive: Whether to run in interactive mode with auto-refresh
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    if interactive:
        return _interactive_monitor(base_path, show_tasks)
    else:
        return _single_monitor(base_path, show_tasks)


def _clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')


def _interactive_monitor(base_path: Path, show_tasks: bool, refresh_interval: int = 5) -> int:
    """Run monitor in interactive mode with auto-refresh.
    
    Args:
        base_path: Base path to search from
        show_tasks: Whether to show detailed task information
        refresh_interval: Seconds between refreshes
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    print(f"{Colors.YELLOW}🔄 Interactive Monitor Mode - Press Ctrl+C to exit{Colors.NC}")
    print()
    
    try:
        while True:
            _clear_screen()
            
            # Show timestamp at top
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{Colors.BOLD}📊 AI Project Orchestrator - Live Monitor{Colors.NC}")
            print(f"{Colors.DIM}Updated: {timestamp} | Refreshing every {refresh_interval}s | Press Ctrl+C to exit{Colors.NC}")
            print()
            
            # Run the monitor logic
            result = _single_monitor(base_path, show_tasks, suppress_header=True)
            
            if result != 0:
                # If there's an error, don't keep looping
                return result
            
            # Wait for next refresh
            time.sleep(refresh_interval)
            
    except KeyboardInterrupt:
        print()
        print(f"{Colors.GREEN}✓ Monitor stopped{Colors.NC}")
        return 0


def _single_monitor(base_path: Path, show_tasks: bool, suppress_header: bool = False) -> int:
    """Run monitor once (non-interactive).
    
    Args:
        base_path: Base path to search from
        show_tasks: Whether to show detailed task information
        suppress_header: Whether to suppress the header (for interactive mode)
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    if not suppress_header:
        print(f"{Colors.BOLD}📊 AI Project Orchestrator - Swarm Monitor{Colors.NC}")
        print()
    
    # Check for initiatives directory
    initiatives_dir = base_path / "ai-project" / "initiatives"
    
    if not initiatives_dir.exists():
        print(f"{Colors.RED}❌ Error: No initiatives found{Colors.NC}")
        print(f"   Looking for: {initiatives_dir}")
        print()
        print("To initialize a project, run:")
        print("  /aipo-create-project  (in Claude Code)")
        return 1
    
    # Get all initiatives
    initiatives = get_all_initiatives(base_path)
    
    if not initiatives:
        print(f"{Colors.YELLOW}⚠️  No initiatives found{Colors.NC}")
        return 0
    
    # Categorize initiatives
    active, completed, not_started, cancelled = categorize_initiatives(initiatives)
    
    # Print summary
    total = len(initiatives)
    print(f"{Colors.BOLD}Overview:{Colors.NC}")
    print(f"  Total initiatives: {total}")
    print(f"  {Colors.GREEN}● Active: {len(active)}{Colors.NC}")
    print(f"  {Colors.BLUE}✓ Completed: {len(completed)}{Colors.NC}")
    print(f"  ○ Not started: {len(not_started)}")
    if cancelled:
        print(f"  {Colors.RED}✗ Cancelled: {len(cancelled)}{Colors.NC}")
    print()
    
    # Show active initiatives in detail
    if active:
        print(f"{Colors.BOLD}🔄 Active Initiatives:{Colors.NC}")
        print()
        for initiative in active:
            progress_pct = initiative.progress_percentage
            progress_bar = create_progress_bar(initiative.completed_count, initiative.task_count)
            
            print(f"  {Colors.GREEN}●{Colors.NC} {Colors.BOLD}{initiative.name}{Colors.NC}")
            print(f"    Progress: {progress_bar} {initiative.completed_count}/{initiative.task_count} ({progress_pct:.0f}%)")
            if initiative.started_at:
                print(f"    Started: {initiative.started_at}")
            if initiative.summary_status:
                print(f"    Status: {initiative.summary_status}")
            
            if show_tasks:
                # Show current and next tasks
                tasks_file = initiative.directory / "tasks.prd"
                if tasks_file.exists():
                    tasks = extract_tasks(tasks_file)
                    in_progress = [t for t in tasks if t['status'] == 'in_progress']
                    pending = [t for t in tasks if t['status'] == 'pending']
                    
                    if in_progress:
                        print(f"    {Colors.YELLOW}→ Working on:{Colors.NC}")
                        for task in in_progress[:3]:  # Show up to 3
                            print(f"      • {task['id']}: {task['title']}")
                    
                    if pending and len(in_progress) < 3:
                        print(f"    Next tasks:")
                        for task in pending[:3]:  # Show up to 3
                            print(f"      ○ {task['id']}: {task['title']}")
            
            print()
    
    # Show completed initiatives (compact)
    if completed:
        print(f"{Colors.BOLD}✅ Completed Initiatives:{Colors.NC}")
        for initiative in completed:
            end_info = f" (ended {initiative.ended_at})" if initiative.ended_at else ""
            print(f"  {Colors.GREEN}✓{Colors.NC} {initiative.name} - {initiative.task_count} tasks{end_info}")
        print()
    
    # Show not started initiatives (compact)
    if not_started:
        print(f"{Colors.BOLD}○ Not Started:{Colors.NC}")
        for initiative in not_started:
            task_info = f" ({initiative.task_count} tasks)" if initiative.task_count > 0 else " (no tasks)"
            print(f"  ○ {initiative.name}{task_info}")
        print()
    
    # Show cancelled (if any)
    if cancelled:
        print(f"{Colors.BOLD}{Colors.RED}✗ Cancelled:{Colors.NC}")
        for initiative in cancelled:
            print(f"  {Colors.RED}✗{Colors.NC} {initiative.name}")
        print()
    
    # Suggest next action
    if active:
        print(f"{Colors.BOLD}💡 Suggested Next Action:{Colors.NC}")
        # Find initiative with lowest completion rate that's active
        active_sorted = sorted(active, key=lambda i: i.progress_percentage)
        next_initiative = active_sorted[0]
        print(f"  Continue working on: {next_initiative.name}")
        print(f"  Use: /start-task {next_initiative.directory.name} TASK-XXX")
    elif not_started:
        print(f"{Colors.BOLD}💡 Suggested Next Action:{Colors.NC}")
        print(f"  Start first initiative: {not_started[0].name}")
        if not_started[0].task_count == 0:
            print(f"  Use: /aipo-create-tasks {not_started[0].directory.name}")
        else:
            print(f"  Use: /start-task {not_started[0].directory.name} TASK-001")
    
    return 0

