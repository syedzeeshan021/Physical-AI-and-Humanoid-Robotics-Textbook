---
id: 1
title: Urdu Translation Analysis
stage: tasks
date: 2025-12-21
surface: agent
model: claude-opus-4-5-20251101
feature: 001-urdu-translation-button
branch: main
user: Claude Code User
command: /sp.analyze
labels: ["analysis", "spec", "tasks", "plan"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-urdu-translation-button/spec.md
  - specs/001-urdu-translation-button/plan.md
  - specs/001-urdu-translation-button/tasks.md
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Identify inconsistencies, duplications, ambiguities, and underspecified items across the three core artifacts (`spec.md`, `plan.md`, `tasks.md`) before implementation. This command MUST run only after `/sp.tasks` has successfully produced a complete `tasks.md`.

## Operating Constraints

**STRICTLY READ-ONLY**: Do **not** modify any files. Output a structured analysis report. Offer an optional remediation plan (user must explicitly approve before any follow-up editing commands would be invoked manually).

**Constitution Authority**: The project constitution (`.specify/memory/constitution.md`) is **non-negotiable** within this analysis scope. Constitution conflicts are automatically CRITICAL and require adjustment of the spec, plan, or tasks—not dilution, reinterpretation, or silent ignoring of the principle. If a principle itself needs to change, that must occur in a separate, explicit constitution update outside `/sp.analyze`.

## Execution Steps

### 1. Initialize Analysis Context

Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` once from repo root and parse JSON for FEATURE_DIR and AVAILABLE_DOCS. Derive absolute paths:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md

Abort with an error message if any required file is missing (instruct the user to run missing prerequisite command).
For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

### 2. Load Artifacts (Progressive Disclosure)

Load only the minimal necessary context from each artifact:

**From spec.md:**

- Overview/Context
- Functional Requirements
- Non-Functional Requirements
- User Stories
- Edge Cases (if present)

**From plan.md:**

- Architecture/stack choices
- Data Model references
- Phases
- Technical constraints

**From tasks.md:**

- Task IDs
- Descriptions
- Phase grouping
- Parallel markers [P]
- Referenced file paths

**From constitution:**

- Load `.specify/memory/constitution.md` for principle validation

### 3. Build Semantic Models

Create internal representations (do not include raw artifacts in output):

- **Requirements inventory**: Each functional + non-functional requirement with a stable key (derive slug based on imperative phrase; e.g., "User can upload file" → `user-can-upload-file`)
- **User story/action inventory**: Discrete user actions with acceptance criteria
- **Task coverage mapping**: Map each task to one or more requirements or stories (inference by keyword / explicit reference patterns like IDs or key phrases)
- **Constitution rule set**: Extract principle names and MUST/SHOULD normative statements

### 4. Detection Passes (Token-Efficient Analysis)

Focus on high-signal findings. Limit to 50 findings total; aggregate remainder in overflow summary.

#### A. Duplication Detection

- Identify near-duplicate requirements
- Mark lower-quality phrasing for consolidation

#### B. Ambiguity Detection

- Flag vague adjectives (fast, scalable, secure, intuitive, robust) lacking measurable criteria
- Flag unresolved placeholders (TODO, TKTK, ???, `<placeholder>`, etc.)

#### C. Underspecification

- Requirements with verbs but missing object or measurable outcome
- User stories missing acceptance criteria alignment
- Tasks referencing files or components not defined in spec/plan

#### D. Constitution Alignment

- Any requirement or plan element conflicting with a MUST principle
- Missing mandated sections or quality gates from constitution

#### E. Coverage Gaps

- Requirements with zero associated tasks
- Tasks with no mapped requirement/story
- Non-functional requirements not reflected in tasks (e.g., performance, security)

#### F. Inconsistency

- Terminology drift (same concept named differently across files)
- Data entities referenced in plan but absent in spec (or vice versa)
- Task ordering contradictions (e.g., integration tasks before foundational setup tasks without dependency note)
- Conflicting requirements (e.g., one requires Next.js while other specifies Vue)

### 5. Severity Assignment

Use this heuristic to prioritize findings:

- **CRITICAL**: Violates constitution MUST, missing core spec artifact, or requirement with zero coverage that blocks baseline functionality
- **HIGH**: Duplicate or conflicting requirement, ambiguous security/performance attribute, untestable acceptance criterion
- **MEDIUM**: Terminology drift, missing non-functional task coverage, underspecified edge case
- **LOW**: Style/wording improvements, minor redundancy not affecting execution order

### 6. Produce Compact Analysis Report

Output a Markdown report (no file writes) with the following structure:

## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Duplication | HIGH | spec.md:L120-134 | Two similar requirements ... | Merge phrasing; keep clearer version |

(Add one row per finding; generate stable IDs prefixed by category initial.)

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|

**Constitution Alignment Issues:** (if any)

**Unmapped Tasks:** (if any)

**Metrics:**

- Total Requirements
- Total Tasks
- Coverage % (requirements with >=1 task)
- Ambiguity Count
- Duplication Count
- Critical Issues Count

### 7. Provide Next Actions

At end of report, output a concise Next Actions block:

- If CRITICAL issues exist: Recommend resolving before `/sp.implement`
- If only LOW/MEDIUM: User may proceed, but provide improvement suggestions
- Provide explicit command suggestions: e.g., "Run /sp.specify with refinement", "Run /sp.plan to adjust architecture", "Manually edit tasks.md to add coverage for 'performance-metrics'"

### 8. Offer Remediation

Ask the user: "Would you like me to suggest concrete remediation edits for the top N issues?" (Do NOT apply them automatically.)

## Operating Principles

### Context Efficiency

- **Minimal high-signal tokens**: Focus on actionable findings, not exhaustive documentation
- **Progressive disclosure**: Load artifacts incrementally; don't dump all content into analysis
- **Token-efficient output**: Limit findings table to 50 rows; summarize overflow
- **Deterministic results**: Rerunning without changes should produce consistent IDs and counts

### Analysis Guidelines

- **NEVER modify files** (this is read-only analysis)
- **NEVER hallucinate missing sections** (if absent, report them accurately)
- **Prioritize constitution violations** (these are always CRITICAL)
- **Use examples over exhaustive rules** (cite specific instances, not generic patterns)
- **Report zero issues gracefully** (emit success report with coverage statistics)

## Context

$ARGUMENTS

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.

## Response snapshot

## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| D1 | Duplication | MEDIUM | spec.md:42-52, plan.md:126-133 | Translation button requirements duplicated in spec and plan with similar details | Consolidate to avoid confusion; keep spec as source of truth for requirements |
| C1 | Coverage Gap | CRITICAL | tasks.md:all, spec.md:130-132 | Non-functional requirements for performance (3 seconds response) have minimal corresponding tasks | Add specific tasks for performance optimization and monitoring |
| C2 | Coverage Gap | HIGH | tasks.md:all, spec.md:82-84 | Security requirements for translation API not adequately covered in tasks | Add explicit security and rate limiting implementation tasks |
| A1 | Ambiguity | HIGH | spec.md:179, plan.md:64-66 | "Basic account registration" requirement is vague without clear definition | Define specific authentication requirements and verification levels |
| I1 | Inconsistency | MEDIUM | plan.md:10, tasks.md:22 | Plan mentions TypeScript but tasks reference JavaScript files | Align technology stack references across documents |
| I2 | Inconsistency | MEDIUM | spec.md:43, plan.md:127-128, tasks.md:134 | Button positioning described differently across documents | Standardize the positioning requirements across all artifacts |
| C3 | Constitution Alignment | CRITICAL | tasks.md:all | Constitution requires Urdu translation button at chapter start, but tasks don't explicitly verify this placement | Add explicit verification tasks for button positioning per constitution |
| C4 | Constitution Alignment | HIGH | spec.md:165, plan.md:38, tasks.md:134 | Constitution requires RTL support but tasks don't explicitly address RTL CSS implementation | Add specific RTL implementation and testing tasks |

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| user-can-translate-content | Yes | T013-T022 | Well covered with implementation tasks |
| authenticated-user-only-access | Yes | T025-T028 | Covered with authentication tasks |
| rtl-text-rendering | Partial | T033, T038 | Implementation exists but lacks comprehensive testing |
| 3-sec-response-time | No | - | Missing explicit performance tasks |
| translation-api-security | Partial | T019 | Rate limiting covered but not other security aspects |

**Constitution Alignment Issues:**
- Constitution explicitly requires "Urdu translation button component at chapter start for authenticated users" (Section 5.1)
- Constitution requires "Right-to-left layout support where needed" (Section 7.3)
- Constitution mandates "Proper authentication checks for translation features" (Section 6.1)

**Unmapped Tasks:**
- T045 (Documentation updates) - Not directly mapped to specific requirements
- T046 (Database indexing) - Not explicitly tied to specific requirements
- T050 (Quickstart validation) - General validation task

**Metrics:**
- Total Requirements: 24 functional + 9 non-functional = 33
- Total Tasks: 51
- Coverage %: ~85% (28 requirements with >=1 task)
- Ambiguity Count: 3
- Duplication Count: 2
- Critical Issues Count: 2

## Next Actions

- CRITICAL issues exist that should be resolved before implementation: Add tasks for performance requirements and verify button placement per constitution
- HIGH priority: Define clear authentication requirements and add RTL testing tasks
- The feature can proceed but with the identified improvements incorporated
- Recommend running `/sp.tasks` to update the task list with missing performance and security requirements

## Remediation Offer

Would you like me to suggest concrete remediation edits for the top 5 issues identified? (Do NOT apply them automatically.)

The analysis shows that while the Urdu translation feature is well-planned overall, there are several areas that need attention, particularly around constitution alignment, performance requirements coverage, and clarifying ambiguous requirements like the authentication level needed.

## Outcome

- ✅ Impact: Critical and high severity issues identified in spec/plan/tasks alignment
- 🧪 Tests: No new tests created during analysis
- 📁 Files: Analyzed 4 files (spec.md, plan.md, tasks.md, constitution.md)
- 🔁 Next prompts: Suggest updating tasks.md with missing requirements
- 🧠 Reflection: Analysis revealed important gaps between constitution requirements and implementation tasks

## Evaluation notes (flywheel)

- Failure modes observed: Missing performance requirement coverage in tasks
- Graders run and results (PASS/FAIL): Analysis completed successfully
- Prompt variant (if applicable): Standard analysis prompt
- Next experiment (smallest change to try): Add performance and security tasks to tasks.md