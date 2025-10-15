# Initiatives

This directory contains all development initiatives for the project.

## Structure

Each initiative is a directory:
```
NNNN-status-name/
├── description.prd    # Initiative PRD
└── tasks.prd          # Task groups, metadata, and status tracking
```

## Status Values

- `planned` - PRD and tasks created, not started
- `active` - Work in progress
- `blocked` - Waiting on dependencies
- `review` - Complete, under review
- `completed` - All tasks done, closed
- `cancelled` - Abandoned

## Example

See `0001-user-authentication/` for a complete example showing:
- Full PRD structure
- tasks.prd with metadata section
- Task groups (0-6) with 37 tasks
- Parallel execution organization
- Status tracking via [START: ] and [END: ] markers
- Cross-initiative dependencies

## Creating Initiatives

Use: `/aipo-create-initiative`

## Workflow

1. Create initiative (generates `NNNN-name/`)
2. Generate tasks (creates tasks.prd with metadata)
3. Work on tasks (marks as `[x]`, updates Summary)
4. Auto-close (last task completion fills [END:] and marks "Completed")

