#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Provides support for the epqis16 Demonstration Instrument.
"""

# IMPORTS #####################################################################

from __future__ import absolute_import
from __future__ import division

#from enum import IntEnum

import quantities as pq

from instruments.abstract_instruments import (
    PowerSupply,
    PowerSupplyChannel,
)

from instruments.util_fns import assume_units, ProxyList, bool_property
from instruments.generic_scpi import SCPIInstrument
# CLASSES #####################################################################

class EpqisDemo(PowerSupply, SCPIInstrument):
    """
    The EpqisDemo is a single channel DC power supply with an on/off button and
    display of the voltage. It is written with the PyQt5 which launces a GUI on
    your computer and listens over a optionally specified port.

    This object inherits from `PowerSupply`.

    Example usage:

    >>> import instruments as ik
    >>> import quantities as pq
    >>> inst = ik.generic_scpi.SCPIInstrument.open_tcpip("localhost",8042)
    >>> inst.voltage = 10 * pq.V
    """

    _channel_count = 4

    def __init__(self, filelike):
        super(EpqisDemo, self).__init__(filelike)

    # INNER CLASSES #

    class Channel(PowerSupplyChannel):

        """
        Class representing a channel on the EpqisDemo.

        This class inherits from `PowerSupplyChannel`.

        .. warning:: This class should NOT be manually created by the user. It
            is designed to be initialized by the `EpqisDemo` class.
        """

        def __init__(self, idx):
            self._idx = idx + 1

        # COMMUNICATION METHODS #

        def sendcmd(self, cmd):
            """
            Function used to send a command to the instrument while wrapping
            the command with the neccessary identifier for the channel.

            :param str cmd: Command that will be sent to the instrument after
                being postfixed with the channel identifier
            """
            self.sendcmd(cmd.format(self=self))

        def query(self, cmd):
            """
            Function used to send a command to the instrument while wrapping
            the command with the neccessary identifier for the channel.

            :param str cmd: Command that will be sent to the instrument after
                being postfixed with the channel identifier
            :return: The result from the query
            :rtype: `str`
            """
            return self.query(cmd.format(self=self))

        # PROPERTIES #
        @property
        def mode(self):
            """
            Gets/sets the mode for the specified channel.
            """
            raise NotImplementedError('This instrument does not support querying '
                                      'or setting the output current.')

        @mode.setter
        def mode(self, newval):
            raise NotImplementedError('This instrument does not support querying '
                                      'or setting the output current.')

        @property
        def voltage(self):
            """
            Gets/sets the voltage for the specified channel.

            Example use:

            >>> import instruments as ik
            >>> import quantities as pq
            >>> inst = ik.generic_scpi.SCPIInstrument.open_tcpip("localhost",8042)
            >>> inst.voltage
                10 * pq.V
            >>> inst.voltage = 42 * pq.mV

            :type: `float`
            """
            value = self.sendcmd('VOLTS? {self._idx}')
            return assume_units(value, pq.millivolt).rescale(pq.volt)

        @voltage.setter
        def voltage(self, newval):
            newval = assume_units(newval, pq.volt).rescale(pq.millivolt).magnitude
            self.sendcmd('VOLTS {{self._idx}} {}'.format(newval))

        @property
        def current(self):
            """
            Gets/sets the current for the specified channel.
            """
            raise NotImplementedError('This instrument does not support querying '
                                      'or setting the output current.')

        @current.setter
        def current(self, newval):
            raise NotImplementedError('This instrument does not support querying '
                                      'or setting the output current.')

        output = bool_property(
            "ENABLE {self._idx}",
            inst_true="ON",
            inst_false="OFF",
            doc="""
            Sets the outputting status of the specified channel.

            This is a toggle setting that can be ON or OFF. 

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

        :rtype: `EpqisDemo.Channel`

        .. seealso::
            `EpqisDemo` for example using this property.
        """
        return ProxyList(self, EpqisDemo.Channel, range(self._channel_count))

    @property
    def voltage(self):
        """
        Gets/sets the voltage for all channels.

        :units: As specified (if a `~quantities.Quantity`) or assumed to be
            of units Volts.
        :type: `list` of `~quantities.quantity.Quantity` with units Volt
        """
        return [
            self.channel[i].voltage for i in range(self._channel_count)
        ]

    @voltage.setter
    def voltage(self, newval):
        if isinstance(newval, (list, tuple)):
            if len(newval) is not self._channel_count:
                raise ValueError('When specifying the voltage for all channels '
                                 'as a list or tuple, it must be of '
                                 'length {}.'.format(self._channel_count))
            for channel, new_voltage in zip(self.channel, newval):
                channel.voltage = new_voltage
        else:
            for channel in self.channel:
                channel.voltage = newval

    @property
    def current(self):
        """
        Gets/sets the current for the specified channel.
        """
        raise NotImplementedError('This instrument does not support querying '
                                  'or setting the output current.')

    @current.setter
    def current(self, newval):
        raise NotImplementedError('This instrument does not support querying '
                                  'or setting the output current.')