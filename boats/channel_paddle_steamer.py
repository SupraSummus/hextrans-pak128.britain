"""channel-paddle-steamer."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

SPEC = Vehicle(
    name='ChannelPaddleSteamerHull',
    waytype='water',
    copyright='James',
    freight='Passagiere',
    engine_type='steam',
    intro_year=1853,
    intro_month=5,
    retire_year=1880,
    retire_month=7,
    speed=20,
    length=10,
    weight=3000,
    power=3550,
    payload=350,
    min_loading_time=2400,
    max_loading_time=3600,
    catering_level=4,
    cost=83865600,
    runningcost=763,
    fixed_cost=634944,
    smoke='Steam',
    sound='ship-horn_b.wav',
    range=250,
    constraint_prev=['none'],
    constraint_next=['ChannelPaddleSteamerAddMail', 'ChannelPaddleSteamerAddPax', 'ChannelPaddleSteamerAddLivestock', 'ChannelPaddleSteamerAddPiece', 'ChannelPaddleSteamerAddCool', 'ChannelPaddleSteamerAddBulk', 'ChannelPaddleSteamerAddLong'],
    payload_by_class=[0, 350, 0, 100],
    comfort_by_class=[0, 80, 0, 144],
    blend='boats/channel-paddle-steamer.blend',
    upstream_dat='boats/channel-paddle-steamer.dat',
)


if __name__ == "__main__":
    bake_main(SPEC, __file__)
