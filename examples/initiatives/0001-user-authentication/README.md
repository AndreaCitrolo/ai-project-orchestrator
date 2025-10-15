# Initiative 0001: User Authentication

**Status**: Completed  
**Type**: Example

This is a complete example initiative demonstrating the AI Project Orchestrator workflow.

## Files

**description.prd**: Full PRD including:
- Goals and user stories
- Requirements and non-goals
- Technical specifications
- Testing and deployment strategy
- Acceptance criteria

**tasks.prd**: 37 tasks organized in 7 groups:
- Metadata section (Initiative ID, Name, Dependencies, Target Date, Estimated Hours)
- [START: ] and [END: ] markers for tracking
- Group 0: Prerequisites (3 tasks)
- Group 1: Database Models (6 tasks)
- Group 2: Core Authentication Services (5 tasks)
- Group 3: API Endpoints (6 tasks)
- Group 4: Middleware & Security (4 tasks)
- Group 5: Testing (7 tasks)
- Group 6: Documentation & Deployment (6 tasks)
- Summary section with completion statistics

## Key Features Demonstrated

**Task Groups for Parallel Execution**
- Groups 1-6 have 4-7 tasks each
- Tasks within group can run in parallel
- Dependencies properly organized

**Dependency Management**
- Within-initiative dependencies
- Cross-initiative references
- Sequential group execution

**Testing Strategy**
- Unit tests (85%+ coverage)
- Integration tests for auth flows
- Security testing

**Collaboration**
- Multi-agent execution (2 agents)
- Feature branch per task
- Clear separation of concerns

## Usage

Review this example to understand:
- How to structure initiative PRDs
- How to organize tasks into groups
- How tasks.prd serves as single source of truth
- How [START: ] and [END: ] markers track initiative lifecycle
- How to handle dependencies
- How to enable parallel work

