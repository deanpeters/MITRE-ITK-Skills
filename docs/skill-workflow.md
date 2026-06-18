# Adding or Updating a Skill

This guide covers two scenarios:

1. **A new tool appears in the MITRE ITK** — you need to create the full skill from scratch
2. **An existing ITK canvas changes** — the MITRE team updates a tool's steps, structure, or worksheet

Both scenarios follow the same quality bar. The core rule: **all skill content must be grounded in MITRE source documents** (the ITK web page, PDF worksheet, and PPTX template). The enrichment layer — Key Concepts, PM Applications, Common Pitfalls, quality checks in templates, good/bad examples — is additive, but it cannot contradict or extend beyond what MITRE describes for the tool.

---

## Scenario 1: New ITK Tool

### Step 1 — Scrape the source page

```bash
python3 scripts/scrape.py --slug <new-slug>
```

This fetches the ITK tool page, downloads the PDF and PPTX, and generates a thin `skills/<slug>/SKILL.md` with the scraped content. Verify the output:

- `skills/<slug>/SKILL.md` exists with populated What Is It, Why Use It, When to Use It, How to Do It sections
- `skills/<slug>/assets/<file>.pdf` and `.pptx` downloaded

If the scraper misses sections (Divi layout differences, new page structure), fill them in manually from the ITK page. The web page is the authoritative source — not the PDF, which is usually image-based with no extractable text.

Add the new slug to the `TOOLS` list in `scripts/scrape.py`, `scripts/enrich.py`, `scripts/generate-skills.py`, and `scripts/generate-templates.py`.

---

### Step 2 — Enrich the SKILL.md

```bash
python3 scripts/enrich.py --slug <new-slug>
```

This calls Claude API to add:

- `best_for` frontmatter array (3–5 specific PM scenarios)
- `## Key Concepts` section
- `## PM Applications` section
- `## Common Pitfalls` section (replaces the thin scraped `## Challenges`)

**Review the output carefully.** The enrichment is generated from the scraped content plus Claude's knowledge of the underlying frameworks. Check that:

- Key Concepts reflect the vocabulary MITRE actually uses for this tool
- PM Applications name real PM artifacts (PRDs, OKRs, sprint ceremonies) — not generic benefits
- Common Pitfalls name specific failure modes with product consequences, not generic warnings
- Nothing contradicts or invents beyond the MITRE source

Edit `skills/<slug>/SKILL.md` directly if any section needs correction.

---

### Step 3 — Write the template

```bash
python3 scripts/generate-templates.py --slug <new-slug>
```

This generates `skills/<slug>/template.md` from the SKILL.md content. The auto-generated template is a starting point — **review and adorn it** before considering it done.

#### What a complete template looks like

The generated template will have the right structure (fields, tables, step sections). What it won't have is adornment. A complete template also includes:

- **Quality checks** — `> **Quality check:**` blocks after each significant field, telling the practitioner what distinguishes a useful answer from a vague one
- **Guidance notes** — brief instructions inside each section explaining what "good" looks like, what to avoid, and why the field matters
- **A Facilitator Checklist** at the end — a scannable list of the most common failure modes the facilitator should verify before calling the session done
- **A Diversity Coverage Check** where the tool requires considering who may be excluded or underrepresented (Stakeholder Identification, Personas, Community Map, Service Blueprint, System Map)

#### Template content rules

- Structure must mirror the actual canvas/worksheet layout from the MITRE PDF and PPTX
- Use markdown tables (`| col | col |`) for any grid, matrix, 2x2, or multi-column canvas structure
- Use `## Step N` headers that match the How to Do It steps in SKILL.md
- `[placeholder text]` for every field a practitioner fills in
- Every template starts with a `## Session Info` block: Date, Facilitator, Team/Project, Time Box, Participants

#### Writing quality checks

A quality check answers: "How do I know if what I wrote in this field is good?" Model:

> **Quality check:** Are goals observable behaviors ("Deliver cited brief by 3pm Friday") or internal states ("Be successful")? Internal states cannot inform a design decision.

Keep them tight — one or two sentences. They should call out the most common mistake for that specific field, not restate the field's purpose.

---

### Step 4 — Write examples

Create `skills/<slug>/examples/sample.md`.

Every example file needs two examples:

**Example 1: Well-constructed (Good)**
A complete, filled-in version of the template for a realistic PM/product scenario. It should:
- Use a realistic but fictional product context (a B2B SaaS tool, a government platform, a consumer app — pick whatever best illustrates the tool)
- Fill in every field with specific, believable content — not lorem ipsum
- Follow all the quality checks in the template
- Use the MITRE ITK's own specificity guidance (e.g., for Personas: "GS-11 contracting officer" not "government user")

After the filled-in example, add a **"Why this works"** section — 4–6 bullets naming the specific things the example does right and why each one matters.

**Example 2: Poorly constructed (Bad)**
A filled-in version of the same template that fails the quality bar. It should:
- Demonstrate the most common failure modes for this specific tool (not generic "be more specific" advice)
- Be recognizably realistic — teams actually produce output that looks like this

After the bad example, add a **"Why this fails"** section — matching the bad example bullet-for-bullet, explaining the consequence of each failure. Then a **"How to fix it"** section with the concrete correction.

#### Context choices for examples

Use the same product context across both examples in the same file — it makes the contrast cleaner. Pick a context that:
- Is familiar to product practitioners (enterprise SaaS, government platform, consumer product, or marketplace)
- Has enough complexity to illustrate the tool's nuances
- Is not the same context used in every other example file (vary across the skill set)

---

### Step 5 — Generate the Claude Code skill file

```bash
python3 scripts/generate-skills.py --slug <new-slug>
```

This writes `skills/<slug>/itk-<alias>.md`. If the slug is long (more than ~30 characters), add a shorter alias to the `SLUG_ALIASES` dict in `scripts/generate-skills.py` before running.

Review the generated file: confirm the best_for scenarios and Key Concepts pulled in cleanly and the "How to Help" section reads correctly.

Then add a corresponding entry to `.claude-plugin/marketplace.json` — copy an existing entry and update `name`, `source`, `description`, `category`, and `tags`. The name must match the `itk-<alias>` pattern; the source path is `./skills/<slug>/itk-<alias>.md`.

---

### Step 6 — Regenerate the catalog

```bash
python3 scripts/generate-catalog.py
```

Verify the new tool appears in `catalog/INDEX.md` under the correct phase.

---

### Step 7 — Commit

Stage and commit all new files together:

```
skills/<slug>/SKILL.md
skills/<slug>/template.md
skills/<slug>/examples/sample.md
skills/<slug>/assets/<file>.pdf
skills/<slug>/assets/<file>.pptx
skills/<slug>/itk-<alias>.md
dist/zips/itk-<slug>.zip
catalog/INDEX.md
```

Also commit the updated `TOOLS` lists in the four scripts if you added the new slug.

---

## Scenario 2: Existing Tool Updated by MITRE

When MITRE revises a tool — new facilitation steps, a redesigned canvas, updated vocabulary — the workflow is the same as Scenario 1, but with re-generation rather than first-time creation.

### Re-scrape

```bash
python3 scripts/scrape.py --slug <slug>
```

This **overwrites** the SKILL.md with freshly scraped content, losing any manually added enrichment. Before re-scraping:

1. Copy the existing `## Key Concepts`, `## PM Applications`, `## Common Pitfalls`, and `best_for` frontmatter out of the current SKILL.md
2. Re-scrape
3. Re-run enrichment, or manually re-insert the saved sections if they're still accurate
4. Review all enriched sections against the new MITRE source — update anything that contradicts the revised tool

### Regenerate template

Delete the existing template first, then regenerate:

```bash
rm skills/<slug>/template.md
python3 scripts/generate-templates.py --slug <slug>
```

Review the new template against the revised canvas structure. Re-apply adornment (quality checks, guidance notes, checklist) — the generator produces a structural skeleton, not a finished template.

### Update examples

Examples reference the template's structure. If the canvas structure changed significantly, the examples need updating too. Open `skills/<slug>/examples/sample.md` and check that:

- The filled-in good example still maps to the revised template fields
- Any steps or sections the MITRE update removed are removed from the examples
- Any new steps or sections are illustrated in the good example

### Regenerate skill file

```bash
python3 scripts/generate-skills.py --slug <slug>
```

---

## Quality Bar Summary

| File | Content source | Adornment source |
|------|---------------|-----------------|
| `SKILL.md` (What Is It, Why Use It, When to Use It, How to Do It) | MITRE ITK web page | n/a — do not add to these sections |
| `SKILL.md` (Key Concepts, PM Applications, Common Pitfalls, `best_for`) | MITRE + Claude enrichment | PM-practitioner framing; must not contradict MITRE |
| `template.md` | Structure mirrors MITRE canvas/worksheet | Quality checks, guidance notes, checklists are additive |
| `examples/sample.md` | Fictional but realistic PM scenario | Good/bad contrast; annotations explain the why |
| `itk-<alias>.md` | Derived from SKILL.md | "How to Help" pattern is fixed across all skills |

---

## File Structure for a Complete Skill

```
skills/<slug>/
  SKILL.md              ← enriched skill documentation
  template.md           ← annotated canvas template
  itk-<alias>.md        ← Claude Code skill invocation file
  examples/
    sample.md           ← good vs. bad filled examples
  assets/
    <file>.pdf          ← original MITRE worksheet (image-based)
    <file>.pptx         ← original MITRE template

dist/zips/
  itk-<slug>.zip        ← pre-built download bundle (auto-regenerated by CI)

.claude-plugin/
  plugin.json           ← plugin metadata (name, version, author)
  marketplace.json      ← one entry per skill; update when adding new skills
```
