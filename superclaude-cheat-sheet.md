

# **SuperClaude V4 Framework Reference Guide: Agents, Modes, Flags, and Swarm Orchestration**

## **I. Executive Summary: SuperClaude V4 Meta-Programming Framework**

The SuperClaude V4 framework represents a significant architectural leap in the utilization of Anthropic's Claude Code, transforming the command-line assistant into a structured, development lifecycle platform.1 This capability is achieved through a systematic process of behavioral instruction injection and component orchestration, integrating specialized LLM components—Agents, Modes, and MCP Servers—into a single, unified execution layer.2 The V4 design philosophy mandates evidence-based development, modularity, and aggressive token efficiency.4

A critical feature of the framework is its role as an active, collaborative partner. SuperClaude V4 is programmed to engage in "Constructive Pushback," challenging the user when an inefficient, best-practice-violating, or security-risky approach is suggested.5 This behavior is governed by an internal Severity System, rating rules on a scale of 1 to 10\. Rules rated as CRITICAL are non-negotiable safeguards—including mandates like "NEVER commit secrets" or operational rules preventing disruptive actions like force pushes to shared branches.5

The V4 release (V4.0.4/4.1.5) introduced a streamlined architecture, including the standardization of all specialized commands with the /sc: prefix.1 This change ensures namespace clarity, preventing conflicts with any custom commands defined by the user in the Claude Code environment.

### **Reconciliation of V4 Specifications**

To provide an authoritative reference, the specifications for SuperClaude V4 must be standardized against the most current documentation. The framework has expanded substantially from earlier iterations. The definitive V4 specifications include:

* **Cognitive Agent System:** Expanded to a "Smarter Agent System" of **16 specialized agents** 2, significantly surpassing the initial 9 core personas.4  
* **Behavioral Modes:** Featuring **7 adaptive behavioral modes** designed to systematically adjust the LLM’s cognitive approach based on the specific context.1  
* **MCP Integration:** Integrating **8 powerful MCP servers** for extended real-world functionality and contextual data retrieval.2

## **II. Core Component Reference: Cognitive Agent System (Personas)**

The Cognitive Agent System provides domain expertise through specialized roles, or personas, ensuring that the LLM utilizes domain-specific system prompts and knowledge when executing tasks.4 This expertise can be automatically activated (e.g., the frontend persona activating upon editing a .tsx file) or explicitly invoked via command-line flags.5 The use of specialized, context-limited agents naturally contributes to the framework’s token efficiency goals, as the system prompt injected into the LLM is smaller and highly relevant, increasing execution accuracy.6

The agent system facilitates complex, multi-stage development by enabling **Persona Chaining**.5 A task is systematically handed off between specialists—beginning with the architect for high-level design, moving to frontend and backend for concurrent implementation, and concluding with security and qa for comprehensive review.5

### **The V4 Agent Expansion: Listing the 16 Specialized Roles**

The core development roles (the initial 9 personas) focus on critical development lifecycle tasks.4 The expansion to 16 specialized agents integrates strategic and management functions, such as the PM Agent for systematic documentation 2 and the Deep Research agent for autonomous knowledge discovery.2

Table 1: SuperClaude V4 Specialized Agents (16 Confirmed) and Focus Areas

| Agent/Persona Flag | Focus Area | Core Belief/Mandate | Primary Tools/Synergy |
| :---- | :---- | :---- | :---- |
| architect | System design, architectural planning | Systems must be designed for change | Sequential, Context7 5 |
| frontend | User experience (UX), UI development, React polish | Obsessed with intuitive, mobile-first interfaces | Magic, Puppeteer/Playwright 5 |
| backend | Server systems, API reliability, database management | Focus on reliability and scale | Context7, Sequential 7 |
| security | Threat modeling, secure code, vulnerability analysis | Paranoid by design; threats exist everywhere | Sequential, Context7 5 |
| analyzer | Root cause detection, deep-dive debugging, problem solving | Acts as the root cause detective | All MCP tools 5 |
| qa | Test strategy, test coverage, quality assurance | Focuses on testing protocols and verification | Puppeteer/Playwright, Context7 7 |
| performance | Optimization, scalability, speed tuning | Ensures application performance and efficiency | Puppeteer/Playwright, Sequential 7 |
| refactorer | Code quality, improvement, technical debt reduction | Specializes in code clarity and cleanup | Sequential, Context7 7 |
| mentor | Knowledge sharing, guided learning, documentation | Provides coaching and documentation focus | Context7, Sequential 7 |
| pm | Project Management, continuous learning | Ensures systematic documentation and task coordination | Task Management Mode, Serena 2 |
| deep-research | Autonomous web research, knowledge discovery | Utilizes external and internal search sources | Tavily, Context7, Playwright 1 |
| devops | CI/CD pipelines, infrastructure automation | Focuses on production deployment and environment management | Chrome DevTools, Bash/Shell 2 |
| technical-writer | Documentation, API specifications, knowledge management | Ensures professional and comprehensive documentation | Context7, Sequential |
| cto | Strategic technology leadership, enterprise architecture | Focuses on high-level business and technical strategy | Business Panel Mode, Sequential |
| product-owner | Requirements gathering, feature prioritization | Ensures alignment between technical and business needs | Brainstorming Mode, Task Management Mode |
| fullstack | Complex feature implementation, cross-stack integration | Generalist developer handling end-to-end tasks | Sequential, Magic, Context7 |

### **Activation Syntax and Usage Examples**

Personas are activated using command flags following the format \--persona-role. This syntax provides explicit control over the agent's behavior for a specific command execution.7

* Example 1: Security Review: Directing the security expert to perform an analysis:  
  /sc:scan \--security \--persona-security "Review user login flow for OWASP Top 10 vulnerabilities".7  
* Example 2: Architectural Design: Applying Domain-Driven Design principles under the highest systemic authority:  
  /sc:design \--api \--ddd \--bounded-context \--persona-architect.7  
* Example 3: Root Cause Analysis (Production): Mandating a rigorous, deep investigation in a sensitive environment:  
  /sc:troubleshoot \--prod \--persona-analyzer \--seq.7 The \--seq flag forces the use of the Sequential MCP, ensuring the multi-step reasoning required for deep debugging in a production context.5

## **III. Core Component Reference: Adaptive Behavioral Modes**

Behavioral Modes adjust Claude's entire cognitive approach, tool usage, and output structure based on the desired outcome.1 These modes are activated via a global mode flag (e.g., \--mode orchestration). The modes conceptually extend the safety and quality assurance provided by the core Claude Code Plan Mode 11, ensuring structured execution beyond the initial planning phase.

### **Defining the 7 Behavioral Modes for Context Switching**

The **Token-Efficiency** mode exemplifies how modes optimize performance. This mode automatically triggers "UltraCompressed Mode" (UCM), which uses shorthand, symbols (e.g., → for "leads to"), and abbreviations to achieve a reported 30-50% reduction in token consumption, which is critical for cost-effective execution on large projects.2

Table 2: SuperClaude V4 Adaptive Behavioral Modes

| Behavioral Mode | Strategic Purpose | Key Characteristic | Primary Command Synergy |
| :---- | :---- | :---- | :---- |
| Brainstorming | Feature idea generation, requirements analysis | Focuses on asking the right questions and identifying gaps.2 | /sc:brainstorm, /sc:design |
| **Business Panel** | Multi-expert strategic analysis and high-level strategy | Synthesizes input from multiple 'CTO/Product Owner' perspectives.2 | /sc:analyze, /sc:review |
| **Deep Research** | Autonomous, evidence-based web research | Coordinated use of external tools (Tavily, Playwright) for fact-checking.1 | /sc:research, /sc:docs |
| **Orchestration** | Efficient tool and agent coordination (The Swarm Engine) | Prioritizes planning, delegation, and sequential/parallel task management.2 | /sc:build, /sc:code |
| **Token-Efficiency** | Context and cost savings | Triggers UltraCompressed Mode (30-50% context savings).2 | Any command on large codebases (--uc flag equivalent) |
| **Task Management** | Systematic organization and execution tracking | Integrates tasks, priorities, and completion status into artifacts (e.g., tasks.md).2 | /sc:focus-start, /sc:design |
| **Introspection** | Meta-cognitive analysis of framework behavior | Debugging SuperClaude's execution or evaluating tool usage patterns.2 | /sc:analyze, /sc:troubleshoot |

### **Mode Activation and Workflow Examples**

The **Task Management Mode** 2 provides a foundational solution to a key limitation of LLMs: short memory and context loss in multi-day projects.5 By enforcing systematic organization, the mode ensures that project artifacts (e.g., design documents, task lists) are constantly updated with current progress and priorities.13 When combined with the Serena MCP (which offers session persistence), this mechanism allows the LLM to resume complex development workflows with perfect, machine-readable context, overcoming the natural short memory of the conversational model.15

* Example 1: Strategic Analysis: Utilizing the Business Panel mode for multi-expert strategic input:  
  /sc:analyze "Evaluate the cost-benefit analysis for migrating to Serverless architecture" \--mode business-panel.2  
* Example 2: Complex Coordination: Activating the Swarm engine for a feature requiring tool and agent handoffs:  
  /sc:build "implement new user dashboard" \--mode orchestration.2 This ensures that the generated plan is focused on coordinating the necessary sequence of actions between different agents (e.g., frontend, backend, QA).5

## **IV. Core Component Reference: MCP Server Integration Architecture**

The Model Context Protocol (MCP) servers function as external, specialized tool interfaces, bridging Claude's capabilities with the real world (APIs, files, web).16 SuperClaude V4 integrates 8 servers, enhancing its ability to retrieve real-time data, perform browser automation, and execute complex code manipulations.1

### **SuperClaude V4 MCP Servers and Functional Roles**

The decision to use a specific server is controlled by the MCP Decision Matrix. Explicit flags (e.g., \--magic) take precedence, but without them, the system analyzes user intent or code context to dynamically select the optimal tool.5

Table 3: SuperClaude V4 MCP Servers and Functional Roles

| MCP Server Name | Flag Trigger | Core Function | Swarm Relevance |
| :---- | :---- | :---- | :---- |
| Context7 (C7) | \--c7 | Up-to-date documentation lookup, RAG | Provides a consistent, verified technical knowledge base for all agents.2 |
| Sequential | \--seq | Complex analysis, multi-step reasoning, synthesis | Provides the structured logic necessary for coordinating multi-agent workflows.2 |
| Magic | \--magic | UI component generation, rapid prototyping | Offloads standardized UI scaffolding from the main LLM.5 |
| Playwright | \--play | Browser automation, end-to-end (E2E) testing | Tool utilized by the qa agent to verify functional completeness.2 |
| **Serena** | N/A (Auto-trigger) | Symbolic code retrieval/editing, session persistence | Enables token-frugal, IDE-like operations for precise code manipulation.15 |
| **Morphllm** | N/A (Auto-trigger) | Bulk code transformations, style enforcement | Facilitates rapid, non-semantic changes across large file sets (e.g., mass refactoring).2 |
| **Tavily** | N/A (Auto-trigger) | Web search for deep research, discovery | Primary tool for the Deep Research mode, providing external web context.2 |
| **Chrome DevTools** | N/A (Auto-trigger) | Performance analysis, profiling, metrics capture | Supplies quantifiable data for the performance agent's optimization tasks.2 |

The inclusion of **Serena MCP** is significant as it fundamentally changes the economics of large-scale agentic development. Traditional LLM agents incur high token costs by reading and writing large amounts of code context to perform simple changes.18 Serena provides symbolic manipulation (like IDE-level function renaming and reference updates), allowing the refactorer agent to execute complex structural changes with token efficiency, thereby enabling the framework to scale to enterprise codebases.15

The strategic coordination of the knowledge retrieval tools—**Tavily** and **Context7**—is essential for evidence-based development.4 Tavily handles real-time, external web research, while Context7 manages reliable, internal technical documentation.2 Deep Research Mode coordinates these tools to first check the verified internal knowledge base (Context7) before querying the external web (Tavily), minimizing potential hallucinations and maximizing the trustworthiness of generated facts.2

* Example 1: Sequential Debugging:  
  /sc:debug "memory leak in worker service" \--seq \--c7 (Uses Sequential for deep reasoning and Context7 for documentation reference).7  
* Example 2: UI Scaffolding:  
  /sc:build \--react \--magic \--persona-frontend (Scaffolds the component using Magic MCP).7

## **V. Core Component Reference: Contextual and Operational Flags**

SuperClaude V4 features a rich collection of operational flags that control context depth, execution speed, quality adherence, and behavioral enforcement.1 These flags provide non-persistent overrides, applying customized behavior solely to the specific command execution.19

### **Categorization and Functionality**

A critical flag is \--strict, which directly invokes the framework’s internal Severity System.5 Using \--strict elevates adherence to security and governance rules (e.g., "NEVER commit secrets") to the CRITICAL level, effectively transforming the AI into a mandatory compliance auditor during execution.5

Table 4: Essential Operational Flags and Use Cases

| Operational Flag | Category | Function | Contextual Example |
| :---- | :---- | :---- | :---- |
| \--strict | Control | Enforces non-negotiable adherence to predefined V4 rules (e.g., security, conventional commits).5 | /sc:build \--api \--strict (Insisting on parameterization to prevent SQL injection). |
| \--parallel | Control | Enables concurrent execution of sub-tasks/sub-agents by the Orchestration Mode.5 | /sc:build \--react \--parallel (Implementing frontend/backend simultaneously). |
| \--tdd | Development | Mandates a Test-Driven Development workflow (tests first).5 | /sc:build \--api \--tdd \--coverage (Ensuring comprehensive testing). |
| \--e2e | Development | Specifies End-to-End testing strategy using browser automation.7 | /sc:test \--e2e \--play \--persona-qa (Full integration tests via Playwright). |
| \--prod | Context | Flags the task as operating in a production or high-risk environment.7 | /sc:troubleshoot \--prod \--safe (Activates highest caution level). |
| \--introspect | Utility | Triggers meta-cognitive analysis of SuperClaude's execution and decision matrix.7 | /sc:analyze \--introspect \--seq (Debugging framework behavior or tool routing). |
| \--uc | Token | Activates Ultra-Compressed Mode (70% token savings).5 | /sc:improve \--large-repo \--uc (Cost-optimization for massive refactoring jobs). |
| \--validate | Utility | Forces verification checks (e.g., dependency status, security review validation).7 | /sc:scan \--security \--validate (Ensuring security findings are confirmed). |
| \`--watch\*\* | Development | Enables file system monitoring for reactive coding (hot reload for AI).7 | /sc:code \--watch \--magic (Rapid iteration on UI components). |

The \--parallel flag is a powerful accelerator, but its effectiveness is contingent upon the **Orchestration Mode**.2 The Orchestration Mode provides the advanced intelligence and task routing required to manage concurrent agent tasks, ensuring that the delegation and coordination processes are structured and efficient.21 Without this mode, concurrent execution lacks the required systemic management framework to prevent context collision and maintain project coherence.

### **Flag Chaining Example**

A command can chain multiple flags to construct a complex, specialized workflow:

/sc:build \--react \--tdd \--strict \--parallel \--persona-frontend \--magic

This command instructs the system to execute a React build, following TDD methodology while enforcing strict governance rules, running sub-tasks in parallel, adopting the expertise of the frontend developer, and leveraging the Magic MCP for rapid component generation.7

## **VI. The Claude Swarm Blueprint: Optimal Orchestration Strategy**

The 'Claude Swarm' involves maximizing coordination and efficiency by deploying the most potent combination of V4 components to tackle complex, multi-faceted engineering tasks. The goal of the optimal command is to blend systemic governance, speed, and quality assurance in a single execution.

### **Strategic Component Selection Rationale**

1. **Command: /sc:design**: Forces the system to produce a structured plan (Design Document) first, adhering to the safety principle of Plan Mode before execution is allowed.12  
2. **Mode: Orchestration**: The native Swarm engine, ensuring efficient tool coordination, structured delegation, and context-aware task routing.1  
3. **Agent: Architect**: Serves as the systemic oversight agent, providing high-level guidance and ensuring the solution adheres to overarching architectural principles ("systems must be designed for change").5  
4. **MCP Logic: Sequential**: Mandatory for coordinating multi-agent workflows. It provides the deep, multi-step reasoning capacity required for the Architect to synthesize complex requirements and structure the delegation process.2

### **The Optimal Master Orchestration Command Combination**

The optimal command structure must incorporate planning, governance, parallelism, and quality mandates to efficiently manage the Swarm instance.

Proposed Optimal Command:  
/sc:design "Implement GDPR-compliant, real-time analytics microservice API" \--mode orchestration \--persona-architect \--seq \--strict \--parallel \--tdd

### **Detailed Justification: Breakdown of Flag and MCP Synergy**

| Component | Syntax | Function in Swarm | Justification |
| :---- | :---- | :---- | :---- |
| **Command** | /sc:design | Establishes a formal, structured output requirement (Design Document).14 | Ensures safe initiation by forcing the creation of an architectural blueprint before any implementation, controlling the output of the Swarm. |
| **Mode** | \--mode orchestration | Activates the multi-agent task routing engine.1 | Provides the necessary architecture to manage concurrent agent execution and efficient resource handoffs, functioning as the primary coordination layer. |
| **Agent** | \--persona-architect | Sets the highest-level systemic perspective for planning.5 | Ensures the resulting microservice design is structurally sound and adheres to enterprise architectural standards.7 |
| **MCP Logic** | \--seq | Activates the Sequential deep reasoning server.5 | Provides the computational synthesis required for the Architect to break down complex, multi-constraint requirements (e.g., "GDPR-compliant" and "real-time") into actionable steps for specialized sub-agents.2 |
| **Control Flag 1** | \--strict | Enforces adherence to critical security and governance rules.5 | Essential for high-stakes compliance like GDPR, guaranteeing the security agent is automatically engaged at a CRITICAL severity level for review.5 |
| **Control Flag 2** | \--parallel | Enables concurrent execution of sub-tasks.7 | Maximizes speed by running tasks concurrently, allowing agents (e.g., backend API design and deep-research compliance verification) to work in parallel, managed by the Orchestration Mode.5 |
| **Quality Flag** | \--tdd | Mandates the highest quality implementation standard.7 | Ensures output reliability by requiring comprehensive test coverage to be designed and implemented before core feature code, minimizing technical debt. |

## **VII. Conclusion and Implementation Recommendations**

The SuperClaude V4 framework provides the necessary scaffolding to deploy a highly structured, governed, and efficient 'Claude Swarm'. By utilizing the optimal command combination, developers move beyond simplistic prompting to initiate a sophisticated, automated engineering workflow that integrates strategic planning, enforcement of compliance rules, and parallel execution.

The framework’s most impactful advancement for scaling agentic coding is the shift toward symbolic code manipulation through the **Serena MCP**.15 For operations involving large-scale changes, such as refactoring an entire microservice or performing bulk structural updates, the recommended workflow must explicitly leverage this capability for cost efficiency. The refactorer persona, when paired with the Sequential MCP and the Token-Efficiency flag (--uc), will automatically trigger the Serena MCP, ensuring complex changes are executed with high precision and low token cost. For non-semantic, high-volume changes like dependency or style guide upgrades, the process should be routed to **Morphllm** 2, the specialized server for bulk transformation, ensuring deterministic and rapid application across the repository.

Adoption of SuperClaude V4 requires developers to embrace the concept of systematic instruction injection. Leveraging specialized modes like Introspection (for debugging framework behavior) and Task Management (for preserving context via Serena) is critical for achieving true autonomous development and maintaining the necessary long-term memory essential for any complex, sustained LLM engineering effort.1

#### **Works cited**

1. SuperClaude \- PyPI, accessed on October 15, 2025, [https://pypi.org/project/SuperClaude/](https://pypi.org/project/SuperClaude/)  
2. SuperClaude-Org/SuperClaude\_Framework: A configuration framework that enhances Claude Code with specialized commands, cognitive personas, and development methodologies. \- GitHub, accessed on October 15, 2025, [https://github.com/SuperClaude-Org/SuperClaude\_Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)  
3. SuperClaude \- PyPI, accessed on October 15, 2025, [https://pypi.org/project/SuperClaude/4.0.4/](https://pypi.org/project/SuperClaude/4.0.4/)  
4. SuperClaude \- ClaudeLog, accessed on October 15, 2025, [https://www.claudelog.com/claude-code-mcps/super-claude/](https://www.claudelog.com/claude-code-mcps/super-claude/)  
5. SuperClaude: Power Up Your Claude Code Instantly \- Apidog, accessed on October 15, 2025, [https://apidog.com/blog/superclaude/](https://apidog.com/blog/superclaude/)  
6. I created an AMAZING MODE called "RIPER-5 Mode" Fixes Claude 3.7 Drastically\! \- Showcase \- Cursor Forum, accessed on October 15, 2025, [https://forum.cursor.com/t/i-created-an-amazing-mode-called-riper-5-mode-fixes-claude-3-7-drastically/65516](https://forum.cursor.com/t/i-created-an-amazing-mode-called-riper-5-mode-fixes-claude-3-7-drastically/65516)  
7. Mirza-Samad-Ahmed-Baig/SuperClaude \- GitHub, accessed on October 15, 2025, [https://github.com/Mirza-Samad-Ahmed-Baig/SuperClaude](https://github.com/Mirza-Samad-Ahmed-Baig/SuperClaude)  
8. I Present : SuperClaude \! : r/ClaudeAI \- Reddit, accessed on October 15, 2025, [https://www.reddit.com/r/ClaudeAI/comments/1lhmts3/i\_present\_superclaude/](https://www.reddit.com/r/ClaudeAI/comments/1lhmts3/i_present_superclaude/)  
9. SuperClaude Framework: Revolutionizing AI Programming with Enhanced ClaudeCode Capabilities \- Tenten \- AI / ML Development, accessed on October 15, 2025, [https://developer.tenten.co/superclaude-framework-revolutionizing-ai-programming-with-enhanced-claudecode-capabilities](https://developer.tenten.co/superclaude-framework-revolutionizing-ai-programming-with-enhanced-claudecode-capabilities)  
10. \[Resource\] 12 Specialized Professional Agents for Claude Code CLI : r/ClaudeAI \- Reddit, accessed on October 15, 2025, [https://www.reddit.com/r/ClaudeAI/comments/1m8s0kh/resource\_12\_specialized\_professional\_agents\_for/](https://www.reddit.com/r/ClaudeAI/comments/1m8s0kh/resource_12_specialized_professional_agents_for/)  
11. Plan Mode Usage, accessed on October 15, 2025, [https://www.claudecode101.com/en/tutorial/workflows/plan-mode](https://www.claudecode101.com/en/tutorial/workflows/plan-mode)  
12. Claude Code Plan Mode: Revolutionizing the Senior Engineer's Workflow \- Medium, accessed on October 15, 2025, [https://medium.com/@kuntal-c/claude-code-plan-mode-revolutionizing-the-senior-engineers-workflow-21d054ee3420](https://medium.com/@kuntal-c/claude-code-plan-mode-revolutionizing-the-senior-engineers-workflow-21d054ee3420)  
13. I built a task management system with Claude (Free templates for you\!) : r/ClaudeAI \- Reddit, accessed on October 15, 2025, [https://www.reddit.com/r/ClaudeAI/comments/1nxf620/i\_built\_a\_task\_management\_system\_with\_claude\_free/](https://www.reddit.com/r/ClaudeAI/comments/1nxf620/i_built_a_task_management_system_with_claude_free/)  
14. SuperClaude and claude code, example flow when starting from scratch \- Reddit, accessed on October 15, 2025, [https://www.reddit.com/r/ClaudeAI/comments/1m6rncg/superclaude\_and\_claude\_code\_example\_flow\_when/](https://www.reddit.com/r/ClaudeAI/comments/1m6rncg/superclaude_and_claude_code_example_flow_when/)  
15. Serena MCP Server: A Deep Dive for AI Engineers, accessed on October 15, 2025, [https://skywork.ai/skypage/en/Serena%20MCP%20Server%3A%20A%20Deep%20Dive%20for%20AI%20Engineers/1970677982547734528](https://skywork.ai/skypage/en/Serena%20MCP%20Server%3A%20A%20Deep%20Dive%20for%20AI%20Engineers/1970677982547734528)  
16. Ultimate Guide to Claude MCP Servers & Setup | 2025 \- Generect, accessed on October 15, 2025, [https://generect.com/blog/claude-mcp/](https://generect.com/blog/claude-mcp/)  
17. Revolutionizing Development with SuperClaude: The Ultimate Claude Code Framework, accessed on October 15, 2025, [https://developer.tenten.co/revolutionizing-development-with-superclaude-the-ultimate-claude-code-framework](https://developer.tenten.co/revolutionizing-development-with-superclaude-the-ultimate-claude-code-framework)  
18. Claude and Serena MCP \- a dream team for coding : r/ClaudeAI \- Reddit, accessed on October 15, 2025, [https://www.reddit.com/r/ClaudeAI/comments/1l42cn6/claude\_and\_serena\_mcp\_a\_dream\_team\_for\_coding/](https://www.reddit.com/r/ClaudeAI/comments/1l42cn6/claude_and_serena_mcp_a_dream_team_for_coding/)  
19. \[Feature Request\] Add (--model) flag to select Claude model, accessed on October 15, 2025, [https://github.com/SuperClaude-Org/SuperClaude\_Framework/issues/305](https://github.com/SuperClaude-Org/SuperClaude_Framework/issues/305)  
20. SuperClaude | Automate Git Documentation with AI, accessed on October 15, 2025, [https://www.superclaude.sh/docs](https://www.superclaude.sh/docs)  
21. Leading AI Orchestration Platform for Claude | Multi-Agent Swarms, accessed on October 15, 2025, [https://claude-flow.ruv.io/capabilities](https://claude-flow.ruv.io/capabilities)