---
description: Create new initiative
argument-hint: [name]
allowed-tools: Read, Write
---

# Create Initiative

1. **Get next ID**: Check `ai-project/initiatives/`, use next NNNN

2. **Gather Requirements with SuperClaude**:
   ```bash
   /sc:spec-panel --format structured --mode discussion
   @agent-system-architect
   @agent-technical-writer
   @agent-quality-engineer
   ```
   
   Map SuperClaude output to AIPO description.prd format below.

3. **Consolidate** answers from SuperClaude:
   - Feature/problem
   - Success criteria
   - User stories
   - Dependencies (other initiatives)
   - Modules affected

4. **Create** `ai-project/initiatives/NNNN-[name]/description.prd`:

```markdown
# Initiative: [Name]

**ID**: [NNNN]
**Name**: [name]
**Status**: Not Started
**Dependencies**: [NNNN,NNNN] or None

## Problem

[Description from answers]

## Solution

[Technical approach]

## Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]

## User Stories

- As [role], I want [feature] so that [benefit]

## Modules Affected

- [Module 1]
- [Module 2]

## Technical Decisions

[Key tech choices]

## Testing Strategy

[Approach]
```

5. **Validate**:
   - [ ] NNNN-name format
   - [ ] Dependencies exist in project-state.prd
   - [ ] Modules exist

6. **User Approval** - STOP and WAIT:
   ```
   📋 Review: ai-project/initiatives/[NNNN]-[name]/description.prd
   
   Reply: "approved" or "edit [feedback]"
   ```

7. **After approval**:
   ```
   ✅ Initiative created
   
   Next: /aipo-create-tasks [NNNN]-[name]
   ```

