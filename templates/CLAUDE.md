# AI Project Orchestrator

Manage software development using batch planning + parallel execution.

## Workflow

1. `/aipo-create-project` - Initialize
2. `/aipo-plan` - Get 2-5 initiatives
3. Loop: `/aipo-create-initiative [name]` → `/aipo-create-tasks [dir]`
4. `/aipo-configure-swarm [file] [dirs...]` - Assign tasks to agents
5. User runs: `claude-swarm start [file]` + `python3 aipo.py monitor`

## Command Map

| User Intent | Command |
|-------------|---------|
| Start project | `/aipo-create-project` |
| Plan work | `/aipo-plan` |
| Add feature | `/aipo-create-initiative [name]` → `/aipo-create-tasks [dir]` |
| Parallel exec | `/aipo-configure-swarm [file] [dirs...]` |
| Check status | `python3 aipo.py status` or read `tasks.prd` Summary |

## Rules

- **Batch first**: Plan all initiatives before configuring swarm
- **One swarm**: Multiple initiatives in single swarm
- **Sequential deps**: plan → create → configure → execute
- **Agents only**: `/aipo-start-task` for swarm agents (not manual)
- **Auto-close**: Last task triggers initiative closure

## Files

```
ai-project/
├── project-state.prd
└── initiatives/NNNN-name/
    ├── description.prd
    └── tasks.prd (status: [START:], [END:], Summary)
```

## Example

```
User: "Build auth + payments"

1. /aipo-plan
2. /aipo-create-initiative user-auth → /aipo-create-tasks 0001-user-auth
3. /aipo-create-initiative payments → /aipo-create-tasks 0002-payments
4. /aipo-configure-swarm 0001-batch.yml 0001-user-auth 0002-payments
5. Tell user: "Run: claude-swarm start 0001-batch.yml"
```

