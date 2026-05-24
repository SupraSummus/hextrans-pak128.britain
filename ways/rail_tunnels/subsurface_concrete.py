"""Sub-surface concrete rail tunnel (1946+) -- cut-and-cover style."""
from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Tunnel

SPEC = Tunnel(
    name="SubSurfaceRailTunnelConcrete",
    waytype="track",
    copyright="James, Freahk, PJMack",
    intro_year=1946,
    intro_month=1,
    topspeed=160,
    max_weight=22,
    cost=1750000,
    maintenance=2500,
    blend="ways/stone-tunnel.blend",
    upstream_dat="ways/tunnels.dat",
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
