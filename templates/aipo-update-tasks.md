---
description: Add or delete tasks
argument-hint: [initiative-dir]
allowed-tools: Read, Edit
---

# Update Tasks

1. **Ask**: What changes?
   - Add tasks? (titles, groups, deps)
   - Delete tasks? (IDs + reason)

2. **Read** `ai-project/initiatives/$1/tasks.prd`

3. **Modify**:
   - **Add**: Insert in appropriate group, assign TASK-XXX ID, add deps
   - **Delete**: Remove line, note in description if referenced

4. **Renumber**: Keep sequential IDs (TASK-001, TASK-002, ...)

5. **Update**:
   - Adjust dependency references
   - Update Summary total count

6. **Validate**:
   - [ ] Dependencies exist
   - [ ] IDs sequential + unique
   - [ ] Group numbers valid
   
   If fails → STOP

7. **Output** (replace $1 with actual dir):
   ```
   ✅ Tasks updated: ai-project/initiatives/[actual-dir]/tasks.prd
   Added: [N] tasks (Groups: [list])
   Deleted: [N] tasks (IDs: [list])
   Total: X tasks in Y groups
   ```

