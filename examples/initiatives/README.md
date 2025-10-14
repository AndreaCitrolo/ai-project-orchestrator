# Initiatives

This directory contains all development initiatives for the project.

## Structure

Each initiative is a directory:
```
NNNN-status-name/
├── description.prd    # Initiative PRD
├── tasks.prd          # Task groups and checklist
└── status.prd         # Progress tracking
```

## Status Values

- `planned` - PRD and tasks created, not started
- `active` - Work in progress
- `blocked` - Waiting on dependencies
- `review` - Complete, under review
- `completed` - All tasks done, closed
- `cancelled` - Abandoned

## Files

**INDEX.prd**: Registry of all initiatives with status and dependencies

## Example

See `0001-completed-user-authentication/` for a complete example showing:
- Full PRD structure
- Task groups (0-6) with 37 tasks
- Parallel execution organization
- Status tracking
- Cross-initiative dependencies

## Creating Initiatives

Use: `../templates/create-initiative`

## Workflow

1. Create initiative (generates `NNNN-planned-name/`)
2. Generate tasks
3. Rename to `NNNN-active-name/`
4. Work on tasks
5. Close (renames to `NNNN-completed-name/`)

