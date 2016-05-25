"""
XML handler for detectors
"""

# Standard library modules.

# Third party modules.
from pkg_resources import iter_entry_points

# Local modules.
from pyhmsa.spec.condition.detector import \
    (DetectorCamera, DetectorSpectrometer, DetectorSpectrometerCL,
     DetectorSpectrometerWDS, DetectorSpectrometerXEDS, Window, WindowLayer)
from pyhmsa.fileformat.xmlhandler.xmlhandler import _XMLHandler
from pyhmsa.fileformat.xmlhandler.condition.condition import _ConditionXMLHandler

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

class DetectorCameraXMLHandler(_ConditionXMLHandler):

    def __init__(self, version):
        super().__init__(DetectorCamera, version)

class _DetectorSpectrometerXMLHandler(_ConditionXMLHandler):

    def __init__(self, clasz, version):
        super().__init__(clasz, version)
        self._handler_window = WindowXMLHandler(version)

    def _parse_calibration(self, element):
        subelement = element.find('Calibration')
        if subelement is None:
            raise ValueError('Element Calibration is missing')

        # Load handlers
        handlers = set()
        for entry_point in iter_entry_points('pyhmsa.fileformat.xmlhandler.condition.calibration'):
            handler_class = entry_point.resolve()
            handler = handler_class(self.version)
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

    def parse(self, element):
        obj = super().parse(element)
        obj.calibration = self._parse_calibration(element)
        return obj

    def _convert_calibration(self, obj):
        # Load handlers
        handlers = set()
        for entry_point in iter_entry_points('pyhmsa.fileformat.xmlhandler.condition.calibration'):
            handler_class = entry_point.resolve()
            handler = handler_class(self.version)
            handlers.add(handler)

        # Find handler
        handlers = list(filter(lambda h: h.can_convert(obj.calibration), handlers))
        if not handlers: # pragma: no cover
            raise ValueError('No handler found to convert calibration')

        return [handlers[0].convert(obj.calibration)]

    def _convert_window(self, obj):
        return [self._handler_window.convert(obj.window)]

    def convert(self, obj):
        element = super().convert(obj)
        element.extend(self._convert_calibration(obj))
        return element

class DetectorSpectrometerXMLHandler(_DetectorSpectrometerXMLHandler):

    def __init__(self, version):
        super().__init__(DetectorSpectrometer, version)

class DetectorSpectrometerCLXMLHandler(_DetectorSpectrometerXMLHandler):

    def __init__(self, version):
        super().__init__(DetectorSpectrometerCL, version)

class DetectorSpectrometerWDSXMLHandler(_DetectorSpectrometerXMLHandler):

    def __init__(self, version):
        super().__init__(DetectorSpectrometerWDS, version)

    def parse(self, element):
        obj = super().parse(element)
        obj.window = self._parse_window(element)
        return obj

    def convert(self, obj):
        element = super().convert(obj)
        element.extend(self._convert_window(obj))
        return element

class DetectorSpectrometerXEDSXMLHandler(_DetectorSpectrometerXMLHandler):

    def __init__(self, version):
        super().__init__(DetectorSpectrometerXEDS, version)

    def parse(self, element):
        obj = super().parse(element)
        obj.window = self._parse_window(element)
        return obj

    def convert(self, obj):
        element = super().convert(obj)
        element.extend(self._convert_window(obj))
        return element
