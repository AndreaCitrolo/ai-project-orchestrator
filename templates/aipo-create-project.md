---
description: Initialize ai-project workspace
allowed-tools: Read, Write
---

# Create Project

## Steps

1. **Check**: IF `ai-project/` exists → STOP, ask user

2. **Brainstorm & Gather Requirements**:
   ```bash
   /sc:brainstorm --strategy systematic --orchestration
   @agent-system-architect
   @agent-backend-architect
   @agent-devops-architect
   @agent-frontend-architect
   ```
   Then use:
   ```bash
   /sc:spec-panel  --mode discussion --format structured --orchestration --ultracompressed
   @agent-system-architect
   @agent-technical-writer
   @agent-quality-engineer
   ```
   This provides:
   - Strategic ideation and exploration (persona-architect)
   - Interactive requirements gathering
   - Structured PRD format output
   - Module decomposition (<500 tokens)
   - Token-efficient context (30-50% reduction)
   
   Map SuperClaude output to AIPO project-state.prd format below.

3. **Consolidate** answers from SuperClaude:
   - Project name, type, languages
   - Description (1-2 sentences)
   - Initial modules (2-4)
   - Key technologies

4. **Create**:
   ```
   ai-project/
   ├── project-state.prd
   ├── initiatives/
   └── modules/
   ```

5. **Write** `ai-project/project-state.prd`:
   ```markdown
   # Project State
   
   **Project**: [Name]
   **Version**: 0.1.0
   **Updated**: [YYYY-MM-DD]
   
   ## Overview
   
   [Description]
   
   **Type**: [Type]
   **Languages**: [Languages]
   
   ## Status
   
   Initiatives: 0 active, 0 completed
   Modules: [N]
   Created: [YYYY-MM-DD]
   
   ## Modules
   
   ### Module: [Name]
   
   **Summary**: [1-2 sentences]
   **Key Decisions**: [List 2-3]
   **Acceptance Criteria**: [List 2-3, unchecked]
   **Tech Stack**: [Technologies]
   **Interfaces**: TBD
   **Dependencies**: [List or None]
   **Token Count**: ~[estimate]
   ```

6. **Create** `.ai-orchestrator` guide:
   ```markdown
   # AI Project Orchestrator Guide
   
   ## Workflow
   1. /aipo-plan
   2. Loop: /aipo-create-initiative → /aipo-create-tasks
   3. /aipo-configure-swarm [file] [dirs...]
   4. Run swarm + monitor
   
   ## Files
   - project-state.prd: Project modules (<500 tokens each)
   - initiatives/NNNN-name/: description.prd + tasks.prd
   ```

7. **Validate**:
   - [ ] project-state.prd exists
   - [ ] All modules defined
   - [ ] All questions answered

8. **User Approval** - STOP and WAIT
   ```
   📋 Review: ai-project/project-state.prd
   
   Reply: "approved" or "edit [feedback]"
   ```
   
   After approval:
   ```
   ✅ Project ready
   
   Next: /aipo-plan
   ```

