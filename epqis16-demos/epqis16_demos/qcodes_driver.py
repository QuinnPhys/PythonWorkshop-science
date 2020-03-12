#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Provides support for the epqis16 Demonstration Instrument.
"""

# IMPORTS #####################################################################

from __future__ import absolute_import
from __future__ import division

from qcodes.instrument.visa import VisaInstrument
import qcodes.utils.validators as vals
import numpy as np

# CLASSES #####################################################################

class EpqisDemoInstrumentChannel(InstrumentChannel):
    def __init__(self, parent, name, channel):
        super().__init__(parent, name)

        self.add_parameter('state',
                           label='Output enabled',
                           set_cmd='{} ENABLE {}'.format(channel, '{}'),
                           get_cmd='{} ENABLE?'.format(channel),
                           #val_mapping={'ON': 1, 'OFF': 0},
                           vals=vals.Enum('ON', 'OFF')
                           )
        self.add_parameter("voltage",
                           label='Measured voltage',
                           get_cmd="{} :MEASure:SCALar:VOLTage:DC?".format(
                               select_cmd),
                           get_parser=float,
                           unit='V',
                          )
        self.add_parameter("set_voltage",
                           label='Target voltage output',
                           set_cmd="{} :SOURce:VOLTage:LEVel:IMMediate:AMPLitude {}".format(
                               select_cmd, '{}'),
                           get_cmd="{} :SOURce:VOLTage:LEVel:IMMediate:AMPLitude?".format(
                               select_cmd),
                           get_parser=float,
                           unit='V',
                           vals=vals.Numbers(0, 32.050)
                          )
        self.add_parameter("current",
                           label='Measured current',
                           get_cmd="{} :MEASure:SCALar:CURRent:DC?".format(
                               select_cmd),
                           get_parser=float,
                           unit='A',
                           )
        self.add_parameter("set_current",
                           label='Target current output',
                           set_cmd="{} :SOURce:CURRent:LEVel:IMMediate:AMPLitude {}".format(
                               select_cmd, '{}'),
                           get_cmd="{} :SOURce:CURRent:LEVel:IMMediate:AMPLitude?".format(
                               select_cmd),
                           get_parser=float,
                           unit='A',
                           vals=vals.Numbers(0.5e-3, self._parent.max_current)
                           )


class EpqisDemoInstrument(VisaInstrument):
    """
    The EpqisDemoInstrument is a single channel DC power supply with an on/off button and
    display of the voltage. It is written with the PyQt5 which launces a GUI on
    your computer and listens over a optionally specified port.
    """

    def __init__(self, name, address, **kwargs):
        super().__init__(name, address, terminator='\r', **kwargs)

        self.add_parameter('attenuation', unit='dB',
                           set_cmd='ATTN ALL {:02.0f}',
                           get_cmd='ATTN? 1',
                           vals=vals.Enum(*np.arange(0, 60.1, 2).tolist()),
                           get_parser=float)
        
        # channel-specific parameters
        channels = ChannelList(self, "SupplyChannel", RohdeSchwarzHMC804xChannel, snapshotable=False)
        for ch_num in range(1, num_channels+1):
            ch_name = "ch{}".format(ch_num)
            channel = RohdeSchwarzHMC804xChannel(self, ch_name, ch_num)
            channels.append(channel)
            self.add_submodule(ch_name, channel)
        channels.lock()
        self.add_submodule("channels", channels)


        self.connect_message()
