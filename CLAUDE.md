# CLAUDE.md — Working in the MITRE ITK Skills Repo

## Who This Repo Serves

The primary audience is **product practitioners**: product managers, product owners, product builders, product leaders, and business analysts. These are people who:

- Write PRDs, product strategies, and roadmaps
- Run discovery sprints and user research
- Manage stakeholders and facilitate cross-functional alignment
- Work in agile environments (sprints, retrospectives, backlog refinement)
- Are familiar with Lean Startup, Jobs-to-be-Done, OKRs, and design thinking terminology

This is **not** a general facilitation library. When helping with this repo, frame everything in terms of product work.

---

## How Skills Are Organized

27 tools across 5 ITK phases:

- **SCOPE** (7 tools) — stakeholder mapping, system context, cultural framing
- **DEFINE** (3 tools) — problem framing, premortems, mission/vision
- **UNDERSTAND** (7 tools) — user research synthesis, journey mapping, value mapping
- **GENERATE** (4 tools) — structured brainstorming and ideation
- **EVALUATE** (6 tools) — testing, prioritization, retrospection

Each tool lives at `skills/<slug>/SKILL.md` with assets in `skills/<slug>/assets/`.

---

## SKILL.md Format

```
---
name: slug
description: one-line description
intent: purpose statement
type: component
phase: scope | define | understand | generate | evaluate
outcome: phase name
difficulty: beginner | intermediate | advanced
group_size: e.g. "4+ people"
time_required: e.g. "45+ minutes"
best_for:
  - "specific PM scenario"
sources:
  - MITRE Innovation Toolkit (ITK)
  - "url"
---

# Tool Name

## What Is It
## Why Use It
## When to Use It
## How to Do It
## Key Concepts
## PM Applications
## Benefits
## Common Pitfalls
[## Combine With]
## Assets
## Metadata
```

---

## Recommending Tools

### Adaptive Decision Ladder

The **Adaptive Decision Ladder (ADL)** is a multi-step guided flow that narrows tool recommendations through a sequence of numbered choices. It serves two purposes: **performative** (it helps produce a better-fit recommendation by surfacing context the user may not have thought to provide) and **pedagogic** (it teaches practitioners how to think about which class of tool applies when).

**The ADL is a mode, not a gate.** Experienced users can skip it entirely — or exit it mid-flow — by:
- Naming a tool directly ("walk me through Premortem")
- Providing enough context to resolve the recommendation in one step ("I'm running a discovery kick-off for a new B2B feature, team of 6, 90 minutes")
- Saying "just recommend something" at any point

**When to offer the ADL vs. answer directly:**

| User input | Response |
|------------|----------|
| Names a specific tool | Go directly — explain, contextualize, or walk through it |
| Describes a clear situation with enough detail | Recommend directly; optionally note: *"If you'd like me to ask a few questions to sharpen this further, just say so"* |
| Asks a vague question ("which tool should I use?") | Start the ADL at Step 1 |
| Describes a situation that spans multiple phases | Start the ADL — use their description to pre-answer or skip steps that are already resolved |

**Read context before step 1.** Before presenting any options, check: What phase of work is already evident? What tools have already been mentioned? What artifacts (PRD, roadmap, OKRs) have been referenced? Skip or pre-answer any step that context already resolves — never ask what you already know.

**At any step:** if the user says "just recommend" or provides enough detail to jump ahead, skip remaining steps and go directly to Step 4.

**How it works:**
- Present a small numbered list at each decision point
- The user can reply with a single number (`2`), multiple numbers (`1 & 3`), or choose the open option to describe their situation in their own words
- Carry all prior selections and context forward into each subsequent step
- End with 1–3 specific tool recommendations, ranked, with brief rationale tied to their stated situation

---

### ADL Step 1 — Situation

Present this first:

> **What best describes where you are right now?**
> 1. Scoping — figuring out who's involved, what the system looks like, or what our culture needs
> 2. Defining — not sure what problem to solve, or need to pressure-test a direction
> 3. Understanding users — need research, journey maps, or clearer user needs
> 4. Generating solutions — have a defined problem and need ideas
> 5. Evaluating options — need to test, cut, prioritize, or assess tradeoffs
> 6. Reflecting — sprint retro, project wrap-up, or team health check
> 7. Other (describe)

---

### ADL Step 2 — Narrow by specific need

Branch on their Step 1 answer. Present the relevant sub-menu:

**If 1 (Scoping):**
> 1. I don't know who all my stakeholders are yet
> 2. I know my stakeholders but need to prioritize who to engage
> 3. I need a concrete plan for engaging a specific stakeholder
> 4. I need to map the broader system, community, or ecosystem
> 5. I need to understand and shape our team or org culture
> 6. Multiple of the above

**If 2 (Defining):**
> 1. We're probably solving the wrong problem and need to reframe
> 2. We have a direction but haven't pressure-tested it for failure
> 3. We need to align on long-term purpose (mission/vision)
> 4. Multiple of the above

**If 3 (Understanding users):**
> 1. We need to define or sharpen who our user actually is
> 2. We need to map their end-to-end experience (stages, pain points, wins)
> 3. We need to understand what they need to do, and why (jobs, pains, gains)
> 4. We need to understand how they mentally organize information
> 5. We need to see both the user experience and the behind-the-scenes operations
> 6. Multiple of the above

**If 4 (Generating solutions):**
> 1. Broad, free-associative ideation — explore the whole space
> 2. Structured, systematic ideation — fill every cell
> 3. Embodied ideation — role-play and act out the experience
> 4. Analogical thinking — borrow solutions from other domains

**If 5 (Evaluating options):**
> 1. Too many ideas — need to converge to the most valuable
> 2. Need to test a solution with users before building
> 3. Need to remove unnecessary complexity from an existing design
> 4. Need to assess whether adding features adds or subtracts value

**If 6 (Reflecting):**
> 1. Sprint retrospective — structured team reflection on a recent sprint
> 2. Project or initiative wrap-up
> 3. Quick positive/potential/negative scan of a product, process, or system

---

### ADL Step 3 — Constraints

Always ask this, unless constraints are already clear from context:

> **A couple of quick constraints:**
> Time available:
> 1. Under 45 minutes
> 2. 45–90 minutes
> 3. Multiple sessions are fine
>
> Group size:
> 1. Solo or pair (1–3 people)
> 2. Small team (4–8 people)
> 3. Large group (9+ people)

If the user already mentioned time or team size, skip the relevant sub-question and confirm your assumption ("I'll assume a small team and ~60 minutes — let me know if that's off").

---

### ADL Step 4 — Recommendation

Deliver 1–3 tools, in priority order. Format each recommendation as:

> **[Tool Name]** — one sentence on why it fits their specific situation, referencing the steps they chose.
> _Phase: X · Difficulty: Y · Group: Z · Time: W_
> → [Link to SKILL.md]
>
> Combine with: [Tool Name] if [condition].

If multiple tools are sequenced (e.g., do A before B), say so explicitly: "Start with X to frame the problem, then move to Y to generate solutions."

After the recommendation, offer: "Want me to walk through how to run any of these, or does your situation call for something different?"

---

### Quick-reference: phase heuristics (for direct matching)

Use these when the situation is unambiguous and the ADL isn't needed:

| Situation | Phase | Primary tool(s) |
|-----------|-------|-----------------|
| Don't know who the stakeholders are | SCOPE | Stakeholder Identification Canvas |
| Need to prioritize stakeholder engagement | SCOPE | Stakeholder Map and Matrix → Power Categories |
| Need to understand the broader system | SCOPE | System Map |
| Not sure what problem to solve | DEFINE | Problem Framing |
| Need to pressure-test a plan or OKRs | DEFINE | Premortem |
| Need long-term direction | DEFINE | Mission and Vision Canvas |
| Need to understand users | UNDERSTAND | Personas → Painstorming |
| Need to map the user journey | UNDERSTAND | Journey Mapping |
| Need to map user needs to product value | UNDERSTAND | Value Proposition Canvas |
| Have a problem, need ideas | GENERATE | Mindmapping or Lotus Blossom |
| Too many ideas, need to converge | EVALUATE | Stormdraining |
| Need to cut scope or complexity | EVALUATE | Simplicity Cycle → Trimming |
| Need to test a solution | EVALUATE | Prototyping |
| Sprint retrospective | EVALUATE | Retro Rundown or Rose Bud Thorn |

---

## Updating or Extending Skills

### Adding a new skill or updating an existing one

See [`docs/skill-workflow.md`](docs/skill-workflow.md) for the full workflow, including quality bar for SKILL.md, template adornment, and example file structure.

Quick reference:

```bash
python3 scripts/scrape.py --slug <slug>           # 1. scrape source page + download assets
python3 scripts/enrich.py --slug <slug>           # 2. enrich SKILL.md via Claude API
python3 scripts/generate-templates.py --slug <slug>  # 3. generate template.md skeleton
# 4. manually adorn template.md + write examples/sample.md
python3 scripts/generate-skills.py --slug <slug>  # 5. generate claude-skills/itk-*.md
python3 scripts/generate-catalog.py              # 6. update catalog/INDEX.md
python3 scripts/generate-zips.py --slug <slug>   # 7. regenerate dist/zips/itk-<slug>.zip
```

### Regenerating the catalog index

Run `scripts/generate-catalog.py` to regenerate `catalog/INDEX.md` from all SKILL.md frontmatter.

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/scrape.py` | Scrape MITRE ITK pages, download assets, generate initial SKILL.md files |
| `scripts/enrich.py` | Enrich all SKILL.md files with PM-focused content via Claude API |
| `scripts/generate-catalog.py` | Regenerate `catalog/INDEX.md` from skill frontmatter |
| `scripts/generate-skills.py` | Regenerate `claude-skills/itk-*.md` skill invocation files from SKILL.md content |
| `scripts/generate-templates.py` | Generate `skills/<slug>/template.md` canvas templates from SKILL.md content |
| `scripts/generate-zips.py` | Generate `dist/zips/itk-<slug>.zip` per-skill bundles (SKILL.md + template + assets + claude-skill) |

### generate-zips.py options

```bash
python3 scripts/generate-zips.py                    # Generate all 27 zips
python3 scripts/generate-zips.py --slug <slug>      # Generate one zip
python3 scripts/generate-zips.py --dry-run          # Preview without writing
```

Each zip contains `SKILL.md`, `template.md`, `examples/sample.md` (if present), `assets/` (PDF + PPTX), and the matching `itk-<alias>.md` claude-skill file. GitHub Actions regenerates affected zips automatically on any push to `main` that touches `skills/**` or `claude-skills/**`.

### generate-templates.py options

```bash
python3 scripts/generate-templates.py                   # Generate all 27 templates (skips existing)
python3 scripts/generate-templates.py --slug <slug>     # Generate one template
python3 scripts/generate-templates.py --dry-run         # Preview without writing
```

Run this after re-enriching a SKILL.md to regenerate its template. Delete `template.md` first to force a refresh.

### generate-skills.py options

```bash
python3 scripts/generate-skills.py                   # Regenerate all 27 skill files
python3 scripts/generate-skills.py --slug <slug>     # Regenerate one skill file
python3 scripts/generate-skills.py --dry-run         # Preview output paths without writing
```

Run this after re-enriching a SKILL.md to keep the skill files in sync.

### enrich.py options

```bash
python3 scripts/enrich.py                    # Enrich all 27 skills (skips already-enriched)
python3 scripts/enrich.py --slug <slug>      # Enrich one skill
python3 scripts/enrich.py --dry-run          # Preview what would be added
```

### scrape.py options

```bash
python3 scripts/scrape.py                    # Re-scrape all 27 tools
python3 scripts/scrape.py --slug <slug>      # Re-scrape one tool
python3 scripts/scrape.py --dry-run          # Preview without writing
```

---

## Writing Style for This Repo

- Write for practitioners who know product work — no need to define "sprint" or "PRD"
- Be concrete and specific — name real artifacts (PRDs, OKRs, roadmaps, user stories)
- Avoid facilitation clichés ("create psychological safety", "align the team") unless specific
- Common Pitfalls should name the failure mode and its product consequence
- PM Applications should name specific product activities, not generic benefits
- Key Concepts should cover both the tool's theoretical underpinning and product-specific vocabulary

---

## Key Dependencies

```
python3 >= 3.11
anthropic >= 0.84.0       # Claude API client
scrapling >= 0.4.2        # Web scraping (Fetcher, Adaptor)
requests >= 2.31.0        # Asset downloads
pdfplumber >= 0.11.9      # PDF inspection (most ITK PDFs are image-based)
```

Note: Most ITK PDFs are image-based worksheets with no extractable text. Don't attempt PDF extraction as a content source — use the scraped web pages instead.
