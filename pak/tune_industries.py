"""Per-industry colour + lighting calibration.

Industries (`industry/*.py`) ship as a list `SPECS = [Factory(...), ...]`
sharing one blend, and most landed with no `materials=` / `lighting=`
set on their SPECs.  This driver seeds image-form `MATERIALS` from the
blend (collapsing `pak.extract_materials`' slot output to the heuristic
`image × diffuse` path that the gradient solver can move via `color=`),
runs `pak.tune_materials.tune`, and writes the result back into the
script between marker comments.

Two operating modes:

* per-script tune: `--all` or a script path runs the solver and (with
  `--apply`) writes `MATERIALS` + `LIGHTING` back into the bake script.
* `--lighting-sweep --on a.py,b.py,...` evaluates a small `Lighting`
  grid across N scripts and prints a table.  Used once to pick the
  catalog-wide lighting; the chosen value goes into `--lighting=...`
  on a subsequent `--apply` run.

After `--apply`, regenerate the committed PNG with
`python3 -m industry.<name>` -- the bake driver re-runs Cycles via the
hex viewpoint and the freshly tuned `MATERIALS` / `LIGHTING` flow
through the SPEC.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from pak import REPO_ROOT
from pak.bake_units import discover, import_script, specs_of
from pak.dat import Factory
from pak.extract_materials import materials_from_blend
from pak.fetch_blend import fetch as fetch_blend
from pak.materials import Lighting, Material, _non_default_items
from pak.tune_materials import tune


def _seed_material(m: Material) -> Material | None:
    """Collapse a slot-form Material to the heuristic `image=` /
    `noise=` form with `color=` set so the gradient solver can move it.

    `pak.tune_materials` only moves `color=`-bearing materials -- adding
    `color=` to a slot-stack material does nothing because the first
    Mix-fac=1 slot overrides the base.  Image slots become
    `image=...` plus `color=(1,1,1)` (multiply path); procedural slots
    become `noise=True` plus a `color=` seeded from the slot's BI MTex
    RGB.  Materials without slots pass through unchanged."""
    if m.slots is None:
        return m
    if not m.slots:
        return None
    s = m.slots[0]
    if s.image is not None:
        return Material(
            image=s.image, texco=s.texco, size=s.size, ofs=s.ofs,
            color=(1.0, 1.0, 1.0),
        )
    if s.procedural in ("CLOUDS", "NOISE", "MUSGRAVE"):
        return Material(noise=True, color=s.color)
    return None


def seed_materials(blend_relpath: str) -> dict[str, Material]:
    raw = materials_from_blend(fetch_blend(blend_relpath))
    return {n: c for n, m in raw.items() if (c := _seed_material(m)) is not None}


def _format_block(materials: dict[str, Material],
                  lighting: Lighting | None) -> str:
    lines = ["# AUTO-TUNED: pak.tune_industries", "MATERIALS = {"]
    for name, m in materials.items():
        parts = []
        for k, v in _non_default_items(m):
            if k == "color" and v is not None:
                v = tuple(round(c, 3) for c in v)
            parts.append(f"{k}={v!r}")
        lines.append(f"    {name!r}: Material({', '.join(parts)}),")
    lines.append("}")
    if lighting is not None:
        kw = ", ".join(f"{k}={v!r}" for k, v in lighting.to_jsonable().items())
        lines.extend(["", f"LIGHTING = Lighting({kw})"])
    lines.append("# END AUTO-TUNED")
    return "\n".join(lines)


# Markers delimit the rewriteable region; re-runs replace what's
# between them rather than appending.
_BLOCK_BEGIN = "# AUTO-TUNED: pak.tune_industries"
_BLOCK_END = "# END AUTO-TUNED"
_FACTORY_RE = re.compile(r"Factory\((?:[^()]|\([^()]*\))*\)", re.DOTALL)
_CLOSE_RE = re.compile(r"\n([ \t]*)\)\s*$")


def inject_into_script(script: Path, block: str) -> None:
    """Insert `block` before the SPECS/SPEC declaration and wire
    `materials=MATERIALS` / `lighting=LIGHTING` into each Factory(...)
    call.  Idempotent -- a prior AUTO-TUNED region is replaced, and
    the Factory-kwargs insert is guarded by `materials=MATERIALS in
    text`."""
    text = script.read_text()
    if _BLOCK_BEGIN in text:
        # Strip the block plus any blank lines fencing it -- otherwise
        # re-runs would accumulate a blank line each pass.
        i = text.index(_BLOCK_BEGIN)
        j = text.index(_BLOCK_END) + len(_BLOCK_END)
        while i > 0 and text[i - 1] == "\n":
            i -= 1
        while j < len(text) and text[j] == "\n":
            j += 1
        text = text[:i] + "\n\n" + text[j:]
    for marker in ("SPECS = [", "SPEC = "):
        if marker in text:
            i = text.rindex(marker)
            text = text[:i] + block + "\n\n" + text[i:]
            break
    else:
        raise SystemExit(f"{script}: no SPECS= / SPEC= to anchor injection")
    text = _ensure_imports(text, block)
    if "materials=MATERIALS" not in text:
        text = _wire_factory_kwargs(text, has_lighting="LIGHTING" in block)
    script.write_text(text)


def _ensure_imports(text: str, block: str) -> str:
    needs_lighting = "Lighting(" in block
    has_pak_materials = "from pak.materials import" in text
    if has_pak_materials and needs_lighting:
        m = re.search(r"from pak\.materials import ([^\n]+)", text)
        if m and "Lighting" not in m.group(1):
            text = text[:m.start(1)] + m.group(1) + ", Lighting" + text[m.end(1):]
        return text
    if has_pak_materials:
        return text
    names = ["Material"] + (["Lighting"] if needs_lighting else [])
    line_end = text.index("\n", text.index("from pak.dat import"))
    return (text[:line_end + 1]
            + f"from pak.materials import {', '.join(sorted(names))}\n"
            + text[line_end + 1:])


def _wire_factory_kwargs(text: str, *, has_lighting: bool) -> str:
    # Read the indent off the Factory's closing `)` -- single-SPEC scripts
    # close at column 0, SPECS-list scripts close at 4 spaces.
    def _add(m: re.Match) -> str:
        body = m.group(0)
        close = _CLOSE_RE.search(body)
        if close is None:
            raise RuntimeError(f"no closing ) in Factory block: {body[-40:]!r}")
        arg = close.group(1) + "    "
        inj = f"{arg}materials=MATERIALS,\n"
        if has_lighting:
            inj += f"{arg}lighting=LIGHTING,\n"
        cut = close.start() + 1
        return body[:cut] + inj + body[cut:]
    return _FACTORY_RE.sub(_add, text)


def run_one(script_path: Path, lighting: Lighting | None,
            max_iters: int, apply: bool,
            ) -> tuple[str, float, float]:
    mod = import_script(script_path)
    fac = specs_of(mod)[0]
    if not isinstance(fac, Factory):
        raise SystemExit(f"{script_path}: SPEC is {type(fac).__name__}, not Factory")
    print(f"=== {script_path.name} ({fac.name}) ===")
    materials = seed_materials(fac.blend)
    print(f"  seeded {len(materials)} materials from {fac.blend}")
    baseline, tuned_drgb, mats = tune(
        fac.blend, fac.upstream_dat, name=fac.name,
        materials=materials, lighting=lighting,
        max_iters=max_iters,
        out_dir=REPO_ROOT / "out" / "tune_industries" / script_path.stem,
    )
    if apply:
        inject_into_script(script_path, _format_block(mats, lighting))
        print(f"  wrote MATERIALS+LIGHTING into {script_path.name}")
    return script_path.stem, baseline, tuned_drgb


# Cross of ambient and elevation around `res_1600_kg_01`'s converged
# (0.55, 45).  Used once to pick the catalog-wide lighting; the chosen
# value goes into `--lighting=...` on a subsequent `--apply` run.
_LIGHTING_GRID: list[tuple[str, Lighting]] = [
    ("default", Lighting()),
    *[
        (f"amb{int(amb*100):03d}_elev{int(elev)}",
         Lighting(world_ambient=(amb, amb, amb),
                  sun_energy_scale=2.0 / 0.028,
                  sun_elev_deg=elev,
                  sun_az_offset_deg=-90.0))
        for amb, elev in [(0.45, 30.0), (0.45, 45.0),
                          (0.55, 45.0), (0.55, 60.0), (0.70, 45.0)]
    ],
]


def _parse_lighting(s: str) -> Lighting:
    kw: dict = {}
    for part in s.split(";"):
        if not part:
            continue
        k, _, v = part.partition("=")
        k, v = k.strip(), v.strip()
        kw[k] = (float(v),) * 3 if k == "world_ambient" else float(v)
    return Lighting(**kw)


def _sweep(scripts: list[Path], max_iters: int) -> None:
    rows: dict[str, dict[str, float]] = {}
    for label, light in _LIGHTING_GRID:
        print(f"\n### lighting {label}: {light}")
        row = {}
        for sp in scripts:
            _, base, tuned_drgb = run_one(sp, light, max_iters, apply=False)
            row[sp.stem] = tuned_drgb
            print(f"  {sp.stem}: baseline={base:.2f} tuned={tuned_drgb:.2f}")
        rows[label] = row
    print("\n=== sweep summary (tuned dRGB; lower better) ===")
    names = sorted({n for r in rows.values() for n in r})
    print(f"{'lighting':<18}  " + "  ".join(f"{n[:10]:>10}" for n in names))
    for label, row in rows.items():
        cells = "  ".join(f"{row.get(n, float('nan')):>10.2f}" for n in names)
        print(f"{label:<18}  {cells}")


def _main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("script", nargs="?")
    g.add_argument("--all", action="store_true")
    g.add_argument("--lighting-sweep", action="store_true")
    ap.add_argument("--on", default="",
                    help="comma-separated scripts for --lighting-sweep")
    ap.add_argument("--lighting", default=None,
                    help="world_ambient=0.45;sun_elev_deg=45;...")
    ap.add_argument("--max-iters", type=int, default=10)
    ap.add_argument("--apply", action="store_true",
                    help="write MATERIALS + LIGHTING into the bake script")
    args = ap.parse_args(argv)

    if args.lighting_sweep:
        if not args.on:
            raise SystemExit("--lighting-sweep requires --on a.py,b.py,...")
        _sweep([Path(p).resolve() for p in args.on.split(",")],
               args.max_iters)
        return 0

    lighting = _parse_lighting(args.lighting) if args.lighting else None
    if args.all:
        scripts = discover("industry")
    elif args.script:
        scripts = [Path(args.script).resolve()]
    else:
        raise SystemExit("specify a script, --all, or --lighting-sweep")

    results = [run_one(sp, lighting, args.max_iters, args.apply)
               for sp in scripts]
    if len(results) > 1:
        print("\n=== summary ===")
        print(f"{'asset':<20}  {'baseline':>9}  {'tuned':>9}  {'delta':>9}")
        for stem, b, t in results:
            print(f"{stem:<20}  {b:>9.2f}  {t:>9.2f}  {b-t:>+9.2f}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(REPO_ROOT))
    sys.exit(_main(sys.argv[1:]))
