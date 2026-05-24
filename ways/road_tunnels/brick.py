"""Brick road tunnel (1900+)."""
from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Tunnel

SPEC = Tunnel(
    name="RoadTunnelBrick",
    waytype="road",
    copyright="James",
    intro_year=1900,
    intro_month=1,
    topspeed=50,
    max_weight=12,
    cost=800000,
    maintenance=1600,
    blend="ways/stone-tunnel.blend",
    upstream_dat="ways/tunnels.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
