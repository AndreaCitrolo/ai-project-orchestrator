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

### 1. Analyze & Classify

```bash
/sc:workflow --breakdown --mode task-management
@agent-system-architect
```

Read all `tasks.prd`, classify: backend/frontend/infra/fullstack
Allocate agents (max 5): 1 per type, add more to busiest
Assign tasks: Update `Agent:` field + `**Swarm**: [$1]` in metadata

### 2. Build Dependency Waves

Extract from `description.prd`, determine waves (topological sort):
- Wave 1: [initiatives with no deps]
- Wave 2: [initiatives depending on Wave 1]

### 3. Generate Swarm File

```yaml
version: 1
swarm:
  name: "[Initiative Names] ([Total] tasks)"
  main: coordinator
  instances:
    coordinator:
      description: "Swarm coordinator"
      directory: .
      model: claude-sonnet-4-20250514
      connections: [list_all_agents]
      mcp_servers:
        sequential:
          command: sequential-mcp
        serena:
          command: serena-mcp
        tavily:
          command: tavily-mcp
        context7:
          command: context7-mcp
      prompt: |
        /sc:task dispatch "Choose best next tasks from ai-project/initiatives/*/tasks.prd and assign it to the most appropriate agent in order to maximize quality, parallelism and minimize the initiatives completion time" --parallel --delegate
        @agent-pm-agent
        

        
        AGENTS: [backend_1:backend, frontend_1:frontend, ...]
        DEPENDENCIES: [Wave 1: init-A,init-B | Wave 2: init-C(→A)]
        
        Get tasks: `python3 aipo.py next --agent [name]`
        Dispatch: @agent_name
        Monitor: Every 5-10 tasks
        
        Start now.
      allowed_tools: [Bash, Read, SlashCommand]
    
    backend_1:
      description: "Backend developer - Python/FastAPI expert, SQLAlchemy ORM, REST APIs, Pydantic schemas"
      directory: .
      model: claude-sonnet-4-20250514
      prompt: |
        Coordinator assigns task → execute:
        /aipo-start-task [initiative-dir] [TASK-ID]
        
        Report completion to coordinator.
      allowed_tools: [Read, Edit, Write, Bash, SlashCommand]
    
    frontend_1:
      description: "Frontend developer - Vue 3/TypeScript expert, Carbon Design System, Pinia state management"
      directory: .
      model: claude-sonnet-4-20250514
      prompt: |
        Coordinator assigns task → execute:
        /aipo-start-task [initiative-dir] [TASK-ID]
        
        Report completion to coordinator.
      allowed_tools: [Read, Edit, Write, Bash, SlashCommand]

    [... repeat for each agent]
```

**Agent patterns** (by type - SuperClaude agents used by /aipo-start-task):
- **Backend**: "Backend developer - [Lang/Framework] expert, [DB/ORM], [API]" → Uses `@agent-backend-architect`
- **Frontend**: "Frontend developer - [Framework] expert, [Design system]" → Uses `@agent-frontend-architect`
- **Infra**: "DevOps engineer - [Cloud] expert, [IaC], [CI/CD]" → Uses `@agent-devops-architect`
- **Fullstack**: "Fullstack engineer - [Backend] + [Frontend] expert" → Uses `@agent-system-architect` + `@agent-fullstack-engineer`

All agents: 3-line prompt (use /aipo-start-task, which invokes SuperClaude internally)

### 4. Write & Validate

Write `$1`, verify:
- [ ] NNNN-*-swarm.yml format
- [ ] All tasks have `Agent:` + `**Swarm**: [$1]`
- [ ] Coordinator: Sonnet 4.5, 4 MCPs, connections list, wave structure
- [ ] Agents: Sonnet 4, 3-line prompts, /aipo-start-task
- [ ] Bidirectional binding

### 5. Output

```
✅ Swarm: [filename]
Agents: [N] | Tasks: [X] | Initiatives: [N] | Dependencies: [waves]

Start: claude-swarm start [filename] --prompt "Start coordinating. Dispatch all available tasks in parallel now."
Monitor: python3 aipo.py monitor --interactive
Activity: python3 aipo.py swarm --activity [filename]
```

## Notes

**SuperClaude Syntax**:
```bash
/sc:command [action] "description" --flags
@agent-persona-name
```

**Coordinator** (14 lines):
- Model: Sonnet 4.5
- MCPs: sequential, serena, tavily, context7
- Command: `/sc:task dispatch "[goal]" --parallel --delegate` + `@agent-pm-agent`

**Agents** (3 lines each, use /aipo-start-task):
```
Coordinator assigns task → execute:
/aipo-start-task [initiative-dir] [TASK-ID]

Report completion to coordinator.
```

**SuperClaude in /aipo-start-task** (flags on commands, agents as MCP resources):
- Backend: `/sc:implement "[task]" --strict --tdd` + `@agent-backend-architect`
- Frontend: `/sc:implement "[task]" --magic` + `@agent-frontend-architect`
- Infra: `/sc:implement "[task]" --strict` + `@agent-devops-architect`
- Fullstack: `/sc:implement "[task]" --tdd` + `@agent-system-architect` + `@agent-fullstack-engineer`

**16 Personas**: backend/frontend/devops/fullstack-architect, system-architect, security-expert, qa-engineer, performance-optimizer, pm-agent, technical-writer, cto, product-owner, deep-research, analyzer, refactorer, mentor

**7 Modes**: --orchestration, --task-manage/--delegate, --uc/--ultracompressed, --brainstorm, /sc:business-panel, --research, --introspection

**Flags**: --parallel, --delegate, --seq, --strict, --tdd, --magic, --orchestrate, --ultracompressed

