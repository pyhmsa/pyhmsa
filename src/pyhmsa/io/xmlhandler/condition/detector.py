#!/usr/bin/env python
"""
================================================================================
:mod:`detector` -- XML handler for detectors
================================================================================

.. module:: detector
   :synopsis: XML handler for detectors

.. inheritance-diagram:: detector

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
from pyhmsa.spec.condition.detector import \
    (DetectorCamera, DetectorSpectrometer, DetectorSpectrometerCL,
     DetectorSpectrometerWDS, DetectorSpectrometerXEDS, Window, WindowLayer)
from pyhmsa.io.xmlhandler import _XMLHandler
from pyhmsa.io.xmlhandler.condition.calibration import \
    (CalibrationConstantXMLHandler, CalibrationLinearXMLHandler,
     CalibrationPolynomialXMLHandler, CalibrationExplicitXMLHandler)

# Globals and constants variables.

class WindowXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'Window'

    def from_xml(self, element):
        obj = self._parse_parameter(element, Window)

        for subelement in element.findall('Layer'):
            material = subelement.attrib['Material']
            thickness = self._parse_numerical_attribute(subelement)
            obj.layers.append(WindowLayer(material, thickness))

        return obj

    def can_convert(self, obj):
        return isinstance(obj, Window)

    def to_xml(self, obj):
        element = self._convert_parameter(obj, etree.Element('Window'))

        for layer in obj.layers:
            value = layer.thickness
            attrib = type('MockAttribute', (object,), {'xmlname': 'Layer'})
            subelement = self._convert_numerical_attribute(value, attrib)
            subelement.set('Material', layer.material)
            element.append(subelement)

        return element

class DetectorCameraXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'Detector' and element.get('Class') == 'Camera'

    def from_xml(self, element):
        return self._parse_parameter(element, DetectorCamera)

    def can_convert(self, obj):
        return isinstance(obj, DetectorCamera)

    def to_xml(self, obj):
        element = etree.Element('Detector', {'Class': 'Camera'})
        return self._convert_parameter(obj, element)

class _DetectorSpectrometerXMLHandler(_XMLHandler):

    def __init__(self, version):
        _XMLHandler.__init__(self, version)
        self._handlers_calibration = \
            [CalibrationConstantXMLHandler(version),
             CalibrationLinearXMLHandler(version),
             CalibrationPolynomialXMLHandler(version),
             CalibrationExplicitXMLHandler(version)]
        self._handler_window = WindowXMLHandler(version)

    def _parse_calibration(self, element):
        subelement = element.find('Calibration')
        if subelement is None:
            raise ValueError('Element Calibration is missing')

        handler = list(filter(lambda h: h.can_parse(subelement),
                              self._handlers_calibration))
        if not handler: # pragma: no cover
            raise ValueError('No handler found to parse calibration')

        return handler[0].from_xml(subelement)

    def _parse_window(self, element):
        subelement = element.find('Window')
        if subelement is None:
            return Window()
        return self._handler_window.from_xml(subelement)

    def _convert_calibration(self, value, element):
        handler = list(filter(lambda h: h.can_convert(value),
                              self._handlers_calibration))
        if not handler: # pragma: no cover
            raise ValueError('No handler found to convert calibration')

        subelement = handler[0].to_xml(value)
        element.append(subelement)
        return element

    def _convert_window(self, value, element):
        if value is None: # pragma: no cover
            return element
        element.append(self._handler_window.to_xml(value))
        return element

class DetectorSpectrometerXMLHandler(_DetectorSpectrometerXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Detector' and element.get('Class') == 'Spectrometer'

    def from_xml(self, element):
        obj = self._parse_parameter(element, DetectorSpectrometer)
        obj.calibration = self._parse_calibration(element)
        return obj

    def can_convert(self, obj):
        return isinstance(obj, DetectorSpectrometer)

    def to_xml(self, obj):
        element = etree.Element('Detector', {'Class': 'Spectrometer'})
        element = self._convert_parameter(obj, element)
        element = self._convert_calibration(obj.calibration, element)
        return element

class DetectorSpectrometerCLXMLHandler(_DetectorSpectrometerXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Detector' and element.get('Class') == 'Spectrometer/CL'

    def from_xml(self, element):
        obj = self._parse_parameter(element, DetectorSpectrometerCL)
        obj.calibration = self._parse_calibration(element)
        return obj

    def can_convert(self, obj):
        return isinstance(obj, DetectorSpectrometerCL)

    def to_xml(self, obj):
        element = etree.Element('Detector', {'Class': 'Spectrometer/CL'})
        element = self._convert_parameter(obj, element)
        element = self._convert_calibration(obj.calibration, element)
        return element

class DetectorSpectrometerWDSXMLHandler(_DetectorSpectrometerXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Detector' and element.get('Class') == 'Spectrometer/WDS'

    def from_xml(self, element):
        obj = self._parse_parameter(element, DetectorSpectrometerWDS)
        obj.calibration = self._parse_calibration(element)
        obj.window = self._parse_window(element)
        return obj

    def can_convert(self, obj):
        return isinstance(obj, DetectorSpectrometerWDS)

    def to_xml(self, obj):
        element = etree.Element('Detector', {'Class': 'Spectrometer/WDS'})
        element = self._convert_parameter(obj, element)
        element = self._convert_calibration(obj.calibration, element)
        element = self._convert_window(obj.window, element)
        return element

class DetectorSpectrometerXEDSXMLHandler(_DetectorSpectrometerXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Detector' and element.get('Class') == 'Spectrometer/XEDS'

    def from_xml(self, element):
        obj = self._parse_parameter(element, DetectorSpectrometerXEDS)
        obj.calibration = self._parse_calibration(element)
        obj.window = self._parse_window(element)
        return obj

    def can_convert(self, obj):
        return isinstance(obj, DetectorSpectrometerXEDS)

    def to_xml(self, obj):
        element = etree.Element('Detector', {'Class': 'Spectrometer/XEDS'})
        element = self._convert_parameter(obj, element)
        element = self._convert_calibration(obj.calibration, element)
        element = self._convert_window(obj.window, element)
        return element
