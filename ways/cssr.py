"""Bake the concrete-sleeper / steel-rail (cssr) main-line track.

110lb/yard flat-bottomed rail — see
http://en.wikipedia.org/wiki/Permanent_way_%28history%29#Post-war_developments

Single source of truth for the asset.  `SPEC` holds the gameplay
scalars; running the script renders `cssr.png` (8 cols × 8 rows of
hex-ribi cells) and emits `cssr.dat` keyed against that atlas.

Run from the repo root:

    python3 -m ways.cssr

or import (`from ways import cssr`) to read `SPEC` without baking.
The dat re-emit path (no Blender) is `python3 -m pak.reemit_dats`.

`BLEND` is the upstream `ns-cssr.blend` strand-atom; `bake_way.py`
composes it along every hex ribi's chord (see CLAUDE.md ->
"Way-bake architecture").
"""

from __future__ import annotations

from pak.bake import bake_way_main
from pak.dat import Way


SPEC = Way(
    name="cssr",
    waytype="track",
    intro_year=1968,
    intro_month=3,
    topspeed=160,
    max_weight=22,
    wear_capacity=4128000000,
    cost=140000,
    maintenance=375,
)
BLEND = "ways/ns-cssr.blend"


if __name__ == "__main__":
    bake_way_main(SPEC, BLEND, __file__)
