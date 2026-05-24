"""Brick-faced rail tunnel portal (1848-1959)."""
from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Tunnel

SPEC = Tunnel(
    name="RailTunnelBrick",
    waytype="track",
    copyright="James",
    intro_year=1848,
    intro_month=9,
    retire_year=1959,
    retire_month=5,
    topspeed=110,
    max_weight=22,
    cost=2700000,
    maintenance=4400,
    blend="ways/stone-tunnel.blend",
    upstream_dat="ways/tunnels.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
