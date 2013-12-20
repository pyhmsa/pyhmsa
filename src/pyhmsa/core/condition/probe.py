#!/usr/bin/env python
"""
================================================================================
:mod:`probe` -- Probe conditions
================================================================================

.. module:: probe
   :synopsis: Probe conditions

.. inheritance-diagram:: pyhmsa.condition.probe

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
from pyhmsa.core.condition import _Condition, extract_numerical_value

# Globals and constants variables.

GUN_TYPE_W_FILAMENT = 'W filament'
GUN_TYPE_LAB6 = 'LaB6'
GUN_TYPE_COLD_FEG = 'Cold FEG'
GUN_TYPE_SCHOTTKY_FEG = 'Schottky FEG'

_GUN_TYPES = frozenset([GUN_TYPE_W_FILAMENT, GUN_TYPE_LAB6,
                        GUN_TYPE_COLD_FEG, GUN_TYPE_SCHOTTKY_FEG])

LENS_MODE_IMAGE = 'IMAGE'
LENS_MODE_DIFFR = 'DIFFR'
LENS_MODE_SCIMG = 'SCIMG'
LENS_MODE_SCDIF = 'SCDIF'

_LENS_MODES = frozenset([LENS_MODE_IMAGE, LENS_MODE_DIFFR, LENS_MODE_SCIMG,
                         LENS_MODE_SCDIF])

class _Probe(_Condition):

    def __init__(self):
        """
        Describes the type and conditions of the analytical probe used to 
        collect a HMSA dataset, such as settings for electron or ion columns, 
        lasers, etc. 
        """
        pass
    
class ProbeEM(_Probe):
    
    def __init__(self, beam_voltage, beam_current=None, gun_type=None,
                  emission_current=None, filament_current=None,
                  extractor_bias=None, beam_diameter=None, 
                  chamber_pressure=None, gun_pressure=None, 
                  scan_magnification=None, working_distance=None):
        """
        Describes the electron column conditions of the transmission electron 
        microscope used to collect a HMSA dataset.
        
        :arg beam_voltage: beam voltage (required)
        :arg beam_current: beam current (optional)
        :arg gun_type: gun type (optional)
        :arg emission_current: emission current (optional)
        :arg filament_current: filament current (optional)
        :arg extractor_bias: extractor bias (optional)
        :arg beam_diameter: beam diameter (optional)
        :arg chamber_pressure: chamber pressure (optional)
        :arg gun_pressure: gun pressure (optional)
        :arg scan_magnification: scan magnification (optional)
        :arg working_distance: working distance (optional)
        """
        _Probe.__init__(self)

        self.beam_voltage = beam_voltage
        self.beam_current = beam_current
        self.gun_type = gun_type
        self.emission_current = emission_current
        self.filament_current = filament_current
        self.extractor_bias = extractor_bias
        self.beam_diameter = beam_diameter
        self.chamber_pressure = chamber_pressure
        self.gun_pressure = gun_pressure
        self.scan_magnification = scan_magnification
        self.working_distance = working_distance

    def get_beam_voltage(self):
        """
        Returns the beam voltage.
        
        :return: beam voltage and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._beam_voltage

    def set_beam_voltage(self, value, unit='kV'):
        """
        Sets the beam voltage.
        
        :arg value: beam voltage
        :arg unit: unit
        """
        nv = extract_numerical_value(value, unit)
        if nv.value is None:
            raise ValueError('Beam voltage is required')
        self._beam_voltage = nv

    beam_voltage = property(get_beam_voltage, set_beam_voltage,
                            doc='Beam voltage')

    def get_beam_current(self):
        """
        Returns the beam current.
        
        :return: beam current and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._beam_current

    def set_beam_current(self, value, unit='nA'):
        """
        Sets the beam current.
        
        :arg value: beam current
        :arg unit: unit
        """
        self._beam_current = extract_numerical_value(value, unit)

    beam_current = property(get_beam_current, set_beam_current,
                            doc='Beam current')

    def get_gun_type(self):
        """
        Returns the gun type.
        
        :return: gun type, either :const:`GUN_TYPE_W_FILAMENT`, 
            :const:`GUN_TYPE_LAB6`, :const:`GUN_TYPE_COLD_FEG` or
            :const:`GUN_TYPE_SCHOTTKY_FEG`
        """
        return self._gun_type

    def set_gun_type(self, value):
        """
        Sets the gun type.
        
        :arg value: gun type, either :const:`GUN_TYPE_W_FILAMENT`, 
            :const:`GUN_TYPE_LAB6`, :const:`GUN_TYPE_COLD_FEG` or
            :const:`GUN_TYPE_SCHOTTKY_FEG`
        """
        if value is not None and value not in _GUN_TYPES:
            raise ValueError('Unknown gun type: %s' % value)
        self._gun_type = value

    gun_type = property(get_gun_type, set_gun_type, doc='Gun type')

    def get_emission_current(self):
        """
        Returns the emission current.
        
        :return: emission current and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._emission_current

    def set_emission_current(self, value, unit=u'\u00b5A'):
        """
        Sets the emission current.
        
        :arg value: emission current
        :arg unit: unit
        """
        self._emission_current = extract_numerical_value(value, unit)

    emission_current = property(get_emission_current, set_emission_current,
                                doc='Emission current')

    def get_filament_current(self):
        """
        Returns the filament current.
        
        :return: filament current and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._filament_current

    def set_filament_current(self, value, unit='A'):
        """
        Sets the filament current.
        
        :arg value: filament current
        :arg unit: unit
        """
        self._filament_current = extract_numerical_value(value, unit)

    filament_current = property(get_filament_current, set_filament_current,
                                doc='Filament current')

    def get_extractor_bias(self):
        """
        Returns the extractor bias.
        
        :return: extractor bias and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._extractor_bias

    def set_extractor_bias(self, value, unit='V'):
        """
        Sets the extractor bias.
        
        :arg value: extractor bias
        :arg unit: unit
        """
        self._extractor_bias = extract_numerical_value(value, unit)

    extractor_bias = property(get_extractor_bias, set_extractor_bias,
                              doc='Extractor bias')

    def get_beam_diameter(self):
        """
        Returns the beam diameter.
        
        :return: beam diameter and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._beam_diameter

    def set_beam_diameter(self, value, unit=u'\u00b5m'):
        """
        Sets the beam diameter.
        
        :arg value: beam diameter
        :arg unit: unit
        """
        self._beam_diameter = extract_numerical_value(value, unit)

    beam_diameter = property(get_beam_diameter, set_beam_diameter,
                             doc='Beam diameter')

    def get_chamber_pressure(self):
        """
        Returns the chamber pressure.
        
        :return: chamber pressure and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._chamber_pressure

    def set_chamber_pressure(self, value, unit='Pa'):
        """
        Sets the chamber pressure.
        
        :arg value: chamber pressure
        :arg unit: unit
        """
        self._chamber_pressure = extract_numerical_value(value, unit)

    chamber_pressure = property(get_chamber_pressure, set_chamber_pressure,
                                doc='Chamber pressure')

    def get_gun_pressure(self):
        """
        Returns the gun pressure.
        
        :return: gun pressure and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._gun_pressure

    def set_gun_pressure(self, value, unit='Pa'):
        """
        Sets the gun pressure.
        
        :arg value: gun pressure
        :arg unit: unit
        """
        self._gun_pressure = extract_numerical_value(value, unit)

    gun_pressure = property(get_gun_pressure, set_gun_pressure,
                            doc='Gun pressure')

    def get_scan_magnification(self):
        """
        Returns the scan magnification.
        
        :return: scan magnification
        """
        return self._scan_magnification

    def set_scan_magnification(self, value):
        """
        Sets the scan magnification.
        
        :arg value: scan magnification
        """
        self._scan_magnification = value

    scan_magnification = property(get_scan_magnification, set_scan_magnification,
                                  doc='Scan magnification')

    def get_working_distance(self):
        """
        Returns the working distance.
        
        :return: working distance and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._working_distance

    def set_working_distance(self, value, unit='mm'):
        """
        Sets the working distance.
        
        :arg value: working distance
        :arg unit: unit
        """
        self._working_distance = extract_numerical_value(value, unit)

    working_distance = property(get_working_distance, set_working_distance,
                                doc='Working distance')

class ProbeTEM(ProbeEM):

    def __init__(self, beam_voltage, lens_mode,
                  beam_current=None, gun_type=None,
                  emission_current=None, filament_current=None,
                  extractor_bias=None, beam_diameter=None,
                  chamber_pressure=None, gun_pressure=None,
                  scan_magnification=None, working_distance=None,
                  camera_magnification=None, convergence_angle=None):
        """
        Describes the electron column conditions of the transmission electron 
        microscope used to collect a HMSA dataset.
        
        :arg beam_voltage: beam voltage (required)
        :arg beam_current: beam current (optional)
        :arg gun_type: gun type (optional)
        :arg emission_current: emission current (optional)
        :arg filament_current: filament current (optional)
        :arg extractor_bias: extractor bias (optional)
        :arg beam_diameter: beam diameter (optional)
        :arg chamber_pressure: chamber pressure (optional)
        :arg gun_pressure: gun pressure (optional)
        :arg scan_magnification: scan magnification (optional)
        :arg working_distance: working distance (optional)
        """
        ProbeEM.__init__(self, beam_voltage, beam_current, gun_type,
                         emission_current, filament_current, extractor_bias,
                         beam_diameter, chamber_pressure, gun_pressure,
                         scan_magnification, working_distance)

        self.lens_mode = lens_mode
        self.camera_magnification = camera_magnification
        self.convergence_angle = convergence_angle

    def get_lens_mode(self):
        """
        Returns the lens mode.
        
        :return: lens mode, either :const:`LENS_MODE_IMAGE`, 
            :const:`LENS_MODE_DIFFR`, :const:`LENS_MODE_SCIMG` or
            :const:`LENS_MODE_SCDIF`
        """
        return self._lens_mode

    def set_lens_mode(self, value):
        """
        Sets the lens mode.
        
        :arg value: lens mode, either :const:`LENS_MODE_IMAGE`, 
            :const:`LENS_MODE_DIFFR`, :const:`LENS_MODE_SCIMG` or
            :const:`LENS_MODE_SCDIF`
        """
        if value is None:
            raise ValueError('Lens mode is required')
        if value not in _LENS_MODES:
            raise ValueError('Unknown lens mode: %s' % value)
        self._lens_mode = value

    lens_mode = property(get_lens_mode, set_lens_mode, doc='Lens mode')

    def get_camera_magnification(self):
        """
        Returns the camera magnification.
        
        :return: camera magnification
        """
        return self._camera_magnification

    def set_camera_magnification(self, value):
        """
        Sets the camera magnification.
        
        :arg value: camera magnification
        """
        self._camera_magnification = value

    camera_magnification = property(get_camera_magnification, set_camera_magnification,
                                  doc='Camera magnification')

    def get_convergence_angle(self):
        """
        Returns the convergence angle, semi-angle of incident beam.
        
        :return: convergence angle and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._convergence_angle

    def set_convergence_angle(self, value, unit='mrad'):
        """
        Sets the convergence angle, semi-angle of incident beam.
        
        :arg value: convergence angle
        :arg unit: unit
        """
        self._convergence_angle = extract_numerical_value(value, unit)

    convergence_angle = property(get_convergence_angle, set_convergence_angle,
                                 doc='Semi-angle of incident beam.')
