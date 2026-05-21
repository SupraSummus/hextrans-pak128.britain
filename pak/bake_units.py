"""Walk the repo for per-asset bake-unit scripts.

A bake unit is a `.py` with both a `.dat` and a `.png` sibling
sharing its stem — the per-asset triple defined in CLAUDE.md ->
"Bake units and per-asset layout".  Top-level dirs like `pak/`,
`tests/`, `grounds/`, `simutranslator/` are excluded; vehicle
categories (`air/`, `trains/`, `trams/`, …) are the consumers.
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

from pak import REPO_ROOT

_SKIP_DIRS = {"pak", "tests", "grounds", "pak1file", "simutranslator",
              ".cache", "build", "__pycache__"}


def discover() -> list[Path]:
    """Per-asset bake scripts in canonical sorted order."""
    scripts: list[Path] = []
    for path in sorted(REPO_ROOT.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        rel = path.relative_to(REPO_ROOT)
        if rel.parts[0] in _SKIP_DIRS:
            continue
        stem = path.with_suffix("")
        if stem.with_suffix(".dat").exists() and stem.with_suffix(".png").exists():
            scripts.append(path)
    return scripts


def unported(category: str | None = None) -> list[Path]:
    """Upstream `.dat`s with no sibling bake script — porting candidates.

    A dat is unported iff no `.py` in its directory has a stem that
    matches the dat's stem (literal) or the dat's stem with hyphens
    turned to underscores and a leading `_` for numeric-leading names
    (the rename rule for Python-identifier-safe module names — see
    CLAUDE.md → "Importable bake scripts").

    `category` restricts to one top-level dir (`trains`, `air`, …);
    `None` walks every category.
    """
    candidates: list[Path] = []
    roots = [REPO_ROOT / category] if category else [
        p for p in REPO_ROOT.iterdir()
        if p.is_dir() and p.name not in _SKIP_DIRS and not p.name.startswith(".")
    ]
    for root in roots:
        if not root.exists():
            continue
        for dat in sorted(root.rglob("*.dat")):
            stem = dat.stem
            siblings = {p.stem for p in dat.parent.glob("*.py")}
            ported_stem = "_" + stem.replace("-", "_") if stem[:1].isdigit() \
                else stem.replace("-", "_")
            if stem in siblings or ported_stem in siblings:
                continue
            candidates.append(dat)
    return candidates


def _main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--ported", action="store_true",
                   help="list ported bake scripts (default)")
    g.add_argument("--unported", action="store_true",
                   help="list upstream dats with no sibling bake script")
    ap.add_argument("category", nargs="?",
                    help="restrict to one top-level dir (e.g. 'trains')")
    args = ap.parse_args(argv)
    paths = unported(args.category) if args.unported else discover()
    if args.category and not args.unported:
        paths = [p for p in paths if p.relative_to(REPO_ROOT).parts[0] == args.category]
    for p in paths:
        print(p.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))


def import_script(script: Path) -> ModuleType:
    """Import a bake-unit script by its repo-relative dotted path."""
    rel = script.relative_to(REPO_ROOT).with_suffix("")
    return importlib.import_module(".".join(rel.parts))


def specs_of(mod: ModuleType) -> list[Any]:
    """Bake unit's specs as a list — `SPECS` (multi-object shared
    sprite) takes precedence over `SPEC` (single-object).  Returns
    `[]` when a script declares neither (distinct-sprite multi-
    object units that don't fit either shape — see TODO.md →
    "Distinct-sprite reemit hook").
    """
    specs = getattr(mod, "SPECS", None)
    if specs is not None:
        return list(specs)
    spec = getattr(mod, "SPEC", None)
    return [spec] if spec is not None else []
