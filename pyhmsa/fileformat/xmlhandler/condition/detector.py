#!/usr/bin/env python
"""
================================================================================
:mod:`detector` -- XML handler for detectors
================================================================================

.. module:: detector
   :synopsis: XML handler for detectors

.. inheritance-diagram:: detector

"""

# Standard library modules.

# Third party modules.
from pkg_resources import iter_entry_points

# Local modules.
from pyhmsa.spec.condition.detector import \
    (DetectorCamera, DetectorSpectrometer, DetectorSpectrometerCL,
     DetectorSpectrometerWDS, DetectorSpectrometerXEDS, Window, WindowLayer)
from pyhmsa.fileformat.xmlhandler.xmlhandler import _XMLHandler

# Globals and constants variables.

class WindowXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'Window'

    def parse(self, element):
        obj = self._parse_parameter(element, Window)

        for subelement in element.findall('Layer'):
            material = subelement.attrib['Material']
            thickness = self._parse_numerical_attribute(subelement)
            obj.layers.append(WindowLayer(material, thickness))

        return obj

    def can_convert(self, obj):
        return type(obj) is Window

    def convert(self, obj):
        element = self._convert_parameter(obj, 'Window')

        for layer in obj.layers:
            value = layer.thickness
            attrib = type('MockAttribute', (object,), {'xmlname': 'Layer'})
            subelement = self._convert_numerical_attribute(value, attrib)[0]
            subelement.set('Material', layer.material)
            element.append(subelement)

        return element

class DetectorCameraXMLHandler(_XMLHandler):

    def can_parse(self, element):
        return element.tag == 'Detector' and element.get('Class') == 'Camera'

    def parse(self, element):
        return self._parse_parameter(element, DetectorCamera)

    def can_convert(self, obj):
        return type(obj) is DetectorCamera

    def convert(self, obj):
        return self._convert_parameter(obj, 'Detector', {'Class': 'Camera'})

class _DetectorSpectrometerXMLHandler(_XMLHandler):

    def __init__(self, version):
        _XMLHandler.__init__(self, version)
        self._handler_window = WindowXMLHandler(version)

    def _parse_calibration(self, element):
        subelement = element.find('Calibration')
        if subelement is None:
            raise ValueError('Element Calibration is missing')

        # Load handlers
        handlers = set()
        for entry_point in iter_entry_points('pyhmsa.fileformat.xmlhandler.condition.calibration'):
            handler = entry_point.load()(self.version)
            handlers.add(handler)

        # Find handler
        handlers = list(filter(lambda h: h.can_parse(subelement), handlers))
        if not handlers: # pragma: no cover
            raise ValueError('No handler found to parse calibration')

        return handlers[0].parse(subelement)

    def _parse_window(self, element):
        subelement = element.find('Window')
        if subelement is None:
            return Window()
        return self._handler_window.parse(subelement)

    def _convert_calibration(self, obj):
        # Load handlers
        handlers = set()
        for entry_point in iter_entry_points('pyhmsa.fileformat.xmlhandler.condition.calibration'):
            handler = entry_point.load()(self.version)
            handlers.add(handler)

        # Find handler
        handlers = list(filter(lambda h: h.can_convert(obj.calibration), handlers))
        if not handlers: # pragma: no cover
            raise ValueError('No handler found to convert calibration')

        return [handlers[0].convert(obj.calibration)]

    def _convert_window(self, obj):
        return [self._handler_window.convert(obj.window)]

class DetectorSpectrometerXMLHandler(_DetectorSpectrometerXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Detector' and element.get('Class') == 'Spectrometer'

    def parse(self, element):
        obj = self._parse_parameter(element, DetectorSpectrometer)
        obj.calibration = self._parse_calibration(element)
        return obj

    def can_convert(self, obj):
        return type(obj) is DetectorSpectrometer

    def convert(self, obj):
        element = self._convert_parameter(obj, 'Detector', {'Class': 'Spectrometer'})
        element.extend(self._convert_calibration(obj))
        return element

class DetectorSpectrometerCLXMLHandler(_DetectorSpectrometerXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Detector' and element.get('Class') == 'Spectrometer/CL'

    def parse(self, element):
        obj = self._parse_parameter(element, DetectorSpectrometerCL)
        obj.calibration = self._parse_calibration(element)
        return obj

    def can_convert(self, obj):
        return type(obj) is DetectorSpectrometerCL

    def convert(self, obj):
        element = self._convert_parameter(obj, 'Detector', {'Class': 'Spectrometer/CL'})
        element.extend(self._convert_calibration(obj))
        return element

class DetectorSpectrometerWDSXMLHandler(_DetectorSpectrometerXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Detector' and element.get('Class') == 'Spectrometer/WDS'

    def parse(self, element):
        obj = self._parse_parameter(element, DetectorSpectrometerWDS)
        obj.calibration = self._parse_calibration(element)
        obj.window = self._parse_window(element)
        return obj

    def can_convert(self, obj):
        return type(obj) is DetectorSpectrometerWDS

    def convert(self, obj):
        element = self._convert_parameter(obj, 'Detector', {'Class': 'Spectrometer/WDS'})
        element.extend(self._convert_calibration(obj))
        element.extend(self._convert_window(obj))
        return element

class DetectorSpectrometerXEDSXMLHandler(_DetectorSpectrometerXMLHandler):

    def can_parse(self, element):
        return element.tag == 'Detector' and element.get('Class') == 'Spectrometer/XEDS'

    def parse(self, element):
        obj = self._parse_parameter(element, DetectorSpectrometerXEDS)
        obj.calibration = self._parse_calibration(element)
        obj.window = self._parse_window(element)
        return obj

    def can_convert(self, obj):
        return type(obj) is DetectorSpectrometerXEDS

    def convert(self, obj):
        element = self._convert_parameter(obj, 'Detector', {'Class': 'Spectrometer/XEDS'})
        element.extend(self._convert_calibration(obj))
        element.extend(self._convert_window(obj))
        return element
