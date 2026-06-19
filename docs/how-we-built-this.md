# How We Built the MITRE ITK Skills Library

A candid account of building a structured AI skills library from a third-party framework — including the structural mistakes, naming disasters, and pivots that shaped the final result. Written for anyone building a similar skills library from an existing framework, playbook, or methodology.

---

## Inspiration

The primary design reference for this library was the **[Product Manager Skills repo](https://github.com/deanpeters/product-manager-skills)** — a Claude Code skills library built around PM frameworks and practices. That repo established the core patterns we adopted here:

- **One skill per directory, one SKILL.md file** — the skill file is the unit of deployment
- **The learning simulator pattern** — when a user invokes a skill, the AI runs the exercise end-to-end against the user's context and returns a filled artifact, not facilitation instructions
- **Three-section output structure** — `## Filled Template` (the artifact, rendered first), `## Steps and Transformations` (how we got there), `## Assumptions Made` (what was inferred)
- **No follow-up questions** — the AI makes explicit labeled assumptions rather than asking the user to fill in missing context

The Streamlit app's skill runner was rebuilt entirely around this pattern after the first version returned facilitation guides instead of artifacts. The PM Skills `app/main.py` was the direct reference for the prompt structure and output layout.

---

## What We Were Building

The [MITRE Innovation Toolkit (ITK)](https://itk.mitre.org/toolkit/tools-at-a-glance/) is a publicly available collection of 27 facilitation tools rooted in human-centered design and systems thinking. The tools are well-documented on the web, with downloadable PDF worksheets and PPTX templates.

The goal was to turn those 27 tools into an AI skills library for product practitioners — not just documentation, but invokable Claude Code skills that would let a PM type `/itk-premortem` and get real output from a real AI session, not a link to a how-to page.

The output needed to serve two purposes simultaneously:
1. **Functional** — each skill produces a filled artifact (a persona, a stakeholder map, a premortem) from the user's context
2. **Pedagogic** — each skill teaches why the tool works and how to apply it in product work

---

## The Pipeline

The final build pipeline has five scripts:

```
scrape.py          → pulls ITK web pages, downloads PDFs/PPTXs, seeds SKILL.md
enrich.py          → calls Claude API to add PM-specific content to SKILL.md
generate-templates.py → generates the canvas template (template.md)
generate-catalog.py   → builds catalog/INDEX.md from all SKILL.md frontmatter
generate-zips.py      → packages each skill as a downloadable zip
```

The sequence for a new skill:

```bash
python3 scripts/scrape.py --slug itk-<alias>
python3 scripts/enrich.py --slug itk-<alias>
python3 scripts/generate-templates.py --slug itk-<alias>
# manually adorn template.md + write examples/sample.md
python3 scripts/generate-catalog.py
python3 scripts/generate-zips.py --slug itk-<alias>
```

Each skill lives at `skills/itk-<alias>/` and contains:

```
SKILL.md       ← the AI skill file (this is what Claude Code, Codex, Cursor load)
template.md    ← annotated canvas template with quality checks
examples/      ← good/bad filled examples
assets/        ← original MITRE PDF and PPTX
```

That's the clean version. Getting there took several wrong turns.

---

## Phase 1: Scraping and Enriching

### What worked

**Scrapling over BeautifulSoup.** The MITRE ITK site uses Divi, a page builder with deeply nested, semantically meaningless HTML. Standard DOM traversal was brittle. Scrapling's CSS selector approach with fuzzy fallbacks handled the layout variation across 27 pages without per-page custom code.

**Claude API for enrichment.** The scraped content gave us the MITRE-sourced sections (What Is It, Why Use It, When to Use It, How to Do It). Claude filled in the PM-specific sections: Key Concepts with product vocabulary, PM Applications naming real artifacts (PRDs, OKRs, sprint ceremonies), Common Pitfalls with specific failure modes and product consequences, and a `best_for` frontmatter array of 3–5 trigger scenarios.

This split — MITRE owns the canonical content, Claude adds the practitioner layer — proved important. It kept the library grounded in the source material while making it useful for a PM who doesn't care about the theoretical underpinning.

**The quality bar for enrichment.** Early enrichment runs produced generic content: "helps teams align," "fosters collaboration," "creates shared understanding." The prompt needed explicit negative constraints: no facilitation clichés, PM Applications must name real artifacts not generic benefits, Common Pitfalls must name the failure mode AND its product consequence. With those guardrails, the output became specific enough to be useful.

### What didn't work

**Trying to extract PDF content.** Most ITK PDFs are image-based worksheets — there's no selectable text. Several hours went into `pdfplumber` before accepting that the web page is the authoritative source and the PDF is a printable artifact. The CLAUDE.md now explicitly notes this so no one repeats the mistake.

---

## Converting Visual Templates to Text

This was one of the more interesting problems in the project. The MITRE ITK's primary artifacts — the PDF worksheets and PPTX templates — are visual canvases: boxes, grids, 2x2 matrices, swim lanes. They're designed to be printed and written on or filled in a slide deck. None of that structure is semantically present in the file — PDFs are image-based with no extractable text, and the PPTX files are slide layouts with floating text boxes.

The challenge: turn a visual canvas into a text-based markdown template that could be filled by an AI and read back as coherent output.

### The approach

**Step 1 — Derive structure from the web page, not the file.**

The MITRE ITK web pages describe each tool's facilitation steps in plain prose. That prose is the canonical description of what fields the canvas has and what each section is for. The scraper pulls this content. The enriched SKILL.md's `## How to Do It` section becomes the authoritative description of the canvas structure.

The PDF and PPTX are downloaded and included in the zip bundle as reference artifacts for practitioners running in-person sessions, but they are never the source of truth for template structure.

**Step 2 — Use Claude to infer the markdown structure from SKILL.md.**

`generate-templates.py` calls Claude with the full SKILL.md content and a prompt that asks it to:

- Mirror the actual canvas layout from the How to Do It steps
- Use markdown tables (`| col | col |`) for any grid, matrix, 2x2, or multi-column structure
- Use `## Step N` headers that match the facilitation steps
- Place `[placeholder text]` in every field a practitioner fills in
- Open with a `## Session Info` block (Date, Facilitator, Team/Project, Time Box, Participants)

The generated template is a structural skeleton — correct shape, correct fields, empty values. It is not a finished template.

**Step 3 — Manual adornment.**

The generator can't write quality checks, because quality checks require judgment about what failure looks like for each specific field. That's a human step. A finished template also includes:

- `> **Quality check:**` blocks after significant fields — one or two sentences on what distinguishes a useful answer from a vague one
- Guidance notes inside each section on what "good" looks like
- A **Facilitator Checklist** at the end — scannable list of the most common failure modes
- A **Diversity Coverage Check** for tools that require considering who may be excluded (Stakeholder Identification, Personas, Community Map, Service Blueprint, System Map)

### What this looks like in practice

A stakeholder map canvas becomes a markdown table with rows for each stakeholder and columns for influence, interest, engagement approach, and notes. A premortem becomes a structured list with a hypothesis row, an impact/likelihood table for risks, and a mitigation column. A persona canvas becomes a set of labeled sections with specific fields (role, goals, frustrations, current workarounds, success metrics) rather than open-ended prose boxes.

The key insight: AI fills text better than it fills visual space. A markdown template with named fields and placeholder text gives the AI a scaffold to work against. Without it, the output tends to be prose narrative rather than structured artifact. With it, the output mirrors the actual canvas format that practitioners recognize.

### The harder cases

Some canvases are genuinely visual in ways that don't translate cleanly to markdown. The **Simplicity Cycle** is an XY scatter plot — complexity on one axis, goodness on the other. The **System Map** is a node-and-edge diagram. For these, the template represents the *inputs* to the visual (the elements to be placed, with their assessed coordinates or relationships) rather than the visual itself, and notes that the output should be transferred to the actual canvas for visualization.

---

## Phase 2: Generating Claude Code Skills

This is where the first major structural mistake happened.

### The mistake: two files per skill

The initial instinct was: the enriched SKILL.md is long and detailed, suitable for a human practitioner reading documentation. A Claude Code skill file should be shorter and more action-oriented. So we generated a separate condensed file — `claude-skills/itk-premortem.md` — from each SKILL.md.

This created a `claude-skills/` directory alongside `skills/`, each with 27 files, with a `generate-skills.py` script to keep them in sync.

The result: two directories, two naming systems, a sync script that had to be run after every enrichment update, and a repo structure that immediately confused anyone who opened it. The `claude-skills/` directory implied a different audience from `skills/`, which contradicted the whole point — there is one audience.

**The lesson:** Don't generate a separate file for deployment. The SKILL.md IS the skill. If it's too long, the enrichment prompt needs constraints, not a post-processing step that extracts a condensed version. A generated condensed file will always drift from the source.

### The fix

Deleted `generate-skills.py`. Moved the content of each `itk-*.md` into its skill's directory. The `claude-skills/` directory was eliminated. Each skill became `skills/<slug>/SKILL.md` with a separate `itk-*.md` alongside it.

Which immediately created the next problem.

---

## Phase 3: The Naming Disaster

### The mistake: two naming systems in one directory

After eliminating `claude-skills/`, each skill directory looked like this:

```
skills/premortem/
  SKILL.md          ← enriched documentation
  itk-premortem.md  ← the "skill" file
  template.md
  assets/
```

This was worse than before. Now there were two markdown files in the same directory, one named after the tool and one named after the slash command. The directory used the old slug (`premortem`), the skill file used the alias with prefix (`itk-premortem.md`). There was no clear answer to "which file is the skill?"

The user's reaction: *"this is confusing and a heinous violation of the Claude/Anthropic standard."*

They were right. The standard is simple: one skill, one file, the directory and file names should tell you what the skill is and how to invoke it.

### The fix

Three changes at once:

1. Rename every skill directory from `skills/<slug>` to `skills/itk-<alias>` — the directory name matches the slash command
2. Delete every `itk-*.md` file — `SKILL.md` is the skill, full stop
3. Update the `name:` field in every SKILL.md's frontmatter to match the alias

That third step was missed in the initial fix and caused the next bug.

### The mistake: forgetting the frontmatter

After renaming directories and deleting the redundant files, the skills loaded in Claude Code as `/personas` instead of `/itk-personas`. The `name:` field in each SKILL.md's frontmatter still had the old slug (`name: personas`). Claude Code reads that field for the slash command name.

A one-line regex fix across all 27 files resolved it — but it required a separate commit because the directory rename didn't automatically update the frontmatter.

**The lesson:** When you rename a skill, there are at least three places the name lives: the directory, the `name:` frontmatter, and any config files (marketplace.json, catalog). A rename script needs to touch all three atomically.

---

## Phase 4: The Streamlit App

A browser-based explorer was added to let users try skills without installing Claude Code. The app used the Adaptive Decision Ladder (ADL) to guide users to the right tool, then ran the skill against their context and returned a filled artifact.

### Mistake 1: Generating facilitation guides instead of artifacts

The first version of the skill runner returned facilitation instructions — "here's how to run a premortem with your team." Users wanted output: a filled premortem table, a completed persona card.

The fix was a prompt rewrite using the "learning simulator" pattern: run the exercise end-to-end internally, produce a filled artifact as the primary output, put the methodology explanation in collapsed expanders below it. Artifact first, pedagogy optional.

### Mistake 2: API key input in the UI

The initial UI included a text input for the API key. This was removed immediately. Keys come from environment variables only (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`). There is no `st.text_input` for credentials anywhere in the app. Users trust an app more when it never asks them to paste a secret into a form field.

### Mistake 3: Output cleared on scroll

A persistent Streamlit rendering bug: after a skill run completed, scrolling to the bottom of the output cleared the screen. Root cause: using `st.empty()` for streaming, then calling `.empty()` on the placeholder after completion, left a ghost DOM element that caused scroll-triggered rerenders.

The partial fix was replacing `output_placeholder.empty()` with `st.rerun()` — save the result to session state, trigger a clean rerender, render from state. This reduced but did not eliminate the issue. The Streamlit app remains marked experimental in the README with the known bug documented.

**The lesson:** Streaming output in Streamlit is fragile. If you need guaranteed-stable output rendering, collect the full response behind a spinner and render once, rather than streaming into a live placeholder.

### Mistake 4: Pedagogic-first layout

The output was originally organized in tabs: "Filled Template," "Steps," "Assumptions." The tabs buried the artifact. Users had to click to find the thing they actually wanted.

The fix: render the artifact directly with `st.markdown()`, put Steps and Assumptions in collapsed `st.expander()` below it. The primary output is immediately visible; the methodology is available but not in the way.

---

## Phase 5: Distribution

### What worked

**Per-skill zip bundles.** Each skill gets a `dist/zips/itk-<alias>.zip` containing SKILL.md, template.md, assets/, and examples/. Users can download a single skill without cloning the repo. GitHub releases or direct file download from the repo both work.

**GitHub Actions for zip maintenance.** A workflow triggers on any push to `main` that touches `skills/**` and regenerates affected zips, committing them back with `[skip ci]`. This means the zips are always current without requiring a manual step.

The one wrinkle: the workflow commits back to main, which means local pushes need `git pull --rebase` before the next push. Not a problem in practice, but worth knowing.

**`.claude-plugin/` for installable plugin deployment.** The `marketplace.json` registers all 27 skills as a Claude Code plugin, with each entry pointing to `./skills/itk-<alias>/SKILL.md`. Users who clone the repo and point Claude Code at it get all 27 skills without any manual installation.

---

## Final Structure

```
skills/
  itk-premortem/
    SKILL.md         ← the skill (name: itk-premortem in frontmatter)
    template.md      ← canvas template with quality checks
    examples/
      sample.md      ← good/bad filled examples
    assets/
      Premortem.pdf
      Premortem.pptx

scripts/
  scrape.py
  enrich.py
  generate-templates.py
  generate-catalog.py
  generate-zips.py

dist/zips/
  itk-premortem.zip
  ...

.claude-plugin/
  plugin.json
  marketplace.json

catalog/
  INDEX.md
```

---

## Lessons for Building Similar Libraries

### 1. One name, everywhere

Pick the canonical name for each skill — the one users will type — and use it for the directory, the `name:` frontmatter, the zip filename, and the config entry. Any divergence creates a class of bugs that only surfaces when someone actually tries to use the skill.

### 2. The skill file IS the skill

Don't generate a separate condensed file for deployment. If the skill file is too long, constrain the enrichment prompt. A generated condensed file will drift from the source and require a sync script. That sync script will be forgotten.

### 3. Split content ownership clearly

For frameworks sourced from a third party (MITRE, a methodology vendor, a standards body): keep the canonical content in sections attributed to the source, and the enrichment layer — PM vocabulary, product applications, failure modes — in separate sections. This makes it obvious what can be updated without changing source content, and what requires checking the source document.

### 4. Anchor enrichment quality with negative constraints

Generic enrichment prompts produce generic output. The quality constraints that matter most:
- Names must be concrete (not "the team" — "a 4-person product squad in discovery")
- PM Applications must name real artifacts (PRD, OKR, sprint retro) — not abstract benefits
- Common Pitfalls must name the failure mode AND its downstream product consequence
- Key Concepts must reflect vocabulary the source material actually uses

### 5. Design the install path before writing the first file

How will users actually get the skills into their tools? The answer shapes every naming and structure decision. For Claude Code: `~/.claude/skills/itk-premortem.md`, installed by filename. For a plugin: `marketplace.json` pointing to the source file. Design this first, then name things to match.

### 6. Mark experimental features as experimental

The Streamlit app ships with a documented known bug. That's fine. Undocumented bugs erode trust; documented ones set expectations. "Known issue: output may clear after generation. Click Run again." is better than a silent failure with no explanation.

### 7. The catalog is a byproduct, not a goal

`catalog/INDEX.md` is generated from frontmatter. It's useful but it's not the library — the skills are the library. Build the scripts to generate it automatically so it stays current without becoming a maintenance obligation.

---

## What This Was Built With

- **Python 3.11** — all scripts
- **Scrapling** — web scraping (handles Divi/JS-heavy pages better than BeautifulSoup)
- **Anthropic Python SDK** — enrichment via Claude API
- **Streamlit** — browser-based explorer
- **GitHub Actions** — zip regeneration on push
- **CC BY-NC-SA 4.0** — license matching MITRE's ShareAlike terms (required by the source)
