"""Concrete road tunnel (1960+)."""
from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Tunnel

SPEC = Tunnel(
    name="RoadTunnelConcrete",
    waytype="road",
    copyright="James",
    intro_year=1960,
    intro_month=1,
    topspeed=110,
    max_weight=16,
    cost=1460000,
    maintenance=1500,
    blend="ways/stone-tunnel.blend",
    upstream_dat="ways/tunnels.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
