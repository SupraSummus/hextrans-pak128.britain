"""Stone narrow-gauge tunnel (1832-1871)."""
from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Tunnel

SPEC = Tunnel(
    name="NarrowTunnelStone",
    waytype="narrowgauge_track",
    copyright="James",
    intro_year=1832,
    intro_month=5,
    retire_year=1871,
    retire_month=7,
    topspeed=20,
    max_weight=8,
    cost=1350000,
    maintenance=2675,
    blend="ways/stone-tunnel.blend",
    upstream_dat="ways/tunnels.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
