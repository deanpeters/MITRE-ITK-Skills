#!/usr/bin/env python3
"""
MITRE ITK Skills Scraper

Fetches each tool page from the MITRE Innovation Toolkit, downloads PDFs/PPTXs,
and generates SKILL.md files modeled on the Product Manager Skills library structure.

Usage:
    python3 scripts/scrape.py [--dry-run] [--slug <tool-slug>]
"""

import re
import sys
import time
import argparse
import requests
from pathlib import Path

from scrapling.fetchers import Fetcher

BASE_URL = "https://itk.mitre.org"

TOOLS = [
    # (alias, itk-phase)
    # SCOPE
    ("itk-community-map", "scope"),
    ("itk-culture-building-canvas", "scope"),
    ("itk-stakeholder-identify", "scope"),
    ("itk-stakeholder-map", "scope"),
    ("itk-system-map", "scope"),
    ("itk-stakeholder-quickstart", "scope"),
    ("itk-stakeholder-power", "scope"),
    # DEFINE
    ("itk-mission-vision", "define"),
    ("itk-premortem", "define"),
    ("itk-problem-framing", "define"),
    # UNDERSTAND
    ("itk-card-sorting", "understand"),
    ("itk-journey-mapping", "understand"),
    ("itk-painstorming", "understand"),
    ("itk-personas", "understand"),
    ("itk-service-blueprint", "understand"),
    ("itk-storyboarding", "understand"),
    ("itk-value-prop", "understand"),
    # GENERATE
    ("itk-bodystorming", "generate"),
    ("itk-lotus-blossom", "generate"),
    ("itk-mindmapping", "generate"),
    ("itk-triz-prism", "generate"),
    # EVALUATE
    ("itk-prototyping", "evaluate"),
    ("itk-retro-rundown", "evaluate"),
    ("itk-rose-bud-thorn", "evaluate"),
    ("itk-simplicity-cycle", "evaluate"),
    ("itk-stormdraining", "evaluate"),
    ("itk-trimming", "evaluate"),
]


def block_text(element):
    return element.get_all_text(separator=" ", ignore_tags=("script", "style")).strip()


def clean(text):
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def strip_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):].strip()
    return text


def parse_tool_page(slug, phase):
    url = f"{BASE_URL}/toolkit-tools/{slug}/"
    print(f"  Fetching: {url}")

    page = Fetcher.get(url)

    blocks = [
        clean(block_text(b))
        for b in page.css(".et_pb_text_inner")
        if block_text(b).strip()
    ]

    pdf_links = [
        l.attrib.get("href", "")
        for l in page.css("a")
        if l.attrib.get("href", "").lower().endswith(".pdf")
    ]
    pptx_links = [
        l.attrib.get("href", "")
        for l in page.css("a")
        if l.attrib.get("href", "").lower().endswith(".pptx")
    ]

    data = {
        "slug": slug,
        "phase": phase,
        "name": "",
        "what_is_it": "",
        "why_use_it": "",
        "when_to_use_it": "",
        "level": "",
        "outcome": "",
        "group_size": "",
        "suggested_time": "",
        "steps": [],
        "benefits": [],
        "challenges": [],
        "combine_with": "",
        "pdf_url": pdf_links[0] if pdf_links else "",
        "pptx_url": pptx_links[0] if pptx_links else "",
    }

    for i, text in enumerate(blocks):
        if i == 0:
            data["name"] = text
        elif text.startswith("What is it"):
            data["what_is_it"] = strip_prefix(text, "What is it")
        elif text.startswith("Why use it"):
            data["why_use_it"] = strip_prefix(text, "Why use it")
        elif text.startswith("When to use it"):
            data["when_to_use_it"] = strip_prefix(text, "When to use it")
        elif text.startswith("Level"):
            data["level"] = strip_prefix(text, "Level")
        elif text.startswith("Outcome"):
            data["outcome"] = strip_prefix(text, "Outcome")
        elif text.startswith("Group Size"):
            data["group_size"] = strip_prefix(text, "Group Size")
        elif text.startswith("Suggested Time"):
            data["suggested_time"] = strip_prefix(text, "Suggested Time")
        elif re.match(r"^STEP \d+", text):
            # "STEP 1 Do this thing" → numbered step
            step_body = re.sub(r"^STEP \d+\s*", "", text)
            data["steps"].append(step_body)
        elif text.startswith("Benefits"):
            raw = strip_prefix(text, "Benefits")
            data["benefits"] = [s.strip() for s in raw.split("  ") if s.strip()]
        elif text.startswith("Challenges"):
            raw = strip_prefix(text, "Challenges")
            data["challenges"] = [s.strip() for s in raw.split("  ") if s.strip()]
        elif text.startswith("Combine With"):
            data["combine_with"] = strip_prefix(text, "Combine With")

    return data


def download_file(url, dest_path):
    if not url:
        return False
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        dest_path.write_bytes(r.content)
        print(f"    Downloaded: {dest_path.name} ({len(r.content) // 1024}KB)")
        return True
    except Exception as e:
        print(f"    Failed to download {url}: {e}")
        return False


def asset_filename(url):
    return url.split("/")[-1] if url else ""


def generate_skill_md(data):
    name = data["name"] or data["slug"].replace("-", " ").title()

    steps_md = ""
    if data["steps"]:
        steps_md = "\n".join(f"{i+1}. {s}" for i, s in enumerate(data["steps"]))
    else:
        steps_md = "_See tool page for step-by-step instructions._"

    benefits_md = (
        "\n".join(f"- {b}" for b in data["benefits"])
        if data["benefits"]
        else "_See tool page._"
    )
    challenges_md = (
        "\n".join(f"- {c}" for c in data["challenges"])
        if data["challenges"]
        else "_See tool page._"
    )

    assets_lines = []
    if data["pdf_url"]:
        assets_lines.append(f"- PDF: [Download](assets/{asset_filename(data['pdf_url'])})")
    if data["pptx_url"]:
        assets_lines.append(
            f"- PPTX Template: [Download](assets/{asset_filename(data['pptx_url'])})"
        )
    assets_md = "\n".join(assets_lines) if assets_lines else "- None"

    combine_with_section = ""
    if data["combine_with"]:
        combine_with_section = f"\n## Combine With\n\n{data['combine_with']}\n"

    description = data["what_is_it"] or f"{name} — a MITRE ITK innovation tool."
    intent = data["why_use_it"] or ""

    return f"""---
name: {data['slug']}
description: {description}
intent: {intent}
type: component
phase: {data['phase']}
outcome: {data['outcome'].lower() if data['outcome'] else data['phase']}
difficulty: {data['level'].lower() if data['level'] else 'beginner'}
group_size: {data['group_size'] or 'varies'}
time_required: {data['suggested_time'] or 'varies'}
sources:
  - MITRE Innovation Toolkit (ITK)
  - "{BASE_URL}/toolkit-tools/{data['slug']}/"
---

# {name}

## What Is It

{data['what_is_it'] or '_See tool page for description._'}

## Why Use It

{data['why_use_it'] or '_See tool page for rationale._'}

## When to Use It

{data['when_to_use_it'] or '_See tool page for timing guidance._'}

## How to Do It

{steps_md}

## Benefits

{benefits_md}

## Challenges

{challenges_md}
{combine_with_section}
## Assets

{assets_md}

## Metadata

| Field | Value |
|-------|-------|
| ITK Phase | {data['phase'].upper()} |
| Difficulty | {data['level'] or 'N/A'} |
| Group Size | {data['group_size'] or 'N/A'} |
| Time Required | {data['suggested_time'] or 'N/A'} |
| Source | [itk.mitre.org]({BASE_URL}/toolkit-tools/{data['slug']}/) |
"""


def process_tool(slug, phase, skills_dir, dry_run=False):
    print(f"\n{'─'*50}")
    print(f"Tool: {slug}  [{phase.upper()}]")

    try:
        data = parse_tool_page(slug, phase)
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

    if dry_run:
        print(f"  DRY RUN — would create skills/{slug}/SKILL.md")
        if data["pdf_url"]:
            print(f"  DRY RUN — would download {data['pdf_url']}")
        if data["pptx_url"]:
            print(f"  DRY RUN — would download {data['pptx_url']}")
        return True

    skill_dir = skills_dir / slug
    assets_dir = skill_dir / "assets"
    skill_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(exist_ok=True)

    if data["pdf_url"]:
        download_file(data["pdf_url"], assets_dir / asset_filename(data["pdf_url"]))
    if data["pptx_url"]:
        download_file(data["pptx_url"], assets_dir / asset_filename(data["pptx_url"]))

    skill_content = generate_skill_md(data)
    (skill_dir / "SKILL.md").write_text(skill_content)
    print(f"    Created: skills/{slug}/SKILL.md")

    return True


def main():
    parser = argparse.ArgumentParser(description="Scrape MITRE ITK tools into SKILL.md files")
    parser.add_argument("--dry-run", action="store_true", help="Print what would happen without writing files")
    parser.add_argument("--slug", help="Process only this tool slug (e.g. community-map)")
    args = parser.parse_args()

    scripts_dir = Path(__file__).parent
    base_dir = scripts_dir.parent
    skills_dir = base_dir / "skills"

    tools_to_process = TOOLS
    if args.slug:
        tools_to_process = [(s, p) for s, p in TOOLS if s == args.slug]
        if not tools_to_process:
            print(f"Unknown slug: {args.slug}")
            sys.exit(1)

    print(f"Processing {len(tools_to_process)} tool(s)...")

    successes = 0
    for slug, phase in tools_to_process:
        ok = process_tool(slug, phase, skills_dir, dry_run=args.dry_run)
        if ok:
            successes += 1
        if not args.dry_run:
            time.sleep(0.75)  # polite crawl rate

    print(f"\n{'='*50}")
    print(f"Done. {successes}/{len(tools_to_process)} tools processed.")
    if not args.dry_run:
        print(f"Skills written to: {skills_dir}")


if __name__ == "__main__":
    main()
