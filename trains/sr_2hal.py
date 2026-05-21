"""sr-2hal."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Railcars/sr-2hal-drving-trailer-br-blue-x.blend'
_UPSTREAM_DAT = 'trains/sr-2hal.dat'

SPECS = [
    Vehicle(
        name='sr-2hal-front',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='Passagiere',
        engine_type='electric',
        intro_year=1938,
        intro_month=6,
        retire_year=1955,
        retire_month=10,
        speed=120,
        length=11,
        weight=43,
        axles=4,
        power=410,
        gear=80,
        tractive_effort=31,
        payload=70,
        min_loading_time=15,
        max_loading_time=45,
        overcrowded_capacity=35,
        cost=1400000,
        runningcost=164,
        fixed_cost=10972,
        bidirectional=0,
        can_lead_from_rear=1,
        sound='x24tohayes-epb.wav',
        constraint_prev=['SR-3SUB(rear)', 'LSWR-EMU(rear)', 'SR-4SUB(rear)', 'SR-2-NOL-rear', 'SR-4LAV(rear)', 'SR-401[BIL]Rear', 'SR-6PAN(rear)', 'sr-2hal-rear', 'SR-404[COR]Rear', 'lbscr-48ft-augmentation-trailer-rear', 'lbscr-54ft-augmentation-trailer-rear', 'lswr-48ft-arc-augmentation-trailer-rear', 'lswr-48ft-augmentation-trailer-rear', 'lswr-56ft-augmentation-trailer-rear', 'SR-5-BEL-driving-motor-rear', 'none'],
        constraint_next=['sr-2hal-rear'],
        payload_by_class=[0, 70],
        comfort_by_class=[0, 72],
        liverytype=['SR-Malachite-Green', 'BR-Early', 'BR-Revised', 'BR-Blue'],
        way_constraint_permissive=[0],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='sr-2hal-rear',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='Passagiere',
        engine_type='electric',
        intro_year=1938,
        intro_month=6,
        retire_year=1955,
        retire_month=10,
        speed=120,
        length=11,
        weight=31,
        axles=4,
        power=0,
        payload=32,
        min_loading_time=15,
        max_loading_time=45,
        overcrowded_capacity=16,
        cost=1400000,
        runningcost=0,
        fixed_cost=1667,
        bidirectional=0,
        can_lead_from_rear=1,
        sound='x24tohayes-epb.wav',
        constraint_prev=['sr-2hal-front'],
        constraint_next=['SR-3SUB(front)', 'LSWR-EMU(front)', 'SR-4SUB(front)', 'SR-2-NOL-front', 'SR-4LAV(front)', 'SR-401[BIL]Front', 'SR-6PAN(front)', 'sr-2hal-front', 'SR-404[COR]Front', 'lbscr-48ft-augmentation-trailer-front', 'lbscr-54ft-augmentation-trailer-front', 'lswr-48ft-arc-augmentation-trailer-front', 'lswr-48ft-augmentation-trailer-front', 'lswr-56ft-augmentation-trailer-front', 'SR-5-BEL-driving-motor-front', 'none'],
        payload_by_class=[0, 32, 0, 24],
        comfort_by_class=[0, 83, 0, 91],
        liverytype=['SR-Malachite-Green', 'BR-Early', 'BR-Revised', 'BR-Blue'],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
