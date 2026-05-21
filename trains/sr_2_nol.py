"""sr-2-nol."""

from __future__ import annotations

from pak.bake import bake_main
from pak.dat import Vehicle

_BLEND = 'trains/Railcars/sr-2-nol-driving-trailer-malachite.blend'
_UPSTREAM_DAT = 'trains/sr-2-nol.dat'

SPECS = [
    Vehicle(
        name='SR-2-NOL-front',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='Passagiere',
        engine_type='electric',
        intro_year=1934,
        intro_month=8,
        retire_year=1940,
        retire_month=12,
        speed=97,
        length=10,
        weight=42.1,
        axles=4,
        power=410,
        gear=80,
        tractive_effort=38,
        payload=75,
        min_loading_time=10,
        max_loading_time=40,
        overcrowded_capacity=37,
        cost=1680000,
        runningcost=164,
        fixed_cost=11167,
        upgrade_price=336000,
        increase_maintenance_after_years=25,
        bidirectional=0,
        can_lead_from_rear=1,
        sound='x24tohayes-epb.wav',
        constraint_prev=['SR-3SUB(rear)', 'LSWR-EMU(rear)', 'SR-4SUB(rear)', 'SR-2-NOL-rear', 'SR-4LAV(rear)', 'SR-401[BIL]Rear', 'SR-6PAN(rear)', 'sr-2hal-rear', 'SR-404[COR]Rear', 'lbscr-48ft-augmentation-trailer-rear', 'lbscr-54ft-augmentation-trailer-rear', 'lswr-48ft-arc-augmentation-trailer-rear', 'lswr-48ft-augmentation-trailer-rear', 'lswr-56ft-augmentation-trailer-rear', 'SR-5-BEL-driving-motor-rear', 'none'],
        constraint_next=['SR-2-NOL-rear'],
        payload_by_class=[0, 75, 0, 0],
        comfort_by_class=[0, 75, 0, 82],
        liverytype=['SR-Olive-Green', 'SR-Malachite-Green', 'BR-Early', 'BR-Revised'],
        upgrade=['BR-414[HAP]Front', 'BR-414[HAP]Rear', 'BR-4EPB(front)', 'BR-2EPB(rear)', 'BR-4EPB(rear)', 'BR-4EPB(centre1)', 'BR-4EPB(centre2)'],
        way_constraint_permissive=[0],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
    Vehicle(
        name='SR-2-NOL-rear',
        waytype='track',
        copyright='Kieron/JamesPetts',
        freight='Passagiere',
        engine_type='electric',
        intro_year=1934,
        intro_month=8,
        retire_year=1940,
        retire_month=12,
        speed=97,
        length=11,
        weight=29.7,
        axles=4,
        power=0,
        payload=60,
        min_loading_time=10,
        max_loading_time=40,
        overcrowded_capacity=30,
        cost=720000,
        runningcost=0,
        fixed_cost=857,
        upgrade_price=140000,
        increase_maintenance_after_years=25,
        bidirectional=0,
        can_lead_from_rear=1,
        sound='x24tohayes-epb.wav',
        constraint_prev=['SR-2-NOL-front'],
        constraint_next=['SR-3SUB(front)', 'LSWR-EMU(front)', 'SR-4SUB(front)', 'SR-2-NOL-front', 'SR-4LAV(front)', 'SR-401[BIL]Front', 'SR-6PAN(front)', 'sr-2hal-front', 'SR-404[COR]Front', 'lbscr-48ft-augmentation-trailer-front', 'lbscr-54ft-augmentation-trailer-front', 'lswr-48ft-arc-augmentation-trailer-front', 'lswr-48ft-augmentation-trailer-front', 'lswr-56ft-augmentation-trailer-front', 'SR-5-BEL-driving-motor-front', 'none'],
        payload_by_class=[0, 60, 0, 25],
        comfort_by_class=[0, 75, 0, 82],
        liverytype=['SR-Olive-Green', 'SR-Malachite-Green', 'BR-Early', 'BR-Revised'],
        upgrade=['BR-414[HAP]Front', 'BR-414[HAP]Rear', 'BR-4EPB(front)', 'BR-2EPB(rear)', 'BR-4EPB(rear)', 'BR-4EPB(centre1)', 'BR-4EPB(centre2)'],
        way_constraint_permissive=[0],
        blend=_BLEND,
        upstream_dat=_UPSTREAM_DAT,
    ),
]


if __name__ == "__main__":
    bake_main(SPECS, __file__)
