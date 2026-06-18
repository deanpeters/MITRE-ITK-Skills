#!/usr/bin/env python3
"""
Generate skills/<slug>/template.md for each MITRE ITK tool.

Each template mirrors the actual canvas or worksheet structure of the tool,
with [placeholder] syntax, markdown tables for grid/matrix layouts, and
headers for section-based areas. Follows the pattern in Product Manager Skills.

Usage:
    python3 scripts/generate-templates.py [--slug <slug>] [--dry-run]
"""

import re
import sys
import time
import argparse
from pathlib import Path
import anthropic

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

TEMPLATE_PROMPT = """\
You are creating a markdown template for a MITRE Innovation Toolkit (ITK) skill used by \
product managers, product owners, and business analysts.

Here is the full skill documentation:

<skill>
{skill_content}
</skill>

Create a practical, fillable markdown template that mirrors the actual canvas or worksheet \
structure of this tool. Requirements:

- Use [placeholder text] syntax for every field a practitioner fills in
- Use markdown tables (| col | col |) for any grid, matrix, 2x2, or multi-column structure \
in the original canvas
- Use ## headers and bullet lists for section-based or free-form areas
- Match the real sections and structure described in the How to Do It steps — if the tool \
has named zones or quadrants, reproduce them
- For tools with numbered steps (like Premortem), structure the template around those steps \
as ## sections
- Include a "## Session Info" block at the top with: Date, Facilitator, Team/Project, \
Time Box fields
- Be immediately usable in a note-taking app, Notion, or pasted into a Claude session
- Do NOT wrap the template in a markdown code fence — return the template content directly

Return ONLY the complete template.md file in this exact format:

# [Tool Name] Template

[One sentence: what situation this template is for and what it produces.]

---

[the full template content starting with ## Session Info]
"""


def generate_template(client: anthropic.Anthropic, skill_content: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=2048,
        thinking={"type": "adaptive"},
        messages=[{
            "role": "user",
            "content": TEMPLATE_PROMPT.format(skill_content=skill_content)
        }],
    )
    for block in response.content:
        if block.type == "text":
            return block.text.strip()
    return ""


def add_template_link_to_skill_md(skill_md_path: Path) -> None:
    """Insert a template.md link into the ## Assets section if not already present."""
    text = skill_md_path.read_text()
    if "template.md" in text:
        return
    # Insert after the last existing asset line, before the blank line that follows Assets
    text = re.sub(
        r"(- PPTX Template: \[Download\]\(assets/[^\)]+\))",
        r"\1\n- Markdown Template: [template.md](template.md)",
        text,
        count=1,
    )
    skill_md_path.write_text(text)


def process_slug(client: anthropic.Anthropic, slug: str, dry_run: bool = False) -> bool:
    skill_dir = SKILLS_DIR / slug
    skill_md_path = skill_dir / "SKILL.md"
    template_path = skill_dir / "template.md"

    if not skill_md_path.exists():
        print(f"  SKIP — no SKILL.md")
        return False

    if template_path.exists():
        print(f"  SKIP — template.md already exists")
        return True

    skill_content = skill_md_path.read_text()

    print(f"  Calling Claude API...")
    try:
        template_content = generate_template(client, skill_content)
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

    if dry_run:
        preview = template_content[:120].replace("\n", " ")
        print(f"  DRY RUN → skills/{slug}/template.md")
        print(f"    Preview: {preview}...")
        return True

    template_path.write_text(template_content + "\n")
    add_template_link_to_skill_md(skill_md_path)
    print(f"  → skills/{slug}/template.md")
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate template.md files for ITK skills")
    parser.add_argument("--slug", help="Process only this tool slug")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.slug and args.slug not in TOOLS:
        print(f"Unknown slug: {args.slug}")
        sys.exit(1)

    client = anthropic.Anthropic()
    slugs = [args.slug] if args.slug else TOOLS

    print(f"Generating {len(slugs)} template(s) via Claude API...")

    successes = 0
    for i, slug in enumerate(slugs, 1):
        print(f"\n[{i}/{len(slugs)}] {slug}")
        if process_slug(client, slug, dry_run=args.dry_run):
            successes += 1
        if not args.dry_run and i < len(slugs):
            time.sleep(1.0)

    print(f"\n{'='*50}")
    print(f"Done. {successes}/{len(slugs)} templates generated.")


if __name__ == "__main__":
    main()
