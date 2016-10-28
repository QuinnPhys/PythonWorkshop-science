from __future__ import print_function, division

import click

import epqis16_demos.demo_instrument

@click.group()
def main():
    pass

main.add_command(epqis16_demos.demo_instrument.demo_instrument)

