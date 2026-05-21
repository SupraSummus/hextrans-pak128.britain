"""gwr-churchward-autotrailer."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

# These are the auto-trailer versions of the steam railmotors
# This is the 57ft version
# See Harris pp. 58-9
SPEC = Vehicle(
    name='gwr-churchward-autotrailer',
    waytype='track',
    copyright='JamesPetts',
    freight='Passagiere',
    intro_year=1906,
    intro_month=10,
    retire_year=1929,
    retire_month=11,
    speed=100,
    length=11,
    weight=30.3,
    axles=4,
    payload=72,
    min_loading_time=20,
    max_loading_time=105,
    overcrowded_capacity=41,
    cost=800000,
    runningcost=0,
    fixed_cost=955,
    upgrade_price=129032,
    bidirectional=1,
    can_lead_from_rear=1,
    constraint_prev=['gwr-517-rebuilt-auto-fitted', 'GWR-1400Tank', 'gwr-6400', 'gwr-railmotor', 'gwr-2021-rebuilt', 'none'],
    constraint_next=['gwr-517-rebuilt-auto-fitted', 'GWR-1400Tank', 'gwr-6400', 'gwr-railmotor', 'gwr-2021-rebuilt', 'none'],
    payload_by_class=[0, 72],
    comfort_by_class=[0, 62],
    liverytype=['GWR-two-tone', 'GWR-overall-brown', 'GWR-lake', 'WW1-Austerity', 'GWR-chocolate-cream-lined', 'GWR-chocolate-cream-plain', 'GWR-shirtbutton', 'GWR-hawksworth', 'BR-Early'],
    blend='trains/Carriages/gwr-churchward-autotrailer-collett.blend',
    upstream_dat='trains/gwr-churchward-autotrailer.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
