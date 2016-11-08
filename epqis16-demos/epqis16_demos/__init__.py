from __future__ import print_function, division

__all__ = [
    'demo_instrument',
    'EpqisDemoInstrument',
    'main'
]

import click

import epqis16_demos.demo_instrument

from epqis16_demos.ik_driver import EpqisDemoInstrument

@click.group()
def main():
    pass

main.add_command(epqis16_demos.demo_instrument.demo_instrument)

