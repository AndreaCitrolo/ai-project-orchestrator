---
description: Configure swarm for parallel execution
argument-hint: [NNNN-name-swarm.yml] [initiative-dirs...]
allowed-tools: Read, Write, Bash
---

# Configure Swarm

## Validation

1. **Check filename**: `NNNN-name-swarm.yml` (e.g., `0001-backend-swarm.yml`)
   - If wrong → STOP, ask for correct format

2. **Validate initiatives** (1-5 supported):
   ```bash
   !python3 ai-project-orchestrator/aipo.py check ai-project/initiatives/[dir]
   ```
   - Must show "✅ ready" with NO warnings
   - ⚠️ Warnings = STOP (fix first)
   - ❌ Errors = STOP (fix first)

## Steps

### 1. Classify Tasks

Read all `tasks.prd` files, classify pending tasks:
- **backend**: API, database, models
- **frontend**: UI, components, pages
- **infra**: CI/CD, deploy, monitoring
- **fullstack**: End-to-end features

### 2. Determine Agents

**Max ~5 agents total**. Allocate by workload:

1. Count tasks per type
2. Assign 1 agent per type (if tasks exist)
3. If <5 agents, add more to busiest type(s)

Examples:
- 45 backend, 12 frontend → `backend_1, backend_2, backend_3, frontend_1` (4 total)
- 20 backend, 20 frontend, 15 infra → `backend_1, backend_2, frontend_1, infra_1` (4 total)
- 60 backend only → `backend_1, backend_2, backend_3, backend_4, backend_5` (5 total)

### 3. Assign Tasks

For each pending task:
1. Classify type (backend/frontend/infra/fullstack)
2. Assign to least-loaded agent of that type
3. Update `tasks.prd` with `Agent: [agent_name]` field
4. Add `**Swarm**: [$1]` to metadata section

### 4. Generate Swarm File

```yaml
version: 1
swarm:
  name: "[Initiative Names] ([Total] tasks)"
  main: coordinator
  instances:
    coordinator:
      description: "Coordinator for parallel execution of [N] initiatives"
      directory: .
      model: claude-opus-4-20250514
      connections: [list_all_agents]
      prompt: |
        You are the swarm coordinator managing [N] agents working on [X] tasks across [Y] initiatives.

        You are powered by Claude Opus 4 - use your advanced reasoning to optimize task distribution.

        **AGENTS** (accessible via MCP tools):
        - backend_1: Use mcp__backend_1__task tool
        - frontend_1: Use mcp__frontend_1__task tool
        [... list all agents with their MCP tool names]

        **YOUR CONTINUOUS WORKFLOW**:

        1. **Check all agents for available tasks**:
           ```bash
           python3 ai-project-orchestrator/aipo.py next --agent backend_1
           python3 ai-project-orchestrator/aipo.py next --agent frontend_1
           [... for each agent]
           ```

        2. **Dispatch tasks to agents**:
           - If output is "agent: /aipo-start-task [dir] [TASK-ID]" → dispatch to @agent
           - If output is "agent: All assigned tasks complete" → agent is done
           - If no task available (dependencies) → agent waits

        3. **When agent completes**:
           - Immediately get next task for that agent
           - Check if completion unblocked other agents (dependencies satisfied)
           - Dispatch new work to any newly unblocked agents

        4. **Monitor progress periodically**:
           - Every 5-10 task completions, run: `python3 ai-project-orchestrator/aipo.py status`
           - Report progress to user

        5. **Keep running until all done**:
           - Continue until ALL agents report "All assigned tasks complete"
           - Then report final summary

        **CRITICAL DEPENDENCY RULES** (YOU MUST ENFORCE):
        [If initiative A depends on B:]
        1. **[init-A]** can ONLY start AFTER **[init-B]** is 100% complete
        2. Before dispatching ANY task from [init-A], verify [init-B] is complete via status check
        [Repeat for all dependencies]

        **HOW TO ENFORCE**:
        - Before dispatching ANY task from dependent initiative, verify prerequisites complete
        - If agent gets task from blocked initiative, DO NOT dispatch it - get next task instead
        - Agents may be idle waiting for dependencies - that's OK

        **WAVE PATTERN** (if dependencies exist):
        - Wave 1: Independent initiatives ([list])
        - Wave 2: Initiatives depending on Wave 1 ([list])
        [... for each wave]

        **COORDINATION RULES**:
        - PREFER delegating to agents using @agent_name syntax
        - You CAN execute tasks yourself if:
          * All agents are blocked waiting for dependencies
          * You need to unblock agents by completing a blocking task
          * An agent is stuck or unavailable
        - Do NOT stop until all [X] tasks complete
        - Keep checking for newly available work as dependencies resolve
        - Be proactive and persistent
        - Actively block work from initiatives with unmet dependencies

        **UNBLOCKING STRATEGY**:
        If agents are idle due to dependencies, you may execute critical blocking tasks
        yourself to unblock them.

        **TRUE PARALLEL EXECUTION**:
        Dispatch tasks to agents using MCP tools. Invoke multiple agents SIMULTANEOUSLY
        for true parallelism.

        To dispatch a task to an agent:
        ```
        Use mcp__backend_1__task with instructions: "Execute /aipo-start-task [dir] [TASK-ID]"
        ```

        **CRITICAL**: Invoke multiple MCP tools simultaneously for true parallelism!

        START NOW: Check all agents and dispatch in parallel.
      allowed_tools: [Bash, Read, Edit, Write, SlashCommand]

    backend_1:
      description: "Backend developer - Python/FastAPI expert, SQLAlchemy ORM, REST APIs, Pydantic schemas"
      directory: .
      model: claude-sonnet-4-20250514
      prompt: |
        Execute backend tasks assigned to you (backend_1).

        The coordinator will tell you which task to execute.
        When given a task, use:

        /aipo-start-task [initiative-dir] [TASK-ID]

        Example: /aipo-start-task 0003-backend-models TASK-001

        Focus on:
        - SQLAlchemy models and database layer
        - FastAPI endpoints and Pydantic schemas
        - Backend tests and utilities

        After completing a task, report to the coordinator.
      allowed_tools: [Read, Edit, Write, Bash, SlashCommand]

    frontend_1:
      description: "Frontend developer - Vue 3/TypeScript expert, Carbon Design System, Pinia state management"
      directory: .
      model: claude-sonnet-4-20250514
      prompt: |
        Execute frontend tasks assigned to you (frontend_1).

        The coordinator will tell you which task to execute.
        When given a task, use:

        /aipo-start-task [initiative-dir] [TASK-ID]

        Example: /aipo-start-task 0005-frontend-foundation TASK-001

        Focus on:
        - Vue 3 components and routing
        - Pinia stores and state management
        - Carbon Design System integration
        - Entity pages and CRUD interfaces

        After completing a task, report to the coordinator.
      allowed_tools: [Read, Edit, Write, Bash, SlashCommand]

    [... repeat for each agent with persona and skills]
```

### 5. Analyze Dependencies

Extract from `description.prd` **Dependencies** section:
1. Build dependency graph
2. Determine waves (topological sort)
3. Generate coordinator rules for each dependency

Example:
- If 0004 depends on 0003 → Add rule: "0004 can ONLY start AFTER 0003 is 100% complete"
- Wave 1: [initiatives with no deps]
- Wave 2: [initiatives depending on Wave 1]

### 6. Populate Template

For **coordinator**:
- List all agents with MCP tool names
- Add `aipo next --agent` commands for each
- Insert dependency rules (from step 5)
- Insert wave pattern (from step 5)
- Fill in task/initiative counts

For **agents** - Create persona-based descriptions with specific skills:

**Backend agents**:
- Description: "Backend developer - [Language/Framework] expert, [DB/ORM], [API style], [Schema tool]"
- Examples:
  - "Backend developer - Python/FastAPI expert, SQLAlchemy ORM, REST APIs, Pydantic schemas"
  - "Backend developer - Django expert, PostgreSQL, GraphQL, Celery task queue"
  - "Backend developer - Node.js/Express expert, Prisma ORM, TypeScript, OpenAPI"
- Focus: SQLAlchemy models, FastAPI endpoints, Pydantic schemas, backend tests

**Frontend agents**:
- Description: "Frontend developer - [Framework/Version] expert, [Design system], [State management]"
- Examples:
  - "Frontend developer - Vue 3/TypeScript expert, Carbon Design System, Pinia state management"
  - "Frontend developer - React 18 expert, Material-UI, Redux Toolkit, React Query"
  - "Frontend developer - Angular expert, Tailwind CSS, NgRx, RxJS"
- Focus: Components, routing, state management, design system integration, entity pages

**Infra agents**:
- Description: "DevOps engineer - [Cloud] expert, [IaC tool], [Container platform], [CI/CD]"
- Examples:
  - "DevOps engineer - AWS/Pulumi expert, Docker, ECS/Fargate, Buildkite CI/CD"
  - "DevOps engineer - GCP/Terraform expert, Kubernetes, Cloud Run, GitHub Actions"
  - "DevOps engineer - Azure expert, Bicep, AKS, Azure DevOps pipelines"
- Focus: Docker, CI/CD, deployment, monitoring, infrastructure as code

**Fullstack agents**:
- Description: "Fullstack engineer - [Backend] + [Frontend] expert, [specialty]"
- Examples:
  - "Fullstack engineer - Python/FastAPI + Vue 3 expert, end-to-end features"
  - "Fullstack engineer - Node.js + React expert, real-time WebSocket features"
- Focus: End-to-end features, API integration, full-stack testing

### 7. Write File

Write `$1` with fully populated config.

### 8. Output

```
✅ Swarm: [filename]

Agents: [N] ([list with types])
Tasks: Backend:X→Y agents, Frontend:A→B agents
Initiatives: [N] ([names])
Dependencies: [wave structure summary]

Next: claude-swarm start [filename]
Monitor: python3 aipo.py monitor --interactive
Activity: python3 aipo.py swarm [filename] --activity
```

## Validation Checklist

After writing file:
- [ ] Swarm file name in `NNNN-*-swarm.yml` format
- [ ] All pending tasks have `Agent:` field in `tasks.prd`
- [ ] All `tasks.prd` have `**Swarm**: [file]` in metadata
- [ ] Coordinator has `connections:` list with all agents
- [ ] Coordinator uses `python3 aipo.py next --agent [name]` for each agent
- [ ] Coordinator prompt includes dependency rules (if any)
- [ ] Coordinator prompt includes wave pattern (if dependencies exist)
- [ ] Coordinator prompt lists all MCP tools (mcp__agent__task)
- [ ] Coordinator has Opus 4 model (best for coordination)
- [ ] Worker agents use Sonnet 4 model
- [ ] Workers use `/aipo-start-task [dir] [TASK-ID]`
- [ ] Workers have SlashCommand in allowed_tools
- [ ] All initiatives validated (no warnings)
- [ ] Bidirectional binding verified

## Error Handling

| Issue | Action |
|-------|--------|
| Wrong filename | STOP, ask for NNNN-name-swarm.yml |
| Initiative warnings | STOP, must fix warnings first |
| Initiative blocked | STOP, fix dependencies |
| No pending tasks | STOP, nothing to configure |
| >5 initiatives | STOP, max 5 supported |

## Notes

**Key Patterns from Working Swarms**:
- **Persona-based agents**: Each agent has a specific role and skill set in their description
  - Example: "Backend developer - Python/FastAPI expert, SQLAlchemy ORM, REST APIs, Pydantic schemas"
  - NOT: "Backend development tasks" or "Backend developer"
- **Double-binding**: tasks.prd references swarm file, swarm config lists initiatives
- **Skill-typed agents**: backend_1, frontend_1 (not generic worker_1)
- **Pre-assigned tasks**: Each task has `Agent:` field for deterministic routing
- **Coordinator model**: Opus 4 for complex reasoning and optimization
- **Worker model**: Sonnet 4 for efficient task execution
- **MCP connections**: Coordinator uses `connections:` + `mcp__agent__task` tools
- **Continuous loop**: Coordinator keeps checking and dispatching until all complete
- **Dependency enforcement**: Coordinator actively blocks work from initiatives with unmet deps
- **Status monitoring**: Coordinator runs `aipo status` periodically to track progress
- **True parallelism**: Coordinator invokes multiple MCP tools simultaneously
- **Unblocking strategy**: Coordinator can execute tasks itself if agents are all blocked

**Example Task Dispatch**:
```
Coordinator: Use mcp__backend_1__task with instructions: "Execute /aipo-start-task 0003-backend-models TASK-001"
Agent backend_1: Receives task, executes /aipo-start-task, reports completion
Coordinator: Immediately runs aipo next --agent backend_1 to get next task
```

