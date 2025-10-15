# AIPO Slash Commands

[Claude Code slash commands](https://docs.claude.com/en/docs/claude-code/slash-commands) for AI Project Orchestrator.

## Install

```bash
python3 aipo.py init
```

Installs:
- `CLAUDE.md` → project root (workflow enforcement)
- Commands → `.claude/commands/`

## Commands

| Command | Purpose |
|---------|---------|
| `/aipo-create-project` | Initialize workspace |
| `/aipo-plan` | Get strategic options (3-7 initiatives, 4-5 strategies) |
| `/aipo-create-initiative [name]` | Create initiative PRD |
| `/aipo-create-tasks [dir]` | Generate task groups |
| `/aipo-update-tasks [dir]` | Modify tasks |
| `/aipo-configure-swarm [file] [dirs...]` | Setup parallel execution (1-5 initiatives) |
| `/aipo-start-task [dir] [ID]` | Execute task (for swarm agents) |

## Workflow

```bash
# 1. Claude Code (with CLAUDE.md context)
> /aipo-create-project
> /aipo-plan
> /aipo-create-initiative auth → /aipo-create-tasks 0001-auth
> /aipo-create-initiative payments → /aipo-create-tasks 0002-payments
> /aipo-configure-swarm 0001-batch.yml 0001-auth 0002-payments

# 2. Execute (swarm uses /aipo-start-task automatically)
$ claude-swarm start 0001-batch.yml
$ python3 aipo.py monitor
```

## Swarm Details

- **Classification**: backend/frontend/infra/fullstack
- **Agents**: Skill-typed (backend_1, frontend_1, etc.)
- **Assignment**: Tasks pre-assigned in tasks.prd (Agent: field)
- **Coordinator**: Uses `aipo next --agent [name]`
- **Workers**: Use `/aipo-start-task` only

## Format

```markdown
---
description: Brief description
argument-hint: [args]
allowed-tools: Read, Write, Bash
---

# Command

Instructions...
```

- `$1, $2` - Positional args
- `@file` - File reference
- `!cmd` - Bash execution

