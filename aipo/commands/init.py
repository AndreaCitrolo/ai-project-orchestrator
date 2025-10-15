"""Initialize AIPO by installing slash commands."""

import shutil
import subprocess
from pathlib import Path

from ..utils import Colors


def init_commands(run_swarm: bool = False) -> int:
    """Initialize AIPO by installing slash commands and context file.
    
    Args:
        run_swarm: Deprecated parameter (ignored)
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    print(f"{Colors.BOLD}🚀 Initializing AI Project Orchestrator{Colors.NC}")
    print()
    
    # Install SuperClaude Framework (required dependency)
    print(f"{Colors.BOLD}📦 Checking SuperClaude Framework...{Colors.NC}")
    
    # Check common installation paths
    sc_paths = [
        "superclaude",  # In PATH
        str(Path.home() / ".local/bin/superclaude"),  # pipx default
    ]
    
    sc_installed = False
    sc_version = None
    for sc_path in sc_paths:
        result = subprocess.run([sc_path, "--version"], capture_output=True, check=False, text=True)
        if result.returncode == 0:
            sc_installed = True
            sc_version = result.stdout.strip()
            print(f"{Colors.GREEN}✓{Colors.NC} SuperClaude installed: {sc_version}")
            break
    
    if not sc_installed:
        print("Installing SuperClaude...")
        try:
            # Use pipx (recommended)
            result = subprocess.run(
                ["pipx", "install", "superclaude"], 
                capture_output=True, 
                check=False,
                text=True
            )
            
            if result.returncode != 0:
                if "already installed" in result.stderr:
                    print(f"{Colors.GREEN}✓{Colors.NC} SuperClaude already installed")
                else:
                    raise Exception(f"pipx install failed: {result.stderr}")
            else:
                print(f"{Colors.GREEN}✓{Colors.NC} SuperClaude Framework installed")
            
            # Check if PATH needs updating
            verify = subprocess.run(["superclaude", "--version"], capture_output=True, check=False)
            if verify.returncode != 0:
                print(f"{Colors.YELLOW}⚠️  SuperClaude installed but not in PATH{Colors.NC}")
                print(f"{Colors.YELLOW}   Add to your shell config (~/.bashrc or ~/.zshrc):{Colors.NC}")
                print(f"{Colors.YELLOW}   export PATH=\"$HOME/.local/bin:$PATH\"{Colors.NC}")
                print(f"{Colors.YELLOW}   Then: source ~/.zshrc{Colors.NC}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.NC}")
            print(f"{Colors.YELLOW}   Install manually: pipx install superclaude{Colors.NC}")
            return 1
    print()
    
    # Determine source directory (where aipo.py is located)
    script_dir = Path(__file__).parent.parent.parent
    commands_src = script_dir / "templates"
    
    if not commands_src.exists():
        print(f"{Colors.RED}❌ Error: Templates directory not found at {commands_src}{Colors.NC}")
        return 1
    
    # Install CLAUDE.md context file to project root
    context_src = commands_src / "CLAUDE.md"
    if context_src.exists():
        context_dest = Path("CLAUDE.md")
        shutil.copy2(context_src, context_dest)
        print(f"{Colors.GREEN}✓{Colors.NC} Installed: CLAUDE.md (workflow enforcement)")
    else:
        print(f"{Colors.YELLOW}⚠️  Warning: CLAUDE.md not found, skipping{Colors.NC}")
    
    # Create .claude directory for commands
    claude_dir = Path(".claude")
    claude_dir.mkdir(exist_ok=True)
    
    # Target directory for slash commands
    claude_commands = claude_dir / "commands"
    
    # Create .claude/commands directory
    claude_commands.mkdir(parents=True, exist_ok=True)
    print(f"{Colors.GREEN}✓{Colors.NC} Created directory: {claude_commands}/")
    
    # Copy command files (skip README and CLAUDE.md)
    command_files = [
        f for f in commands_src.glob("*.md") 
        if f.stem.upper() not in ["README", "CLAUDE"]
    ]
    
    if not command_files:
        print(f"{Colors.RED}❌ Error: No command files found in {commands_src}{Colors.NC}")
        return 1
    
    copied_count = 0
    for cmd_file in command_files:
        dest_file = claude_commands / cmd_file.name
        shutil.copy2(cmd_file, dest_file)
        print(f"{Colors.GREEN}✓{Colors.NC} Installed: /{cmd_file.stem}")
        copied_count += 1
    
    print()
    print(f"{Colors.GREEN}✅ Installed {copied_count} slash commands{Colors.NC}")
    print()
    print("Available commands:")
    for cmd_file in sorted(command_files, key=lambda x: x.stem):
        print(f"  /{cmd_file.stem}")
    
    print()
    print(f"{Colors.BOLD}📋 Next steps:{Colors.NC}")
    print()
    print("1. Open Claude Code in this directory")
    print("   The context file will automatically enforce the workflow")
    print()
    print("2. Start working:")
    print("   > /aipo-create-project")
    print("   > /aipo-plan")
    print("   > /aipo-create-initiative [name]")
    print("   ...")
    print()
    print("3. When ready for parallel execution:")
    print("   > /aipo-configure-swarm [file] [initiatives...]")
    print("   $ claude-swarm start [file]")
    print("   $ python3 aipo.py monitor")
    print()
    print(f"{Colors.GREEN}✨ You're all set!{Colors.NC}")
    
    return 0

