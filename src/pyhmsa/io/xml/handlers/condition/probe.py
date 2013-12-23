#!/usr/bin/env python
"""
================================================================================
:mod:`probe` -- XML handler for probe condition
================================================================================

.. module:: probe
   :synopsis: XML handler for probe condition

.. inheritance-diagram:: probe

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.
from pyhmsa.core.condition.probe import _Probe, ProbeEM, ProbeTEM
from pyhmsa.io.xml.handler import _XMLHandler
from pyhmsa.io.xml.handlers.type.numerical import NumericalXMLHandler

# Globals and constants variables.

class _ProbeXMLHandler(_XMLHandler):

    def __init__(self):
        _XMLHandler.__init__(self)
        self._handler_numerical = NumericalXMLHandler()

    def can_parse(self, element):
        return element.tag == 'Probe'

    def from_xml(self, element):
        return _Probe()

    def can_convert(self, obj):
        return isinstance(obj, _Probe)

    def to_xml(self, obj):
        return etree.Element('Probe')

class ProbeEMXMLHandler(_ProbeXMLHandler):

    def can_parse(self, element):
        if not _ProbeXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'EM'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('BeamVoltage')
        kwargs['beam_voltage'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('BeamCurrent')
        if subelement is not None:
            kwargs['beam_current'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('GunType')
        if subelement is not None:
            kwargs['gun_type'] = subelement.text

        subelement = element.find('EmissionCurrent')
        if subelement is not None:
            kwargs['emission_current'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('FilamentCurrent')
        if subelement is not None:
            kwargs['filament_current'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('ExtractorBias')
        if subelement is not None:
            kwargs['extractor_bias'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('BeamDiameter')
        if subelement is not None:
            kwargs['beam_diameter'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('ChamberPressure')
        if subelement is not None:
            kwargs['chamber_pressure'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('GunPressure')
        if subelement is not None:
            kwargs['gun_pressure'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('ScanMagnification')
        if subelement is not None:
            kwargs['scan_magnification'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('WorkingDistance')
        if subelement is not None:
            kwargs['working_distance'] = self._handler_numerical.from_xml(subelement)

        obj = ProbeEM(**kwargs)
        obj.__dict__.update(_ProbeXMLHandler.from_xml(self, element).__dict__)
        return obj

    def can_convert(self, obj):
        return isinstance(obj, ProbeEM)

    def to_xml(self, obj):
        element = _ProbeXMLHandler.to_xml(self, obj)
        element.set('Class', 'EM')

        subelement = self._handler_numerical.to_xml(obj.beam_voltage)
        subelement.tag = 'BeamVoltage'
        element.append(subelement)

        if obj.beam_current:
            subelement = self._handler_numerical.to_xml(obj.beam_current)
            subelement.tag = 'BeamCurrent'
            element.append(subelement)

        if obj.gun_type:
            subelement = etree.Element('GunType')
            subelement.text = obj.gun_type
            element.append(subelement)

        if obj.emission_current:
            subelement = self._handler_numerical.to_xml(obj.emission_current)
            subelement.tag = 'EmissionCurrent'
            element.append(subelement)

        if obj.filament_current:
            subelement = self._handler_numerical.to_xml(obj.filament_current)
            subelement.tag = 'FilamentCurrent'
            element.append(subelement)

        if obj.extractor_bias:
            subelement = self._handler_numerical.to_xml(obj.extractor_bias)
            subelement.tag = 'ExtractorBias'
            element.append(subelement)

        if obj.beam_diameter:
            subelement = self._handler_numerical.to_xml(obj.beam_diameter)
            subelement.tag = 'BeamDiameter'
            element.append(subelement)

        if obj.chamber_pressure:
            subelement = self._handler_numerical.to_xml(obj.chamber_pressure)
            subelement.tag = 'ChamberPressure'
            element.append(subelement)

        if obj.gun_pressure:
            subelement = self._handler_numerical.to_xml(obj.gun_pressure)
            subelement.tag = 'GunPressure'
            element.append(subelement)

        if obj.scan_magnification:
            subelement = self._handler_numerical.to_xml(obj.scan_magnification)
            subelement.tag = 'ScanMagnification'
            element.append(subelement)

        if obj.working_distance:
            subelement = self._handler_numerical.to_xml(obj.working_distance)
            subelement.tag = 'WorkingDistance'
            element.append(subelement)

        return element

class ProbeTEMXMLHandler(ProbeEMXMLHandler):

    def can_parse(self, element):
        if not _ProbeXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'TEM'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('LensMode')
        kwargs['lens_mode'] = subelement.text

        subelement = element.find('CameraMagnification')
        if subelement is not None:
            kwargs['camera_magnification'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('ConvergenceAngle')
        if subelement is not None:
            kwargs['convergence_angle'] = self._handler_numerical.from_xml(subelement)

        parent = ProbeEMXMLHandler.from_xml(self, element)
        obj = ProbeTEM(parent.beam_voltage, **kwargs)
        obj.__dict__.update(parent.__dict__)
        return obj

    def can_convert(self, obj):
        return isinstance(obj, ProbeTEM)

    def to_xml(self, obj):
        element = ProbeEMXMLHandler.to_xml(self, obj)
        element.set('Class', 'TEM')

        subelement = etree.Element('LensMode')
        subelement.text = obj.lens_mode
        element.append(subelement)

        if obj.camera_magnification:
            subelement = self._handler_numerical.to_xml(obj.camera_magnification)
            subelement.tag = 'CameraMagnification'
            element.append(subelement)

        if obj.convergence_angle:
            subelement = self._handler_numerical.to_xml(obj.convergence_angle)
            subelement.tag = 'ConvergenceAngle'
            element.append(subelement)

        return element
