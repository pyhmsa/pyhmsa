#!/usr/bin/env python
"""
================================================================================
:mod:`calibration` -- Calibration of measurements
================================================================================

.. module:: calibration
   :synopsis: Calibration of measurements

.. inheritance-diagram:: pyhmsa.condition.calibration

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
from pyhmsa.type.unit import validate_unit
from pyhmsa.type.numerical import extract_value

# Globals and constants variables.

class _Calibration(object):
    
    def __init__(self, quantity, unit):
        """
        Describes the calibration of a set of measurement ordinals with respect 
        to a physical quantity, such as converting channels in an EELS spectrum 
        to energy, or steps in a WDS peak scan to position, angle, wavelength 
        or energy.
        
        :arg quantity: physical quantity (required)
        :arg unit: unit (required)
        """
        if quantity is None:
            raise ValueError('Quantity is required')
        self._quantity = quantity

        if unit is None:
            raise ValueError('Unit is required')
        validate_unit(unit)
        self._unit = unit

    def get_quantity(self):
        """
        Returns the quantity, the physical quantity of the calibration object, 
        such as "Energy", "Wavelength", "Position", etc.
        
        :return: quantity
        :rtype: :class:`str`
        """
        return self._quantity

    quantity = property(get_quantity, doc='Physical quantity')

    def get_unit(self):
        """
        Returns the unit.
        
        :return: unit
        :rtype: :class:`str` 
        """
        return self._unit

    unit = property(get_unit, doc='Unit')

class CalibrationConstant(_Calibration):

    def __init__(self, quantity, unit, value):
        """
        Defines the energy/wavelength/etc calibration of a spectrometer or other 
        measurement device operating at a fixed position, such as a CL 
        monochromator.
        
        :arg quantity: physical quantity (required)
        :arg unit: unit (required)
        :arg value: value (required)
        """
        _Calibration.__init__(self, quantity, unit)

        if value is None:
            raise ValueError('Value is required')
        self._value = extract_value(value)

    def get_value(self):
        """
        Returns the constant value.
        
        :return: value
        """
        return self._value

    value = property(get_value, doc='Value')

class CalibrationLinear(_Calibration):

    def __init__(self, quantity, unit, gain, offset):
        """
        Defines the energy/wavelength/etc calibration of a spectrometer or 
        other measurement device, for which the measurement ordinals (e.g. 
        channel numbers) have a linear relationship to the physical quantity 
        (e.g. nm), with a constant offset and gain.
        
        :arg quantity: physical quantity (required)
        :arg unit: unit (required)
        :arg gain: gain (required)
        :arg offset: offset, the calibration value (energy, wavelength, 
            position, etc.) corresponding to the first measurement ordinal
            (required)
        """
        _Calibration.__init__(self, quantity, unit)

        if gain is None:
            raise ValueError('Gain is required')
        self._gain = extract_value(gain)

        if offset is None:
            raise ValueError('Offset is required')
        self._offset = extract_value(offset)

    def get_gain(self):
        """
        Returns the gain.
        
        :return: gain
        """
        return self._gain

    gain = property(get_gain, doc='Gain')

    def get_offset(self):
        """
        Returns the offset, the calibration value (energy, wavelength, 
        position, etc.) corresponding to the first measurement ordinal.
        
        :return: offset
        """
        return self._offset

    offset = property(get_offset,
                      doc='Calibration value corresponding to the first measurement ordinal')

class CalibrationPolynomial(_Calibration):

    def __init__(self, quantity, unit, coefficients):
        """
        Defines the energy/wavelength/etc calibration of a spectrometer or 
        other measurement device, for which the measurement ordinals (e.g. 
        channel numbers) have a relationship to the physical quantity (e.g. nm) 
        that may be modelled by an nth order polynomial.
        
        :arg quantity: physical quantity (required)
        :arg unit: unit (required)
        :arg coefficients: iterable of coefficients (required)
        """
        _Calibration.__init__(self, quantity, unit)

        if coefficients is None:
            raise ValueError('Coefficients are required')
        if len(coefficients) == 0:
            raise ValueError('At least one coefficient must be given')
        self._coefficients = extract_value(coefficients)
    
    def get_coefficients(self):
        """
        Returns the polynomial coefficients.
        
        :return: coefficients
        :rtype: :class:`tuple`
        """
        return self._coefficients

    coefficients = property(get_coefficients, doc='Polynomial coefficients')

class CalibrationExplicit(_Calibration):

    def __init__(self, quantity, unit, values):
        """
        Defines the energy/wavelength/etc calibration of a spectrometer or 
        other measurement device, for which relationship between the measurement 
        ordinals (e.g. channel numbers) and physical quantity (e.g. nm) cannot 
        be adequately modelled by linear or polynomial functions, and therefore 
        must be declared explicitly for each ordinal as an array of floating 
        point values.
        
        :arg quantity: physical quantity (required)
        :arg unit: unit (required)
        :arg values: explicit values (required)
        """
        _Calibration.__init__(self, quantity, unit)

        if values is None:
            raise ValueError('Values are required')
        if len(values) == 0:
            raise ValueError('At least one value must be given')
        self._values = extract_value(values)

    def get_values(self):
        """
        Returns the explicit values.
        
        :return: values
        :rtype: :class:`tuple`
        """
        return self._values

    values = property(get_values, doc='Explicit values')
