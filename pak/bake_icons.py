"""Slice upstream icon / cursor cells into per-asset sibling PNGs.

The build-time half of the upstream-icon-passthrough system (see
CLAUDE.md → "Upstream icon passthrough" for the rationale).  Same
shape as the parametric ground bakers: read SPEC, fetch the
SHA-pinned upstream PNG, crop the named 128-px cell(s), write a
tight single-row `<basename>_icon.png` sibling -- committed, not
gitignored.  Slot 0 is icon, slot 1 cursor (matches `_icon_ref`
in `pak.dat`).

Usage: `python3 -m pak.bake_icons [dat-path ...]` (no args walks
every ported bake unit).
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from . import REPO_ROOT
from .bake_units import discover, import_script, specs_of
from .fetch_pak import fetch

CELL_PX = 128

_CELL_REF_RE = re.compile(
    r"^\s*(?:\./)?(?P<stem>[A-Za-z0-9_./-]+?)\.(?P<row>\d+)\.(?P<col>\d+)\s*$"
)


@dataclass(frozen=True)
class _CellRef:
    stem: str  # dat-relative PNG path stem, no `.png` suffix
    row: int
    col: int


def _parse(ref: str) -> _CellRef:
    m = _CELL_REF_RE.match(ref)
    if not m:
        raise ValueError(f"bad cell ref: {ref!r}")
    return _CellRef(m["stem"], int(m["row"]), int(m["col"]))


def _crop_cell(img: Image.Image, cell: _CellRef) -> Image.Image:
    x = cell.col * CELL_PX
    y = cell.row * CELL_PX
    return img.crop((x, y, x + CELL_PX, y + CELL_PX))


def _compose_atlas(src: Image.Image, cells: list[_CellRef]) -> Image.Image:
    """Crop each cell from `src` and paste left-to-right in a single row."""
    out = Image.new("RGBA", (CELL_PX * len(cells), CELL_PX))
    for slot, cell in enumerate(cells):
        out.paste(_crop_cell(src, cell), (slot * CELL_PX, 0))
    return out


def _spec_cells(spec) -> list[_CellRef]:
    """Cells `slice_for` would slice -- empty when no `icon_src`."""
    icon_src = getattr(spec, "icon_src", None)
    if icon_src is None:
        return []
    cells = [_parse(icon_src)]
    cursor_src = getattr(spec, "cursor_src", None)
    if cursor_src is not None:
        cells.append(_parse(cursor_src))
    return cells


def slice_for(dat: Path, spec) -> Path | None:
    """Write `<dat>_icon.png` from `spec.icon_src` (and `cursor_src`).

    Returns the written path, or `None` if the SPEC declares no
    icon source.
    """
    cells = _spec_cells(spec)
    if not cells:
        return None
    # Every cell must come from the same upstream PNG -- one fetch
    # per asset, and the slicer doesn't yet model mix-and-match.
    stems = {c.stem for c in cells}
    if len(stems) != 1:
        raise ValueError(
            f"{dat.name}: icon_src / cursor_src must share an upstream "
            f"PNG, got {stems}"
        )
    rel_dir = dat.parent.relative_to(REPO_ROOT).as_posix()
    src_png = fetch(f"{rel_dir}/{cells[0].stem}.png")
    with Image.open(src_png) as src:
        out = _compose_atlas(src, cells)
    out_path = dat.with_name(f"{dat.stem}_icon.png")
    out.save(out_path, optimize=True)
    return out_path


def main(argv: list[str]) -> int:
    if argv:
        dats = [Path(a).resolve() for a in argv]
    else:
        dats = [script.with_suffix(".dat") for script in discover()]
    for dat in dats:
        script = dat.with_suffix(".py")
        if not script.exists():
            continue
        for spec in specs_of(import_script(script)):
            out = slice_for(dat, spec)
            if out is not None:
                print(out.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
