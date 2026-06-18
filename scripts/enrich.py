#!/usr/bin/env python3
"""
MITRE ITK Skills Enrichment Script

Reads each SKILL.md, calls Claude API to generate richer PM-focused content,
and updates the file with best_for frontmatter and new body sections.

Usage:
    python3 scripts/enrich.py [--slug <tool-slug>] [--dry-run]
"""

import json
import re
import sys
import time
import argparse
from pathlib import Path
import anthropic

SKILLS_DIR = Path(__file__).parent.parent / "skills"

TOOLS = [
    "itk-bodystorming",
    "itk-card-sorting",
    "itk-community-map",
    "itk-culture-building-canvas",
    "itk-journey-mapping",
    "itk-lotus-blossom",
    "itk-mindmapping",
    "itk-mission-vision",
    "itk-painstorming",
    "itk-personas",
    "itk-premortem",
    "itk-problem-framing",
    "itk-prototyping",
    "itk-retro-rundown",
    "itk-rose-bud-thorn",
    "itk-service-blueprint",
    "itk-simplicity-cycle",
    "itk-stakeholder-identify",
    "itk-stakeholder-map",
    "itk-stakeholder-power",
    "itk-stakeholder-quickstart",
    "itk-stormdraining",
    "itk-storyboarding",
    "itk-system-map",
    "itk-trimming",
    "itk-triz-prism",
    "itk-value-prop",
]

ENRICH_PROMPT = """\
You are enriching a MITRE Innovation Toolkit (ITK) skill file for product managers, \
product owners, product builders, and business analysts.

Here is the current content of the skill file:

<skill>
{skill_content}
</skill>

Return a JSON object with EXACTLY these keys:

{{
  "best_for": [
    "3 to 5 short, specific scenarios (10-20 words each) naming the exact PM/product situation \
where this tool is most valuable. Examples of good specificity: \
'Early discovery when the problem space is ambiguous and stakeholders disagree on scope', \
'Sprint retrospectives to surface systemic friction before roadmap planning', \
'Preparing a stakeholder briefing that must align teams with conflicting priorities'."
  ],

  "key_concepts": [
    {{
      "term": "Concept name (1-4 words)",
      "definition": "1-2 sentence explanation of what this concept means \
and why it matters for using this tool effectively in product work."
    }}
  ],

  "pm_applications": [
    "4-6 concrete PM/product applications — specific activities a PM/PO/BA would use \
this for, naming real artifacts and ceremonies: PRD sections, OKR planning, \
discovery sprints, backlog grooming, roadmap reviews, stakeholder briefings, \
executive presentations, etc. Each item should be a full sentence describing \
a specific use case."
  ],

  "common_pitfalls": [
    "4-6 specific, actionable failure modes — what teams get wrong, \
what causes this tool to produce low-value output, and how to avoid it. \
Be direct and concrete. Avoid generic warnings like 'don't rush it' — instead \
name the specific mistake and its consequence."
  ]
}}

Requirements:
- Write for experienced practitioners — assume they know agile, PRDs, OKRs, user stories, \
Lean Startup, Jobs-to-be-Done
- Be concrete, not generic — no platitudes
- key_concepts should cover both the tool's theoretical framework AND product-specific vocabulary
- pm_applications must name real PM artifacts and activities that practitioners recognize
- common_pitfalls should name the specific mistake and its product consequence
- Return ONLY valid JSON — no markdown fences, no preamble, no explanation\
"""


def enrich_skill(client: anthropic.Anthropic, skill_content: str) -> dict:
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=2048,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": ENRICH_PROMPT.format(skill_content=skill_content)}],
    )

    text = ""
    for block in response.content:
        if block.type == "text":
            text = block.text
            break

    text = text.strip()
    # Strip markdown fences if model wraps anyway
    if text.startswith("```"):
        text = re.sub(r"^```\w*\n?", "", text)
        text = re.sub(r"\n?```$", "", text.rstrip())

    return json.loads(text)


def rebuild_skill_md(original: str, enrichment: dict) -> str:
    result = original

    # 1. Add best_for to frontmatter (before sources:)
    best_for = enrichment.get("best_for", [])
    if best_for:
        items = "\n".join(
            f'  - "{item.replace(chr(34), chr(39))}"' for item in best_for
        )
        best_for_block = f"best_for:\n{items}\n"
        result = re.sub(r"(sources:\n)", best_for_block + r"\1", result, count=1)

    # 2. Build Key Concepts section
    kc_list = enrichment.get("key_concepts", [])
    key_concepts_md = ""
    if kc_list:
        lines = ["## Key Concepts\n"]
        for kc in kc_list:
            term = kc.get("term", "").strip()
            defn = kc.get("definition", "").strip()
            if term and defn:
                lines.append(f"**{term}** — {defn}\n")
        key_concepts_md = "\n".join(lines)

    # 3. Build PM Applications section
    pm_apps = enrichment.get("pm_applications", [])
    pm_apps_md = ""
    if pm_apps:
        lines = ["## PM Applications\n"] + [f"- {app}" for app in pm_apps]
        pm_apps_md = "\n".join(lines)

    # 4. Insert Key Concepts + PM Applications before ## Benefits
    new_sections = "\n\n".join(filter(None, [key_concepts_md, pm_apps_md]))
    if new_sections:
        result = re.sub(
            r"(\n## Benefits)",
            "\n\n" + new_sections + "\n" + r"\1",
            result,
            count=1,
        )

    # 5. Replace ## Challenges with ## Common Pitfalls
    pitfalls = enrichment.get("common_pitfalls", [])
    if pitfalls:
        lines = ["## Common Pitfalls\n"] + [f"- {p}" for p in pitfalls]
        pitfalls_md = "\n".join(lines)
        result = re.sub(
            r"## Challenges\n.*?(?=\n## |\Z)",
            pitfalls_md + "\n",
            result,
            flags=re.DOTALL,
            count=1,
        )

    return result


def process_skill(client: anthropic.Anthropic, slug: str, dry_run: bool = False) -> bool:
    skill_md_path = SKILLS_DIR / slug / "SKILL.md"

    if not skill_md_path.exists():
        print(f"  SKIP — no SKILL.md found at {skill_md_path}")
        return False

    original = skill_md_path.read_text()

    if "## Key Concepts" in original:
        print(f"  SKIP — already enriched")
        return True

    print(f"  Calling Claude API (claude-opus-4-8)...")
    try:
        enrichment = enrich_skill(client, original)
    except json.JSONDecodeError as e:
        print(f"  ERROR: JSON parse failed — {e}")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

    if dry_run:
        best_for = enrichment.get("best_for", [])
        kc = enrichment.get("key_concepts", [])
        apps = enrichment.get("pm_applications", [])
        pitfalls = enrichment.get("common_pitfalls", [])
        print(
            f"  DRY RUN — best_for={len(best_for)}, key_concepts={len(kc)}, "
            f"pm_applications={len(apps)}, common_pitfalls={len(pitfalls)}"
        )
        if best_for:
            print(f"    best_for[0]: {best_for[0][:80]}")
        return True

    new_content = rebuild_skill_md(original, enrichment)
    skill_md_path.write_text(new_content)
    print(f"  Updated: skills/{slug}/SKILL.md")
    return True


def main():
    parser = argparse.ArgumentParser(description="Enrich SKILL.md files with Claude API")
    parser.add_argument("--slug", help="Process only this tool slug (e.g. value-proposition-canvas)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    args = parser.parse_args()

    client = anthropic.Anthropic()

    if args.slug:
        if args.slug not in TOOLS:
            print(f"Unknown slug: {args.slug}")
            print(f"Known slugs: {', '.join(TOOLS)}")
            sys.exit(1)
        slugs = [args.slug]
    else:
        slugs = TOOLS

    print(f"Enriching {len(slugs)} skill(s) via Claude API...")

    successes = 0
    for i, slug in enumerate(slugs, 1):
        print(f"\n[{i}/{len(slugs)}] {slug}")
        ok = process_skill(client, slug, dry_run=args.dry_run)
        if ok:
            successes += 1
        if not args.dry_run and i < len(slugs):
            time.sleep(1.0)

    print(f"\n{'='*50}")
    print(f"Done. {successes}/{len(slugs)} skills enriched.")


if __name__ == "__main__":
    main()
