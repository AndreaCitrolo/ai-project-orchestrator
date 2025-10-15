---
description: Initialize ai-project workspace
allowed-tools: Read, Write
---

# Create Project

## Steps

1. **Check**: IF `ai-project/` exists → STOP, ask user
2. **Ask** (all at once):
   - Project name, type, languages?
   - Description (1-2 sentences)?
   - Initial modules (2-4)?
   - Key technologies?

3. **Create**:
   ```
   ai-project/
   ├── project-state.prd
   ├── initiatives/
   └── modules/
   ```

4. **Write** `ai-project/project-state.prd`:
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

5. **Create** `.ai-orchestrator` guide:
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

6. **Validate**:
   - [ ] project-state.prd exists
   - [ ] All modules defined
   - [ ] All questions answered

7. **User Approval** - STOP and WAIT
   ```
   📋 Review: ai-project/project-state.prd
   
   Reply: "approved" or "edit [feedback]"
   ```
   
   After approval:
   ```
   ✅ Project ready
   
   Next: /aipo-plan
   ```

