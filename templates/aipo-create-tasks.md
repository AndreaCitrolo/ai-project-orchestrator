---
description: Generate task groups from initiative
argument-hint: [initiative-dir]
allowed-tools: Read, Write
---

# Create Tasks

1. **Read** `ai-project/initiatives/$1/description.prd`
2. **Read** `@ai-project/project-state.prd`
3. **Generate** 15-50 tasks organized in groups (Group 0: setup, Group 1+: features)
4. **Write** `ai-project/initiatives/$1/tasks.prd`:

```markdown
**ID**: [NNNN]
**Name**: [Name]
**Dependencies**: [NNNN,NNNN] or None
**Swarm**: [file] (added by /aipo-configure-swarm)

[START: ]
[END: ]

## Summary

**Status**: Not Started
**Progress**: 0/X tasks (0%)
**Current Group**: 0

## Tasks

### Group 0: Prerequisites

- [ ] TASK-001: [Title] (Xh) **Agent**: [name]
  - [Details]
  - **Deps**: None

### Group 1: [Feature Name]

- [ ] TASK-002: [Title] (Xh) **Agent**: [name]
  - [Details]
  - **Deps**: TASK-001

[Groups 2-N...]
```

5. **Validate**:
   - [ ] 15-50 tasks
   - [ ] Groups: 0 (prereqs), 1-N (features)
   - [ ] Time estimates
   - [ ] Metadata + Summary sections

6. **User Approval** - STOP and WAIT:
   ```
   📋 Review: ai-project/initiatives/[actual-dir]/tasks.prd
   
   Reply: "approved" or "edit [feedback]"
   ```

7. **After approval**:
   ```
   ✅ Tasks ready
   
   Next: /aipo-configure-swarm NNNN-name-swarm.yml [actual-dir] [others...]
   
   Note: /aipo-start-task for swarm agents only
   Manual testing: /aipo-start-task [actual-dir] TASK-001
   ```

