#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Provides support for the epqis16 Demonstration Instrument.
"""

# IMPORTS #####################################################################

from __future__ import absolute_import
from __future__ import division

from enum import IntEnum

import quantities as pq

from instruments.abstract_instruments import (
    PowerSupply,
    PowerSupplyChannel,
)
from instruments.abstract_instruments import Instrument
from instruments.util_fns import assume_units, ProxyList

# CLASSES #####################################################################


class EpqisDemo(PowerSupply, PowerSupplyChannel):

    """
    The EpqisDemo is a single channel DC power supply with an on/off button and display of the voltage.
    It is written with the PyQt5 which launces a GUI on your computer and listens over a optionally 
    specified port. By 

    Because it is a single channel output, this object inherits from both
    PowerSupply and PowerSupplyChannel.

    Example usage:

    >>> import instruments as ik
    >>> import quantities as pq
    >>> inst = ik.generic_scpi.SCPIInstrument.open_tcpip("localhost",8042)
    >>> inst.voltage = 10 * pq.V
    """

    def __init__(self, filelike):
        super(EpqisDemo, self).__init__(filelike)
        self._channel_count = 1

    # INNER CLASSES #

    class Channel(PowerSupplyChannel):

        """
        Class representing a channel on the EpqisDemo.

        This class inherits from `PowerSupplyChannel`.

        .. warning:: This class should NOT be manually created by the user. It
            is designed to be initialized by the `EpqisDemo` class.
        """

        def __init__(self, parent, name, idx):
            self._parent = parent
            self._name = name
            self._idx = idx + 1

        # COMMUNICATION METHODS #

        def _format_cmd(self, cmd):
            cmd = cmd.split(" ")
            if len(cmd) == 1:
                cmd = "{cmd} {idx}".format(cmd=cmd[0], idx=self._idx)
            else:
                cmd = "{cmd} {idx},{value}".format(
                    cmd=cmd[0],
                    idx=self._idx,
                    value=cmd[1]
                )
            return cmd

        def sendcmd(self, cmd):
            """
            Function used to send a command to the instrument while wrapping
            the command with the neccessary identifier for the channel.

            :param str cmd: Command that will be sent to the instrument after
                being prefixed with the channel identifier
            """
            cmd = self._format_cmd(cmd)
            self._hp.sendcmd(cmd)

        def query(self, cmd):
            """
            Function used to send a command to the instrument while wrapping
            the command with the neccessary identifier for the channel.

            :param str cmd: Command that will be sent to the instrument after
                being prefixed with the channel identifier
            :return: The result from the query
            :rtype: `str`
            """
            cmd = self._format_cmd(cmd)
            return self._hp.query(cmd)

        # PROPERTIES #

        @property
        def name(self):
            """
            The name of the connected instrument, as reported by the
            standard SCPI command ``*IDN?``.

            :rtype: `str`
            """
            return self.query("*IDN?")

        voltage = unitful_property(
            "VOLTS",
            pq.volt,
            set_fmt="{} {:.1f}",
            output_decoration=float,
            doc="""
            Sets the voltage of the specified channel. 


            :units: As specified, or assumed to be :math:`\\text{V}` otherwise.
            :type: `float` or `~quantities.quantity.Quantity`
            """
        )

        output = bool_property(
            "ENABLE",
            inst_true="ON",
            inst_false="OFF",
            set_fmt="{} {:.1f}",
            doc="""
            Sets the outputting status of the specified channel.

            This is a toggle setting. True will turn on the channel output
            while False will turn it off.

            :type: `bool`
            """
        )



    # ENUMS #

    # class Mode(Enum):
    #     """
    #     Enum containing valid output modes for the EpqisDemo
    #     """
    #     off = 'OFF'
    #     on = 'ON'


    # PROPERTIES #

    @property
    def channel(self):
        """
        Gets a specific channel object. The desired channel is specified like
        one would access a list.

        :rtype: `HP6624a.Channel`

        .. seealso::
            `HP6624a` for example using this property.
        """
        return ProxyList(self, EpqisDemo.Channel, range(self.channel_count))

    @property
    def voltage(self):
        """
        Sets the voltage. This device has a voltage range of 0V to +30V.

        Querying the voltage is not supported by this instrument.

        :units: As specified (if a `~quantities.quantity.Quantity`) or assumed
            to be of units Volts.
        :type: `~quantities.quantity.Quantity` with units Volt
        """
        return [
            self.channel[i].voltage for i in range(self.channel_count)
        ]

    @voltage.setter
    def voltage(self, newval):
        if isinstance(newval, (list, tuple)):
            if len(newval) is not self.channel_count:
                raise ValueError('When specifying the voltage for all channels '
                                 'as a list or tuple, it must be of '
                                 'length {}.'.format(self.channel_count))
            for i in range(self.channel_count):
                self.channel[i].voltage = newval[i]
        else:
            for i in range(self.channel_count):
                self.channel[i].voltage = newval

        @voltage.setter
        def voltage(self, newval):
            newval = assume_units(newval, pq.volt).rescale(pq.millivolt).magnitude
            self._parent.sendcmd('VOLTS {}'.format(newval))


        @property
        def output(self):
            """
            Sets the output status of the specified channel. This either enables
            or disables the output.

            Querying the output status is not supported by this instrument.

            :type: `bool`
            """
            raise NotImplementedError('This instrument does not support '
                                      'querying the output status.')

        @output.setter
        def output(self, newval):
            if newval is 'ON':
                self._parent.sendcmd('ENABLE ON')
            else:
                self._parent.sendcmd('ENABLE OFF')

    @property
    def channel_count(self):
        """
        Gets/sets the number of output channels available for the connected
        power supply.

        :type: `int`
        """
        return self._channel_count

    @channel_count.setter
    def channel_count(self, newval):
        if not isinstance(newval, int):
            raise TypeError('Channel count must be specified as an integer.')
        if newval < 1:
            raise ValueError('Channel count must be >=1')
        self._channel_count = newval


    # METHODS #

  
