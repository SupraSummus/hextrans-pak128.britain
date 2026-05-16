"""Blackpool Brush railcoach tram (built 1937)."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle


# http://en.wikipedia.org/wiki/Blackpool_tramway#Boat_cars
# http://blackpool-trams.yolasite.com/brush-trams.php
# Capacity: http://www.britishtramsonline.co.uk/blackpoolfleet.doc
SPEC = Vehicle(
    name="Blackpool-Brush",
    waytype="tram_track",
    copyright="James",
    freight="Passagiere",
    engine_type="electric",
    intro_year=1937, intro_month=6,
    retire_year=1953, retire_month=6,
    speed=65,
    weight=12,
    axles=4,
    power=85,
    gear=80,
    tractive_effort=40,
    payload=48,
    min_loading_time=10,
    max_loading_time=50,
    overcrowded_capacity=6,
    cost=446000,
    runningcost=34,
    fixed_cost=6372,
    increase_maintenance_after_years=30,
    bidirectional=1,
    can_lead_from_rear=1,
    sound="tom-tait-tram.wav",
    constraint_prev=["none"],
    constraint_next=["none"],
    comfort=49,
    liverytype=["Blackpool-green", "WW2-Austerity", "Blackpool-green-postwar"],
    # Originally the English Electric railcoaches; sufficiently similar
    # that the brush should also upgrade to Progress twin-power.
    upgrade=["Blackpool-ProgressTwin-Power"],
    # Upstream's sparse `way_constraint_permissive[1]=1` and
    # `way_constraint_prohibitive[0]=0` (category-indexed flags)
    # don't fit the dense-list schema yet -- dropped here; see
    # TODO.md "Sparse way_constraint indexing".
)
BLEND = "trams/blackpool-brush.blend"


if __name__ == "__main__":
    bake_main(SPEC, BLEND, __file__)
