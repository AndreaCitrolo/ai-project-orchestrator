---
description: Create new initiative
argument-hint: [name]
allowed-tools: Read, Write
---

# Create Initiative

1. **Get next ID**: Check `ai-project/initiatives/`, use next NNNN

2. **Ask** (all at once):
   - Feature/problem?
   - Success criteria?
   - User stories?
   - Dependencies (other initiatives)?
   - Modules affected?

3. **Create** `ai-project/initiatives/NNNN-[name]/description.prd`:

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

4. **Validate**:
   - [ ] NNNN-name format
   - [ ] Dependencies exist in project-state.prd
   - [ ] Modules exist

5. **User Approval** - STOP and WAIT:
   ```
   📋 Review: ai-project/initiatives/[NNNN]-[name]/description.prd
   
   Reply: "approved" or "edit [feedback]"
   ```

6. **After approval**:
   ```
   ✅ Initiative created
   
   Next: /aipo-create-tasks [NNNN]-[name]
   ```

