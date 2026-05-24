"""Brick narrow-gauge tunnel (1871+)."""
from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Tunnel

SPEC = Tunnel(
    name="NarrowTunnelBrick",
    waytype="narrowgauge_track",
    copyright="James",
    intro_year=1871,
    intro_month=7,
    topspeed=40,
    max_weight=12,
    cost=1500000,
    maintenance=2500,
    blend="ways/stone-tunnel.blend",
    upstream_dat="ways/tunnels.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
