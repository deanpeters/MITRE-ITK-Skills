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

When a user describes a product situation and asks which tool to use, match the situation to the appropriate phase, then narrow by context.

### Phase selection heuristic

| Situation | Phase |
|-----------|-------|
| "We don't know who our stakeholders are" | SCOPE |
| "We need to understand the system we're operating in" | SCOPE |
| "We're not sure what problem to solve" | DEFINE |
| "We need to pressure-test our plan" | DEFINE |
| "We need to understand our users" | UNDERSTAND |
| "We need to map the user experience" | UNDERSTAND |
| "We have a problem and need solution ideas" | GENERATE |
| "We have too many ideas" | EVALUATE → Stormdraining or Trimming |
| "We need to test a solution" | EVALUATE → Prototyping |
| "We need to reflect on a sprint or project" | EVALUATE → Retro Rundown |

### Common PM scenarios and recommended tools

**Starting a quarter or initiative**
→ Problem Framing + Premortem + Mission and Vision Canvas

**Running discovery**
→ Painstorming → Personas → Journey Mapping → Value Proposition Canvas

**Stakeholder complexity**
→ Stakeholder Identification Canvas → Stakeholder Map and Matrix → Stakeholder Power Categories → Quickstart Stakeholder Engagement Canvas

**Feature brainstorming**
→ Mindmapping or Lotus Blossom → Stormdraining (to converge)

**Cutting scope**
→ Simplicity Cycle → Trimming

**Sprint retrospective**
→ Retro Rundown or Rose Bud Thorn

**Understanding a complex system**
→ System Map → Community Map

---

## Updating or Extending Skills

### Adding a new skill

Follow the SKILL.md format exactly. Required sections: What Is It, Why Use It, When to Use It, How to Do It, Key Concepts, PM Applications, Benefits, Common Pitfalls, Assets, Metadata. The `best_for` frontmatter field should have 3–5 specific PM scenarios.

### Enriching existing skills

Run `scripts/enrich.py --slug <slug>` to call Claude API and add Key Concepts, PM Applications, and Common Pitfalls. The script skips files already containing `## Key Concepts`.

### Regenerating the catalog index

Run `scripts/generate-catalog.py` to regenerate `catalog/INDEX.md` from all SKILL.md frontmatter.

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/scrape.py` | Scrape MITRE ITK pages, download assets, generate initial SKILL.md files |
| `scripts/enrich.py` | Enrich all SKILL.md files with PM-focused content via Claude API |
| `scripts/generate-catalog.py` | Regenerate `catalog/INDEX.md` from skill frontmatter |

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
