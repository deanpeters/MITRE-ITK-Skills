"""
Generate per-skill zip files in dist/zips/.

Each zip (itk-<slug>.zip) bundles:
  - SKILL.md
  - template.md          (if present)
  - examples/sample.md   (if present)
  - assets/              (all files)
  - itk-<alias>.md       (matching claude-skills invocation file)

Usage:
  python3 scripts/generate-zips.py                  # all 27 skills
  python3 scripts/generate-zips.py --slug premortem  # one skill
  python3 scripts/generate-zips.py --dry-run         # preview without writing
"""

import argparse
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
OUTPUT_DIR = REPO_ROOT / "dist" / "zips"


def find_claude_skill(skill_dir: Path) -> Path | None:
    """Find the itk-*.md file inside the skill directory."""
    matches = list(skill_dir.glob("itk-*.md"))
    return matches[0] if matches else None


def zip_skill(slug: str, dry_run: bool = False) -> bool:
    skill_dir = SKILLS_DIR / slug
    if not skill_dir.is_dir():
        print(f"  SKIP  {slug} — directory not found")
        return False

    claude_skill = find_claude_skill(skill_dir)

    zip_path = OUTPUT_DIR / f"itk-{slug}.zip"
    entries: list[tuple[Path, str]] = []  # (src_path, arcname)

    # Required: SKILL.md
    entries.append((skill_dir / "SKILL.md", "SKILL.md"))

    # Optional: template.md
    if (skill_dir / "template.md").exists():
        entries.append((skill_dir / "template.md", "template.md"))

    # Optional: examples/sample.md
    if (skill_dir / "examples" / "sample.md").exists():
        entries.append((skill_dir / "examples" / "sample.md", "examples/sample.md"))

    # Optional: assets/
    assets_dir = skill_dir / "assets"
    if assets_dir.is_dir():
        for asset in sorted(assets_dir.iterdir()):
            if asset.is_file():
                entries.append((asset, f"assets/{asset.name}"))

    # Optional: claude-skills invocation file
    if claude_skill:
        entries.append((claude_skill, claude_skill.name))
    else:
        print(f"  WARN  {slug} — no matching claude-skills file found")

    if dry_run:
        print(f"  DRY   {zip_path.relative_to(REPO_ROOT)}")
        for src, arc in entries:
            print(f"          {arc}  ← {src.relative_to(REPO_ROOT)}")
        return True

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for src, arc in entries:
            zf.write(src, arc)

    size_kb = zip_path.stat().st_size // 1024
    print(f"  OK    {zip_path.relative_to(REPO_ROOT)}  ({size_kb} KB, {len(entries)} files)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate per-skill zip files")
    parser.add_argument("--slug", help="Generate zip for one skill only")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    if args.slug:
        slugs = [args.slug]
    else:
        slugs = sorted(d.name for d in SKILLS_DIR.iterdir() if d.is_dir())

    print(f"Generating {len(slugs)} zip(s)  [dry-run={args.dry_run}]")
    ok = sum(zip_skill(slug, dry_run=args.dry_run) for slug in slugs)
    print(f"Done — {ok}/{len(slugs)} generated")


if __name__ == "__main__":
    main()
