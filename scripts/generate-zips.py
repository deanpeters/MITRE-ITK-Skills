"""
Generate per-skill zip files in dist/zips/.

Each zip (<alias>.zip) bundles:
  - SKILL.md
  - template.md          (if present)
  - examples/sample.md   (if present)
  - assets/              (all files)

Usage:
  python3 scripts/generate-zips.py                       # all 27 skills
  python3 scripts/generate-zips.py --slug itk-premortem  # one skill
  python3 scripts/generate-zips.py --dry-run             # preview without writing
"""

import argparse
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
OUTPUT_DIR = REPO_ROOT / "dist" / "zips"


def zip_skill(alias: str, dry_run: bool = False) -> bool:
    skill_dir = SKILLS_DIR / alias
    if not skill_dir.is_dir():
        print(f"  SKIP  {alias} — directory not found")
        return False

    zip_path = OUTPUT_DIR / f"{alias}.zip"
    entries: list[tuple[Path, str]] = []

    entries.append((skill_dir / "SKILL.md", "SKILL.md"))

    if (skill_dir / "template.md").exists():
        entries.append((skill_dir / "template.md", "template.md"))

    if (skill_dir / "examples" / "sample.md").exists():
        entries.append((skill_dir / "examples" / "sample.md", "examples/sample.md"))

    assets_dir = skill_dir / "assets"
    if assets_dir.is_dir():
        for asset in sorted(assets_dir.iterdir()):
            if asset.is_file():
                entries.append((asset, f"assets/{asset.name}"))

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
    parser.add_argument("--slug", help="Generate zip for one skill only (e.g. itk-premortem)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    if args.slug:
        aliases = [args.slug]
    else:
        aliases = sorted(d.name for d in SKILLS_DIR.iterdir() if d.is_dir() and d.name.startswith("itk-"))

    print(f"Generating {len(aliases)} zip(s)  [dry-run={args.dry_run}]")
    ok = sum(zip_skill(alias, dry_run=args.dry_run) for alias in aliases)
    print(f"Done — {ok}/{len(aliases)} generated")


if __name__ == "__main__":
    main()
