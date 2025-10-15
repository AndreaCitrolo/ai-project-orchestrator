"""Swarm command - manage swarm lifecycle."""

import os
import signal
import subprocess
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from ..core import get_all_initiatives
from ..utils import Colors, extract_initiative_ids, find_initiative_directory


def swarm_command(swarm_file: str, cancel: bool = False, archive: bool = False, activity: bool = False) -> int:
    """Manage swarm lifecycle.
    
    Args:
        swarm_file: Path to swarm configuration file
        cancel: If True, cancel running swarm
        archive: If True, archive completed swarm
        activity: If True, analyze agent activity and parallelism
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    swarm_path = Path(swarm_file)
    
    if not swarm_path.exists():
        print(f"{Colors.RED}❌ Error: Swarm file not found: {swarm_file}{Colors.NC}")
        return 1
    
    if cancel:
        return _cancel_swarm(swarm_path)
    elif archive:
        return _archive_swarm(swarm_path)
    elif activity:
        return _analyze_agents(swarm_path)
    else:
        print(f"{Colors.RED}❌ Error: Must specify --cancel, --archive, or --activity{Colors.NC}")
        print()
        print("Usage:")
        print(f"  aipo swarm {swarm_file} --cancel    # Cancel running swarm")
        print(f"  aipo swarm {swarm_file} --archive   # Archive completed swarm")
        print(f"  aipo swarm {swarm_file} --activity  # Analyze agent activity")
        return 1


def _cancel_swarm(swarm_path: Path) -> int:
    """Cancel a running swarm gracefully."""
    
    print(f"{Colors.BOLD}🛑 Canceling Swarm: {swarm_path.name}{Colors.NC}")
    print()
    
    # Find running claude-swarm processes for this config
    try:
        result = subprocess.run(
            ["pgrep", "-f", f"claude-swarm.*{swarm_path.name}"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            print(f"Found {len(pids)} running process(es)")
            print()
            
            # Send SIGTERM for graceful shutdown
            for pid in pids:
                try:
                    os.kill(int(pid), signal.SIGTERM)
                    print(f"{Colors.GREEN}✓{Colors.NC} Sent SIGTERM to process {pid}")
                except ProcessLookupError:
                    print(f"{Colors.YELLOW}⚠{Colors.NC}  Process {pid} already terminated")
                except PermissionError:
                    print(f"{Colors.RED}❌{Colors.NC} Permission denied for process {pid}")
            
            print()
            print(f"{Colors.GREEN}✅ Cancellation signal sent{Colors.NC}")
            print(f"{Colors.YELLOW}💡 Swarm should stop gracefully. Check logs for status.{Colors.NC}")
            return 0
        else:
            print(f"{Colors.YELLOW}⚠️  No running processes found for {swarm_path.name}{Colors.NC}")
            print(f"{Colors.YELLOW}💡 Swarm may have already stopped{Colors.NC}")
            return 0
            
    except FileNotFoundError:
        print(f"{Colors.RED}❌ Error: 'pgrep' command not found{Colors.NC}")
        print(f"{Colors.YELLOW}💡 Manually stop the swarm process{Colors.NC}")
        return 1


def _archive_swarm(swarm_path: Path) -> int:
    """Archive a completed swarm."""
    
    print(f"{Colors.BOLD}📦 Archiving Swarm: {swarm_path.name}{Colors.NC}")
    print()
    
    # Extract initiative IDs from swarm file
    initiative_ids = extract_initiative_ids(swarm_path)
    
    if not initiative_ids:
        print(f"{Colors.RED}❌ Error: Could not find initiative IDs in swarm config{Colors.NC}")
        return 1
    
    # Convert IDs to directory names
    base_path = Path(".")
    initiative_dirs = []
    for init_id in initiative_ids:
        directory = find_initiative_directory(init_id, base_path)
        if directory:
            initiative_dirs.append(directory.name)
        else:
            print(f"{Colors.YELLOW}⚠️  Initiative {init_id} directory not found{Colors.NC}")
            initiative_dirs.append(f"{init_id}-unknown")
    
    print(f"Found {len(initiative_dirs)} initiative(s) in swarm:")
    for dir_name in initiative_dirs:
        print(f"  • {dir_name}")
    print()
    
    # Check that all initiatives are completed
    initiatives_dir = Path("ai-project/initiatives")
    initiatives = get_all_initiatives(initiatives_dir)
    
    incomplete_initiatives = []
    for dir_name in initiative_dirs:
        # Extract initiative ID from directory name (NNNN-name format)
        init_id = dir_name.split('-')[0]
        
        initiative = next((i for i in initiatives if i.id == init_id), None)
        if not initiative:
            print(f"{Colors.RED}❌ Initiative not found: {dir_name}{Colors.NC}")
            incomplete_initiatives.append(dir_name)
        elif initiative.status != 'completed':
            print(f"{Colors.RED}❌ Initiative not completed: {dir_name} (status: {initiative.status}){Colors.NC}")
            incomplete_initiatives.append(dir_name)
        else:
            print(f"{Colors.GREEN}✓{Colors.NC} {dir_name} is completed")
    
    print()
    
    if incomplete_initiatives:
        print(f"{Colors.RED}❌ Cannot archive: {len(incomplete_initiatives)} initiative(s) not completed{Colors.NC}")
        print()
        print("Complete all initiatives in the swarm before archiving:")
        for dir_name in incomplete_initiatives:
            print(f"  • {dir_name}")
        return 1
    
    # All initiatives completed - proceed with archival
    print(f"{Colors.GREEN}✅ All initiatives completed{Colors.NC}")
    print()
    
    # Create archive directory if it doesn't exist
    archive_dir = Path("ai-project/swarms/archived")
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate archive filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_name = swarm_path.stem + f"-{timestamp}" + swarm_path.suffix
    archive_path = archive_dir / archive_name
    
    # Move swarm file to archive
    try:
        swarm_path.rename(archive_path)
        print(f"{Colors.GREEN}✓{Colors.NC} Archived swarm config: {archive_path}")
    except Exception as e:
        print(f"{Colors.RED}❌ Error moving swarm file: {e}{Colors.NC}")
        return 1
    
    # Update task files to remove swarm reference
    print()
    print(f"{Colors.BOLD}Updating task files...{Colors.NC}")
    for dir_name in initiative_dirs:
        task_file = initiatives_dir / dir_name / "tasks.prd"
        if task_file.exists():
            try:
                content = task_file.read_text()
                # Remove or comment out the Swarm field
                updated_content = content.replace(
                    f"**Swarm**: {swarm_path.name}",
                    f"**Swarm**: {swarm_path.name} (archived {timestamp})"
                )
                task_file.write_text(updated_content)
                print(f"{Colors.GREEN}✓{Colors.NC} Updated: {task_file}")
            except Exception as e:
                print(f"{Colors.YELLOW}⚠{Colors.NC}  Could not update {task_file}: {e}")
    
    print()
    print(f"{Colors.GREEN}✅ Swarm archived successfully{Colors.NC}")
    print()
    print(f"Archive location: {archive_path}")
    
    return 0


def _analyze_agents(swarm_path: Path) -> int:
    """Analyze agent activity and parallelism from Claude Swarm logs."""
    
    print(f"{Colors.BOLD}📊 Agent Activity Analysis: {swarm_path.name}{Colors.NC}")
    print()
    
    # Find the most recent session for this swarm
    session_path = _find_latest_session()
    
    if not session_path:
        print(f"{Colors.RED}❌ Error: No Claude Swarm sessions found{Colors.NC}")
        print(f"{Colors.YELLOW}💡 Run: claude-swarm start {swarm_path.name}{Colors.NC}")
        return 1
    
    log_file = session_path / "session.log.json"
    
    if not log_file.exists():
        print(f"{Colors.RED}❌ Error: Log file not found: {log_file}{Colors.NC}")
        return 1
    
    print(f"📁 Session: {session_path.name}")
    print()
    
    # Parse logs and extract agent activity
    agent_work = _parse_agent_activity(log_file)
    
    if not agent_work:
        print(f"{Colors.YELLOW}⚠️  No agent activity found in logs{Colors.NC}")
        return 0
    
    # Display results
    _display_agent_analysis(agent_work)
    
    return 0


def _find_latest_session() -> Path | None:
    """Find the most recent Claude Swarm session."""
    
    # Claude Swarm stores sessions in ~/.claude-swarm/sessions/
    home = Path.home()
    sessions_base = home / ".claude-swarm" / "sessions"
    
    if not sessions_base.exists():
        return None
    
    # Find sessions for current project
    cwd = Path.cwd()
    # Session directory format: path+with+plus+signs/session-uuid
    # Strip leading slash before replacing
    cwd_encoded = str(cwd).lstrip("/").replace("/", "+")
    
    project_sessions = sessions_base / cwd_encoded
    
    if not project_sessions.exists():
        return None
    
    # Get all session directories sorted by creation time
    sessions = [d for d in project_sessions.iterdir() if d.is_dir()]
    
    if not sessions:
        return None
    
    # Return most recent session
    sessions.sort(key=lambda d: d.stat().st_mtime, reverse=True)
    return sessions[0]


def _parse_agent_activity(log_file: Path) -> dict:
    """Parse session.log.json and extract agent work periods.
    
    Returns:
        Dict mapping agent name to list of (start_time, end_time) tuples
    """
    
    agent_work = defaultdict(list)
    current_work = {}  # agent -> start_time
    last_result = {}  # agent -> last result time (avoid duplicates)
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    timestamp = entry.get('timestamp', '')
                    instance = entry.get('instance', '')
                    event = entry.get('event', {})
                    event_type = event.get('type', '')
                    from_instance = event.get('from_instance', '')
                    
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    
                    # Filter to agent instances only (exclude coordinator, user)
                    if instance in ['coordinator', 'user', '']:
                        continue
                    
                    # Agent receives task from coordinator (start work)
                    if event_type == 'request' and from_instance == 'coordinator':
                        current_work[instance] = dt
                    
                    # Agent sends result (end work)
                    if event_type == 'result':
                        if instance in current_work:
                            # Avoid duplicate results at same timestamp
                            if instance not in last_result or last_result[instance] != dt:
                                start = current_work[instance]
                                agent_work[instance].append((start, dt))
                                last_result[instance] = dt
                                del current_work[instance]
                
                except (json.JSONDecodeError, ValueError, KeyError):
                    continue
    
    except Exception as e:
        print(f"{Colors.RED}❌ Error parsing log file: {e}{Colors.NC}")
        return {}
    
    return dict(agent_work)


def _display_agent_analysis(agent_work: dict):
    """Display formatted agent activity analysis."""
    
    # Calculate session time range
    all_times = []
    for periods in agent_work.values():
        for start, end in periods:
            all_times.append(start)
            all_times.append(end)
    
    if not all_times:
        return
    
    min_time = min(all_times)
    max_time = max(all_times)
    session_duration = (max_time - min_time).total_seconds() / 60
    
    # Print agent work periods
    print(f"{Colors.BOLD}{'═' * 70}{Colors.NC}")
    print(f"{Colors.BOLD}AGENT WORK PERIODS{Colors.NC}")
    print(f"{Colors.BOLD}{'═' * 70}{Colors.NC}")
    print()
    
    for agent, periods in sorted(agent_work.items()):
        total_time = sum((end - start).total_seconds() for start, end in periods)
        utilization = (total_time / (session_duration * 60)) * 100 if session_duration > 0 else 0
        
        print(f"{Colors.BOLD}{agent}{Colors.NC}: {len(periods)} tasks, {total_time/60:.1f} min active ({utilization:.0f}%)")
        
        for i, (start, end) in enumerate(periods, 1):
            duration = (end - start).total_seconds() / 60
            print(f"  #{i}: {start.strftime('%H:%M:%S')} → {end.strftime('%H:%M:%S')} ({duration:.1f}m)")
    
    # Calculate parallelism timeline
    print()
    print(f"{Colors.BOLD}{'═' * 70}{Colors.NC}")
    print(f"{Colors.BOLD}PARALLELISM TIMELINE{Colors.NC}")
    print(f"{Colors.BOLD}{'═' * 70}{Colors.NC}")
    print()
    print(f"Session: {min_time.strftime('%H:%M:%S')} to {max_time.strftime('%H:%M:%S')}")
    print(f"Duration: {session_duration:.1f} minutes")
    print()
    
    # Sample every minute
    current = min_time
    samples = []
    total_agents = len(agent_work)
    
    while current <= max_time:
        active_agents = []
        for agent, periods in agent_work.items():
            for start, end in periods:
                if start <= current < end:
                    active_agents.append(agent)
                    break
        samples.append((current, len(active_agents), active_agents))
        current = datetime.fromtimestamp(current.timestamp() + 60, tz=current.tzinfo)
    
    # Print timeline
    for time, active, agents in samples:
        bar = '█' * active + '░' * (total_agents - active)
        agent_list = ', '.join(agents) if agents else '(idle)'
        print(f"{time.strftime('%H:%M')} {bar} {active}/{total_agents} | {agent_list}")
    
    # Calculate statistics
    print()
    print(f"{Colors.BOLD}{'═' * 70}{Colors.NC}")
    print(f"{Colors.BOLD}STATISTICS{Colors.NC}")
    print(f"{Colors.BOLD}{'═' * 70}{Colors.NC}")
    print()
    
    active_counts = [s[1] for s in samples]
    avg_parallelism = sum(active_counts) / len(active_counts) if active_counts else 0
    max_parallelism = max(active_counts) if active_counts else 0
    avg_percentage = (avg_parallelism / total_agents) * 100 if total_agents > 0 else 0
    max_percentage = (max_parallelism / total_agents) * 100 if total_agents > 0 else 0
    
    print(f"Average Parallelism: {avg_parallelism:.1f}/{total_agents} agents ({avg_percentage:.0f}%)")
    print(f"Peak Parallelism: {max_parallelism}/{total_agents} agents ({max_percentage:.0f}%)")
    
    # Distribution
    distribution = Counter(active_counts)
    print()
    print("Parallelism Distribution:")
    for level in range(total_agents + 1):
        count = distribution.get(level, 0)
        pct = (count / len(samples)) * 100 if samples else 0
        bar = '█' * int(pct / 5)
        print(f"  {level} agents: {count:3d} min ({pct:5.1f}%) {bar}")
    
    # Insights
    print()
    print(f"{Colors.BOLD}{'═' * 70}{Colors.NC}")
    print(f"{Colors.BOLD}EFFICIENCY INSIGHTS{Colors.NC}")
    print(f"{Colors.BOLD}{'═' * 70}{Colors.NC}")
    print()
    
    idle_minutes = distribution.get(0, 0)
    idle_pct = (idle_minutes / len(samples)) * 100 if samples else 0
    
    if max_parallelism == total_agents:
        print(f"{Colors.GREEN}✅ Good:{Colors.NC} Peak parallelism reached ({total_agents}/{total_agents} agents)")
    else:
        print(f"{Colors.YELLOW}⚠️  Note:{Colors.NC} Peak was {max_parallelism}/{total_agents} agents (never reached full capacity)")
    
    if idle_minutes > 0:
        print(f"{Colors.YELLOW}⚠️  Note:{Colors.NC} {idle_minutes} minutes idle time ({idle_pct:.0f}% of session)")
    
    if avg_percentage < 50:
        print(f"{Colors.YELLOW}💡 Tip:{Colors.NC} Average {avg_percentage:.0f}% utilization - consider workload distribution")
    elif avg_percentage >= 70:
        print(f"{Colors.GREEN}💡 Tip:{Colors.NC} Average {avg_percentage:.0f}% utilization - good parallelism!")
    
    print()

