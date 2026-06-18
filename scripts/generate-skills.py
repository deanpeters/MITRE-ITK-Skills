#!/usr/bin/env python3
"""
Generate itk-<alias>.md Claude Code skill files inside each skills/<slug>/ directory.

Each file is a Claude Code skill — instructional content Claude loads when
the user invokes /itk-<alias>. Content is derived from SKILL.md frontmatter
and Key Concepts sections.

Usage:
    python3 scripts/generate-skills.py [--slug <slug>] [--dry-run]
"""

import re
import sys
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SKILLS_DIR = BASE_DIR / "skills"

TOOLS = [
    "bodystorming",
    "card-sorting",
    "community-map",
    "culture-building-canvas",
    "journey-mapping",
    "lotus-blossom",
    "mindmapping",
    "mission-and-vision-canvas",
    "painstorming",
    "personas",
    "premortem",
    "problem-framing",
    "prototyping",
    "quickstart-stakeholder-engagement-canvas",
    "retro-rundown",
    "rose-bud-thorn",
    "service-blueprint",
    "simplicity-cycle",
    "stakeholder-identification-canvas",
    "stakeholder-map-and-matrix",
    "stakeholder-power-categories",
    "stormdraining",
    "storyboarding",
    "system-map",
    "trimming",
    "triz-prism",
    "value-proposition-canvas",
]

# Slugs that get shorter aliases for slash-command ergonomics
SLUG_ALIASES = {
    "quickstart-stakeholder-engagement-canvas": "stakeholder-quickstart",
    "stakeholder-identification-canvas": "stakeholder-identify",
    "stakeholder-map-and-matrix": "stakeholder-map",
    "mission-and-vision-canvas": "mission-vision",
    "value-proposition-canvas": "value-prop",
    "stakeholder-power-categories": "stakeholder-power",
}


def skill_alias(slug):
    return SLUG_ALIASES.get(slug, slug)


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}

    fm = {}
    current_list = None
    last_key = None

    for line in m.group(1).splitlines():
        if line.startswith("  - "):
            if current_list is not None:
                item = line[4:].strip().strip('"')
                if item:
                    current_list.append(item)
        elif line.startswith("  ") and not line.startswith("  -"):
            # Block scalar continuation — fold into previous string value
            if last_key and isinstance(fm.get(last_key), str):
                fm[last_key] = fm[last_key] + " " + line.strip()
        elif ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"')
            current_list = None
            last_key = key
            if val:
                fm[key] = val
            else:
                current_list = []
                fm[key] = current_list

    return fm


def extract_section(body, heading):
    pattern = rf"## {re.escape(heading)}\n\n(.*?)(?=\n## |\Z)"
    m = re.search(pattern, body, re.DOTALL)
    return m.group(1).strip() if m else ""


def extract_title(body):
    m = re.search(r"^# (.+)$", body, re.MULTILINE)
    return m.group(1).strip() if m else ""


def generate_skill_file(slug):
    text = (SKILLS_DIR / slug / "SKILL.md").read_text()

    fm = parse_frontmatter(text)
    body_start = re.match(r"^---\n.*?\n---\n?", text, re.DOTALL)
    body = text[body_start.end():] if body_start else text

    title = extract_title(body) or slug.replace("-", " ").title()
    description = fm.get("description", "")
    phase = fm.get("phase", "").upper()
    difficulty = fm.get("difficulty", "").capitalize()
    group_size = fm.get("group_size", "")
    time_required = fm.get("time_required", "")

    best_for = fm.get("best_for", [])
    if isinstance(best_for, str):
        best_for = [best_for]

    key_concepts_text = extract_section(body, "Key Concepts")
    common_pitfalls_text = extract_section(body, "Common Pitfalls")

    best_for_md = (
        "\n".join(f"- {item}" for item in best_for)
        if best_for
        else "_See full skill reference._"
    )
    kc_md = key_concepts_text or "_See full skill reference._"
    pitfalls_md = common_pitfalls_text or "_See full skill reference._"

    alias = skill_alias(slug)

    return f"""\
# ITK: {title}

Help a product practitioner apply **{title}** from the MITRE Innovation Toolkit.

**Phase:** {phase} · **Difficulty:** {difficulty} · **Group:** {group_size} · **Time:** {time_required}

> {description}

---

## When This Tool Fits Best

{best_for_md}

---

## Key Concepts

{kc_md}

---

## Common Pitfalls to Watch For

{pitfalls_md}

---

## How to Help

- **Read context first.** Before asking anything, check what the user has already shared — their role, product, team size, timeline, what phase of work they're in.
- **Experienced users can skip straight to the work.** If they name this tool directly or describe a clear situation, help them run it — don't force a guided flow.
- **Use the Adaptive Decision Ladder when the situation is unclear.** Offer numbered options; the user can reply `2`, `1 & 3`, or describe freely. Skip steps that context already resolves.
- **Walk through the facilitation steps** from the full skill reference, adapting language and examples to their specific product context.
- **Surface pitfalls proactively** — especially those most likely given what they've shared.
- **Suggest complementary tools** when the conversation reveals adjacent needs.
- **Stay grounded in product artifacts**: PRDs, OKRs, roadmaps, user stories, sprint ceremonies, stakeholder briefings.

## Full Reference

→ [`skills/{slug}/SKILL.md`](../skills/{slug}/SKILL.md)
"""


def process_slug(slug, dry_run=False):
    skill_md_path = SKILLS_DIR / slug / "SKILL.md"
    if not skill_md_path.exists():
        print(f"  SKIP — no SKILL.md at {skill_md_path}")
        return False

    alias = skill_alias(slug)
    out_path = SKILLS_DIR / slug / f"itk-{alias}.md"

    if dry_run:
        print(f"  DRY RUN → skills/{slug}/itk-{alias}.md")
        return True

    content = generate_skill_file(slug)
    out_path.write_text(content)
    print(f"  → skills/{slug}/itk-{alias}.md")
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate itk-*.md skill files inside skills/<slug>/")
    parser.add_argument("--slug", help="Process only this tool slug")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.slug and args.slug not in TOOLS:
        print(f"Unknown slug: {args.slug}")
        print(f"Known slugs: {', '.join(TOOLS)}")
        sys.exit(1)

    slugs = [args.slug] if args.slug else TOOLS
    print(f"Generating {len(slugs)} skill file(s) into skills/<slug>/...")

    successes = 0
    for slug in slugs:
        print(f"  {slug}")
        if process_slug(slug, dry_run=args.dry_run):
            successes += 1

    print(f"\nDone. {successes}/{len(slugs)} skill files written")


if __name__ == "__main__":
    main()
