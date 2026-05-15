"""Walk the repo for per-asset bake-unit scripts.

A bake unit is a `.py` with both a `.dat` and a `.png` sibling
sharing its stem — the per-asset triple defined in CLAUDE.md ->
"Bake units and per-asset layout".  Top-level dirs like `tools/`,
`tests/`, `grounds/`, `simutranslator/` are excluded; vehicle
categories (`air/`, `trains/`, `trams/`, …) are the consumers.
"""

from __future__ import annotations

import importlib
from pathlib import Path
from types import ModuleType


_REPO = Path(__file__).resolve().parents[2]
_SKIP_DIRS = {"tools", "tests", "grounds", "simutranslator", ".cache",
              "build", "__pycache__"}


def discover() -> list[Path]:
    """Per-asset bake scripts in canonical sorted order."""
    scripts: list[Path] = []
    for path in sorted(_REPO.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        rel = path.relative_to(_REPO)
        if rel.parts[0] in _SKIP_DIRS:
            continue
        stem = path.with_suffix("")
        if stem.with_suffix(".dat").exists() and stem.with_suffix(".png").exists():
            scripts.append(path)
    return scripts


def import_script(script: Path) -> ModuleType:
    """Import a bake-unit script by its repo-relative dotted path."""
    rel = script.relative_to(_REPO).with_suffix("")
    return importlib.import_module(".".join(rel.parts))
