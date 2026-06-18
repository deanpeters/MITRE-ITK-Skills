# MITRE ITK Skills for Product Practitioners

![MITRE ITK Skills](docs/mitre-itk-skills.banner.png)

A structured library of 27 innovation and design-thinking tools from the [MITRE Innovation Toolkit (ITK)](https://itk.mitre.org/toolkit/tools-at-a-glance/), adapted for product managers, product owners, product builders, and business analysts.

---

## Why This Exists

The MITRE Innovation Toolkit is a well-designed collection of facilitation tools rooted in human-centered design, systems thinking, and collaborative problem solving. These tools are used by researchers, engineers, and strategists at MITRE and beyond — but their documentation is written for a broad audience of facilitators.

This library repurposes the ITK for a specific reader: **product practitioners** — people writing PRDs, running discovery sprints, aligning stakeholders, building roadmaps, and shipping software. Each skill file goes beyond the original ITK instructions to answer the questions PMs actually ask:

- *When in a product cycle would I reach for this?*
- *What does this look like in a sprint review vs. a discovery kickoff?*
- *What are the failure modes specific to product contexts?*
- *What vocabulary do I need to use this fluently with my team?*

The goal is dual: **functional** (you can run these tools) and **pedagogic** (you understand *why* they work and how they connect to product thinking more broadly).

---

## The Five Phases

The ITK organizes tools into five sequential phases that mirror a design-thinking double diamond. Product work rarely follows this sequence literally, but the phases are useful mental frames for knowing which tool class to reach for.

| Phase | Purpose | Tools |
|-------|---------|-------|
| **SCOPE** | Get clarity on the problem space, stakeholders, and context | 7 |
| **DEFINE** | Clarify and prioritize the specific problems and hypotheses | 3 |
| **UNDERSTAND** | Explore the defined problem through user research and synthesis | 7 |
| **GENERATE** | Brainstorm and create solutions | 4 |
| **EVALUATE** | Test, assess, and iterate on solutions | 6 |

---

## Navigating the Library

### By Phase

Browse all 27 tools organized by phase in the [catalog index](catalog/INDEX.md).

### By Product Activity

**Starting a new initiative or quarter**
- [Problem Framing](skills/itk-problem-framing/SKILL.md) — frame the right problem before committing to a direction
- [Premortem](skills/itk-premortem/SKILL.md) — stress-test OKRs and plans before locking them
- [Mission and Vision Canvas](skills/itk-mission-vision/SKILL.md) — align teams on the aspirational destination

**Stakeholder mapping and engagement**
- [Stakeholder Identification Canvas](skills/itk-stakeholder-identify/SKILL.md) — broaden who you're considering
- [Stakeholder Map and Matrix](skills/itk-stakeholder-map/SKILL.md) — prioritize by influence and interest
- [Stakeholder Power Categories](skills/itk-stakeholder-power/SKILL.md) — categorize by power dynamics
- [Quickstart Stakeholder Engagement Canvas](skills/itk-stakeholder-quickstart/SKILL.md) — plan your engagement approach
- [Community Map](skills/itk-community-map/SKILL.md) — fast stakeholder capture for workshops

**User and customer discovery**
- [Personas](skills/itk-personas/SKILL.md) — define who you're building for
- [Painstorming](skills/itk-painstorming/SKILL.md) — structured elicitation of user pain
- [Journey Mapping](skills/itk-journey-mapping/SKILL.md) — end-to-end experience visualization
- [Service Blueprint](skills/itk-service-blueprint/SKILL.md) — frontstage/backstage service visualization
- [Value Proposition Canvas](skills/itk-value-prop/SKILL.md) — map user needs to product value
- [Card Sorting](skills/itk-card-sorting/SKILL.md) — understand user mental models
- [Storyboarding](skills/itk-storyboarding/SKILL.md) — narrative experience communication

**Ideation and solution generation**
- [Mindmapping](skills/itk-mindmapping/SKILL.md) — relationship-driven concept exploration
- [Lotus Blossom](skills/itk-lotus-blossom/SKILL.md) — structured divergent brainstorming
- [Bodystorming](skills/itk-bodystorming/SKILL.md) — embodied ideation for physical or interaction design
- [TRIZ Prism](skills/itk-triz-prism/SKILL.md) — analogical problem-solving from known solutions

**Prioritization and evaluation**
- [Stormdraining](skills/itk-stormdraining/SKILL.md) — converge a large idea set to the most valuable
- [Trimming](skills/itk-trimming/SKILL.md) — structured removal of unnecessary complexity
- [Simplicity Cycle](skills/itk-simplicity-cycle/SKILL.md) — assess complexity vs. value of design elements
- [Rose Bud Thorn](skills/itk-rose-bud-thorn/SKILL.md) — positive/potential/negative categorization
- [Prototyping](skills/itk-prototyping/SKILL.md) — low-cost hypothesis testing

**Team health and retrospectives**
- [Retro Rundown](skills/itk-retro-rundown/SKILL.md) — structured team reflection
- [Culture Building Canvas](skills/itk-culture-building-canvas/SKILL.md) — shaping team or org culture intentionally
- [System Map](skills/itk-system-map/SKILL.md) — mapping systemic forces and relationships

---

## How to Use a Skill File

Each tool's SKILL.md is structured as:

| Section | What It Contains |
|---------|-----------------|
| **Frontmatter** | Metadata: phase, difficulty, group size, time required, best-fit scenarios (`best_for`) |
| **What Is It** | Definition from the MITRE ITK |
| **Why Use It** | The core purpose and organizational benefit |
| **When to Use It** | Trigger conditions — moments in product work when this tool applies |
| **How to Do It** | Step-by-step facilitation instructions |
| **Key Concepts** | Vocabulary and frameworks behind the tool, explained for product practitioners |
| **PM Applications** | Specific PM/product activities: PRDs, roadmaps, OKRs, sprint ceremonies, stakeholder briefings |
| **Benefits** | What the tool is good at |
| **Common Pitfalls** | Specific failure modes to avoid |
| **Combine With** | Tools that pair well |
| **Assets** | Downloadable PDF worksheet and PPTX template from the MITRE ITK |

The `best_for` frontmatter field lists 3–5 specific scenarios where the tool is most valuable — useful for quickly scanning whether a tool fits your current situation.

---

## Difficulty Levels

Tools are rated by facilitation complexity, not conceptual complexity.

- **Beginner** — Can be run with minimal facilitation experience and no prior exposure to the tool
- **Intermediate** — Benefits from a facilitator who has run it before; requires some preparation
- **Advanced** — Requires an experienced facilitator and careful setup to produce high-quality output

---

## Asset Downloads

Each skill directory includes the original MITRE ITK assets:
- `assets/*.pdf` — printable worksheet for in-person use
- `assets/*.pptx` — digital template for remote facilitation

Most PDF worksheets are image-based (designed for printing and writing on), so the PPTX templates are better for digital facilitation.

---

## Try It in the Browser

> **Experimental.** `streamlit_app.py` is a work in progress. Known issue: after a skill run completes, the output may clear itself before you can read it. This is a Streamlit rendering bug we haven't fully resolved — if it happens, clicking "Run" again will regenerate the output.

`streamlit_app.py` is a browser-based explorer for the full skill library. Walk the Adaptive Decision Ladder to find the right tool for your situation, or browse all 27 tools directly. Pick a tool, describe your session context, and get a filled artifact — no account or API key required.

**Deployed app:** _(link once deployed to Streamlit Community Cloud)_

**Run locally:**

```bash
pip install -r requirements.txt

# Set your API key as an environment variable — keys are never entered into the UI
export ANTHROPIC_API_KEY=sk-ant-...   # for Anthropic
export OPENAI_API_KEY=sk-...          # for OpenAI
# or run Ollama locally (no key needed)

streamlit run streamlit_app.py
```

The sidebar lets you choose provider (Anthropic, OpenAI, Local model) and model. The app reads credentials from your environment — no key entry in the UI.

---

## Docs

| Document | Purpose |
|---|---|
| [Skill Workflow](docs/skill-workflow.md) | How to add a new ITK tool or update an existing one — SKILL.md, template, examples, and Claude skill file |
| [Meet the MITRE ITK Skills Repo](docs/Meet%20the%20MITRE%20ITK%20Skills%20Repo.md) | Introductory blog post: who this library is for, why it exists, and how to use it |

---

## Using as Claude Code Skills

The `claude-skills/` directory contains 27 ready-to-use [Claude Code](https://claude.ai/code) skill files — one per tool, prefixed with `itk-`. Each file loads the tool's best-fit scenarios, key concepts, and common pitfalls directly into a Claude session, with built-in guidance for running the Adaptive Decision Ladder or skipping it when you already know what you need.

### Install via plugin

This repo ships a `.claude-plugin/` directory that registers all 27 skills as a Claude Code plugin. Clone the repo and point Claude Code to it:

```bash
git clone https://github.com/deanpeters/MITRE-ITK-Skills.git
```

Then add the repo path to your Claude Code plugin sources in `~/.claude/settings.json`:

```json
{
  "plugins": ["~/path/to/MITRE-ITK-Skills"]
}
```

### Install via symlink

```bash
# Clone the repo
git clone https://github.com/deanpeters/MITRE-ITK-Skills.git

# Symlink all 27 skills into your Claude Code skills directory
for dir in MITRE-ITK-Skills/skills/itk-*/; do
  alias=$(basename "$dir")
  ln -s "$(pwd)/$dir/SKILL.md" ~/.claude/skills/"$alias".md
done
```

Or copy an individual skill:

```bash
cp MITRE-ITK-Skills/skills/itk-itk-premortem/SKILL.md ~/.claude/skills/itk-premortem.md
```

### Invoke

Once installed, invoke any skill in a Claude Code session:

```
/itk-premortem
/itk-value-prop
/itk-journey-mapping
/itk-stakeholder-map
```

### Skill name reference

| Invoke as | Full tool name |
|---|---|
| `/itk-premortem` | Premortem |
| `/itk-problem-framing` | Problem Framing |
| `/itk-mission-vision` | Mission and Vision Canvas |
| `/itk-personas` | Personas |
| `/itk-painstorming` | Painstorming |
| `/itk-journey-mapping` | Journey Mapping |
| `/itk-value-prop` | Value Proposition Canvas |
| `/itk-service-blueprint` | Service Blueprint |
| `/itk-card-sorting` | Card Sorting |
| `/itk-storyboarding` | Storyboarding |
| `/itk-stakeholder-identify` | Stakeholder Identification Canvas |
| `/itk-stakeholder-map` | Stakeholder Map and Matrix |
| `/itk-stakeholder-power` | Stakeholder Power Categories |
| `/itk-stakeholder-quickstart` | Quickstart Stakeholder Engagement Canvas |
| `/itk-community-map` | Community Map |
| `/itk-system-map` | System Map |
| `/itk-culture-building-canvas` | Culture Building Canvas |
| `/itk-mindmapping` | Mindmapping |
| `/itk-lotus-blossom` | Lotus Blossom |
| `/itk-bodystorming` | Bodystorming |
| `/itk-triz-prism` | TRIZ Prism |
| `/itk-prototyping` | Prototyping |
| `/itk-stormdraining` | Stormdraining |
| `/itk-trimming` | Trimming |
| `/itk-simplicity-cycle` | Simplicity Cycle |
| `/itk-retro-rundown` | Retro Rundown |
| `/itk-rose-bud-thorn` | Rose Bud Thorn |

---

## License

This repository is licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) — the same license used by the MITRE Innovation Toolkit, as required by its ShareAlike terms.

You are free to share and adapt the material for non-commercial purposes, provided you give appropriate credit to both The MITRE Corporation and this repository, and distribute any derivative works under the same license. See [LICENSE](LICENSE) for full terms.

## Source and Attribution

All tools, descriptions, and facilitation instructions are sourced from the [MITRE Innovation Toolkit](https://itk.mitre.org/toolkit/tools-at-a-glance/), published by The MITRE Corporation. Approved for Public Release; Distribution Unlimited. Case #18-1663-5.

The Key Concepts, PM Applications, Common Pitfalls, `best_for` enrichment, canvas templates, and examples in this repository were developed by Dean Peters and generated with Claude.
