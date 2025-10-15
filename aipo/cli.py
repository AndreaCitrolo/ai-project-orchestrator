"""Command-line interface for AIPO."""

import argparse
import sys
from pathlib import Path

from .utils import Colors
from .commands import (
    init_commands,
    monitor_swarm,
    validate_swarm,
    check_initiative,
    list_initiatives,
    status_command,
    next_command,
    unblock_command,
    swarm_command,
)
from .commands.validate import print_summary


def main() -> int:
    """Main CLI entry point.
    
    Returns:
        Exit code
    """
    parser = argparse.ArgumentParser(
        description="AI Project Orchestrator (AIPO) - Validation and management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  aipo init                    # Install slash commands
  aipo init --run-swarm        # Install commands and run orchestrator
  aipo status                  # Quick project health check
  aipo status --json           # JSON output for CI/CD
  aipo next                    # Get next recommended task
  aipo next --all              # Show next task for each initiative
  aipo next --agent backend_1  # Get next task for agent (reads from tasks.prd)
  aipo unblock                 # Analyze dependencies and suggest unblocking actions
  aipo monitor                 # Monitor current swarm status
  aipo monitor --show-tasks    # Monitor with detailed task view
  aipo monitor --interactive   # Live monitoring with auto-refresh
  aipo swarm my-swarm.yml --cancel   # Cancel running swarm
  aipo swarm my-swarm.yml --archive  # Archive completed swarm
  aipo swarm my-swarm.yml --activity # Analyze agent activity and parallelism
  aipo validate fullstack-feature-swarm.yml
  aipo check ai-project/initiatives/0003-backend-models
  aipo list
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Init command
    init_parser = subparsers.add_parser('init', help='Install slash commands and optionally run orchestrator')
    init_parser.add_argument('--run-swarm', action='store_true', help='Start claude-swarm orchestrator after installing commands')
    init_parser.add_argument('--no-color', action='store_true', help='Disable colored output')

    # Status command
    status_parser = subparsers.add_parser('status', help='Quick project health check')
    status_parser.add_argument('--json', action='store_true', help='Output JSON format')
    status_parser.add_argument('--no-color', action='store_true', help='Disable colored output')

    # Next command
    next_parser = subparsers.add_parser('next', help='Get next recommended task')
    next_parser.add_argument('--all', action='store_true', help='Show next task for each active initiative')
    next_parser.add_argument('--agent', type=str, help='Agent name (reads assignments from tasks.prd)')
    next_parser.add_argument('--initiatives', type=str, help='(Deprecated) Comma-separated initiative dirs')
    next_parser.add_argument('initiative_dir', nargs='?', help='Specific initiative directory')
    next_parser.add_argument('--no-color', action='store_true', help='Disable colored output')

    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Monitor current swarm status (no LLM)')
    monitor_parser.add_argument('--show-tasks', action='store_true', help='Show detailed task information')
    monitor_parser.add_argument('--interactive', action='store_true', help='Live monitoring with auto-refresh')
    monitor_parser.add_argument('--no-color', action='store_true', help='Disable colored output')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate swarm configuration')
    validate_parser.add_argument('swarm_file', type=Path, help='Path to swarm YAML file')
    validate_parser.add_argument('--no-color', action='store_true', help='Disable colored output')

    # Check command
    check_parser = subparsers.add_parser('check', help='Check a single initiative')
    check_parser.add_argument('directory', type=Path, help='Path to initiative directory')
    check_parser.add_argument('--no-color', action='store_true', help='Disable colored output')

    # List command
    list_parser = subparsers.add_parser('list', help='List all initiatives')
    list_parser.add_argument('--no-color', action='store_true', help='Disable colored output')

    # Unblock command
    unblock_parser = subparsers.add_parser('unblock', help='Analyze dependencies and suggest unblocking actions')
    unblock_parser.add_argument('--no-color', action='store_true', help='Disable colored output')

    # Swarm command
    swarm_parser = subparsers.add_parser('swarm', help='Manage swarm lifecycle')
    swarm_parser.add_argument('swarm_file', type=str, help='Path to swarm YAML file')
    swarm_parser.add_argument('--cancel', action='store_true', help='Cancel running swarm')
    swarm_parser.add_argument('--archive', action='store_true', help='Archive completed swarm')
    swarm_parser.add_argument('--activity', action='store_true', help='Analyze agent activity and parallelism')
    swarm_parser.add_argument('--no-color', action='store_true', help='Disable colored output')

    args = parser.parse_args()

    # Disable colors if requested or not a TTY
    if hasattr(args, 'no_color') and args.no_color or not sys.stdout.isatty():
        Colors.disable()

    # Execute command
    if args.command == 'init':
        return init_commands(run_swarm=args.run_swarm)

    elif args.command == 'status':
        return status_command(output_json=args.json)

    elif args.command == 'next':
        return next_command(
            show_all=args.all,
            initiative_dir=args.initiative_dir,
            agent=getattr(args, 'agent', None),
            agent_initiatives=getattr(args, 'initiatives', None)
        )

    elif args.command == 'monitor':
        return monitor_swarm(show_tasks=args.show_tasks, interactive=args.interactive)

    elif args.command == 'validate':
        if not args.swarm_file.exists():
            print(f"{Colors.RED}❌ Error: Swarm file not found: {args.swarm_file}{Colors.NC}")
            return 1

        initiatives, blocking_errors, warnings = validate_swarm(args.swarm_file)
        return print_summary(initiatives, blocking_errors, warnings, args.swarm_file)

    elif args.command == 'check':
        return check_initiative(args.directory)

    elif args.command == 'list':
        return list_initiatives()

    elif args.command == 'unblock':
        return unblock_command()

    elif args.command == 'swarm':
        return swarm_command(args.swarm_file, cancel=args.cancel, archive=args.archive, activity=args.activity)

    else:
        parser.print_help()
        return 1

