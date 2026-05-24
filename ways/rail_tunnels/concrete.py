"""Concrete rail tunnel portal (1954-1997)."""
from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Tunnel

SPEC = Tunnel(
    name="RailTunnelConcrete",
    waytype="track",
    copyright="James",
    intro_year=1954,
    intro_month=7,
    retire_year=1997,
    retire_month=5,
    topspeed=150,
    max_weight=26,
    cost=3000000,
    maintenance=4000,
    blend="ways/stone-tunnel.blend",
    upstream_dat="ways/tunnels.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
