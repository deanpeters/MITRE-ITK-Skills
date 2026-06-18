#!/usr/bin/env python3
"""Generate catalog/INDEX.md from all SKILL.md files."""

import re
from pathlib import Path

PHASES = ["scope", "define", "understand", "generate", "evaluate"]

PHASE_DESCRIPTIONS = {
    "scope": "Get clarity and consensus about the problem space, stakeholders, and broader context.",
    "define": "Clarify and prioritize the key problems and hypotheses you want to explore.",
    "understand": "Explore the problem you've defined and gain user insights.",
    "generate": "Brainstorm and create solutions that help address the problems.",
    "evaluate": "Test or evaluate different solutions and iterate on them.",
}


def read_frontmatter(skill_md_path):
    text = skill_md_path.read_text()
    fm = {}
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                fm[k.strip()] = v.strip()
    return fm


def main():
    base_dir = Path(__file__).parent.parent
    skills_dir = base_dir / "skills"
    catalog_dir = base_dir / "catalog"
    catalog_dir.mkdir(exist_ok=True)

    by_phase = {p: [] for p in PHASES}

    for skill_dir in sorted(skills_dir.iterdir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        fm = read_frontmatter(skill_md)
        phase = fm.get("phase", "").strip('"').lower()
        if phase not in by_phase:
            phase = "scope"
        by_phase[phase].append({
            "slug": skill_dir.name,
            "description": fm.get("description", "").strip('"'),
            "difficulty": fm.get("difficulty", "").strip('"'),
            "group_size": fm.get("group_size", "").strip('"'),
            "time_required": fm.get("time_required", "").strip('"'),
        })

    lines = ["# MITRE ITK Skills — Catalog\n"]
    lines.append("27 tools across 5 innovation phases, sourced from the [MITRE Innovation Toolkit](https://itk.mitre.org/toolkit/tools-at-a-glance/).\n")

    total = sum(len(v) for v in by_phase.values())
    lines.append(f"**Total skills:** {total}\n")

    for phase in PHASES:
        tools = by_phase[phase]
        lines.append(f"\n## {phase.upper()} ({len(tools)} tools)\n")
        lines.append(f"_{PHASE_DESCRIPTIONS[phase]}_\n")
        for t in tools:
            link = f"../skills/{t['slug']}/SKILL.md"
            meta = " · ".join(filter(None, [t["difficulty"], t["group_size"], t["time_required"]]))
            display = t['slug'].removeprefix('itk-').replace('-', ' ').title()
            lines.append(f"- [{display}]({link}) — {t['description']}" + (f" _{meta}_" if meta else ""))

    index_path = catalog_dir / "INDEX.md"
    index_path.write_text("\n".join(lines) + "\n")
    print(f"Catalog written to {index_path}")


if __name__ == "__main__":
    main()
