"""gwr-railmotor."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# These are the auto-trailer versions of the steam railmotors
# This is the 57ft version
# See Harris pp. 58-9
# https://en.wikipedia.org/wiki/GWR_steam_rail_motors
SPEC = Vehicle(
    name='gwr-railmotor',
    waytype='track',
    copyright='JamesPetts',
    freight='Passagiere',
    engine_type='steam',
    intro_year=1903,
    intro_month=4,
    retire_year=1929,
    retire_month=11,
    speed=90,
    length=11,
    weight=39.4,
    axle_load=11,
    power=130,
    tractive_effort=61,
    payload=56,
    min_loading_time=20,
    max_loading_time=105,
    overcrowded_capacity=35,
    cost=1715000,
    runningcost=62,
    fixed_cost=18500,
    bidirectional=1,
    can_lead_from_rear=1,
    smoke='Steam',
    sound='laurie-gwr-railmotor.wav',
    payload_by_class=[0, 56],
    comfort_by_class=[0, 62],
    liverytype=['GWR-two-tone', 'GWR-overall-brown', 'GWR-lake', 'ww1-austerity', 'GWR-chocolate-cream-lined', 'GWR-chocolate-cream-plain', 'GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
    upgrade=['gwr-churchward-autotrailer'],
    blend='trains/Railcars/gwr-railmotor-collett.blend',
    upstream_dat='trains/gwr-railmotor.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
