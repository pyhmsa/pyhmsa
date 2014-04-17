#!/usr/bin/env python
"""
================================================================================
:mod:`detector` -- Detector condition
================================================================================

.. module:: detector
   :synopsis: Detector condition

.. inheritance-diagram:: pyhmsa.condition.detector

"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.condition import _Condition
from pyhmsa.spec.condition.calibration import _Calibration
from pyhmsa.util.parameter import \
    (Parameter, NumericalAttribute, EnumAttribute, TextAttribute,
     FrozenAttribute, UnitAttribute, ObjectAttribute)

# Globals and constants variables.
SIGNAL_TYPE_EDS = 'EDS'
SIGNAL_TYPE_WDS = 'WDS'
SIGNAL_TYPE_ELS = 'ELS'
SIGNAL_TYPE_AES = 'AES'
SIGNAL_TYPE_PES = 'PES'
SIGNAL_TYPE_XRF = 'XRF'
SIGNAL_TYPE_CLS = 'CLS'
SIGNAL_TYPE_GAM = 'GAM'
SIGNAL_TYPE_EBSD = 'EBSD'
SIGNAL_TYPE_BEI = 'BEI'
SIGNAL_TYPE_SEI = 'SEI'

_SIGNAL_TYPES = frozenset([SIGNAL_TYPE_EDS, SIGNAL_TYPE_WDS, SIGNAL_TYPE_ELS,
                           SIGNAL_TYPE_AES, SIGNAL_TYPE_PES, SIGNAL_TYPE_XRF,
                           SIGNAL_TYPE_CLS, SIGNAL_TYPE_GAM, SIGNAL_TYPE_EBSD,
                           SIGNAL_TYPE_BEI, SIGNAL_TYPE_SEI])

COLLECTION_MODE_PARALLEL = 'Parallel'
COLLECTION_MODE_SERIAL = 'Serial'

_COLLECTION_MODES = frozenset([COLLECTION_MODE_PARALLEL, COLLECTION_MODE_SERIAL])

PHA_MODE_INTEGRAL = 'Integral'
PHA_MODE_DIFFERENTIAL = 'Differential'

_PHA_MODES = frozenset([PHA_MODE_INTEGRAL, PHA_MODE_DIFFERENTIAL])

XEDS_TECHNOLOGY_GE = 'Ge'
XEDS_TECHNOLOGY_SILI = 'SiLi'
XEDS_TECHNOLOGY_SDD = 'SDD'
XEDS_TECHNOLOGY_UCAL = 'microcalorimeter'

_XEDS_TECHNOLOGIES = frozenset([XEDS_TECHNOLOGY_GE, XEDS_TECHNOLOGY_SILI,
                                XEDS_TECHNOLOGY_SDD, XEDS_TECHNOLOGY_UCAL])

class PulseHeightAnalyser(Parameter):

    bias = NumericalAttribute('V', False, 'Bias', 'bias')
    gain = NumericalAttribute(None, False, 'Gain', 'gain')
    base_level = NumericalAttribute('V' , False, 'BaseLevel', 'base level')
    window = NumericalAttribute('V', False, 'Window', 'window')
    mode = EnumAttribute(_PHA_MODES, False, 'Mode', 'mode')

    def __init__(self, bias=None, gain=None, base_level=None, window=None,
                  mode=None):
        """
        Defines the condition of the pulse height analyser of a WDS
        spectrometer.

        :arg bias: bias (optional)
        :arg gain: gain (optional)
        :arg base_level: base level (optional)
        :arg window: window (optional)
        :arg mode: mode, either :const:`PHA_MODE_INTEGRAL` or
            :const:`PHA_MODE_DIFFERENTIAL` (optional)
        """
        self.bias = bias
        self.gain = gain
        self.base_level = base_level
        self.window = window
        self.mode = mode

class WindowLayer(Parameter):

    material = TextAttribute(True, doc='material')
    thickness = NumericalAttribute('um', True, doc='thickness')

    def __init__(self, material, thickness):
        """
        Defines a layer of a window.

        :arg material: material
        :arg thickness: thickness
        """
        self.material = material
        self.thickness = thickness

class Window(Parameter):

    layers = FrozenAttribute(list, doc='modifiable list of layers')

    def __init__(self, layers=None):
        """
        Defines the layer(s) of a window.

        :arg layers: iterable of :class:`.Layer` (optional)
        """
        if layers is None:
            layers = []
        self.layers.extend(layers)

    def append_layer(self, material, thickness):
        """
        Helper function that creates a new :class:`.Layer` and appends it to
        this window.

        :arg material: material
        :arg thickness: thickness

        :return: created layer
        :rtype: :class:`.Layer`
        """
        layer = WindowLayer(material, thickness)
        self.layers.append(layer)
        return layer

class _Detector(_Condition):

    TEMPLATE = 'Detector'

    signal_type = EnumAttribute(_SIGNAL_TYPES, False, 'SignalType', 'type of signal')
    manufacturer = TextAttribute(False, 'Manufacturer', 'manufacturer')
    model = TextAttribute(False, 'Model', 'model')
    serial_number = TextAttribute(False, 'SerialNumber', 'serial number')
    measurement_unit = UnitAttribute('counts', False, 'MeasurementUnit', 'measurement unit')
    elevation = NumericalAttribute('degrees', False, 'Elevation', 'elevation')
    azimuth = NumericalAttribute('degrees', False, 'Azimuth', 'azimuth')
    distance = NumericalAttribute('mm', False, 'Distance', 'distance')
    area = NumericalAttribute('mm2', False, 'Area', 'area')
    solid_angle = NumericalAttribute('sr', False, 'SolidAngle', 'solid angle')
    semi_angle = NumericalAttribute('mrad', False, 'SemiAngle', 'semi-angle')
    temperature = NumericalAttribute('degreesC', False, 'Temperature', 'temperature')

    def __init__(self, signal_type=None, manufacturer=None, model=None,
                  serial_number=None, measurement_unit='counts', elevation=None,
                  azimuth=None, distance=None, area=None, solid_angle=None,
                  semi_angle=None, temperature=None):
        """
        Describes the type and configuration of a detector used to collect a
        HMSA dataset.

        :arg signal_type: type of signal (optional)
        :arg manufacturer: manufacturer (optional)
        :arg model: model (optional)
        :arg serial_number: serial number (optional)
        :arg measurement_unit: measurement unit (optional)
        :arg elevation: elevation (optional)
        :arg azimuth: azimuth (optional)
        :arg distance: distance (optional)
        :arg area: area (optional)
        :arg solid_angle: solid angle (optional)
        :arg semi_angle: semi-angle (optional)
        :arg temperature: temperature (optional)
        """
        _Condition.__init__(self)

        self.signal_type = signal_type
        self.manufacturer = manufacturer
        self.model = model
        self.serial_number = serial_number
        self.measurement_unit = measurement_unit
        self.elevation = elevation
        self.azimuth = azimuth
        self.distance = distance
        self.area = area
        self.solid_angle = solid_angle
        self.semi_angle = semi_angle
        self.temperature = temperature

class DetectorCamera(_Detector):

    CLASS = 'Camera'

    pixel_count_u = NumericalAttribute(None, True, 'UPixelCount', 'number of pixels along the horizontal axis')
    pixel_count_v = NumericalAttribute(None, True, 'VPixelCount', 'number of pixels along the vertical axis')
    exposure_time = NumericalAttribute('ms', False, 'ExposureTime', 'exposure time')
    magnification = NumericalAttribute(None, False, 'Magnification', 'magnification')
    focal_length = NumericalAttribute('mm', False, 'FocalLength', 'focal length')

    def __init__(self, pixel_count_u, pixel_count_v,
                  exposure_time=None, magnification=None, focal_length=None,
                  signal_type=None, manufacturer=None, model=None,
                  serial_number=None, measurement_unit='counts', elevation=None,
                  azimuth=None, distance=None, area=None, solid_angle=None,
                  semi_angle=None, temperature=None):
        """
        Describes the calibration and collection mode of a camera used to
        collect a HMSA dataset, such as an EBSD or TEM camera.
        The camera detector is expected to have two datum axes (U and V) which
        are, in general, assumed to be independent of the specimen coordinate
        dimensions (X/Y/Z).

        :arg pixel_count_u: number of pixels along the horizontal axis (required)
        :arg pixel_count_y: number of pixels along the vertical axis (required)
        :arg exposure_time: exposure time (optional)
        :arg magnification: magnification (optional)
        :arg focal_length: focal length (optional)
        :arg signal_type: type of signal (optional)
        :arg manufacturer: manufacturer (optional)
        :arg model: model (optional)
        :arg serial_number: serial number (optional)
        :arg measurement_unit: measurement unit (optional)
        :arg elevation: elevation (optional)
        :arg azimuth: azimuth (optional)
        :arg distance: distance (optional)
        :arg area: area (optional)
        :arg solid_angle: solid angle (optional)
        :arg semi_angle: semi-angle (optional)
        :arg temperature: temperature (optional)
        """
        _Detector.__init__(self, signal_type, manufacturer, model,
                           serial_number, measurement_unit, elevation, azimuth,
                           distance, area, solid_angle, semi_angle, temperature)

        self.pixel_count_u = pixel_count_u
        self.pixel_count_v = pixel_count_v
        self.exposure_time = exposure_time
        self.magnification = magnification
        self.focal_length = focal_length

class DetectorSpectrometer(_Detector):

    CLASS = 'Spectrometer'

    channel_count = NumericalAttribute(None, True, 'ChannelCount', 'number of channels')
    calibration = ObjectAttribute(_Calibration, True, doc='calibration')
    collection_mode = EnumAttribute(_COLLECTION_MODES, False, 'CollectionMode', 'mode of collection')

    def __init__(self, channel_count, calibration, collection_mode=None,
                  signal_type=None, manufacturer=None, model=None,
                  serial_number=None, measurement_unit='counts', elevation=None,
                  azimuth=None, distance=None, area=None, solid_angle=None,
                  semi_angle=None, temperature=None):
        """
        Describes the calibration and collection mode of a spectrometer used to
        collect a HMSA dataset.

        :arg channel_count: number of channels (required)
        :arg calibration: calibration (required)
        :type calibration: :class:`._Calibration`
        :arg collection mode: mode of collection, either
            :const:`COLLECTION_MODE_PARALLEL` or
            :const:`COLLECTION_MODE_SERIAL` (optional)
        :arg signal_type: type of signal (optional)
        :arg manufacturer: manufacturer (optional)
        :arg model: model (optional)
        :arg serial_number: serial number (optional)
        :arg measurement_unit: measurement unit (optional)
        :arg elevation: elevation (optional)
        :arg azimuth: azimuth (optional)
        :arg distance: distance (optional)
        :arg area: area (optional)
        :arg solid_angle: solid angle (optional)
        :arg semi_angle: semi-angle (optional)
        :arg temperature: temperature (optional)
        """
        _Detector.__init__(self, signal_type, manufacturer, model,
                           serial_number, measurement_unit, elevation, azimuth,
                           distance, area, solid_angle, semi_angle, temperature)

        self.channel_count = channel_count
        self.calibration = calibration
        self.collection_mode = collection_mode

class DetectorSpectrometerCL(DetectorSpectrometer):

    CLASS = 'Spectrometer/CL'

    grating_d = NumericalAttribute('mm-1', False, 'Grating-d', 'grating spacing')

    def __init__(self, channel_count, calibration,
                  grating_d=None,
                  collection_mode=None,
                  signal_type=None, manufacturer=None, model=None,
                  serial_number=None, measurement_unit='counts', elevation=None,
                  azimuth=None, distance=None, area=None, solid_angle=None,
                  semi_angle=None, temperature=None):
        """
        Describes the type and configuration of a cathodoluminescence
        spectrometer.

        .. note::

           If the spectrometer is operating as a monochromator (e.g.
           monochromatic CL mapping), the calibration definition shall be of
           type :class:`.CalibrationConstant`.

        :arg channel_count: number of channels (required)
        :arg calibration: calibration (required)
        :type calibration: :class:`._Calibration`
        :arg grating_d: grading spacing (optional)
        :arg collection mode: mode of collection, either
            :const:`COLLECTION_MODE_PARALLEL` or
            :const:`COLLECTION_MODE_SERIAL` (optional)
        :arg signal_type: type of signal (optional)
        :arg manufacturer: manufacturer (optional)
        :arg model: model (optional)
        :arg serial_number: serial number (optional)
        :arg measurement_unit: measurement unit (optional)
        :arg elevation: elevation (optional)
        :arg azimuth: azimuth (optional)
        :arg distance: distance (optional)
        :arg area: area (optional)
        :arg solid_angle: solid angle (optional)
        :arg semi_angle: semi-angle (optional)
        :arg temperature: temperature (optional)
        """
        DetectorSpectrometer.__init__(self, channel_count, calibration,
                                      collection_mode, signal_type, manufacturer,
                                      model, serial_number, measurement_unit,
                                      elevation, azimuth, distance, area,
                                      solid_angle, semi_angle, temperature)

        self.grating_d = grating_d


class DetectorSpectrometerWDS(DetectorSpectrometer):

    CLASS = 'Spectrometer/WDS'

    dispersion_element = TextAttribute(False, 'DispersionElement', 'dispersion element')
    crystal_2d = NumericalAttribute(u'\u00c5', False, 'Crystal-2d', 'crystal 2d-spacing')
    rowland_circle_diameter = NumericalAttribute('mm', False, 'RowlandCircleDiameter', 'Rowland circle diameter')
    pulse_height_analyser = ObjectAttribute(PulseHeightAnalyser, False, 'PulseHeightAnalyser', 'pulse height analyzer')
    window = ObjectAttribute(Window, False, doc='window')

    def __init__(self, channel_count, calibration, collection_mode=None,
                  dispersion_element=None, crystal_2d=None,
                  rowland_circle_diameter=None, pulse_height_analyser=None,
                  window=None,
                  signal_type=None, manufacturer=None, model=None,
                  serial_number=None, measurement_unit='counts', elevation=None,
                  azimuth=None, distance=None, area=None, solid_angle=None,
                  semi_angle=None, temperature=None):
        """
        Describes the type and configuration of a wavelength dispersive x-ray
        spectrometer.

        .. note::

           If the spectrometer is operating as a monochromator (e.g. WDS
           mapping), the calibration definition shall be of  type
           :class:`.CalibrationConstant`.

        :arg channel_count: number of channels (required)
        :arg calibration: calibration (required)
        :type calibration: :class:`._Calibration`
        :arg collection mode: mode of collection, either
            :const:`COLLECTION_MODE_PARALLEL` or
            :const:`COLLECTION_MODE_SERIAL` (optional)
        :arg dispersion_element element: dispersion element (optional)
        :arg crystal_2d: crystal 2d-spacing (optional)
        :arg rowland_circle_diameter: Rowland circle diameter (optional)
        :arg pulse_height_analyser: pulse height analyser (optional)
        :type pulse_height_analyser: :class:`.PulseHeightAnalyser`
        :arg window: window (optional)
        :type window: :class:`.Layer`
        :arg signal_type: type of signal (optional)
        :arg manufacturer: manufacturer (optional)
        :arg model: model (optional)
        :arg serial_number: serial number (optional)
        :arg measurement_unit: measurement unit (optional)
        :arg elevation: elevation (optional)
        :arg azimuth: azimuth (optional)
        :arg distance: distance (optional)
        :arg area: area (optional)
        :arg solid_angle: solid angle (optional)
        :arg semi_angle: semi-angle (optional)
        :arg temperature: temperature (optional)
        """
        DetectorSpectrometer.__init__(self, channel_count, calibration,
                                      collection_mode, signal_type, manufacturer,
                                      model, serial_number, measurement_unit,
                                      elevation, azimuth, distance, area,
                                      solid_angle, semi_angle, temperature)
        self.dispersion_element = dispersion_element
        self.crystal_2d = crystal_2d
        self.rowland_circle_diameter = rowland_circle_diameter
        if pulse_height_analyser is None:
            pulse_height_analyser = PulseHeightAnalyser()
        self.pulse_height_analyser = pulse_height_analyser
        if window is None:
            window = Window()
        self.window = window

class DetectorSpectrometerXEDS(DetectorSpectrometer):

    CLASS = 'Spectrometer/XEDS'

    technology = EnumAttribute(_XEDS_TECHNOLOGIES, False, 'Technology', 'technology')
    nominal_throughput = NumericalAttribute('counts', False, 'NominalThroughput', 'nominal throughput')
    time_constant = NumericalAttribute('us', False, 'TimeConstant', 'time constant')
    strobe_rate = NumericalAttribute('Hz', False, 'StrobeRate', 'strobe rate')
    window = ObjectAttribute(Window, False, doc='window')

    def __init__(self, channel_count, calibration, collection_mode=None,
                  technology=None, nominal_throughput=None, time_constant=None,
                  strobe_rate=None, window=None,
                  signal_type=None, manufacturer=None, model=None,
                  serial_number=None, measurement_unit='counts', elevation=None,
                  azimuth=None, distance=None, area=None, solid_angle=None,
                  semi_angle=None, temperature=None):
        """
        Describes the type and configuration of an energy dispersive x-ray
        spectrometer.

        :arg channel_count: number of channels (required)
        :arg calibration: calibration (required)
        :type calibration: :class:`._Calibration`
        :arg collection mode: mode of collection, either
            :const:`COLLECTION_MODE_PARALLEL` or
            :const:`COLLECTION_MODE_SERIAL` (optional)
        :arg technology: technology (optional)
        :arg nominal_throughput: nominal throughput (optional)
        :arg time_constant: time constant (optional)
        :arg strobe_rate: strobe rate (optional)
        :arg window: window (optional)
        :type window: :class:`.Layer`
        :arg signal_type: type of signal (optional)
        :arg manufacturer: manufacturer (optional)
        :arg model: model (optional)
        :arg serial_number: serial number (optional)
        :arg measurement_unit: measurement unit (optional)
        :arg elevation: elevation (optional)
        :arg azimuth: azimuth (optional)
        :arg distance: distance (optional)
        :arg area: area (optional)
        :arg solid_angle: solid angle (optional)
        :arg semi_angle: semi-angle (optional)
        :arg temperature: temperature (optional)
        """
        DetectorSpectrometer.__init__(self, channel_count, calibration,
                                      collection_mode, signal_type, manufacturer,
                                      model, serial_number, measurement_unit,
                                      elevation, azimuth, distance, area,
                                      solid_angle, semi_angle, temperature)
        self.technology = technology
        self.nominal_throughput = nominal_throughput
        self.time_constant = time_constant
        self.strobe_rate = strobe_rate
        if window is None:
            window = Window()
        self.window = window
