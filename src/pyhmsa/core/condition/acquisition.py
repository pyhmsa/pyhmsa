#!/usr/bin/env python
"""
================================================================================
:mod:`acquisition` -- Acquisition conditions
================================================================================

.. module:: acquisition
   :synopsis: Acquisition conditions

.. inheritance-diagram:: pyhmsa.condition.acquisition

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.core.condition import _Condition, flatten
from pyhmsa.type.numerical import extract_value

# Globals and constants variables.
RASTER_MODE_STAGE = 'Stage'
RASTER_MODE_BEAM = 'Beam'

_RASTER_MODES = frozenset([RASTER_MODE_BEAM, RASTER_MODE_STAGE])

RASTER_MODE_Z_FIB = 'FIB'

_RASTER_MODES_Z = frozenset([RASTER_MODE_Z_FIB])

POSITION_LOCATION_START = 'Start'
POSITION_LOCATION_CENTER = 'Center'
POSITION_LOCATION_END = 'End'

_POSITION_LOCATIONS = frozenset([POSITION_LOCATION_START,
                                 POSITION_LOCATION_CENTER,
                                 POSITION_LOCATION_END])

class _Acquisition(_Condition):

    def __init__(self, dwell_time=None, total_time=None, dwell_time_live=None):
        """
        Describes the position and duration of one or more measurements of the 
        specimen.
        
        :arg dwell_time: uniform real time taken for each individual measurement (optional)
        :arg total_time: total real time taken to collect all measurements (optional)
        :arg dwell_time_live: analogous detector live time for each individual measurement (optional)
        """
        _Condition.__init__(self)

        self.dwell_time = dwell_time
        self.total_time = total_time
        self.dwell_time_live = dwell_time_live

    def get_dwell_time(self):
        """
        Returns the dwell time, the uniform real time taken for each individual
        measurement, such as a point spectrum acquisition, a single point in a 
        linescan, or a pixel in a map.
        
        :return: dwell time value and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._dwell_time

    def set_dwell_time(self, value, unit='s'):
        """
        Sets the dwell time, the uniform real time taken for each individual
        measurement, such as a point spectrum acquisition, a single point in a 
        linescan, or a pixel in a map.
        
        :arg value: dwell time
        :arg unit: unit (default: ``s``)
        """
        self._dwell_time = extract_value(value, unit)

    dwell_time = property(get_dwell_time, set_dwell_time,
                          doc="Uniform real time taken for each individual measurement")

    def get_total_time(self):
        """
        Returns the total time, the total real time taken to collect all 
        measurements in the acquisition set.
        
        :return: total time value and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._total_time

    def set_total_time(self, value, unit='s'):
        """
        Sets the total time, the total real time taken to collect all 
        measurements in the acquisition set.
        
        :arg value: total time
        :arg unit: unit (default: ``s``)
        """
        self._total_time = extract_value(value, unit)

    total_time = property(get_total_time, set_total_time,
                          doc='Total real time taken to collect all measurements')

    def get_dwell_time_live(self):
        """
        Returns the live dwell time, the analogous detector live time for each 
        individual measurement.
        
        :return: live dwell value and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._dwell_time_live

    def set_dwell_time_live(self, value, unit='s'):
        """
        Sets the live dwell time, the analogous detector live time for each 
        individual measurement.
        
        :arg value: live dwell time
        :arg unit: unit (default: ``s``)
        """
        self._dwell_time_live = extract_value(value, unit)

    dwell_time_live = property(get_dwell_time_live, set_dwell_time_live,
                               doc='Analogous detector live time for each individual measurement')

class AcquisitionPoint(_Acquisition):

    def __init__(self, position,
                 dwell_time=None, total_time=None, dwell_time_live=None):
        """
        Defines the position and duration for a singular measurement of the 
        specimen.

        :arg position: physical location on (or in) the specimen (required)
        :arg dwell_time: uniform real time taken for each individual measurement (optional)
        :arg total_time: total real time taken to collect all measurements (optional)
        :arg dwell_time_live: analogous detector live time for each individual measurement (optional)
        """
        _Acquisition.__init__(self, dwell_time, total_time, dwell_time_live)

        self.position = position

    def get_position(self):
        """
        Returns the physical location on (or in) the specimen.
        
        :return: specimen position
        :rtype: :class:`.SpecimenPosition`
        """
        return self._specimen_position

    def set_position(self, value):
        """
        Sets the physical location on (or in) the specimen.
        
        :arg value: specimen position
        :type value: :class:`.SpecimenPosition`
        """
        if value is None:
            raise ValueError("Specimen position is required")
        self._specimen_position = value

    position = property(get_position, set_position,
                        doc='Physical location on (or in) the specimen')

class AcquisitionMultipoint(_Acquisition):

    def __init__(self, positions=None,
                 dwell_time=None, total_time=None, dwell_time_live=None):
        """
        Defines the position and duration of an irregular sequence of 
        measurements of the specimen.

        :arg positions: iterable of specimen positions (optional) 
        :arg dwell_time: uniform real time taken for each individual measurement (optional)
        :arg total_time: total real time taken to collect all measurements (optional)
        :arg dwell_time_live: analogous detector live time for each individual measurement (optional)
        """
        _Acquisition.__init__(self, dwell_time, total_time, dwell_time_live)

        if positions is None:
            positions = []
        self._positions = list(positions)

    def get_positions(self):
        """
        Returns a modifiable list of specimen positions.
        Positions can be added, removed and modified using the normal Python
        method for a :class:`list` (e.g. :meth:`append`, :meth:`remove`, etc.).
        
        :return: specimen positions
        :rtype: :class:`list`
        """
        return self._positions

    positions = property(get_positions, doc='Modifiable list of specimen positions')

    def get_point_count(self):
        """
        Returns the number of specimen positions defined.
        """
        return np.uint32(len(self._positions))

    point_count = property(get_point_count, doc='Number of specimen positions')

class _AcquisitionRaster(_Acquisition):

    def __init__(self, raster_mode=None, positions=None,
                 dwell_time=None, total_time=None, dwell_time_live=None):
        """
        Defines the position and duration of a regular raster over the specimen.

        :arg raster_mode: mode of rastering, :const:`RASTER_MODE_STAGE` or 
            :const:`RASTER_MODE_BEAM` (optional)
        :arg dwell_time: uniform real time taken for each individual measurement (optional)
        :arg total_time: total real time taken to collect all measurements (optional)
        :arg dwell_time_live: analogous detector live time for each individual measurement (optional)
        """
        _Acquisition.__init__(self, dwell_time, total_time, dwell_time_live)

        self.raster_mode = raster_mode

        if positions is None:
            positions = {}
        self._positions = positions.copy()

    def get_raster_mode(self):
        """
        Returns the mode of rastering.
        
        :return: :const:`RASTER_MODE_STAGE` or :const:`RASTER_MODE_BEAM`
        """
        return self._raster_mode

    def set_raster_mode(self, value):
        """
        Sets the mode of rastering.
        
        :arg value: raster mode, either :const:`RASTER_MODE_STAGE` or 
            :const:`RASTER_MODE_BEAM`
        """
        if value is not None and value not in _RASTER_MODES:
            raise ValueError('Unknown raster mode: %s' % value)
        self._raster_mode = value

    raster_mode = property(get_raster_mode, set_raster_mode,
                           doc='mode of rastering')

    def get_positions(self):
        """
        Returns the defined physical location(s) of the raster.
        A copy of the positions :class:`dict` is returned. 
        Use specific method to modify the position(s).
        
        :return: physical location(s) of the raster
        :rtype: :class:`dict`
        """
        return self._positions.copy()

    positions = property(get_positions,
                         doc='Read-only dictionary of specimen positions')

class AcquisitionRasterLinescan(_AcquisitionRaster):

    def __init__(self, step_count, step_size=None,
                  position_start=None, position_end=None,
                  raster_mode=None,
                  dwell_time=None, total_time=None, dwell_time_live=None):
        """
        Defines the position and duration of a one-dimensional raster over the 
        specimen.
        Applies only to a linear sequence of steps, using equal step sizes and 
        dwell times for each measurement.
        For irregular step sizes, refer to :class:`.AcquisitionMultiPoint`

        :arg step_count: number of steps (required)
        :arg step_size: dimension of each step (optional)
        :arg position_start: start position (optional)
        :arg position_end: end position (optional)
        :arg raster_mode: mode of rastering, :const:`RASTER_MODE_STAGE` or 
            :const:`RASTER_MODE_BEAM` (optional)
        :arg dwell_time: uniform real time taken for each individual measurement (optional)
        :arg total_time: total real time taken to collect all measurements (optional)
        :arg dwell_time_live: analogous detector live time for each individual measurement (optional)
        """
        _AcquisitionRaster.__init__(self, raster_mode,
                                    dwell_time, total_time, dwell_time_live)

        self.step_count = step_count
        self.step_size = step_size
        self.position_start = position_start
        self.position_end = position_end

    def get_step_count(self):
        """
        Returns the number of steps.
        
        :return: number of steps
        """
        return self._step_count

    def set_step_count(self, value):
        """
        Sets the number of steps.
        
        :arg value: number of steps
        """
        if value is None:
            raise ValueError("Step count is required")
        self._step_count = np.uint32(value)

    step_count = property(get_step_count, set_step_count,
                          doc='Number of steps')
    
    def get_step_size(self):
        """
        Returns the step size, dimension of each step.
        
        :return: step size and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._step_size

    def set_step_size(self, value, unit=u'\u00b5m'):
        """
        Sets the step size, dimension of each step.
        
        :arg value: step size
        :arg unit: unit (default: ``\u00b5mm``)
        """
        self._step_size = extract_value(value, unit)

    step_size = property(get_step_size, set_step_size,
                         doc='Dimension of each step')

    def get_position_start(self):
        """
        Returns the start position.
        
        :return: start position
        :rtype: :class:`.SpecimenPosition`
        """
        return self._positions.get(POSITION_LOCATION_START)

    def set_position_start(self, value):
        """
        Sets the start position.
        
        :arg value: start position
        :type value: :class:`.SpecimenPosition`
        """
        if value is None:
            self._positions.pop(POSITION_LOCATION_START, None)
        else:
            self._positions[POSITION_LOCATION_START] = value

    position_start = property(get_position_start, set_position_start,
                              doc='Start position')

    def get_position_end(self):
        """
        Returns the end position.
        
        :return: end position
        :rtype: :class:`.SpecimenPosition`
        """
        return self._positions.get(POSITION_LOCATION_END)

    def set_position_end(self, value):
        """
        Sets the end position.
        
        :arg value: end position
        :type value: :class:`.SpecimenPosition`
        """
        if value is None:
            self._positions.pop(POSITION_LOCATION_END, None)
        else:
            self._positions[POSITION_LOCATION_END] = value

    position_end = property(get_position_end, set_position_end,
                            doc='End position')

class AcquisitionRasterXY(_AcquisitionRaster):

    def __init__(self, step_count_x, step_count_y,
                  step_size_x=None, step_size_y=None, frame_count=None,
                  position=None,
                  raster_mode=None,
                  dwell_time=None, total_time=None, dwell_time_live=None):
        """
        Defines the position and duration of a two-dimensional X/Y raster over 
        the specimen.

        :arg step_count_x: number of steps in x direction (required)
        :arg step_count_y: number of steps in y direction (required)
        :arg step_size_x: dimension of each step in x direction (optional)
        :arg step_size_y: dimension of each step in y direction (optional)
        :arg frame_count: number of accumulated frames (optional)
        :arg position: specimen position (optional)
        :arg raster_mode: mode of rastering, :const:`RASTER_MODE_STAGE` or 
            :const:`RASTER_MODE_BEAM` (optional)
        :arg dwell_time: uniform real time taken for each individual measurement (optional)
        :arg total_time: total real time taken to collect all measurements (optional)
        :arg dwell_time_live: analogous detector live time for each individual measurement (optional)
        """
        _AcquisitionRaster.__init__(self, raster_mode,
                                    dwell_time, total_time, dwell_time_live)

        self.step_count_x = step_count_x
        self.step_count_y = step_count_y
        self.step_size_x = step_size_x
        self.step_size_y = step_size_y
        self.frame_count = frame_count
        self.position = position

    def get_step_count_x(self):
        """
        Returns the number of steps in x direction.
        
        :return: number of steps
        """
        return self._step_count_x

    def set_step_count_x(self, value):
        """
        Sets the number of steps in x direction.
        
        :arg value: number of steps
        """
        if value is None:
            raise ValueError("Step count x is required")
        self._step_count_x = np.uint32(value)

    step_count_x = property(get_step_count_x, set_step_count_x,
                            doc='Number of steps in x direction')

    def get_step_count_y(self):
        """
        Returns the number of steps in y direction.
        
        :return: number of steps
        """
        return self._step_count_y

    def set_step_count_y(self, value):
        """
        Sets the number of steps in y direction.
        
        :arg value: number of steps
        """
        if value is None:
            raise ValueError("Step count y is required")
        self._step_count_y = np.uint32(value)

    step_count_y = property(get_step_count_y, set_step_count_y,
                            doc='Number of steps in y direction')

    def get_step_size_x(self):
        """
        Returns the step size, dimension of each step in x direction.
        
        :return: step size and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._step_size_x

    def set_step_size_x(self, value, unit=u'\u00b5m'):
        """
        Sets the step size, dimension of each step in x direction.
        
        :arg value: step size
        :arg unit: unit (default: ``\u00b5mm``)
        """
        self._step_size_x = extract_value(value, unit)

    step_size_x = property(get_step_size_x, set_step_size_x,
                           doc='Dimension of each step in the x direction')

    def get_step_size_y(self):
        """
        Returns the step size, dimension of each step in y direction.
        
        :return: step size and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._step_size_y

    def set_step_size_y(self, value, unit=u'\u00b5m'):
        """
        Sets the step size, dimension of each step in y direction.
        
        :arg value: step size
        :arg unit: unit (default: ``\u00b5mm``)
        """
        self._step_size_y = extract_value(value, unit)

    step_size_y = property(get_step_size_y, set_step_size_y,
                           doc='Dimension of each step in the y direction')

    def get_frame_count(self):
        """
        Returns the frame count, number of accumulated frames.
        
        :return: frame count
        """
        return self._frame_count

    def set_frame_count(self, value):
        """
        Sets the frame count, number of accumulated frames.
        
        :arg value: frame count
        """
        if value is not None:
            value = np.uint32(value)
        self._frame_count = value

    frame_count = property(get_frame_count, set_frame_count,
                           doc='Number of accumulated frames')

    def get_position(self):
        """
        Returns the physical location on (or in) the specimen.
        
        :return: specimen position
        :rtype: :class:`.SpecimenPosition`
        """
        try:
            loc = next(iter(self._positions.keys()))
            return self._positions[loc]
        except StopIteration:
            return None

    def set_position(self, value, loc=None):
        """
        Sets the physical location on (or in) the specimen.
        
        :arg value: specimen position
        :type value: :class:`.SpecimenPosition`
        :arg loc: location, either :const:`POSITION_LOCATION_START` or
            :const:`POSITION_LOCATION_CENTER`
        """
        value, loc, *_ = list(flatten([value, loc]))

        if loc is None:
            loc = POSITION_LOCATION_START

        self._positions.clear()

        if value is not None:
            self._positions[loc] = value

    position = property(get_position, set_position,
                        doc='Physical location on (or in) the specimen')

class AcquisitionRasterXYZ(_AcquisitionRaster):

    def __init__(self, step_count_x, step_count_y, step_count_z,
                  step_size_x=None, step_size_y=None, step_size_z=None,
                  position=None, raster_mode_z=None,
                  raster_mode=None,
                  dwell_time=None, total_time=None, dwell_time_live=None):
        """
        Defines the position and duration of a three-dimensional X/Y/Z raster 
        over the specimen.

        :arg step_count_x: number of steps in x direction (required)
        :arg step_count_y: number of steps in y direction (required)
        :arg step_count_z: number of steps in z direction (required)
        :arg step_size_x: dimension of each step in x direction (optional)
        :arg step_size_y: dimension of each step in y direction (optional)
        :arg step_size_z: dimension of each step in z direction (optional)
        :arg position: specimen position (optional)
        :arg raster_mode_z: mode of rastering in z direction, 
            :const:`RASTER_MODE_Z_FIB` (optional)
        :arg raster_mode: mode of rastering, :const:`RASTER_MODE_STAGE` or 
            :const:`RASTER_MODE_BEAM` (optional)
        :arg dwell_time: uniform real time taken for each individual measurement (optional)
        :arg total_time: total real time taken to collect all measurements (optional)
        :arg dwell_time_live: analogous detector live time for each individual measurement (optional)
        """
        _AcquisitionRaster.__init__(self, raster_mode,
                                    dwell_time, total_time, dwell_time_live)

        self.step_count_x = step_count_x
        self.step_count_y = step_count_y
        self.step_count_z = step_count_z
        self.step_size_x = step_size_x
        self.step_size_y = step_size_y
        self.step_size_z = step_size_z
        self.position = position
        self.raster_mode_z = raster_mode_z

    def get_step_count_x(self):
        """
        Returns the number of steps in x direction.
        
        :return: number of steps
        """
        return self._step_count_x

    def set_step_count_x(self, value):
        """
        Sets the number of steps in x direction.
        
        :arg value: number of steps
        """
        if value is None:
            raise ValueError("Step count x is required")
        self._step_count_x = np.uint32(value)

    step_count_x = property(get_step_count_x, set_step_count_x,
                            doc='Number of steps in x direction')

    def get_step_count_y(self):
        """
        Returns the number of steps in y direction.
        
        :return: number of steps
        """
        return self._step_count_y

    def set_step_count_y(self, value):
        """
        Sets the number of steps in y direction.
        
        :arg value: number of steps
        """
        if value is None:
            raise ValueError("Step count y is required")
        self._step_count_y = np.uint32(value)

    step_count_y = property(get_step_count_y, set_step_count_y,
                            doc='Number of steps in y direction')

    def get_step_count_z(self):
        """
        Returns the number of steps in z direction.
        
        :return: number of steps
        """
        return self._step_count_z

    def set_step_count_z(self, value):
        """
        Sets the number of steps in z direction.
        
        :arg value: number of steps
        """
        if value is None:
            raise ValueError("Step count z is required")
        self._step_count_z = np.uint32(value)

    step_count_z = property(get_step_count_z, set_step_count_z,
                            doc='Number of steps in z direction')

    def get_step_size_x(self):
        """
        Returns the step size, dimension of each step in x direction.
        
        :return: step size and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._step_size_x

    def set_step_size_x(self, value, unit=u'\u00b5m'):
        """
        Sets the step size, dimension of each step in x direction.
        
        :arg value: step size
        :arg unit: unit (default: ``\u00b5mm``)
        """
        self._step_size_x = extract_value(value, unit)

    step_size_x = property(get_step_size_x, set_step_size_x,
                           doc='Dimension of each step in the x direction')

    def get_step_size_y(self):
        """
        Returns the step size, dimension of each step in y direction.
        
        :return: step size and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._step_size_y

    def set_step_size_y(self, value, unit=u'\u00b5m'):
        """
        Sets the step size, dimension of each step in y direction.
        
        :arg value: step size
        :arg unit: unit (default: ``\u00b5mm``)
        """
        self._step_size_y = extract_value(value, unit)

    step_size_y = property(get_step_size_y, set_step_size_y,
                           doc='Dimension of each step in the y direction')

    def get_step_size_z(self):
        """
        Returns the step size, dimension of each step in z direction.
        
        :return: step size and unit
        :rtype: :class:`.NumericalValue`
        """
        return self._step_size_z

    def set_step_size_z(self, value, unit=u'\u00b5m'):
        """
        Sets the step size, dimension of each step in z direction.
        
        :arg value: step size
        :arg unit: unit (default: ``\u00b5mm``)
        """
        self._step_size_z = extract_value(value, unit)

    step_size_z = property(get_step_size_z, set_step_size_z,
                           doc='Dimension of each step in the z direction')

    def get_position(self):
        """
        Returns the physical location on (or in) the specimen.
        
        :return: specimen position
        :rtype: :class:`.SpecimenPosition`
        """
        try:
            loc = next(iter(self._positions.keys()))
            return self._positions[loc]
        except StopIteration:
            return None

    def set_position(self, value, loc=None):
        """
        Sets the physical location on (or in) the specimen.
        
        :arg value: specimen position
        :type value: :class:`.SpecimenPosition`
        :arg loc: location, either :const:`POSITION_LOCATION_START` or
            :const:`POSITION_LOCATION_CENTER`
        """
        value, loc, *_ = list(flatten([value, loc]))

        if loc is None:
            loc = POSITION_LOCATION_START

        self._positions.clear()

        if value is not None:
            self._positions[loc] = value

    position = property(get_position, set_position,
                        doc='Physical location on (or in) the specimen')

    def get_raster_mode_z(self):
        """
        Returns the mode of rastering in z direction.
        
        :return: :const:`RASTER_MODE_STAGE` or :const:`RASTER_MODE_BEAM`
        """
        return self._raster_mode_z

    def set_raster_mode_z(self, mode):
        """
        Sets the mode of rastering in z direction.
        
        :arg mode: raster mode, :const:`RASTER_MODE_Z_FIB`
        """
        if mode is not None and mode not in _RASTER_MODES_Z:
            raise ValueError('Unknown raster mode: %s' % mode)
        self._raster_mode_z = mode

    raster_mode_z = property(get_raster_mode_z, set_raster_mode_z,
                             doc='mode of rastering in z direction')
