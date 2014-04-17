#!/usr/bin/env python
"""
================================================================================
:mod:`acquisition` -- Acquisition conditions
================================================================================

.. module:: acquisition
   :synopsis: Acquisition conditions

.. inheritance-diagram:: pyhmsa.condition.acquisition

"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.condition import _Condition
from pyhmsa.spec.condition.specimenposition import SpecimenPosition
from pyhmsa.util.parameter import \
    NumericalAttribute, ObjectAttribute, EnumAttribute, FrozenAttribute
from pyhmsa.util.cookbook import flatten

# Globals and constants variables.
RASTER_MODE_STAGE = 'Stage' #: Stage raster mode
RASTER_MODE_BEAM = 'Beam' #: Beam raster mode

_RASTER_MODES = frozenset([RASTER_MODE_BEAM, RASTER_MODE_STAGE])

RASTER_MODE_Z_FIB = 'FIB' #: Z raster mode (FIB)

_RASTER_MODES_Z = frozenset([RASTER_MODE_Z_FIB])

POSITION_LOCATION_START = 'Start' #: Start position
POSITION_LOCATION_CENTER = 'Center' #: Center position
POSITION_LOCATION_END = 'End' #: End position

_POSITION_LOCATIONS = frozenset([POSITION_LOCATION_START,
                                 POSITION_LOCATION_CENTER,
                                 POSITION_LOCATION_END])

class _Acquisition(_Condition):

    TEMPLATE = 'Acquisition'

    dwell_time = NumericalAttribute('s', False, 'DwellTime', "uniform real time taken for each individual measurement")
    total_time = NumericalAttribute('s', False, 'TotalTime', "total real time taken to collect all measurements")
    dwell_time_live = NumericalAttribute('s', False, 'DwellTime_Live', "analogous detector live time for each individual measurement")

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

class AcquisitionPoint(_Acquisition):

    CLASS = 'Point'

    position = ObjectAttribute(SpecimenPosition, True, "SpecimenPosition",
                               'physical location on (or in) the specimen')

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

class AcquisitionMultipoint(_Acquisition):

    CLASS = 'Multipoint'

    positions = FrozenAttribute(list, doc='specimen positions')

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
        self.positions.extend(positions)

class _AcquisitionRaster(_Acquisition):

    CLASS = 'Raster'

    raster_mode = EnumAttribute(_RASTER_MODES, False, 'RasterMode', 'mode of rastering')
    positions = FrozenAttribute(dict, doc='defined physical location(s) of the raster')

    def __init__(self, raster_mode=None,
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

class AcquisitionRasterLinescan(_AcquisitionRaster):

    CLASS = 'Raster/Linescan'

    step_count = NumericalAttribute(None, True, 'StepCount', 'number of steps')
    step_size = NumericalAttribute('um', False, 'StepSize', 'dimension of each step')

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

    def get_position_start(self):
        """
        Returns the start position.

        :return: start position
        :rtype: :class:`.SpecimenPosition`
        """
        return self.positions.get(POSITION_LOCATION_START)

    def set_position_start(self, value):
        """
        Sets the start position.

        :arg value: start position
        :type value: :class:`.SpecimenPosition`
        """
        if value is None:
            self.positions.pop(POSITION_LOCATION_START, None)
        else:
            self.positions[POSITION_LOCATION_START] = value

    position_start = property(get_position_start, set_position_start,
                              doc='Start position')

    def get_position_end(self):
        """
        Returns the end position.

        :return: end position
        :rtype: :class:`.SpecimenPosition`
        """
        return self.positions.get(POSITION_LOCATION_END)

    def set_position_end(self, value):
        """
        Sets the end position.

        :arg value: end position
        :type value: :class:`.SpecimenPosition`
        """
        if value is None:
            self.positions.pop(POSITION_LOCATION_END, None)
        else:
            self.positions[POSITION_LOCATION_END] = value

    position_end = property(get_position_end, set_position_end,
                            doc='End position')

class AcquisitionRasterXY(_AcquisitionRaster):

    CLASS = 'Raster/XY'

    step_count_x = NumericalAttribute(None, True, 'XStepCount', 'number of steps in x direction')
    step_count_y = NumericalAttribute(None, True, 'YStepCount', 'number of steps in y direction')
    step_size_x = NumericalAttribute('um', False, 'XStepSize', 'dimension of each step in x direction')
    step_size_y = NumericalAttribute('um', False, 'YStepSize', 'dimension of each step in y direction')
    frame_count = NumericalAttribute(None, False, 'FrameCount', 'number of accumulated frames')

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

    def get_position(self, include_location=False):
        """
        Returns the physical location on (or in) the specimen.

        :return: specimen position
        :rtype: :class:`.SpecimenPosition`
        """
        try:
            location = next(iter(self.positions.keys()))
            position = self.positions[location]
        except StopIteration:
            location = position = None

        if include_location:
            return position, location
        else:
            return position

    def set_position(self, value, loc=None):
        """
        Sets the physical location on (or in) the specimen.

        :arg value: specimen position
        :type value: :class:`.SpecimenPosition`
        :arg loc: location, either :const:`POSITION_LOCATION_START` or
            :const:`POSITION_LOCATION_CENTER`
        """
        values = list(flatten([value, loc]))
        value = values[0]
        loc = values[1]

        if loc is None:
            loc = POSITION_LOCATION_START

        self.positions.clear()

        if value is not None:
            self.positions[loc] = value

    position = property(get_position, set_position,
                        doc='Physical location on (or in) the specimen')

class AcquisitionRasterXYZ(_AcquisitionRaster):

    CLASS = 'Raster/XYZ'

    step_count_x = NumericalAttribute(None, True, 'XStepCount', 'number of steps in x direction')
    step_count_y = NumericalAttribute(None, True, 'YStepCount', 'number of steps in y direction')
    step_count_z = NumericalAttribute(None, True, 'ZStepCount', 'number of steps in z direction')
    step_size_x = NumericalAttribute('um', False, 'XStepSize', 'dimension of each step in x direction')
    step_size_y = NumericalAttribute('um', False, 'YStepSize', 'dimension of each step in y direction')
    step_size_z = NumericalAttribute('um', False, 'ZStepSize', 'dimension of each step in z direction')
    raster_mode_z = EnumAttribute(_RASTER_MODES_Z, False, 'ZRasterMode', 'mode of rastering in z direction')

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

    def get_position(self, include_location=False):
        """
        Returns the physical location on (or in) the specimen.

        :return: specimen position
        :rtype: :class:`.SpecimenPosition`
        """
        try:
            location = next(iter(self.positions.keys()))
            position = self.positions[location]
        except StopIteration:
            location = position = None

        if include_location:
            return position, location
        else:
            return position

    def set_position(self, value, loc=None):
        """
        Sets the physical location on (or in) the specimen.

        :arg value: specimen position
        :type value: :class:`.SpecimenPosition`
        :arg loc: location, either :const:`POSITION_LOCATION_START` or
            :const:`POSITION_LOCATION_CENTER`
        """
        values = list(flatten([value, loc]))
        value = values[0]
        loc = values[1]

        if loc is None:
            loc = POSITION_LOCATION_START

        self.positions.clear()

        if value is not None:
            self.positions[loc] = value

    position = property(get_position, set_position,
                        doc='Physical location on (or in) the specimen')

