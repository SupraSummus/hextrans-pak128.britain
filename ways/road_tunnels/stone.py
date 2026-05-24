"""Stone road tunnel (1750-1940)."""
from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Tunnel

SPEC = Tunnel(
    name="RoadTunnelStone",
    waytype="road",
    copyright="James",
    intro_year=1750,
    intro_month=1,
    retire_year=1940,
    retire_month=1,
    topspeed=35,
    max_weight=12,
    cost=880000,
    maintenance=1000,
    blend="ways/stone-tunnel.blend",
    upstream_dat="ways/tunnels.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
