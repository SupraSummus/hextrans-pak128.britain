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
from pak._fetch import load_lock
from pak.dat import Bridge, Building
from pak.fetch_blend import SOURCE as JP_SOURCE
from pak.fetch_jh_blend import SOURCE as JH_SOURCE

_SKIP_DIRS = {"pak", "tests", "grounds", "pak1file", "simutranslator",
              ".cache", "build", "__pycache__"}


def discover(category: str | None = None) -> list[Path]:
    """Per-asset bake scripts in canonical sorted order.

    `category` restricts to one top-level dir (`trains`, `air`, …);
    `None` walks every category.
    """
    scripts: list[Path] = []
    for path in sorted(REPO_ROOT.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        rel = path.relative_to(REPO_ROOT)
        if rel.parts[0] in _SKIP_DIRS:
            continue
        if category is not None and rel.parts[0] != category:
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


def _spec_blends(spec: Any) -> list[tuple[str, str]]:
    """`(source, path)` pairs one SPEC's blend fields declare."""
    if isinstance(spec, Bridge):
        return [("jh", p) for p in (spec.blend_image, spec.blend_start,
                                    spec.blend_ramp, spec.blend_pillar)
                if p is not None]
    source = getattr(spec, "blend_source", "jp")
    out = [(source, spec.blend)] if spec.blend is not None else []
    if isinstance(spec, Building) and spec.blend_winter is not None:
        out.append((source, spec.blend_winter))
    return out


def referenced_blends() -> set[tuple[str, str]]:
    """`(source, blend)` pairs every ported SPEC declares."""
    return {ref for script in discover()
            for spec in specs_of(import_script(script))
            for ref in _spec_blends(spec)}


def unused_blends() -> list[tuple[str, str]]:
    """Lock-file `.blend` entries no ported SPEC references.

    Either stale (script removed without trimming the lock) or
    in-flight (blend fetched ahead of its SPEC).  Locks also carry
    texture / script paths whose consumers are runtime (e.g.
    `pak.render._reload_external_textures`) and can't be statically
    derived — those are filtered out here, not reported as unused.
    """
    locked: set[tuple[str, str]] = set()
    for tag, src in (("jp", JP_SOURCE), ("jh", JH_SOURCE)):
        _, files = load_lock(src)
        locked.update((tag, p) for p in files if p.endswith(".blend"))
    return sorted(locked - referenced_blends())


def _main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--ported", action="store_true",
                   help="list ported bake scripts (default)")
    g.add_argument("--unported", action="store_true",
                   help="list upstream dats with no sibling bake script")
    g.add_argument("--unused-blends", action="store_true",
                   help="list lock-file blends no ported SPEC references")
    ap.add_argument("category", nargs="?",
                    help="restrict to one top-level dir (e.g. 'trains')")
    args = ap.parse_args(argv)
    if args.unused_blends:
        for source, path in unused_blends():
            if args.category and not path.lower().startswith(args.category.lower() + "/"):
                continue
            print(f"{source}:{path}")
        return 0
    paths = unported(args.category) if args.unported else discover(args.category)
    for p in paths:
        print(p.relative_to(REPO_ROOT))
    return 0


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


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
