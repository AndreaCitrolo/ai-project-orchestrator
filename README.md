# AI Project Orchestrator

Structured framework for AI agents: batch planning + parallel execution + minimal context.

**Version**: 2.1.0

## Overview

**Solves**:
- Context loss between sessions
- Poor dependency tracking
- No parallel execution
- Inconsistent state

**How**:
- Modular state (<500 tokens/module)
- Initiative-based organization
- Task groups for parallel work
- Explicit dependencies
- File-centric (minimal LLM output)

## Requirements

- **Python 3.10+** (uses union type syntax: `Type | None`)
- **No external dependencies** (standard library only)
- **Claude Code** (for slash commands)
- **Claude Swarm** (optional, for parallel execution)

## Quick Start

```bash
# 1. Install
python3 aipo.py init  # Creates CLAUDE.md + .claude/commands/

# 2. Claude Code (CLAUDE.md auto-loads context)
> /aipo-create-project
> /aipo-plan
> /aipo-create-initiative auth → /aipo-create-tasks 0001-auth
> /aipo-create-initiative payments → /aipo-create-tasks 0002-payments
> /aipo-configure-swarm 0001-batch.yml 0001-auth 0002-payments

# 3. Execute
$ claude-swarm start 0001-batch.yml
$ python3 aipo.py monitor
```

## Directory Structure

```
ai-project-orchestrator/
├── aipo.py                   # CLI
├── aipo/                     # Python package
│   ├── models.py, core.py, utils.py
│   └── commands/             # init, status, next, monitor, validate, check, list
├── templates/
│   ├── CLAUDE.md             # Context (→ project root)
│   └── aipo-*.md             # Commands (→ .claude/commands/)
└── examples/

Project structure (after init):
├── CLAUDE.md                 # Workflow enforcement
├── .claude/commands/         # Slash commands
└── ai-project/               # Created by /aipo-create-project
    ├── project-state.prd
    └── initiatives/NNNN-name/
        ├── description.prd
        └── tasks.prd
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Initiative** | Feature/capability, NNNN-name format |
| **Task Groups** | Group 0: prereqs, 1-N: features (parallel within group) |
| **Status** | Not Started / Active / Completed / Cancelled |
| **Dependencies** | Cross-initiative (NNNN), intra-task (TASK-XXX) |
| **Swarm** | Parallel execution config (1-5 initiatives) |
| **Agents** | Skill-typed (backend_1, frontend_1, etc.) |

## Workflow

1. **Plan**: `/aipo-plan` → 4-5 strategies (Max Parallel, Fast Feedback, Homogeneous, Functional Slice, Dependency-Opt)
2. **Create**: Loop: `/aipo-create-initiative` → `/aipo-create-tasks`
3. **Configure**: `/aipo-configure-swarm [file] [dirs...]` - assigns tasks to agents
4. **Execute**: `claude-swarm start [file]` + `python3 aipo.py monitor`
5. **Auto-close**: Last task completion triggers initiative closure

## Commands

### Slash Commands (Claude Code)

| Command | Purpose |
|---------|---------|
| `/aipo-create-project` | Initialize workspace |
| `/aipo-plan` | Strategic options (2-5 initiatives) |
| `/aipo-create-initiative [name]` | Create PRD |
| `/aipo-create-tasks [dir]` | Generate groups (15-50 tasks) |
| `/aipo-update-tasks [dir]` | Modify tasks |
| `/aipo-configure-swarm [file] [dirs...]` | Setup parallel exec (1-5 initiatives) |
| `/aipo-start-task [dir] [ID]` | Execute (for swarm agents) |

### CLI Commands

| Command | Purpose |
|---------|---------|
| `init` | Install commands + CLAUDE.md |
| `status` | Health check |
| `status --json` | JSON output (CI/CD) |
| `next` | Next task recommendation |
| `next --all` | Next per initiative |
| `next --agent [name]` | Agent assignment |
| `monitor` | Real-time swarm tracking |
| `monitor --interactive` | Live monitoring (auto-refresh) |
| `check [dir]` | Validate initiative |
| `validate [file]` | Validate swarm config |
| `list` | List initiatives |
| `unblock` | Dependency analysis |
| `swarm --cancel [file]` | Stop swarm |
| `swarm --archive [file]` | Archive completed swarm |
| `swarm --activity [file]` | Analyze agent parallelism |

## Files

### project-state.prd
```markdown
# Project State

**Project**: [Name]
**Version**: [X.Y.Z]
**Updated**: [Date]

## Overview
[Description, type, languages]

## Status
Initiatives: X active, Y completed

## Modules
### Module: [Name]
**Summary**: [<500 tokens]
**Decisions**: [List]
**Criteria**: [Checklist]
**Tech**: [Stack]
**Dependencies**: [List]
```

### initiatives/NNNN-name/description.prd
```markdown
# Initiative: [Name]

**ID**: [NNNN]
**Name**: [name]
**Status**: [Status]
**Dependencies**: [NNNN,NNNN] or None

## Problem, Solution, Criteria, Stories, Modules, Testing
```

### initiatives/NNNN-name/tasks.prd
```markdown
**ID**: [NNNN]
**Name**: [Name]
**Dependencies**: [List]
**Swarm**: [file.yml]

[START: ]
[END: ]

## Summary
**Status**: [Status]
**Progress**: X/Y (Z%)
**Group**: N

## Tasks
### Group 0: Prerequisites
- [ ] TASK-001: [Title] (Xh) **Agent**: [name]
  **Deps**: None

### Group 1-N: Features
...
```

## Architecture

**Token Efficiency**:
- Project state: Modular (<500 tokens/module)
- Initiative: Compact PRD
- Tasks: Group-based, dependency-explicit
- Swarm: Pre-assigned agents (deterministic)

**Parallel Execution**:
- Tasks in same group → parallel
- Sequential groups (0, 1, 2, ...)
- Skill-based agents (backend_1, frontend_1, ...)
- Coordinator: `aipo next --agent [name]`
- Workers: `/aipo-start-task [dir] [ID]`

**State Management**:
- All state in .prd files
- No directory renaming
- `[START:]`/`[END:]` timestamps
- Summary sections for status
- Double-binding (tasks ↔ swarm)

## Example

```
User: "Build auth + payments"

1. /aipo-plan
   → ⚡ Max Parallel: [Auth,Payments] (~2w, 2 swarms)

2. /aipo-create-initiative user-auth
   /aipo-create-tasks 0001-user-auth
   (37 tasks: 15 backend, 12 frontend, 5 infra, 5 fullstack)

3. /aipo-create-initiative payments
   /aipo-create-tasks 0002-payments
   (28 tasks: 12 backend, 10 frontend, 6 fullstack)

4. /aipo-configure-swarm 0001-multi.yml 0001-user-auth 0002-payments
   → Agents: backend_1, backend_2, frontend_1, fullstack_1
   → Tasks assigned in tasks.prd files

5. $ claude-swarm start 0001-multi.yml &
   $ python3 aipo.py monitor
   
   ⚙️ 0001-user-auth: ███████░░░ 15/37 (40%)
      Active: TASK-016 (backend_1), TASK-017 (frontend_1)
   
   ⚙️ 0002-payments: █████░░░░░ 8/28 (28%)
      Active: TASK-009 (backend_2)

6. Auto-close when complete
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Commands not showing | Run `aipo init` in project root |
| Claude Swarm not found | Install: `gem install claude-swarm` |
| Task validation fails | Check deps with `aipo check [dir]` |
| Initiative not closing | Verify last task marked `[x]` |
| Swarm validation errors | Run `aipo validate [file]`, fix warnings |
| Dependency deadlocks | Run `aipo unblock` for analysis |

## Features

- **Batch Planning**: Plan 2-5 initiatives before execution
- **Parallel Execution**: Multiple agents, multiple initiatives
- **Skill-Based Agents**: backend_1, frontend_1, infra_1, fullstack_1
- **Task Assignment**: Pre-assigned in tasks.prd (deterministic)
- **Monitoring**: Real-time progress tracking
- **Auto-Close**: Last task triggers initiative closure
- **Dependency Analysis**: `aipo unblock` for blocked work
- **Swarm Management**: Cancel/archive swarms
- **Validation**: Strict checks before swarm creation

## Best Practices

1. **Always use `/aipo-plan`** before creating initiatives
2. **Create all initiatives** before configuring swarm
3. **One swarm per batch** (1-5 initiatives)
4. **Group 0 for prerequisites** (shared setup tasks)
5. **Keep modules <500 tokens** in project-state.prd
6. **Use semantic task IDs** (TASK-001, TASK-002, ...)
7. **Document dependencies** (cross-initiative and intra-task)
8. **Monitor swarms** with `python3 aipo.py monitor`
9. **Manual start-task** only for testing/debug

## Links

- [CHANGELOG](CHANGELOG.md) - Version history
- [Templates](templates/) - Slash command templates
- [Examples](examples/) - Complete examples

---

**License**: MIT  
**Version**: 3.0.0  
**Updated**: 2025-10-14

