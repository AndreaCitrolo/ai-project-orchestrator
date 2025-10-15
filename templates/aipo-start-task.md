---
description: Execute task (auto-closes initiative)
argument-hint: [initiative-dir] [TASK-ID]
allowed-tools: Read, Edit, Write, Bash
---

# Start Task

⚠️ **For swarm agents** (manual use: testing/debug only)  
Normal workflow: `/aipo-configure-swarm` → swarm uses this automatically

## Steps

1. **Validate** - Read `ai-project/initiatives/$1/tasks.prd`:
   - [ ] Task exists, not marked `[x]`
   - [ ] Dependencies complete
   - [ ] In current/next group (no skipping)
   
   If blocked → STOP: "❌ [reason]"

2. **Load**:
   - `ai-project/project-state.prd` (relevant modules)
   - `ai-project/initiatives/$1/description.prd`
   - Task details

3. **Start**: If first task → set `[START: YYYY-MM-DD HH:MM]`

4. **Implement**: Follow requirements from description.prd

5. **Test**: Run tests, verify passing

6. **Mark Done**:
   - Check `[x]` in tasks.prd
   - Update Summary progress

7. **Auto-close** (if last task):
   a. Set `[END: YYYY-MM-DD HH:MM]`
   b. Update Summary: `**Status**: Completed`
   c. Update `ai-project/project-state.prd`:
      - Mark module criteria complete
      - Update completion stats
   d. Output:
      ```
      ✅ INITIATIVE COMPLETE
      Initiative: [actual-dir]
      Tasks: X/X completed
      Modules: [list]
      Completed: [date]
      ```

8. **Suggest** (if tasks remain): List next available tasks

9. **Output** (use actual values, not $1 or $2):
   ```
   ✅ TASK-XXX: [description]
   Status: DONE
   Group N: X/Y tasks
   Next: [TASK-YYY or "None" or "COMPLETE"]
   ```

## Validation

Before marking complete:
- [ ] Code written
- [ ] Tests written + passing
- [ ] tasks.prd updated
- [ ] Summary updated
- [ ] No TODO/FIXME

If fails → STOP, don't mark complete

