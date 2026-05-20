"""Stone-faced rail tunnel portal (1829-1915)."""
from __future__ import annotations

from pak.bake import bake_tunnel_main
from pak.dat import Tunnel

SPEC = Tunnel(
    name="RailTunnelStone",
    waytype="track",
    copyright="James",
    intro_year=1829,
    intro_month=3,
    retire_year=1916,
    retire_month=1,
    topspeed=80,
    max_weight=22,
    cost=2200000,
    maintenance=3000,
    blend="ways/stone-tunnel.blend",
    upstream_dat="ways/tunnels.dat",
)


if __name__ == "__main__":
    bake_tunnel_main(SPEC, __file__)
