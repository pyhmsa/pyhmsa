#!/usr/bin/env python
"""
================================================================================
:mod:`probe` -- Probe conditions
================================================================================

.. module:: probe
   :synopsis: Probe conditions

.. inheritance-diagram:: pyhmsa.condition.probe

"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.condition import _Condition
from pyhmsa.util.parameter import NumericalAttribute, EnumAttribute

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

    TEMPLATE = 'Probe'

    def __init__(self):
        """
        Describes the type and conditions of the analytical probe used to
        collect a HMSA dataset, such as settings for electron or ion columns,
        lasers, etc.
        """
        pass

class ProbeEM(_Probe):

    CLASS = 'EM'

    beam_voltage = NumericalAttribute('kV', True, 'BeamVoltage', 'beam voltage')
    beam_current = NumericalAttribute('nA', False, 'BeamCurrent', 'beam current')
    gun_type = EnumAttribute(_GUN_TYPES, False, 'GunType', 'type of gun')
    emission_current = NumericalAttribute('uA', False, 'EmissionCurrent', 'emission current')
    filament_current = NumericalAttribute('A', False, 'FilamentCurrent', 'filament current')
    extractor_bias = NumericalAttribute('V', False, 'ExtractorBias', 'extractor bias')
    beam_diameter = NumericalAttribute('um', False, 'BeamDiameter', 'beam diameter')
    chamber_pressure = NumericalAttribute('Pa', False, 'ChamberPressure', 'chamber pressure')
    gun_pressure = NumericalAttribute('Pa', False, 'GunPressure', 'gun pressure')
    scan_magnification = NumericalAttribute(None, False, 'ScanMagnification', 'scan magnficiation')
    working_distance = NumericalAttribute('mm', False, 'WorkingDistance', 'working_distance')

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
        :arg gun_type: type of gun (optional)
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

class ProbeTEM(ProbeEM):

    CLASS = 'TEM'

    lens_mode = EnumAttribute(_LENS_MODES, True, 'LensMode', 'lens mode')
    camera_magnification = NumericalAttribute(None, False, 'CameraMagnification', 'camera magnification')
    convergence_angle = NumericalAttribute('mrad', False, 'ConvergenceAngle', 'semi-angle of incident beam')

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
        :arg lens_mode: lens mode (required)
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
        :arg camera_magnification: camera magnification (optional)
        :arg convergence_angle: semi-angle of incident beam (optional)
        """
        ProbeEM.__init__(self, beam_voltage, beam_current, gun_type,
                         emission_current, filament_current, extractor_bias,
                         beam_diameter, chamber_pressure, gun_pressure,
                         scan_magnification, working_distance)

        self.lens_mode = lens_mode
        self.camera_magnification = camera_magnification
        self.convergence_angle = convergence_angle
