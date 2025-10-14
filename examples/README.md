# Examples

This directory contains complete, realistic examples of how to use the AI Project Orchestrator.

## Purpose

These examples demonstrate:
- How to structure initiatives with PRDs, task lists, and status tracking
- How to use task groups for parallel execution
- How to manage dependencies within and across initiatives
- How to reference project state modules
- Best practices for organizing work
- The `.ai-orchestrator` file showing command reference

## Key Files

- **`project-state-example.prd`** - Extended example (TaskFlow SaaS project)
- **`.ai-orchestrator`** - Quick reference showing available commands and workflow
- **`modules/`** - Example detailed module documentation (see modules/README.md)
- **`initiatives/`** - Example initiatives showing complete workflow (see initiatives/README.md)

**Note**: See `../project-state.prd` for AI Project Orchestrator's own project state (reference implementation).

## Example Initiatives

### initiatives/0001-completed-user-authentication

A complete example showing how to implement a user authentication system with:
- JWT-based authentication
- Role-based access control (RBAC)
- Password hashing and validation
- Multiple task groups enabling parallel work
- Dependencies properly organized
- References to project state modules

**Key Learning Points:**
- Task Group 0 contains prerequisite setup
- Models are in earlier groups than APIs that use them
- Cross-initiative dependencies are clearly marked
- Status tracking shows progress through task groups

## How to Use These Examples

1. **Study the Structure**: Review the folder structure and file organization
2. **Read the PRD**: See how initiatives reference the project state and specific modules
3. **Analyze Task Groups**: Understand how tasks are grouped for parallel execution
4. **Follow Dependencies**: See how tasks reference each other within and across initiatives
5. **Track Status**: Learn how status files track progress and blockers

## Adapting for Your Project

Feel free to copy and modify these examples as templates for your own initiatives. Replace the specific content with your project's requirements while maintaining the structure and conventions.

