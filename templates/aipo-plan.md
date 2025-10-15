---
description: Plan next initiatives with strategic options
argument-hint: (optional)
allowed-tools: Read, Bash
---

# Plan

1. Run: `!python3 ai-project-orchestrator/aipo.py status --json`
2. Read @ai-project/project-state.prd
3. **Analyze with SuperClaude** (context-aware):
   - **LOOP** project-state.prd exists (existing project):
   ```bash
     /sc:brainstorm "plan next initiatives provide options: dimensions task parallelization, time to user testing" --orchestrate --ultracompressed
     @agent-system-architect
     @agent-frontend-architect
     @agent-backend-architect
     @agent-devops-architect
     ```
     
     ```bash
     /sc:improve --orchestrate --ultracompressed --safe --interactive --type quality
     @agent-system-architect
     @agent-frontend-architect
     @agent-backend-architect
     @agent-devops-architect
     ```


   This provides strategic analysis (persona-architect) with token-efficient context.
   Map SuperClaude suggestions to AIPO strategy format below.
4. List 3-7 candidate initiatives (1 line each)
5. Show 4-5 strategies optimizing different dimensions
6. Recommend one

## Strategy Types

- **⚡ Max Parallel**: [A,B,C] parallel - fastest
- **🔄 Fast Feedback**: [D]→feedback→[E] - early validation
- **🎯 Homogeneous**: Backend[A,B] → Frontend[C] - focused work
- **🔀 Functional Slice**: Feature-X[A+C] → Feature-Y[B+D] - vertical features
- **📦 Dependency-Opt**: Wave1[A] → Wave2[B,C] - unblock progressively

## Output (Max 35 lines)

```
📋 Planning (Progress: X%)

CANDIDATES
──────────
A. [Name] (Size, deps:X, feedback:Y) - 1 sentence
B. [Name] (Size, deps:X, feedback:Y) - 1 sentence
...

STRATEGIES
──────────
⚡ Max Parallel: [A,B,C] parallel → ~Xw
   ✓ Fastest | ✗ Late feedback

🔄 Fast Feedback: [D]→[E] → ~Xw  
   ✓ Early validation | ✗ Slower

🎯 Homogeneous: Backend[A,B]→Frontend[C] → ~Xw
   ✓ Focus | ✗ Serial delivery

🔀 Functional: X[A+C]→Y[B+D] → ~Xw
   ✓ Value early | ✗ Context switching

→ Strategy X: [why] | Start: /aipo-create-initiative [name]
```

## Guidelines

| Phase | Best Strategy |
|-------|---------------|
| 0-20% | Dependency-Opt (foundation) |
| 20-60% | Homogeneous (focused dev) |
| 60-80% | Fast Feedback (validate) |
| 80%+ | Max Parallel (ship) |

