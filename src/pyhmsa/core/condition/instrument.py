#!/usr/bin/env python
"""
================================================================================
:mod:`instrument` -- Instrument condition
================================================================================

.. module:: instrument
   :synopsis: Instrument condition

.. inheritance-diagram:: pyhmsa.condition.instrument

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.core.condition import _Condition

# Globals and constants variables.

class Instrument(_Condition):

    def __init__(self, manufacturer, model, serial_number=None):
        """
        Describes the type of instrument used to collect a HMSA dataset.
        
        :arg manufacturer: manufacturer (required)
        :arg model: model (required)
        :arg serial_number: serial number (optional)
        """
        _Condition.__init__(self)

        self.manufacturer = manufacturer
        self.model = model
        self.serial_number = serial_number

    def get_manufacturer(self):
        """
        Returns the manufacturer.
        """
        return self._manufacturer

    def set_manufacturer(self, value):
        """
        Sets the manufacturer.
        
        :arg value: manufacturer
        """
        if value is None:
            raise ValueError('Manufacturer is required')
        self._manufacturer = value

    manufacturer = property(get_manufacturer, set_manufacturer,
                           doc='Manufacturer')

    def get_model(self):
        """
        Returns the model.
        """
        return self._model

    def set_model(self, value):
        """
        Sets the model.
        
        :arg value: model
        """
        if value is None:
            raise ValueError('Model is required')
        self._model = value

    model = property(get_model, set_model, doc='Model')

    def get_serial_number(self):
        """
        Returns the serial number.
        """
        return self._serial_number

    def set_serial_number(self, value):
        """
        Sets the serial number.
        
        :arg value: serial number
        """
        self._serial_number = value

    serial_number = property(get_serial_number, set_serial_number,
                           doc='Serial number')
