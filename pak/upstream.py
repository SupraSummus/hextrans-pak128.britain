"""Resolve the upstream image stem encoded in an asset's dat.

Asset SPECs declare `upstream_dat=<path>` -- the source-of-truth
upstream dat path within the pak repo -- and diff harnesses derive
image paths from that.  The dat's `*Image[…]=` values carry the
image stem the upstream pakset uses; resolving against the dat's
parent directory gives the pak-relative path the fetch layer
expects.

The ref-value shapes that show up in upstream Britain dats:

  * Vehicles: `EmptyImage[<facing>][<livery>]=./<sub>/<stem>_<facing>.0.0`
    optionally with a per-image offset tail (`…_E.0.0,-33,14`).
  * Buildings: `BackImage[L][y][x][h][p][s]=<sub>/<stem>.<row>.<col>` —
    no facing in the stem; one atlas PNG covers every layout cell.
  * Trees: `image[<age>][<season>]=./<stem>.0.0` — no facing either;
    upstream ships per-(season,age) per-facing PNGs and the diff
    harness composes the lookup path.

`pak.dat.iter_image_refs` already strips the `,offset` tail and the
`.<row>.<col>` atlas coords into the `basename` field, so the only
upstream-specific work left is the optional `_<facing>` strip and
the resolve against the dat's parent directory.
"""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

_FACING_TOKENS = ("S", "SE", "E", "NE", "N", "NW", "W", "SW")
_REC_FACING = re.compile(r"_(?:" + "|".join(_FACING_TOKENS) + r")$")


def _first_image_basename(local_dat: Path, *, name: str | None) -> str:
    """First parseable image-ref's `basename` from `local_dat` (atlas
    tail + offset already stripped by `iter_image_refs`).  When `name`
    is set, scan only the matching object (case-insensitive); otherwise
    scan every object in order — multi-object upstream dats
    (citybuildings, train carriage families) need the name filter."""
    from pak.dat import find_object, iter_image_refs, parse

    objects = parse(local_dat)
    scan = [find_object(objects, name, source=local_dat)] if name else objects
    for obj in scan:
        for ref in iter_image_refs(obj):
            if ref.basename is not None:
                return ref.basename
    raise SystemExit(f"no image refs in upstream dat: {local_dat}")


def _resolve_stem(basename: str, dat_parent: PurePosixPath) -> str:
    """Strip the leading `./` and any trailing `_<facing>` from
    `basename`, then resolve against `dat_parent`."""
    s = _REC_FACING.sub("", basename.removeprefix("./"))
    return (dat_parent / s).as_posix()


def image_stem(upstream_dat: str, *, name: str | None = None) -> str:
    """Pak-relative POSIX-path stem (no extension) of the image refs
    encoded in `upstream_dat`.

    Fetches `upstream_dat` from the pinned upstream pak, reads the
    matching object's first image ref, and strips the per-image
    offset, `.<row>.<col>`, and `_<facing>` suffixes; the result
    resolves against the dat's parent directory.  Diff harnesses
    append their per-class extension (`_<facing>.png`,
    `-<season>-<age>_<facing>.png`, `.png`) to land on the actual PNG.

    `name` filters multi-object dats (e.g. `citybuildings/com-1870.dat`
    holds seven distinct buildings); pass the SPEC's `name` when the
    dat is known to be multi-object.  Single-object dats can leave it
    unset.
    """
    from pak.fetch_pak import fetch as fetch_pak

    local = fetch_pak(upstream_dat)
    basename = _first_image_basename(local, name=name)
    return _resolve_stem(basename, PurePosixPath(upstream_dat).parent)
