"""Status command - quick project health check."""

import json
from pathlib import Path
from typing import Dict, Any

from ..core import get_all_initiatives, categorize_initiatives
from ..utils import Colors


def status_command(base_path: Path = Path("."), output_json: bool = False) -> int:
    """Quick project health check.
    
    Args:
        base_path: Base path to search from
        output_json: Whether to output JSON format
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Get all initiatives
    initiatives = get_all_initiatives(base_path)
    
    if not initiatives:
        if output_json:
            print(json.dumps({"error": "No initiatives found"}, indent=2))
        else:
            print(f"{Colors.RED}❌ No initiatives found{Colors.NC}")
        return 1
    
    # Categorize initiatives
    active, completed, not_started, cancelled = categorize_initiatives(initiatives)
    
    # Calculate overall statistics
    total_tasks = sum(i.task_count for i in initiatives)
    completed_tasks = sum(i.completed_count for i in initiatives)
    overall_progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Count blockers and warnings
    blockers = sum(len(i.issues) for i in initiatives)
    warnings = sum(len(i.warnings) for i in initiatives)
    
    # Find initiatives with dependencies
    blocked_initiatives = [
        i for i in initiatives
        if i.dependencies and not i.is_completed
    ]
    
    if output_json:
        # JSON output for CI/CD and automation
        data: Dict[str, Any] = {
            "overview": {
                "total_initiatives": len(initiatives),
                "active": len(active),
                "completed": len(completed),
                "not_started": len(not_started),
                "cancelled": len(cancelled)
            },
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "pending": total_tasks - completed_tasks,
                "completion_percentage": round(overall_progress, 1)
            },
            "health": {
                "blockers": blockers,
                "warnings": warnings,
                "status": "healthy" if blockers == 0 else "blocked"
            },
            "active_initiatives": [
                {
                    "id": i.id,
                    "name": i.name,
                    "progress": round(i.progress_percentage, 1),
                    "tasks_completed": i.completed_count,
                    "tasks_total": i.task_count
                }
                for i in active
            ]
        }
        print(json.dumps(data, indent=2))
    else:
        # Human-readable output
        status_emoji = "🟢" if blockers == 0 else "🔴"
        
        print(f"{Colors.BOLD}📊 Project Status{Colors.NC}")
        print()
        
        # Overall health
        print(f"{status_emoji} Overall: {overall_progress:.0f}% complete ({completed_tasks}/{total_tasks} tasks)")
        
        if blockers > 0:
            print(f"{Colors.RED}⚠️  {blockers} blocker(s){Colors.NC}")
        if warnings > 0:
            print(f"{Colors.YELLOW}⚠️  {warnings} warning(s){Colors.NC}")
        
        print()
        
        # Initiative breakdown
        print(f"Initiatives: {len(active)} active, {len(completed)} completed, {len(not_started)} not started", end="")
        if cancelled:
            print(f", {len(cancelled)} cancelled", end="")
        print()
        
        # Active initiatives summary
        if active:
            print()
            print(f"{Colors.BOLD}Active:{Colors.NC}")
            for i in active:
                print(f"  • {i.name}: {i.progress_percentage:.0f}% ({i.completed_count}/{i.task_count})")
        
        # Blockers detail
        if blockers > 0:
            print()
            print(f"{Colors.BOLD}{Colors.RED}Blockers:{Colors.NC}")
            for i in initiatives:
                if i.issues:
                    print(f"  • {i.name}:")
                    for issue in i.issues:
                        print(f"    - {issue}")
        
        # Dependencies check
        if blocked_initiatives:
            print()
            print(f"{Colors.BOLD}Dependencies:{Colors.NC}")
            for i in blocked_initiatives:
                deps_status = []
                for dep_id in i.dependencies:
                    dep = next((d for d in initiatives if d.id == dep_id), None)
                    if dep:
                        status_icon = "✓" if dep.is_completed else "⧗"
                        deps_status.append(f"{status_icon} {dep_id}")
                    else:
                        deps_status.append(f"✗ {dep_id}")
                print(f"  • {i.name} → {', '.join(deps_status)}")
    
    return 0 if blockers == 0 else 1

