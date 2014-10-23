#!/usr/bin/env python
"""
================================================================================
:mod:`calibration` -- Calibration of measurements
================================================================================

.. module:: calibration
   :synopsis: Calibration of measurements

.. inheritance-diagram:: pyhmsa.condition.calibration

"""

# Standard library modules.
import bisect

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.util.parameter import \
    (Parameter, TextAttribute, NumericalAttribute, UnitAttribute,
     OrderedNumericalAttribute, TextListAttribute)

# Globals and constants variables.

class _Calibration(Parameter):

    quantity = TextAttribute(True, 'Quantity', 'physical quantity')
    unit = UnitAttribute(None, True, 'Unit', 'unit')

    def __init__(self, quantity, unit):
        """
        Describes the calibration of a set of measurement ordinals with respect
        to a physical quantity, such as converting channels in an EELS spectrum
        to energy, or steps in a WDS peak scan to position, angle, wavelength
        or energy.

        :arg quantity: physical quantity such as "Energy", "Wavelength",
            "Position", etc. (required)
        :arg unit: unit (required)
        """
        self.quantity = quantity
        self.unit = unit

    def __call__(self, index):
        return self.get_quantity(index)

    def get_quantity(self, index):
        raise NotImplementedError

    def get_index(self, value):
        raise NotImplementedError

class CalibrationConstant(_Calibration):

    value = NumericalAttribute(None, True, "Value", "constant value")

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

        self.value = value

    def get_quantity(self, index):
        return self.value

    def get_index(self, value):
        return 0 if value == self.value else -1

class CalibrationLinear(_Calibration):

    gain = NumericalAttribute(None, True, "Gain", "gain")
    offset = NumericalAttribute(None, True, "Offset", "offset")

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

        self.gain = gain
        self.offset = offset

    def get_quantity(self, index):
        return self.func(index)

    def get_index(self, value):
        return int((self.func - value).r[0])

    @property
    def func(self):
        if not hasattr(self, '_func'):
            self._func = np.poly1d([self.gain, self.offset])
        return self._func

class CalibrationPolynomial(_Calibration):

    coefficients = NumericalAttribute(None, True, 'Coefficients', 'polynomial coefficients')

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

        self.coefficients = coefficients

    def get_quantity(self, index):
        return self.func(index)

    def get_index(self, value):
        for root in (self.func - value).r:
            if not np.iscomplex(root) and root >= 0:
                return int(np.real(root))
        return -1

    @property
    def func(self):
        if not hasattr(self, '_func'):
            self._func = np.poly1d(self.coefficients)
        return self._func

class CalibrationExplicit(_Calibration):

    values = OrderedNumericalAttribute(None, True, "Values", "explicit values")
    labels = TextListAttribute(False, 'Labels', 'text labels for each of the calibration points')

    def __init__(self, quantity, unit, values, labels=None):
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

        self.values = values
        self.labels = labels

    def get_quantity(self, index):
        return self.values[index]

    def get_index(self, value):
        index = bisect.bisect_left(self.values, value)
        if index != len(self.values):
            return index
        return -1

    def get_label(self, index):
        if self.labels is None:
            return None
        return self.labels[index]
