# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **BMad Method** installation repository for AI-driven agile planning and development. BMad is a comprehensive framework that uses specialized AI agents (PM, Architect, Developer, QA, Scrum Master, etc.) to guide software projects from planning through implementation.

**Key Characteristics:**
- Agent-based development workflow with role-specific personas
- Structured planning artifacts (PRD, Architecture, Stories, Quality Gates)
- Supports both Greenfield (new projects) and Brownfield (existing codebases)
- Test-driven with integrated QA workflow throughout development lifecycle

## Core Architecture

### Directory Structure

```
.bmad-core/                 # BMad framework core (version 4.44.1)
├── agents/                 # Agent persona definitions (PM, Architect, Dev, QA, SM, etc.)
├── tasks/                  # Executable workflow tasks (create-doc, shard-doc, qa-gate, etc.)
├── templates/              # Document templates (PRD, Architecture, Story, QA Gate, etc.)
├── workflows/              # Project workflow definitions (greenfield/brownfield × ui/service/fullstack)
├── checklists/             # Quality and validation checklists
├── data/                   # Reference data (technical preferences, test frameworks, BMad KB)
├── agent-teams/            # Team composition configurations
├── core-config.yaml        # Project-specific configuration
├── user-guide.md           # Complete BMad Method documentation
└── enhanced-ide-development-workflow.md  # Step-by-step development guide

.claude/commands/BMad/      # Claude Code integration
├── agents/                 # Mirrored agent definitions for Claude Code
└── tasks/                  # Mirrored task definitions for Claude Code

docs/                       # Project artifacts (created during planning/development)
├── prd.md                  # Product Requirements Document
├── architecture.md         # System architecture
├── prd/                    # Sharded epic documents
├── architecture/           # Sharded architecture documents (coding-standards, tech-stack, source-tree)
├── stories/                # User story implementations
└── qa/
    ├── assessments/        # Risk profiles, test designs, NFR assessments, requirement traces
    └── gates/              # Quality gate decisions (PASS/CONCERNS/FAIL/WAIVED)
```

### Configuration File (.bmad-core/core-config.yaml)

Critical configuration that defines project structure:

```yaml
prd:
  prdFile: docs/prd.md
  prdSharded: true
  prdShardedLocation: docs/prd

architecture:
  architectureFile: docs/architecture.md
  architectureSharded: true
  architectureShardedLocation: docs/architecture

devLoadAlwaysFiles:          # Files Dev agent ALWAYS loads
  - docs/architecture/coding-standards.md
  - docs/architecture/tech-stack.md
  - docs/architecture/source-tree.md

devStoryLocation: docs/stories
qa:
  qaLocation: docs/qa
```

## Agent System

BMad uses specialized agents with distinct roles. Each agent has specific responsibilities and access to particular tasks/templates:

### Core Agents

**PM (Product Manager)** - Creates PRDs, manages requirements
- Tasks: `create-doc`, `advanced-elicitation`, `nfr-assess`
- Templates: `prd-tmpl`, `brownfield-prd-tmpl`, `project-brief-tmpl`

**Architect** - Designs system architecture, documents codebase
- Tasks: `create-doc`, `document-project`, `shard-doc`
- Templates: `architecture-tmpl`, `fullstack-architecture-tmpl`, `front-end-architecture-tmpl`, `brownfield-architecture-tmpl`

**Dev (Developer - James)** - Implements stories, writes tests
- Tasks: `execute-checklist`, `apply-qa-fixes`, `validate-next-story`
- Checklists: `story-dod-checklist`
- **CRITICAL**: Only updates story file Dev Agent Record sections (checkboxes, Debug Log, Completion Notes, Change Log, File List, Status)

**QA (Quinn - Test Architect)** - Quality assurance, test strategy, risk assessment
- Tasks: `risk-profile`, `test-design`, `trace-requirements`, `nfr-assess`, `review-story`, `qa-gate`
- Templates: `qa-gate-tmpl`
- Command Aliases: `*risk` → `*risk-profile`, `*design` → `*test-design`, `*trace` → `*trace-requirements`, `*nfr` → `*nfr-assess`

**SM (Scrum Master)** - Creates and drafts stories from epics
- Tasks: `create-next-story`, `create-brownfield-story`, `brownfield-create-epic`
- Templates: `story-tmpl`

**PO (Product Owner)** - Validates alignment across artifacts
- Tasks: `shard-doc`, `validate-next-story`
- Checklists: `po-master-checklist`, `change-checklist`, `story-draft-checklist`

**Analyst** - Market research, competitor analysis, brainstorming
- Tasks: `facilitate-brainstorming-session`, `advanced-elicitation`
- Templates: `market-research-tmpl`, `competitor-analysis-tmpl`, `brainstorming-output-tmpl`

**UX Expert** - Front-end specifications, UI prompt generation
- Tasks: `generate-ai-frontend-prompt`
- Templates: `front-end-spec-tmpl`

### Special Agents

**BMad-Master** - Can perform any task except story implementation, explains BMad Method
**BMad-Orchestrator** - Heavyweight web-only agent, morphs into other agents, high context usage (NOT for IDE use)

## Workflows

### Planning Workflow (Web UI or IDE)

1. **Optional Research** (Analyst): Brainstorming → Market Research → Competitor Analysis → Project Brief
2. **PRD Creation** (PM): From Project Brief or interactive creation → Defines FRs, NFRs, Epics, Stories
3. **Optional UX** (UX Expert): Front End Spec → UI Prompt Generation (for Lovable/V0)
4. **Architecture** (Architect): Create Architecture from PRD (+ UX Spec if applicable)
5. **Optional Early QA** (QA): Early test architecture input on high-risk areas
6. **Validation** (PO): Run master checklist → Ensure alignment → Update if needed
7. **Document Sharding** (PO): Shard PRD and Architecture into epics/stories
8. **Ready for Development**

**Artifacts**: `docs/prd.md`, `docs/architecture.md`, `docs/epics/`, `docs/stories/`

### Core Development Cycle (IDE)

1. **Story Creation** (SM): Review previous notes → Draft next story from sharded epic + architecture → Optional PO validation
2. **Optional Pre-Dev QA** (QA): High-risk stories get `*risk` + `*design` assessments
3. **User Approval**: Review and approve story or request changes
4. **Implementation** (Dev): Sequential task execution → Implement + Write tests → Run validations
5. **Optional Mid-Dev QA** (QA): `*trace` for coverage validation, `*nfr` for quality attributes
6. **Dev Completion**: Mark ready for review + add notes
7. **User Verification**: Request QA review, approve, or request fixes
8. **QA Review** (QA): Test architecture analysis + active refactoring → Quality gate decision
9. **Gate Decision**: PASS/CONCERNS/FAIL → Update gate if needed
10. **CRITICAL**: Verify regression tests and linting pass → **COMMIT CHANGES** → Mark story done
11. **Repeat**: Continue cycle for next story

### Brownfield (Existing Codebase) Workflow

**Approach A - PRD-First** (Recommended for large codebases):
1. Create brownfield PRD first (identifies required scope)
2. Document only relevant areas based on PRD
3. More efficient - avoids documenting unused code

**Approach B - Document-First** (Good for smaller projects):
1. Document entire system first
2. Create PRD with full context
3. More thorough - captures everything

**Key Tasks**: `brownfield-create-prd`, `brownfield-create-epic`, `brownfield-create-story`, `document-project`

## Quality Assurance System

### QA Agent (Quinn - Test Architect)

Quinn is not just a reviewer but a **Test Architect** with deep expertise in test strategy, quality gates, and risk-based testing. Provides advisory authority while actively improving code when safe.

### Command Reference

| Command | Timing | Purpose | Output |
|---------|--------|---------|--------|
| `*risk` | After story draft | Identify risks (technical, security, performance, data, business) | `docs/qa/assessments/{epic}.{story}-risk-{YYYYMMDD}.md` |
| `*design` | After story draft | Create test strategy (scenarios, levels, priorities) | `docs/qa/assessments/{epic}.{story}-test-design-{YYYYMMDD}.md` |
| `*trace` | Mid-development | Verify test coverage mapping to acceptance criteria | `docs/qa/assessments/{epic}.{story}-trace-{YYYYMMDD}.md` |
| `*nfr` | During development | Validate non-functional requirements (security, performance, reliability, maintainability) | `docs/qa/assessments/{epic}.{story}-nfr-{YYYYMMDD}.md` |
| `*review` | After development | Comprehensive test architecture review + active refactoring | QA Results in story + gate file |
| `*gate` | Post-review | Update quality gate status | `docs/qa/gates/{epic}.{story}-{slug}.yml` |

### Risk Scoring System

| Score | Calculation | Priority | Gate Impact |
|-------|-------------|----------|-------------|
| 9 | High probability × High impact | P0 - Must test thoroughly | FAIL if untested |
| 6 | Medium-high combinations | P1 - Should test well | CONCERNS if gaps |
| 4 | Medium combinations | P1 - Should test | CONCERNS if notable gaps |
| 2-3 | Low-medium combinations | P2 - Nice to have | Note in review |
| 1 | Minimal risk | P2 - Minimal | Note in review |

### Quality Gate Statuses

- **PASS**: All critical requirements met, no blocking issues
- **CONCERNS**: Non-critical issues found, team review recommended
- **FAIL**: Critical issues (security risks, missing P0 tests) - must fix
- **WAIVED**: Issues acknowledged and accepted with documented reason, approver, expiry date

### Test Quality Standards

Quinn enforces:
- No flaky tests (proper async handling)
- No hard waits (dynamic strategies only)
- Stateless tests (run independently and in parallel)
- Self-cleaning (tests manage their own data)
- Appropriate test levels (unit for logic, integration for interactions, E2E for journeys)
- Explicit assertions (keep in tests, not buried in helpers)

## Development Best Practices

### Dev Agent Workflow

**Critical Rules:**
- Story contains ALL needed info (except `devLoadAlwaysFiles`)
- NEVER load PRD/architecture/other docs unless explicitly directed
- ONLY update Dev Agent Record sections: Tasks checkboxes, Debug Log, Completion Notes, Change Log, File List, Status
- DO NOT modify: Story, Acceptance Criteria, Dev Notes, Testing sections

**develop-story Command Flow:**
1. Read (first or next) task
2. Implement task and subtasks
3. Write tests
4. Execute validations
5. Only if ALL pass → update task checkbox with `[x]`
6. Update story File List with new/modified/deleted source files
7. Repeat until complete
8. Run `execute-checklist` for `story-dod-checklist`
9. Set story status: 'Ready for Review'
10. HALT

**Blocking Conditions:**
- Unapproved dependencies needed (confirm with user)
- Ambiguous requirements after story check
- 3 consecutive failures implementing/fixing
- Missing configuration
- Failing regression tests

**Ready for Review Criteria:**
- Code matches requirements
- All validations pass
- Follows coding standards
- File List complete

### Context Management

- Keep relevant files only in context
- Keep files lean and focused
- Use appropriate agent for each task
- Work in small, focused tasks
- Maintain clean project structure
- **Commit regularly** - save work frequently

### Technical Preferences

Located at `.bmad-core/data/technical-preferences.md` - biases PM and Architect recommendations for design patterns, technology selection, etc.

## Command Execution

### Command Syntax

Commands require `*` prefix when used (e.g., `*help`, `*risk`, `*design`)

### Dependency Resolution

Dependencies map to `.bmad-core/{type}/{name}`:
- `type` = folder (tasks, templates, checklists, data, utils)
- `name` = file-name
- Example: `create-doc.md` → `.bmad-core/tasks/create-doc.md`

**IMPORTANT**: Only load dependency files when user requests specific command execution

### Request Resolution

Match user requests to commands/dependencies flexibly:
- "draft story" → `*create` → `create-next-story` task
- "make a new prd" → `tasks/create-doc.md` + `templates/prd-tmpl.md`
- ALWAYS ask for clarification if no clear match

## Special Situations

### High-Risk or Brownfield Stories

**ALWAYS run this sequence:**
```
*risk {story}    # First - identify dangers
*design {story}  # Second - plan defense
# During dev:
*trace {story}   # Verify regression coverage
*nfr {story}     # Check performance impact
# Finally:
*review {story}  # Deep integration analysis
```

### Complex Integrations
- Run `*trace` multiple times during development
- Focus on integration test coverage
- Use `*nfr` to validate cross-system performance

### Performance-Critical Features
- Run `*nfr` early and often (not just at review)
- Establish performance baselines before changes
- Document acceptable performance degradation

### Data Migrations
- **REQUIRED**: `*risk`, `*design`, `*trace`, `*review`, `*gate`
- Extra focus on rollback strategies
- Verify data integrity validation

## Interactive Modes

- **Incremental Mode**: Step-by-step with user input (default)
- **YOLO Mode**: Rapid generation with minimal interaction (use with caution)

## File Naming Conventions

**Stories**: `{epic}.{story}-{slug}.md` in `docs/stories/`
**QA Assessments**: `{epic}.{story}-{type}-{YYYYMMDD}.md` in `docs/qa/assessments/`
**QA Gates**: `{epic}.{story}-{slug}.yml` in `docs/qa/gates/`
**Epics**: `epic-{n}*.md` in `docs/prd/` (pattern defined in `core-config.yaml`)

## Version Information

**BMad Core Version**: 4.44.1
**Install Date**: 2025-10-05
**IDEs Supported**: claude-code, github-copilot
**PRD Version**: v4
**Architecture Version**: v4

## Getting Help

- **User Guide**: `.bmad-core/user-guide.md` - Complete BMad Method documentation
- **Enhanced Workflow**: `.bmad-core/enhanced-ide-development-workflow.md` - Step-by-step guide
- **Brownfield Guide**: `.bmad-core/working-in-the-brownfield.md` - Working with existing codebases
- **Discord Community**: https://discord.gg/gk8jAdXWmj
- **GitHub Issues**: https://github.com/bmadcode/bmad-method/issues
- **YouTube**: https://www.youtube.com/@BMadCode

## Critical Reminders

1. **Agent Activation**: Each agent loads `.bmad-core/core-config.yaml` on startup
2. **Stay In Character**: Agents maintain their persona throughout conversations
3. **Task Instructions Override**: When executing formal task workflows, task instructions override base behavioral constraints
4. **Elicitation Required**: Tasks with `elicit=true` require user interaction - cannot be bypassed
5. **Numbered Options**: Always use numbered lists when presenting choices
6. **Commit Before Proceeding**: ALWAYS commit changes after story completion before moving to next story
7. **Regression Testing**: Verify ALL regression tests and linting pass before marking complete
