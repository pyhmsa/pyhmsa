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
from pyhmsa.core.condition.detector import \
    (_Detector, DetectorCamera, DetectorSpectrometer, DetectorSpectrometerCL,
     DetectorSpectrometerWDS, DetectorSpectrometerXEDS, PulseHeightAnalyser,
     Window, WindowLayer)
from pyhmsa.io.xml.handler import _XMLHandler
from pyhmsa.io.xml.handlers.type.numerical import NumericalXMLHandler
from pyhmsa.io.xml.handlers.condition.calibration import \
    (CalibrationConstantXMLHandler, CalibrationLinearXMLHandler, 
     CalibrationPolynomialXMLHandler, CalibrationExplicitXMLHandler)

# Globals and constants variables.

class PulseHeightAnalyserXMLHandler(_XMLHandler):

    def __init__(self):
        _XMLHandler.__init__(self)
        self._handler_numerical = NumericalXMLHandler()

    def can_parse(self, element):
        return element.tag == 'PulseHeightAnalyser'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('Bias')
        if subelement is not None:
            kwargs['bias'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('Gain')
        if subelement is not None:
            kwargs['gain'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('BaseLevel')
        if subelement is not None:
            kwargs['base_level'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('Window')
        if subelement is not None:
            kwargs['window'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('Mode')
        if subelement is not None:
            kwargs['mode'] = subelement.text

        return PulseHeightAnalyser(**kwargs)

    def can_convert(self, obj):
        return isinstance(obj, PulseHeightAnalyser)

    def to_xml(self, obj):
        element = etree.Element('PulseHeightAnalyser')

        if obj.bias:
            subelement = self._handler_numerical.to_xml(obj.bias)
            subelement.tag = 'Bias'
            element.append(subelement)

        if obj.gain:
            subelement = self._handler_numerical.to_xml(obj.gain)
            subelement.tag = 'Gain'
            element.append(subelement)

        if obj.base_level:
            subelement = self._handler_numerical.to_xml(obj.base_level)
            subelement.tag = 'BaseLevel'
            element.append(subelement)

        if obj.window:
            subelement = self._handler_numerical.to_xml(obj.window)
            subelement.tag = 'Window'
            element.append(subelement)

        if obj.mode:
            subelement = etree.Element('Mode')
            subelement.text = obj.mode
            element.append(subelement)

        return element

class WindowXMLHandler(_XMLHandler):

    def __init__(self):
        _XMLHandler.__init__(self)
        self._handler_numerical = NumericalXMLHandler()

    def can_parse(self, element):
        return element.tag == 'Window'

    def from_xml(self, element):
        layers = []
        for subelement in element.findall('Layer'):
            material = subelement.attrib['Material']
            thickness = self._handler_numerical.from_xml(subelement)
            layers.append(WindowLayer(material, thickness))

        return Window(layers)

    def can_convert(self, obj):
        return isinstance(obj, Window)

    def to_xml(self, obj):
        element = etree.Element('Window')

        for layer in obj.layers:
            subelement = self._handler_numerical.to_xml(layer.thickness)
            subelement.tag = 'Layer'
            subelement.set('Material', layer.material)
            element.append(subelement)

        return element

class _DetectorXMLHandler(_XMLHandler):

    def __init__(self):
        _XMLHandler.__init__(self)
        self._handler_numerical = NumericalXMLHandler()

    def can_parse(self, element):
        return element.tag == 'Detector'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('SignalType')
        if subelement is not None:
            kwargs['signal_type'] = subelement.text

        subelement = element.find('Manufacturer')
        if subelement is not None:
            kwargs['manufacturer'] = subelement.text

        subelement = element.find('Model')
        if subelement is not None:
            kwargs['model'] = subelement.text

        subelement = element.find('SerialNumber')
        if subelement is not None:
            kwargs['serial_number'] = subelement.text

        subelement = element.find('MeasurementUnit')
        if subelement is not None:
            kwargs['measurement_unit'] = subelement.text

        subelement = element.find('Elevation')
        if subelement is not None:
            kwargs['elevation'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('Azimuth')
        if subelement is not None:
            kwargs['azimuth'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('Distance')
        if subelement is not None:
            kwargs['distance'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('Area')
        if subelement is not None:
            kwargs['area'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('SolidAngle')
        if subelement is not None:
            kwargs['solid_angle'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('SemiAngle')
        if subelement is not None:
            kwargs['semi_angle'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('Temperature')
        if subelement is not None:
            kwargs['temperature'] = self._handler_numerical.from_xml(subelement)

        return _Detector(**kwargs)

    def can_convert(self, obj):
        return isinstance(obj, _Detector)

    def to_xml(self, obj):
        element = etree.Element('Detector')

        if obj.signal_type:
            subelement = etree.Element('SignalType')
            subelement.text = obj.signal_type
            element.append(subelement)

        if obj.manufacturer:
            subelement = etree.Element('Manufacturer')
            subelement.text = obj.manufacturer
            element.append(subelement)

        if obj.model:
            subelement = etree.Element('Model')
            subelement.text = obj.model
            element.append(subelement)

        if obj.serial_number:
            subelement = etree.Element('SerialNumber')
            subelement.text = obj.serial_number
            element.append(subelement)

        if obj.measurement_unit:
            subelement = etree.Element('MeasurementUnit')
            subelement.text = obj.measurement_unit
            element.append(subelement)

        if obj.elevation:
            subelement = self._handler_numerical.to_xml(obj.elevation)
            subelement.tag = 'Elevation'
            element.append(subelement)

        if obj.azimuth:
            subelement = self._handler_numerical.to_xml(obj.azimuth)
            subelement.tag = 'Azimuth'
            element.append(subelement)

        if obj.distance:
            subelement = self._handler_numerical.to_xml(obj.distance)
            subelement.tag = 'Distance'
            element.append(subelement)

        if obj.area:
            subelement = self._handler_numerical.to_xml(obj.area)
            subelement.tag = 'Area'
            element.append(subelement)

        if obj.solid_angle:
            subelement = self._handler_numerical.to_xml(obj.solid_angle)
            subelement.tag = 'SolidAngle'
            element.append(subelement)

        if obj.semi_angle:
            subelement = self._handler_numerical.to_xml(obj.semi_angle)
            subelement.tag = 'SemiAngle'
            element.append(subelement)

        if obj.temperature:
            subelement = self._handler_numerical.to_xml(obj.temperature)
            subelement.tag = 'Temperature'
            element.append(subelement)

        return element

class DetectorCameraXMLHandler(_DetectorXMLHandler):

    def can_parse(self, element):
        if not _DetectorXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'Camera'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('UPixelCount')
        kwargs['pixel_count_u'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('VPixelCount')
        kwargs['pixel_count_v'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('ExposureTime')
        if subelement is not None:
            kwargs['exposure_time'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('Magnification')
        if subelement is not None:
            kwargs['magnification'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('FocalLength')
        if subelement is not None:
            kwargs['focal_length'] = self._handler_numerical.from_xml(subelement)

        obj = DetectorCamera(**kwargs)
        obj.__dict__.update(_DetectorXMLHandler.from_xml(self, element).__dict__)
        return obj

    def can_convert(self, obj):
        if not _DetectorXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, DetectorCamera)

    def to_xml(self, obj):
        element = _DetectorXMLHandler.to_xml(self, obj)
        element.set('Class', 'Camera')

        subelement = self._handler_numerical.to_xml(obj.pixel_count_u)
        subelement.tag = 'UPixelCount'
        element.append(subelement)

        subelement = self._handler_numerical.to_xml(obj.pixel_count_v)
        subelement.tag = 'VPixelCount'
        element.append(subelement)

        if obj.exposure_time:
            subelement = self._handler_numerical.to_xml(obj.exposure_time)
            subelement.tag = 'ExposureTime'
            element.append(subelement)

        if obj.magnification:
            subelement = self._handler_numerical.to_xml(obj.magnification)
            subelement.tag = 'Magnification'
            element.append(subelement)

        if obj.focal_length:
            subelement = self._handler_numerical.to_xml(obj.focal_length)
            subelement.tag = 'FocalLength'
            element.append(subelement)

        return element

class DetectorSpectrometerXMLHandler(_DetectorXMLHandler):

    def __init__(self):
        _DetectorXMLHandler.__init__(self)
        self._handlers_calibration = \
            [CalibrationConstantXMLHandler(), CalibrationLinearXMLHandler(),
             CalibrationPolynomialXMLHandler(), CalibrationExplicitXMLHandler()]

    def can_parse(self, element):
        if not _DetectorXMLHandler.can_parse(self, element):
            return False
        return element.get('Class', '').startswith('Spectrometer')

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('ChannelCount')
        kwargs['channel_count'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('Calibration')
        handler = list(filter(lambda h: h.can_parse(subelement),
                              self._handlers_calibration))
        if not handler: # pragma: no cover
            raise ValueError('No handler found to parse calibration')
        kwargs['calibration'] = handler[0].from_xml(subelement)

        subelement = element.find('CollectionMode')
        if subelement is not None:
            kwargs['collection_mode'] = subelement.text

        obj = DetectorSpectrometer(**kwargs)
        obj.__dict__.update(_DetectorXMLHandler.from_xml(self, element).__dict__)
        return obj

    def can_convert(self, obj):
        if not _DetectorXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, DetectorSpectrometer)

    def to_xml(self, obj):
        element = _DetectorXMLHandler.to_xml(self, obj)
        element.set('Class', 'Spectrometer')

        subelement = self._handler_numerical.to_xml(obj.channel_count)
        subelement.tag = 'ChannelCount'
        element.append(subelement)

        handler = list(filter(lambda h: h.can_convert(obj.calibration),
                              self._handlers_calibration))
        if not handler: # pragma: no cover
            raise ValueError('No handler found to convert calibration')
        subelement = handler[0].to_xml(obj.calibration)
        element.append(subelement)

        if obj.collection_mode:
            subelement = etree.Element('CollectionMode')
            subelement.text = obj.collection_mode
            element.append(subelement)

        return element

class DetectorSpectrometerCLXMLHandler(DetectorSpectrometerXMLHandler):

    def can_parse(self, element):
        if not DetectorSpectrometerXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'Spectrometer/CL'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('Grating-d')
        if subelement is not None:
            kwargs['grating_d'] = self._handler_numerical.from_xml(subelement)

        parent = DetectorSpectrometerXMLHandler.from_xml(self, element)
        obj = DetectorSpectrometerCL(parent.channel_count, parent.calibration,
                                     **kwargs)
        obj.__dict__.update(parent.__dict__)
        return obj

    def can_convert(self, obj):
        if not DetectorSpectrometerXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, DetectorSpectrometerCL)

    def to_xml(self, obj):
        element = DetectorSpectrometerXMLHandler.to_xml(self, obj)
        element.set('Class', 'Spectrometer/CL')

        if obj.grating_d:
            subelement = self._handler_numerical.to_xml(obj.grating_d)
            subelement.tag = 'Grating-d'
            element.append(subelement)

        return element

class DetectorSpectrometerWDSXMLHandler(DetectorSpectrometerXMLHandler):

    def __init__(self):
        DetectorSpectrometerXMLHandler.__init__(self)
        self._handler_pha = PulseHeightAnalyserXMLHandler()
        self._handler_window = WindowXMLHandler()

    def can_parse(self, element):
        if not DetectorSpectrometerXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'Spectrometer/WDS'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('DispersionElement')
        if subelement is not None:
            kwargs['dispersion_element'] = subelement.text

        subelement = element.find('Crystal-2d')
        if subelement is not None:
            kwargs['crystal_2d'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('RowlandCircleDiameter')
        if subelement is not None:
            kwargs['rowland_circle_diameter'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('PulseHeightAnalyser')
        if subelement is not None:
            kwargs['pulse_height_analyser'] = self._handler_pha.from_xml(subelement)

        subelement = element.find('Window')
        if subelement is not None:
            kwargs['window'] = self._handler_window.from_xml(subelement)

        parent = DetectorSpectrometerXMLHandler.from_xml(self, element)
        obj = DetectorSpectrometerWDS(parent.channel_count, parent.calibration,
                                      **kwargs)
        obj.__dict__.update(parent.__dict__)
        return obj

    def can_convert(self, obj):
        if not DetectorSpectrometerXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, DetectorSpectrometerWDS)

    def to_xml(self, obj):
        element = DetectorSpectrometerXMLHandler.to_xml(self, obj)
        element.set('Class', 'Spectrometer/WDS')

        if obj.dispersion_element:
            subelement = etree.Element('DispersionElement')
            subelement.text = obj.dispersion_element
            element.append(subelement)

        if obj.crystal_2d:
            subelement = self._handler_numerical.to_xml(obj.crystal_2d)
            subelement.tag = 'Crystal-2d'
            element.append(subelement)

        if obj.rowland_circle_diameter:
            subelement = self._handler_numerical.to_xml(obj.rowland_circle_diameter)
            subelement.tag = 'RowlandCircleDiameter'
            element.append(subelement)

        if obj.pulse_height_analyser:
            subelement = self._handler_pha.to_xml(obj.pulse_height_analyser)
            element.append(subelement)

        if obj.window:
            subelement = self._handler_window.to_xml(obj.window)
            element.append(subelement)

        return element

class DetectorSpectrometerXEDSXMLHandler(DetectorSpectrometerXMLHandler):

    def __init__(self):
        DetectorSpectrometerXMLHandler.__init__(self)
        self._handler_window = WindowXMLHandler()

    def can_parse(self, element):
        if not DetectorSpectrometerXMLHandler.can_parse(self, element):
            return False
        return element.get('Class') == 'Spectrometer/XEDS'

    def from_xml(self, element):
        kwargs = {}

        subelement = element.find('Technology')
        if subelement is not None:
            kwargs['technology'] = subelement.text
            
        subelement = element.find('NominalThroughput')
        if subelement is not None:
            kwargs['nominal_throughput'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('TimeConstant')
        if subelement is not None:
            kwargs['time_constant'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('StrobeRate')
        if subelement is not None:
            kwargs['strobe_rate'] = self._handler_numerical.from_xml(subelement)

        subelement = element.find('Window')
        if subelement is not None:
            kwargs['window'] = self._handler_window.from_xml(subelement)

        parent = DetectorSpectrometerXMLHandler.from_xml(self, element)
        obj = DetectorSpectrometerXEDS(parent.channel_count, parent.calibration,
                                       **kwargs)
        obj.__dict__.update(parent.__dict__)
        return obj

    def can_convert(self, obj):
        if not DetectorSpectrometerXMLHandler.can_convert(self, obj):
            return False
        return isinstance(obj, DetectorSpectrometerXEDS)

    def to_xml(self, obj):
        element = DetectorSpectrometerXMLHandler.to_xml(self, obj)
        element.set('Class', 'Spectrometer/XEDS')

        if obj.technology:
            subelement = etree.Element('Technology')
            subelement.text = obj.technology
            element.append(subelement)

        if obj.nominal_throughput:
            subelement = self._handler_numerical.to_xml(obj.nominal_throughput)
            subelement.tag = 'NominalThroughput'
            element.append(subelement)

        if obj.time_constant:
            subelement = self._handler_numerical.to_xml(obj.time_constant)
            subelement.tag = 'TimeConstant'
            element.append(subelement)

        if obj.strobe_rate:
            subelement = self._handler_numerical.to_xml(obj.strobe_rate)
            subelement.tag = 'StrobeRate'
            element.append(subelement)

        if obj.window:
            subelement = self._handler_window.to_xml(obj.window)
            element.append(subelement)

        return element
