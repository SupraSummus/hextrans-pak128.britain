"""Walk the repo for per-asset bake-unit scripts.

A bake unit is a `.py` with both a `.dat` and a `.png` sibling
sharing its stem — the per-asset triple defined in CLAUDE.md ->
"Bake units and per-asset layout".  Top-level dirs like `pak/`,
`tests/`, `grounds/`, `simutranslator/` are excluded; vehicle
categories (`air/`, `trains/`, `trams/`, …) are the consumers.
"""

from __future__ import annotations

import importlib
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
