#!/usr/bin/env python
"""
================================================================================
:mod:`detector` -- Detector condition
================================================================================

.. module:: detector
   :synopsis: Detector condition

.. inheritance-diagram:: pyhmsa.condition.detector

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
from pyhmsa.core.condition import _Condition, extract_numerical_value

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
XEDS_TECHNOLOGY_UCAL = u'\u00b5-cal'

_XEDS_TECHNOLOGIES = frozenset([XEDS_TECHNOLOGY_GE, XEDS_TECHNOLOGY_SILI,
                                XEDS_TECHNOLOGY_SDD, XEDS_TECHNOLOGY_UCAL])

class PulseHeightAnalyser(object):
    
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

    def get_bias(self):
        """
        Returns the bias.
        
        :return: bias and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._bias

    def set_bias(self, value, unit='V'):
        """
        Sets the bias.
        
        :arg value: bias
        :arg unit: unit
        """
        self._bias = extract_numerical_value(value, unit)

    bias = property(get_bias, set_bias, doc='Bias')

    def get_gain(self):
        """
        Returns the gain.
        
        :return: gain
        """
        return self._gain

    def set_gain(self, value):
        """
        Sets the gain.
        
        :arg value: gain
        """
        self._gain = value

    gain = property(get_gain, set_gain, doc='Gain')

    def get_base_level(self):
        """
        Returns the base level.
        
        :return: base level and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._base_level

    def set_base_level(self, value, unit='V'):
        """
        Sets the base level.
        
        :arg value: base level
        :arg unit: unit
        """
        self._base_level = extract_numerical_value(value, unit)

    base_level = property(get_base_level, set_base_level, doc='Base level')

    def get_window(self):
        """
        Returns the window.
        
        :return: window and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._window

    def set_window(self, value, unit='V'):
        """
        Sets the window.
        
        :arg value: window
        :arg unit: unit
        """
        self._window = extract_numerical_value(value, unit)

    window = property(get_window, set_window, doc='Window')

    def get_mode(self):
        """
        Returns the mode.
        
        :return: mode, either :const:`PHA_MODE_INTERGRAL` or
            :const:`PHA_MODE_DIFFERENTIAL`
        """
        return self._mode

    def set_mode(self, value):
        """
        Sets the mode.
        
        :arg value: mode, either :const:`PHA_MODE_INTERGRAL` or
            :const:`PHA_MODE_DIFFERENTIAL`
        """
        if value is not None and value not in _PHA_MODES:
            raise ValueError('Unknown mode: %s' % value)
        self._mode = value

    mode = property(get_mode, set_mode, doc='Mode')

class WindowLayer(object):

    def __init__(self, material, thickness):
        """
        Defines a layer of a window.
        """
        self.material = material
        self.thickness = thickness

    def get_material(self):
        """
        Returns the material.
        """
        return self._material

    def set_material(self, value):
        """
        Sets the material.
        
        :arg value: material
        """
        if value is None:
            raise ValueError('Material is required')
        self._material = value

    material = property(get_material, set_material, doc='Material')

    def get_thickness(self):
        """
        Returns the thickness.
        
        :return: thickness and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._thickness

    def set_thickness(self, value, unit=u'\u00b5m'):
        """
        Sets the thickness.
        
        :arg value: thickness
        :arg unit: unit
        """
        if value is None:
            raise ValueError('Thickness is required')
        self._thickness = extract_numerical_value(value, unit)

    thickness = property(get_thickness, set_thickness, doc='Thickness')

class Window(object):
    
    def __init__(self, layers=None):
        """
        Defines the layer(s) of a window.
        
        :arg layers: iterable of :class:`.Layer` (optional)
        """
        if layers is None:
            layers = []
        self._layers = list(layers)

    def get_layers(self):
        """
        Returns a modifiable list of layers.
        Layers can be added, removed and modified using the normal Python
        method for a :class:`list` (e.g. :meth:`append`, :meth:`remove`, etc.).
        
        :return: layers
        :rtype: :class:`list`
        """
        return self._layers

    layers = property(get_layers, doc='Modifiable list of layers')

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

    def get_signal_type(self):
        """
        Returns the type of signal.
        """
        return self._signal_type

    def set_signal_type(self, value):
        """
        Sets the type of signal.
        
        :arg signal_type: type of signal
        """
        if value is not None and value not in _SIGNAL_TYPES:
            raise ValueError('Unknown signal type: %s' % value)
        self._signal_type = value

    signal_type = property(get_signal_type, set_signal_type,
                           doc='Type of signal')

    def get_manufacturer(self):
        """
        Returns the manufacturer.
        """
        return self._manufacturer

    def set_manufacturer(self, value):
        """
        Sets the manufacturer.
        
        :arg value: manufacturer
        """
        self._manufacturer = value

    manufacturer = property(get_manufacturer, set_manufacturer,
                           doc='Manufacturer')

    def get_model(self):
        """
        Returns the model.
        """
        return self._model

    def set_model(self, value):
        """
        Sets the model.
        
        :arg value: model
        """
        self._model = value

    model = property(get_model, set_model, doc='Model')

    def get_serial_number(self):
        """
        Returns the serial number.
        """
        return self._serial_number

    def set_serial_number(self, value):
        """
        Sets the serial number.
        
        :arg value: serial number
        """
        self._serial_number = value

    serial_number = property(get_serial_number, set_serial_number,
                           doc='Serial number')

    def get_measurement_unit(self):
        """
        Returns the measurement unit.
        """
        return self._measurement_unit

    def set_measurement_unit(self, value):
        """
        Sets the measurement unit.
        
        :arg unit: measurement unit
        """
        if value is None:
            value = 'counts'
        validate_unit(value)
        self._measurement_unit = value

    measurement_unit = property(get_measurement_unit, set_measurement_unit,
                           doc='Measurement unit')

    def get_elevation(self):
        """
        Returns the elevation angle.
        
        :return: elevation angle and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._elevation

    def set_elevation(self, value, unit=u'\u00b0'):
        """
        Sets the elevation angle.
        
        :arg value: elevation angle
        :arg unit: unit
        """
        self._elevation = extract_numerical_value(value, unit)

    elevation = property(get_elevation, set_elevation, doc='Elevation angle')

    def get_azimuth(self):
        """
        Returns the azimuth angle.
        
        :return: azimuth angle and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._azimuth

    def set_azimuth(self, value, unit=u'\u00b0'):
        """
        Sets the azimuth angle.
        
        :arg value: azimuth angle
        :arg unit: unit
        """
        self._azimuth = extract_numerical_value(value, unit)

    azimuth = property(get_azimuth, set_azimuth, doc='Azimuth angle')

    def get_distance(self):
        """
        Returns the distance.
        
        :return: distance and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._distance

    def set_distance(self, value, unit='mm'):
        """
        Sets the distance.
        
        :arg value: distance
        :arg unit: unit
        """
        self._distance = extract_numerical_value(value, unit)

    distance = property(get_distance, set_distance, doc='Distance')

    def get_area(self):
        """
        Returns the area.
        
        :return: area and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._area

    def set_area(self, value, unit='mm2'):
        """
        Sets the area.
        
        :arg value: area
        :arg unit: unit
        """
        self._area = extract_numerical_value(value, unit)

    area = property(get_area, set_area, doc='Area')

    def get_solid_angle(self):
        """
        Returns the solid angle.
        
        :return: solid angle and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._solid_angle

    def set_solid_angle(self, value, unit='sr'):
        """
        Sets the solid angle.
        
        :arg value: solid angle
        :arg unit: unit
        """
        self._solid_angle = extract_numerical_value(value, unit)

    solid_angle = property(get_solid_angle, set_solid_angle, doc='Solid angle')

    def get_semi_angle(self):
        """
        Returns the semi-angle.
        
        :return: semi-angle and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._semi_angle

    def set_semi_angle(self, value, unit='mrad'):
        """
        Sets the semi-angle.
        
        :arg value: semi-angle
        :arg unit: unit
        """
        self._semi_angle = extract_numerical_value(value, unit)

    semi_angle = property(get_semi_angle, set_semi_angle, doc='Semi-angle')

    def get_temperature(self):
        """
        Returns the temperature.
        
        :return: temperature and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._temperature

    def set_temperature(self, value, unit=u'\u00b0\u0043'):
        """
        Sets the temperature.
        
        :arg value: temperature
        :arg unit: unit
        """
        self._temperature = extract_numerical_value(value, unit)

    temperature = property(get_temperature, set_temperature, doc='Temperature')

class DetectorCamera(_Detector):

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

    def get_pixel_count_u(self):
        """
        Returns the number of pixels along the horizontal axis.
        """
        return self._pixel_count_u

    def set_pixel_count_u(self, value):
        """
        Sets the number of pixels along the horizontal axis.
        
        :arg value: number of pixels
        """
        if value is None:
            raise ValueError('Pixel count along the horizontal axis is required')
        self._pixel_count_u = value

    pixel_count_u = property(get_pixel_count_u, set_pixel_count_u,
                             doc='Number of pixels along the horizontal axis')

    def get_pixel_count_v(self):
        """
        Returns the number of pixels along the vertical axis.
        """
        return self._pixel_count_v

    def set_pixel_count_v(self, value):
        """
        Sets the number of pixels along the vertical axis.
        
        :arg value: number of pixels
        """
        if value is None:
            raise ValueError('Pixel count along the vertical axis is required')
        self._pixel_count_v = value

    pixel_count_v = property(get_pixel_count_v, set_pixel_count_v,
                             doc='Number of pixels along the vertical axis')

    def get_exposure_time(self):
        """
        Returns the exposure time.
        
        :return: exposure time and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._exposure_time

    def set_exposure_time(self, value, unit='ms'):
        """
        Sets the exposure time.
        
        :arg value: exposure time
        :arg unit: unit
        """
        self._exposure_time = extract_numerical_value(value, unit)

    exposure_time = property(get_exposure_time, set_exposure_time,
                             doc='Exposure time')

    def get_magnification(self):
        """
        Returns the magnification.
        
        :return: magnification
        """
        return self._magnification

    def set_magnification(self, value):
        """
        Sets the magnification.
        
        :arg value: magnification
        """
        self._magnification = value

    magnification = property(get_magnification, set_magnification,
                             doc='Magnification')

    def get_focal_length(self):
        """
        Returns the focal length.
        
        :return: focal_length and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._focal_length

    def set_focal_length(self, value, unit='mm'):
        """
        Sets the focal length.
        
        :arg value: focal length
        :arg unit: unit
        """
        self._focal_length = extract_numerical_value(value, unit)

    focal_length = property(get_focal_length, set_focal_length,
                            doc='Focal length')

class DetectorSpectrometer(_Detector):

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

    def get_channel_count(self):
        """
        Returns the number of channels.
        
        :return: number of channels
        """
        return self._channel_count

    def set_channel_count(self, value):
        """
        Sets the number of channels.
        
        :arg value: number of channels
        """
        if value is None:
            raise ValueError('Channel count is required')
        self._channel_count = value

    channel_count = property(get_channel_count, set_channel_count,
                             doc='Number of channels')

    def get_calibration(self):
        """
        Returns the calibration.
        
        :return: calibration
        """
        return self._calibration

    def set_calibration(self, value):
        """
        Sets the calibration.
        
        :arg value: calibration
        """
        if value is None:
            raise ValueError('Calibration is required')
        self._calibration = value

    calibration = property(get_calibration, set_calibration,
                             doc='Calibration')

    def get_collection_mode(self):
        """
        Returns the mode of collection.
        
        :return: mode of collection, either :const:`COLLECTION_MODE_PARALLEL` 
            or :const:`COLLECTION_MODE_SERIAL`
        """
        return self._collection_mode

    def set_collection_mode(self, value):
        """
        Sets the mode of collection.
        
        :arg value: mode of collection, either :const:`COLLECTION_MODE_PARALLEL` 
            or :const:`COLLECTION_MODE_SERIAL`
        """
        if value is not None and value not in _COLLECTION_MODES:
            raise ValueError('Unknown collection mode: %s' % value)
        self._collection_mode = value

    collection_mode = property(get_collection_mode, set_collection_mode,
                             doc='Mode of collection')

class DetectorSpectrometerCL(DetectorSpectrometer):

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
        :arg grating_d: gradint spacing (optional)
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

    def get_grating_d(self):
        """
        Returns the grating spacing.
        
        :return: grating spacing and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._grating_d

    def set_grating_d(self, value, unit='mm-1'):
        """
        Sets the grating spacing.
        
        :arg value: grating spacing
        :arg unit: unit
        """
        self._grating_d = extract_numerical_value(value, unit)

    grating_d = property(get_grating_d, set_grating_d,
                            doc='Grating spacing')

class DetectorSpectrometerWDS(DetectorSpectrometer):

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
        self.pulse_height_analyser = pulse_height_analyser
        self.window = window

    def get_dispersion_element(self):
        """
        Returns the dispersion element.
        
        :return: dispersion element
        :rtype: :class:`.NumericalValue`
        """
        return self._dispersive_element

    def set_dispersion_element(self, value):
        """
        Sets the dispersion element.
        
        :arg value: dispersion element
        """
        self._dispersive_element = value

    dispersion_element = property(get_dispersion_element, set_dispersion_element,
                                  doc='Dispersion element')

    def get_crystal_2d(self):
        """
        Returns the crystal 2d-spacing.
        
        :return: crystal 2d-spacing and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._crystal_2d

    def set_crystal_2d(self, value, unit=u'\u00c5'):
        """
        Sets the crystal 2d-spacing.
        
        :arg value: crystal 2d-spacing
        :arg unit: unit
        """
        self._crystal_2d = extract_numerical_value(value, unit)

    crystal_2d = property(get_crystal_2d, set_crystal_2d,
                          doc='Crystal 2d-spacing')

    def get_rowland_circle_diameter(self):
        """
        Returns the Rowland circle diameter.
        
        :return: Rowland circle diameter and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._rowland_circle_diameter

    def set_rowland_circle_diameter(self, value, unit='mm'):
        """
        Sets the Rowland circle diameter.
        
        :arg value: Rowland circle diameter
        :arg unit: unit
        """
        self._rowland_circle_diameter = extract_numerical_value(value, unit)

    rowland_circle_diameter = property(get_rowland_circle_diameter,
                                       set_rowland_circle_diameter,
                                       doc='Rowland circle diameter')

    def get_pulse_height_analyser(self):
        """
        Returns the pulse height analyser.
        
        :return: pulse height analyser
        :rtype: :class:`.PulseHeightAnalyser`
        """
        return self._pulse_height_analyser

    def set_pulse_height_analyser(self, value):
        """
        Sets the pulse height analyser.
        
        :arg value: pulse_height_analyser
        :type pha: :class:`PulseHeightAnalyser`
        """
        self._pulse_height_analyser = value

    pulse_height_analyser = property(get_pulse_height_analyser,
                                     set_pulse_height_analyser,
                                     doc='Pulse height analyser')

    def get_window(self):
        """
        Returns the window.
        
        :return: window
        :rtype: :class:`.Window`
        """
        return self._window

    def set_window(self, value):
        """
        Sets the window.
        
        :arg value: window
        :type window: :class:`.Window`
        """
        self._window = value

    window = property(get_window, set_window, doc='Window')

class DetectorSpectrometerXEDS(DetectorSpectrometer):
    
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
        self.window = window

    def get_technology(self):
        """
        Returns the technology.
        
        :return: technology
        """
        return self._technology

    def set_technology(self, value):
        """
        Sets the technology.
        
        :arg value: technology
        """
        if value is not None and value not in _XEDS_TECHNOLOGIES:
            raise ValueError('Unknown technology: %s' % value)
        self._technology = value

    technology = property(get_technology, set_technology, doc='Technology')

    def get_nominal_throughput(self):
        """
        Returns the nominal throughput.
        
        :return: nominal throughput and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._nominal_throughput

    def set_nominal_throughput(self, value, unit='counts'):
        """
        Sets the nominal throughput.
        
        :arg value: nominal throughput
        :arg unit: unit
        """
        self._nominal_throughput = extract_numerical_value(value, unit)

    nominal_throughput = property(get_nominal_throughput,
                                  set_nominal_throughput,
                                  doc='Nominal throughput')

    def get_time_constant(self):
        """
        Returns the time constant.
        
        :return: time constant and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._time_constant

    def set_time_constant(self, value, unit=u'\u00b5s'):
        """
        Sets the time constant.
        
        :arg value: time constant
        :arg unit: unit
        """
        self._time_constant = extract_numerical_value(value, unit)

    time_constant = property(get_time_constant, set_time_constant,
                             doc='Time constant')

    def get_strobe_rate(self):
        """
        Returns the strobe rate.
        
        :return: strobe rate and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._strobe_rate

    def set_strobe_rate(self, value, unit='Hz'):
        """
        Sets the strobe rate.
        
        :arg value: strobe rate
        :arg unit: unit
        """
        self._strobe_rate = extract_numerical_value(value, unit)

    strobe_rate = property(get_strobe_rate, set_strobe_rate,
                             doc='Strobe rate')

    def get_window(self):
        """
        Returns the window.
        
        :return: window
        :rtype: :class:`.Window`
        """
        return self._window

    def set_window(self, value):
        """
        Sets the window.
        
        :arg value: window
        :type window: :class:`.Window`
        """
        self._window = value

    window = property(get_window, set_window, doc='Window')
