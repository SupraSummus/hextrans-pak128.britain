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

`_strip_ref` is the pure transform — drops the `,offset` tail, the
`.<row>.<col>` atlas coords, and the optional `_<facing>`, then
resolves against the dat's parent directory.  `image_stem` is the
network-touching driver that fetches the dat and walks its objects
(filtered by `name=` for multi-object dats).
"""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

_FACING_TOKENS = ("S", "SE", "E", "NE", "N", "NW", "W", "SW")
_REC_ROWCOL = re.compile(r"\.\d+\.\d+\s*$")
_REC_FACING = re.compile(r"_(?:" + "|".join(_FACING_TOKENS) + r")$")
# Match image-ref keys in any case: emptyimage, backimage, frontimage,
# image, freightimage, livery_image, hasdriver_image, …; followed by at
# least one `[index]` bracket.
_IMAGE_KEY_RE = re.compile(
    r"^(?:empty|back|front|freight|hasdriver|livery_)?image(?:\[[^\]]*\])+$",
    re.I,
)


def _first_image_ref(local_dat: Path, *, name: str | None) -> str:
    """First image-ref value in `local_dat`.  When `name` is set, search
    only the object whose `name=`/`Name=` matches (case-insensitive);
    otherwise scan every object in order.  Multi-object upstream dats
    (citybuildings, train carriage families) need the name filter so the
    right block's image stem comes back."""
    from pak.dat import parse

    objects = parse(local_dat)
    if not objects:
        raise SystemExit(f"empty upstream dat: {local_dat}")
    if name is not None:
        wanted = name.lower()
        matched = [
            obj for obj in objects
            if any(k.lower() == "name" and v.strip().lower() == wanted
                   for k, v in obj)
        ]
        if not matched:
            raise SystemExit(
                f"no obj named {name!r} in upstream dat: {local_dat}"
            )
        scan = matched
    else:
        scan = objects
    for obj in scan:
        for key, value in obj:
            if _IMAGE_KEY_RE.match(key):
                return value.strip()
    raise SystemExit(f"no image refs in upstream dat: {local_dat}")


def _strip_ref(ref: str, dat_parent: PurePosixPath) -> str:
    """Pure transform from an image-ref value to a pak-relative POSIX
    path stem (no extension).  Drops a `./` prefix, the comma-separated
    per-image offset tail (`<ref>,-33,14`), the `.<row>.<col>` atlas
    suffix, and the optional `_<facing>` suffix; resolves against
    `dat_parent`."""
    s = ref.split(",", 1)[0].strip().removeprefix("./")
    s = _REC_ROWCOL.sub("", s)
    s = _REC_FACING.sub("", s)
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
    ref = _first_image_ref(local, name=name)
    return _strip_ref(ref, PurePosixPath(upstream_dat).parent)
