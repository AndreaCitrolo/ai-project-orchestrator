# AI Project Orchestrator

A structured framework for AI agents to efficiently develop complex projects with parallel execution and reduced context requirements.

---

## 🎯 Overview

Addresses critical challenges in AI-assisted development:
- Context loss between sessions
- Poor dependency tracking  
- No parallel execution support
- Inconsistent project state

**Solution:**
- Modular project state (<500 tokens/module)
- Initiative-based work organization
- Task groups for parallel agent execution
- Explicit dependency management

**Design Principles:**
- Token efficient: Minimal templates, info in PRD files
- Enforcing: Critical steps cannot be skipped
- File-centric: All state persisted, minimal LLM output
- Validation: Checkpoints before proceeding

---

## 📁 Directory Structure

```
ai-project-orchestrator/
├── README.md                   # Complete documentation
├── LICENSE                     # MIT License
├── project-state.prd           # This project's state
├── templates/                  # Executable commands
│   ├── create-project          # Initialize new project
│   ├── create-initiative       # Create new initiative
│   ├── generate-tasks          # Generate task groups
│   ├── update-tasks            # Add or delete tasks
│   ├── start-task              # Start, work, and complete task
│   └── close-initiative        # Close completed initiative
└── examples/                   # Complete examples
    ├── project-state-example.prd  # Extended example
    ├── .ai-orchestrator        # Command reference
    ├── README.md               # Examples guide
    ├── modules/                # Example module docs
    │   ├── README.md
    │   └── authentication-system.prd
    └── initiatives/            # Example initiatives
        ├── README.md           # Initiatives guide
        ├── INDEX.prd           # Initiative registry
        └── 0001-completed-user-authentication/
            ├── README.md       # Initiative example guide
            ├── description.prd
            ├── tasks.prd
            └── status.prd
```

---

## 🚀 Quick Start

### 1. Create New Project

Initialize your project workspace:

```bash
# In your AI assistant (Claude, Cursor, etc.):
Use templates/create-project

# Answer questions about your project:
# - Project name, type, languages
# - Initial modules (2-4)
# - Tech stack

# Creates ai-project/ directory with:
# - project-state.prd
# - .ai-orchestrator guide
```

### 2. Create First Initiative

```bash
# From within ai-project/ directory:
Use ../templates/create-initiative

# Provide feature description when prompted
# Answer clarifying questions
# PRD is generated in initiatives/ directory
```

### 3. Generate Tasks

```bash
Use ../templates/generate-tasks 0001-planned-[name]

# Tasks organized into groups for parallel execution
# Saved to initiatives/0001-planned-[name]/tasks.prd
```

### 4. Start Working

```bash
# Rename initiative from 'planned' to 'active'
mv initiatives/0001-planned-[name] initiatives/0001-active-[name]

# Start first task (handles full workflow: start → work → complete)
Use ../templates/start-task 0001-active-[name] TASK-001
```

### 5. Parallel Execution (Multiple Agents)

```bash
# Agent 1
Use ../templates/start-task 0001-active-[name] TASK-003

# Agent 2 (simultaneously)
Use ../templates/start-task 0001-active-[name] TASK-004

# Agent 3 (simultaneously)
Use ../templates/start-task 0001-active-[name] TASK-005
```

All agents work on tasks in the same group in parallel!

### 6. Close Initiative

```bash
# When all tasks complete:
Use ../templates/close-initiative 0001-active-[name]

# Updates project-state.prd
# Renames to 0001-completed-[name]
# Unblocks dependent initiatives
```

---

## 🏗️ Key Concepts

### Task Groups

Tasks organized into sequential groups. Within a group, tasks run in parallel:

```
Group 0: Prerequisites (env, database)
   ↓ (all must complete)
Group 1: Models (can work in parallel)
   ↓
Group 2: Services (can work in parallel)
   ↓
Group 3: APIs (can work in parallel)
```

**3-5 tasks per group** = optimal for multi-agent execution

### Initiative Status

Status in directory name:
- `NNNN-planned-name` - PRD done, tasks not started
- `NNNN-active-name` - Work in progress
- `NNNN-blocked-name` - Waiting on dependencies
- `NNNN-completed-name` - All done
- `NNNN-cancelled-name` - Abandoned

### Naming Conventions

- **Initiatives**: `0001-status-name` (4-digit, lowercase-with-hyphens)
- **Tasks**: `TASK-001` (3-digit within initiative)
- **Files**: `.prd` extension (not .md)
- **Modules**: `module-name.prd`

### Dependencies

**Within initiative:**
```
- [ ] TASK-005: Create API endpoint
  Dependencies: TASK-003, TASK-004
```

**Cross-initiative:**
```
- [ ] TASK-010: Add authentication
  Dependencies: TASK-008
  Cross-initiative: 0001-completed-auth/TASK-015
```

---

## 📋 Templates (Commands)

All templates are executable commands for AI assistants:

| Command | Purpose |
|---------|---------|
| `templates/create-project` | Initialize new project workspace |
| `templates/create-initiative` | Create new initiative with PRD |
| `templates/generate-tasks` | Generate parallelized task groups |
| `templates/update-tasks` | Add or delete tasks (preserves existing) |
| `templates/start-task` | Start, work on, and complete task (full workflow) |
| `templates/close-initiative` | Close and update project state |

Each command:
- Enforces critical steps (no skipping)
- Validates before proceeding
- Minimal output (info in PRD files)
- Strict error handling

---

## 💡 Workflow Example

### Scenario: New Project with User Authentication

**Step 0: Initialize Project** (if starting fresh)
```
> Use templates/create-project
AI: "What is the name of your project?"
You: "TaskFlow - Task Management App"
AI: [asks about type, languages, modules]
AI: "✅ Created ai-project/ with project-state.prd and .ai-orchestrator"
```

**Step 1: Create Initiative**
```
> cd ai-project
> Use ../templates/create-initiative
AI: "What problem does this solve?"
You: "Users need to login securely"
AI: [asks more questions]
AI: "✅ Created initiatives/0001-planned-user-auth/"
```

**Step 2: Generate Tasks**
```
> Use ../templates/generate-tasks 0001-planned-user-auth
AI: [generates 37 tasks in 7 groups]
AI: "✅ Tasks saved to initiatives/0001-planned-user-auth/tasks.prd"
```

**Step 3: Start Work**
```
> Rename to active: mv initiatives/0001-planned-user-auth initiatives/0001-active-user-auth
> Use ../templates/start-task 0001-active-user-auth TASK-001

TASK-001: Set up development environment
Status: DONE
Group 0: 1/3 tasks
Next: TASK-002
```

**Step 4: Parallel Execution (2 agents)**
```
# Agent 1
> Use ../templates/start-task 0001-active-user-auth TASK-004
TASK-004: Create User model
Status: DONE
Group 1: 1/4 tasks
Next: TASK-005

# Agent 2 (simultaneously)
> Use ../templates/start-task 0001-active-user-auth TASK-005
TASK-005: Create Role model
Status: DONE
Group 1: 2/4 tasks
Next: TASK-006
```

**Step 5: Close**
```
> Use ../templates/close-initiative 0001-active-user-auth

Initiative 0001: CLOSED
Modules updated: Authentication System
Unblocked: None
```

---

## 📊 Benefits

### Context Efficiency
- Agents read only relevant modules (<500 tokens each)
- 50%+ reduction in context per task
- Faster task startup

### Parallel Execution
- 2 agents → 60-70% time reduction
- 3 agents → 50-60% time reduction
- Clear task boundaries prevent conflicts

### Dependency Management
- Explicit within/cross-initiative dependencies
- Blocked tasks identified before work starts
- No wasted effort on blocked work

### Consistency
- Single source of truth (project-state.prd)
- State evolves with project
- Clear history in completed initiatives

---

## 🎓 Learning Resources

**Essential Reading:**
1. [project-state.prd](project-state.prd) - This project's state (reference implementation)
2. [examples/project-state-example.prd](examples/project-state-example.prd) - Extended example (TaskFlow SaaS)
3. [examples/initiatives/0001-completed-user-authentication/](examples/initiatives/0001-completed-user-authentication/) - Complete initiative example
4. See "Examples and Use Cases" section below for detailed scenarios

**Commands:**
- [templates/create-project](templates/create-project) - Project initialization
- [templates/create-initiative](templates/create-initiative) - Full command documentation
- [templates/generate-tasks](templates/generate-tasks) - Task generation rules
- [templates/update-tasks](templates/update-tasks) - Add/delete tasks with validation
- [templates/start-task](templates/start-task) - Complete task workflow (start → work → complete)
- [templates/close-initiative](templates/close-initiative) - Closing process

---

## 🚨 Common Pitfalls

### ❌ Missing Group 0
Don't start features without setup tasks.  
✅ Always create Group 0 with environment, database, config.

### ❌ Too Many Tasks in One Group
Don't put 20 tasks in Group 1.  
✅ Break into groups of 3-5 tasks for parallelism.

### ❌ Wrong Dependency Order
Don't create API before the model it uses.  
✅ Follow: Models → Services → APIs → UI

### ❌ Forgetting Cross-Initiative Deps
Don't assume other initiative's work exists.  
✅ Explicitly reference: `0001-completed-base/TASK-010`

### ❌ Bloated Project State
Don't write 2000-token modules.  
✅ Keep modules <500 tokens, link to detailed docs in separate module files if needed

---

## 📈 Success Metrics

Track these to measure effectiveness:

1. **Context Reduction**: Tokens per task (<50% vs without system)
2. **Parallelism**: Average tasks per group (target: 3-5)
3. **Velocity**: Initiative completion time (target: 60-70% with 2 agents)
4. **Dependency Errors**: Blocked tasks (target: <5%)
5. **Agent Productivity**: Tasks/agent/day

---

## 🔧 Best Practices

### Token Efficiency
- Modules: <500 tokens (ENFORCED)
- Status updates: Timestamp + brief note only
- Task descriptions: Concise, action-oriented
- No verbose LLM output - info in PRD files

### Enforcement
- Templates validate before proceeding
- Critical steps: Testing, file updates (REQUIRED)
- Dependencies checked automatically
- NO skipping validation checklists

### Task Organization
- Group 0: ALWAYS prerequisites
- Groups 1+: 3-5 tasks (parallel execution)
- Dependencies: BEFORE use, not after
- Estimates: 1-6h per task

### File-Centric State
- All info in PRD files (not LLM output)
- project-state.prd: Source of truth
- status.prd: Append-only log
- tasks.prd: Single checklist

### Multi-Agent Coordination
- Separate branches per task
- Rebase frequently
- status.prd: Coordination point
- Group completion: Merge point

---

## 📝 Naming Conventions

Consistent naming ensures clarity, enables automation, and helps LLMs parse and understand the project structure.

### Initiatives

**Directory Pattern**: `NNNN-status-brief-descriptive-name`

- `NNNN`: 4-digit zero-padded sequential number (0001, 0002, ..., 9999)
- `status`: planned, active, blocked, review, completed, cancelled
- Brief, lowercase, hyphen-separated descriptive name

**Examples**:
```
✅ Correct:
  0001-planned-user-authentication
  0002-active-dashboard-ui
  0015-blocked-payment-integration
  0100-completed-database-migration

❌ Incorrect:
  1-planned-user-auth              (not zero-padded)
  001-active-user-authentication   (only 3 digits)
  0001_planned_user_authentication (underscore instead of hyphen)
  0001-Planned-User-Authentication (uppercase letters)
  0001-user-authentication         (missing status)
```

**Rules**:
- Numbers are sequential in order of creation
- Numbers are never reused, even if an initiative is cancelled
- Status is always part of the directory name
- All lowercase with hyphens

### Tasks

**Task ID Pattern**: `TASK-XXX`

- `TASK-` prefix (uppercase)
- 3-digit zero-padded number within the initiative

**Examples**: `TASK-001`, `TASK-015`, `TASK-100`

**Task Group Pattern**: `Task Group N: Descriptive Name`

**Examples**:
```
Task Group 0: Prerequisites
Task Group 1: Database Models
Task Group 2: Core Services
```

### Modules

**In project-state.prd**: `Module: Descriptive Name`

**Examples**:
```
Module: Authentication System
Module: Database Layer
Module: API Gateway
```

**Module Files**: `module-name.prd` (lowercase with hyphens)

**Examples**: `authentication-system.prd`, `database-layer.prd`

### Files

**Initiative Files** (exact names):
```
NNNN-status-name/
  ├── description.prd
  ├── tasks.prd
  └── status.prd
```

**Template Files**: executable commands (no extension)
```
templates/create-initiative
templates/generate-tasks
templates/start-task
```

### References

**Within-Initiative**: `Dependencies: TASK-003, TASK-005`

**Cross-Initiative**: `Cross-initiative: 0001-completed-auth/TASK-015`

**Module References in PRDs**:
```markdown
## References

**Project State**: project-state.prd
**Target Modules**:
- Authentication System (to be created)
- Database Layer (existing)
```

### Status Values

Use these exact values:
- `planned` - PRD created, not started
- `active` - Work in progress
- `blocked` - Waiting on dependencies
- `review` - Complete, under review
- `completed` - All done, closed
- `cancelled` - Abandoned

### Dates

**Format**: `YYYY-MM-DD` (ISO 8601)

**Examples**: `2025-10-10`, `2025-01-05`

### Quick Reference

| Item | Pattern | Example |
|------|---------|---------|
| Initiative Directory | `NNNN-status-name` | `0001-planned-user-auth` |
| Task ID | `TASK-XXX` | `TASK-015` |
| Module Name | `Module: Name` | `Module: Auth System` |
| Module File | `name.prd` | `auth-system.prd` |
| Task Group | `Task Group N: Name` | `Task Group 2: Services` |
| Date | `YYYY-MM-DD` | `2025-10-10` |
| Status | Exact text | `active` |

---

## 💼 Examples and Use Cases

### Scenario 1: Greenfield Web Application

**Context**: Starting a new task management SaaS app from scratch

#### Step 1: Initialize Project State

Create `project-state.prd`:

```markdown
# Project State

**Last Updated**: 2025-10-10
**Project**: TaskFlow - Task Management SaaS
**Version**: 0.1.0

## Overview

Task management SaaS for small teams.

**Project Type**: Web Application (SaaS)
**Primary Language(s)**: Python (backend), TypeScript (frontend)
**Architecture Pattern**: Monolith with separate frontend

## Modules

### Module: Development Environment

**Summary**: Local development setup with Docker Compose.

**Key Decisions**:
- Docker Compose for local dev
- Python 3.11 + FastAPI
- Next.js 14 for frontend

**Tech Stack**: Docker, Python 3.11, Node.js 20, PostgreSQL 15

**Interfaces**:
- `make setup`: Initialize
- `make dev`: Start services
```

#### Step 2: Create First Initiative

```
Use templates/create-initiative

"I want to build user authentication with email/password and JWT tokens"
```

AI asks questions (testing strategy, git workflow, deployment, etc.)

**Generated**: `initiatives/0001-planned-user-authentication/`

#### Step 3: Generate Tasks

```
Use templates/generate-tasks 0001-planned-user-authentication
```

**Generated**: 37 tasks in 7 task groups

#### Step 4: Execute with 2 Agents

**Agent 1**: Works on Group 0 (setup)
**Agent 2**: Waits for Group 0

After Group 0 completes:

**Agent 1**: `TASK-003: Create User model`
**Agent 2**: `TASK-004: Create Role model`

Both work in parallel!

#### Step 5: Close Initiative

```
Use templates/close-initiative 0001-active-user-authentication
```

**Result**: 37 tasks in 2 weeks (vs 3-4 weeks single agent)

---

### Scenario 2: Multi-Agent Parallel Execution

**Context**: Large initiative with 60 tasks, using 3 agents

**Initiative**: `0005-active-dashboard-ui` (60 tasks, 8 groups)

#### Execution Timeline

**Week 1 - Group 0: Setup**
- Agent-1: TASK-001 (Setup Next.js)
- Agents 2&3 wait

**Week 1 - Group 1: Components**
- Agent-1: TASK-005 (Button component)
- Agent-2: TASK-006 (Input component)
- Agent-3: TASK-007 (Card component)

All working in parallel on separate branches!

**Week 2 - Group 2: Pages**
- Agent-1: TASK-012 (Dashboard page)
- Agent-2: TASK-013 (Projects page)
- Agent-3: TASK-014 (Tasks page)

**Week 2 - Group 3: API Integration**
- Agent-1: TASK-020 (Dashboard APIs)
- Agent-2: TASK-021 (Projects APIs)
- Agent-3: TASK-022 (Tasks APIs)

#### Results

- **Duration**: 3 weeks with 3 agents
- **Single Agent Estimate**: 7-8 weeks
- **Speedup**: ~2.5x
- **Merge Conflicts**: 8 (resolved quickly)

---

### Scenario 3: Cross-Initiative Dependencies

**Context**: Multiple initiatives with dependencies

#### Initiative Structure

```
0000-completed-api-framework
├─> 0001-completed-user-auth
│   ├─> 0003-active-user-profiles
│   └─> 0004-planned-admin-panel [BLOCKED]
└─> 0002-completed-database-setup
    └─> 0005-active-analytics
```

#### Handling Blocked Initiative

**Initiative 0004** status:
```markdown
Status: blocked
Waiting on: 0003-user-profiles/TASK-020
```

**Agent workflow**:
1. Attempts to start TASK-003
2. Checks cross-initiative dependency
3. Finds 0003/TASK-020 not complete
4. Agent recommends working on tasks without dependencies

#### Unblocking Process

Once 0003 completes:

1. Close initiative 0003
2. System updates index: 0004 now `planned` (ready)
3. Agent can proceed with 0004 tasks

---

### Scenario 4: Large Refactoring

**Context**: Migrating from REST to GraphQL API

**Challenge**:
- 50+ REST endpoints
- Can't break existing functionality
- Want to test incrementally

**Solution**: Phased initiative

#### Task Organization

```markdown
## Task Group 0: Infrastructure
- TASK-001: Install GraphQL libraries
- TASK-002: Set up GraphQL server at /graphql

## Task Group 1: Schema (3 agents parallel)
- TASK-004: Define User schema
- TASK-005: Define Project schema
- TASK-006: Define Task schema

## Task Group 2: Resolvers (4 agents parallel)
- TASK-008: User resolvers
- TASK-009: Project resolvers
- TASK-010: Task resolvers

## Task Group 3: Frontend - Mocked
- TASK-015: Update Dashboard (mocked GraphQL)
- TASK-016: Update Projects (mocked GraphQL)

## Task Group 4: Integration
- TASK-020: Connect Dashboard to real GraphQL
- TASK-021: Connect Projects to real GraphQL
```

**Key Technique**: Group 3 uses mocked responses, allowing frontend work before backend is complete. Group 4 integrates with real backend.

**Results**: 4 weeks with 3-4 agents (vs 10-12 weeks sequential)

---

### Common Patterns

#### Pattern 1: Foundation First

```
Group 0: Environment, DB, Config
Group 1: Models, Core Services
Group 2: Business Logic
Group 3: APIs
Group 4: UI
Group 5: Testing
Group 6: Deployment
```

**Use when**: Building new features from scratch

#### Pattern 2: Parallel Streams

```
Stream A: Backend (Groups 0-3)
Stream B: Frontend with Mocks (Groups 0-2)
Integration: Connect A + B (Group 4)
```

**Use when**: Frontend and backend can develop independently

#### Pattern 3: Incremental Replacement

```
Group 0: New system setup
Group 1: Migrate Component A (alongside old)
Group 2: Migrate Component B
Group 3: Migrate Component C
Group 4: Deprecate old system
```

**Use when**: Replacing existing system without breaking it

---

## 🔄 Migration Guide

### From ai-dev-tasks

#### Overview of Changes

| Feature | ai-dev-tasks | AI Project Orchestrator |
|---------|--------------|---------------------------|
| **Work Organization** | Single PRD + task list | Initiatives with PRDs + task groups |
| **Task Structure** | Parent tasks + subtasks | Task groups (0, 1, 2, ...) |
| **Parallel Execution** | Not supported | Built-in via task groups |
| **Project State** | Not tracked | project-state.prd with modules |
| **Dependencies** | Implicit | Explicit within/cross-initiative |
| **Multi-Agent** | Single agent focus | Designed for 2-3+ agents |

#### Migration Steps

**Phase 1: Setup (30 minutes)**

1. **Create project-state.prd**:
   - Add project overview
   - Define 2-3 initial modules (Dev Environment, Database, API)
   - Keep each module <500 tokens

2. **Create initiatives directory**:
   ```bash
   mkdir -p initiatives modules
   ```

**Phase 2: Convert PRDs (15 min per PRD)**

**Old location**:
```
tasks/0001-prd-user-authentication.md
```

**New location**:
```
initiatives/0001-planned-user-authentication/
  ├── description.prd
  ├── tasks.prd
  └── status.prd
```

**Add to PRD**:
```markdown
## References

**Project State**: project-state.prd
**Target Modules**:
- Authentication System (to be created)
- Database Layer (existing)

## Project Behavior Specifications

### Testing Strategy
- Unit tests with 85%+ coverage
- Integration tests for auth flows

### Version Control
- Feature branch per initiative

### Deployment
- CI/CD to staging, manual to production

### Collaboration
- 2 agents for parallel execution
```

**Phase 3: Convert Tasks (20 min per list)**

**Old format**:
```markdown
- [ ] 1.0 Set up development environment
  - [ ] 1.1 Install Python 3.11
  - [ ] 1.2 Set up PostgreSQL
- [ ] 2.0 Create database models
  - [ ] 2.1 Create User model
```

**New format**:
```markdown
## Task Group 0: Prerequisites

- [ ] TASK-001: Install Python 3.11 and dependencies
  - Dependencies: None
  - Estimated: 1h

- [ ] TASK-002: Set up PostgreSQL database
  - Dependencies: None
  - Estimated: 1h

## Task Group 1: Database Models

- [ ] TASK-003: Create User model
  - Dependencies: TASK-002
  - Estimated: 1.5h

- [ ] TASK-004: Create Role model
  - Dependencies: TASK-002
  - Estimated: 1h
```

**Conversion tips**:
1. Group tasks by dependencies
2. Create Group 0 for setup
3. Use 3-5 tasks per group
4. Add dependency references
5. Add time estimates

---

### From Scratch

**Quick Start (5 minutes)**

1. **Initialize project**:
   ```
   Use templates/create-project
   ```
   
   This creates:
   - `ai-project/` directory
   - `project-state.prd` with your modules
   - `.ai-orchestrator` guide

2. **Create first initiative**:
   ```
   cd ai-project
   Use ../templates/create-initiative
   ```

3. **Generate tasks**:
   ```
   Use ../templates/generate-tasks [initiative-dir]
   ```

4. **Start building**:
   ```
   Use ../templates/start-task [initiative-dir] TASK-001
   ```

---

### Migration Checklist

**Phase 1: Setup**
- [ ] Create directories (initiatives, modules)
- [ ] Create project-state.prd with 2-3 modules
- [ ] Create initiatives/INDEX.prd

**Phase 2: Content Migration**
- [ ] Convert PRDs to initiative format
- [ ] Add References section to each PRD
- [ ] Add Project Behavior Specifications
- [ ] Convert task lists to task groups
- [ ] Add task dependencies
- [ ] Create status.prd for each initiative

**Phase 3: Cleanup**
- [ ] Archive old system (don't delete)
- [ ] Test with one initiative
- [ ] Update team documentation

---

### Common Migration Issues

**Issue**: Too many small tasks (50+ tiny subtasks)

**Solution**: Combine related subtasks into single tasks. Aim for 20-40 tasks total per initiative.

---

**Issue**: Unclear dependencies

**Solution**: Review what each task touches. Use dependency rules (models before APIs, etc.).

---

**Issue**: No clear modules

**Solution**: Start with obvious ones (Frontend, Backend, Database). Use directory structure as guide.

---

**Issue**: Mixed initiative boundaries

**Solution**: Split into separate initiatives with cross-initiative dependencies. Smaller is better.

---

## 🤝 Contributing

Improvements welcome!

**What to contribute:**
- Better command templates
- More examples
- Bug fixes
- Additional dependency rules

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 AI Project Orchestrator Contributors

---

## 🙏 Credits

This project was largely inspired by and builds upon concepts from **[ai-dev-tasks](https://github.com/PierrunoYT/ai-dev-tasks)**.

### When to Use Each Project

**Use ai-dev-tasks if:**
- Single contributor / solo development
- Simple, linear task workflow
- Quick project setup needed
- Don't need parallel execution

**Use AI Project Orchestrator if:**
- Multiple AI agents working in parallel
- Complex, long-term projects
- Need initiative-based organization
- Cross-initiative dependencies
- Modular project state management
- Token efficiency critical

We recommend starting with **ai-dev-tasks** for most projects and migrating to AI Project Orchestrator when you need its advanced features.

---

## Quick Reference

| Action | Command |
|--------|---------|
| Initialize project | `Use templates/create-project` |
| Create initiative | `Use templates/create-initiative` |
| Generate tasks | `Use templates/generate-tasks [initiative-dir]` |
| Update tasks | `Use templates/update-tasks [initiative-dir]` |
| Work on task | `Use templates/start-task [initiative-dir] [TASK-ID]` |
| Close initiative | `Use templates/close-initiative [initiative-dir]` |
| View this project's state | `cat project-state.prd` |
| View example initiatives | `cat examples/initiatives/INDEX.prd` |
| View example state | `cat examples/project-state-example.prd` |

---

**Version**: 2.0.0  
**Last Updated**: 2025-10-10

Happy building with AI! 🚀🤖
