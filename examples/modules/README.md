# Modules Directory

This directory contains **optional detailed module documentation** that extends the module definitions in the main `project-state.md` file.

## Purpose

While the `project-state.md` file contains concise module summaries optimized for LLM consumption (target: <500 tokens per module), some modules may require more extensive documentation. This directory provides a place for:

- Detailed API documentation
- Complex database schemas with relationships
- Extensive configuration options
- Architecture diagrams and flowcharts
- Implementation notes and examples
- Migration guides for the module

## When to Use This Directory

Create a standalone module file here when:

1. **Complexity**: The module has extensive details that would make the project-state.md entry too large
2. **Reference Material**: You need detailed API specs, schemas, or configuration that agents rarely need but should have available
3. **Separation of Concerns**: High-level vs. detailed documentation should be separated for clarity

## File Naming Convention

Module files should be named descriptively and use lowercase with hyphens:

```
module-name.md
```

Examples:
- `authentication.md`
- `database.md`
- `api-gateway.md`
- `payment-processing.md`

## Structure

Each module file should follow this structure:

```markdown
# Module: [Module Name]

## Overview
Brief description linking back to project-state.md

## Architecture
Detailed architecture explanation

## API Reference
Complete API documentation

## Database Schema
Detailed table structures and relationships

## Configuration
All configuration options

## Examples
Usage examples and code snippets

## Dependencies
Other modules this depends on

## Notes
Implementation notes, gotchas, future considerations
```

## Relationship to project-state.md

- **project-state.md**: Contains high-level module summaries that agents read first
- **modules/[name].md**: Contains deep-dive documentation that agents reference when working on specific tasks

The project-state.md entry should reference the detailed module file when it exists:

```markdown
## Module: Authentication System

**Summary**: Handles user authentication and authorization...

**For detailed documentation**: See `modules/authentication.md`
```

## Keep It Optional

Not every module needs a detailed file here. Only create them when the additional detail provides value. Many modules will be adequately documented in the project-state.md file alone.

