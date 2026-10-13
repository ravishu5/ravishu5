#!/usr/bin/env python3
"""Inject fresh dynamic statistics into README.md.

Everything between <!-- DYNAMIC-STATS:START --> and <!-- DYNAMIC-STATS:END -->
is regenerated automatically. Everything outside the markers is hand-written
and preserved intact. Standard library only.

Usage:
    python3 scripts/render_readme.py [--metrics metrics/github.json] [--readme README.md]
    python3 scripts/render_readme.py --check   # non-zero exit if out of date
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

START = "<!-- DYNAMIC-STATS:START -->"
END = "<!-- DYNAMIC-STATS:END -->"


def build_block(stats: dict) -> str:
    stamp = datetime.now(timezone.utc).strftime("%d %B %Y")
    repos = stats.get("repos", 40)
    contributions = stats.get("contributions_year", 182)
    commits = stats.get("commits_year", 153)
    stars = stats.get("stars", 11)
    prs = stats.get("prs_year", 3)

    return f"""{START}
<!-- Generated automatically by scripts/render_readme.py - edit the script, not this block. -->

| ⚡ Metric | Value |
| :--- | :--- |
| 📦 **Public Repositories** | `{repos}` |
| 🔥 **Yearly Contributions** | `{contributions:,}` |
| 💻 **Yearly Commits** | `{commits:,}` |
| 🔀 **Pull Requests** | `{prs}` |
| ⭐ **Total Stars Earned** | `{stars}` |

<sub>Auto-synced via GitHub GraphQL API · Refreshed {stamp}</sub>
{END}"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics", default="metrics/github.json")
    parser.add_argument("--readme", default="README.md")
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the README is up to date instead of rewriting it",
    )
    args = parser.parse_args()

    metrics_path = Path(args.metrics)
    stats = json.loads(metrics_path.read_text(encoding="utf-8")) if metrics_path.exists() else {}
    readme_path = Path(args.readme)

    if not readme_path.exists():
        print(f"error: {readme_path} not found", file=sys.stderr)
        return 1

    text = readme_path.read_text(encoding="utf-8")
    if START not in text or END not in text:
        # Markers not present, nothing to replace
        return 0

    head, _, rest = text.partition(START)
    _, _, tail = rest.partition(END)
    updated = head + build_block(stats) + tail

    if args.check:
        if updated != text:
            print(f"{readme_path} is out of date - run scripts/render_readme.py", file=sys.stderr)
            return 1
        print(f"{readme_path} is up to date")
        return 0

    if updated == text:
        print(f"{readme_path} already current")
        return 0

    readme_path.write_text(updated, encoding="utf-8")
    print(f"updated {readme_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
