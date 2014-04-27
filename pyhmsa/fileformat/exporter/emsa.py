#!/usr/bin/env python
"""
================================================================================
:mod:`emsa` -- Export HMSA data file to EMSA file format
================================================================================

.. module:: emsa
   :synopsis: Export HMSA data file to EMSA file format

.. inheritance-diagram:: pyhmsa.fileformat.exporter.esma

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2014 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.fileformat.exporter.exporter import _Exporter, _ExporterThread
from pyhmsa.fileformat.common.emsa import calculate_checksum

from pyhmsa.spec.datum.analysis import Analysis1D
from pyhmsa.spec.condition.detector import DetectorSpectrometer
from pyhmsa.spec.condition.probe import _Probe
from pyhmsa.spec.condition.acquisition import AcquisitionPoint

from pyhmsa.type.numerical import convert_unit

# Globals and constants variables.

class _ExporterEMSAThread(_ExporterThread):

    _NCOLUMNS = 4

    def _run(self, datafile, filepath, *args, **kwargs):

        lines = self._create_lines(datafile)

        with open(filepath, 'w') as fp:
            fp.write('\n'.join(lines))

        return filepath

    def _create_lines(self, datafile):
        lines = []
        lines += self._create_header_lines(datafile)
        lines += self._create_required_keywords_lines(datafile)
        lines += self._create_optional_keywords_lines(datafile)
        lines += self._create_data_lines(datafile)
        return lines

    def _create_keyword_line(self, tag, value=''):
        if value is None:
            return []
        tag = tag.ljust(12)
        assert len(tag) == 12
        return ["#%s: %s" % (tag, value)]

    def _create_header_lines(self, datafile):
        lines = []
        lines += self._create_keyword_line('FORMAT', 'EMSA/MAS Spectral Data File')
        lines += self._create_keyword_line('VERSION', '1.0')
        return lines

    def _create_required_keywords_lines(self, datafile):
        header = datafile.header
        datum = next(iter(datafile.data.findvalues(Analysis1D)))
        detector = next(iter(datafile.conditions.findvalues(DetectorSpectrometer)))

        lines = []
        lines += self._create_keyword_line('TITLE', header.title)
        lines += self._create_keyword_line('DATE', header.date.strftime('%d-%b-%Y'))
        lines += self._create_keyword_line('TIME', header.time.strftime('%H:%M'))
        lines += self._create_keyword_line('OWNER', header.author)
        lines += self._create_keyword_line('NPOINTS', len(datum))
        lines += self._create_keyword_line('NCOLUMNS', self._NCOLUMNS)
        lines += self._create_keyword_line('XUNITS', detector.calibration.unit)
        lines += self._create_keyword_line('YUNITS', detector.measurement_unit)
        lines += self._create_keyword_line('DATATYPE', 'Y')
        lines += self._create_keyword_line('XPERCHAN', detector.calibration.gain)
        lines += self._create_keyword_line('OFFSET', detector.calibration.offset)
        return lines

    def _create_optional_keywords_lines(self, datafile):
        detector = next(iter(datafile.conditions.findvalues(DetectorSpectrometer)))
        probes = datafile.conditions.findvalues(_Probe)
        probe = next(iter(probes)) if probes else None
        acqs = datafile.conditions.findvalues(AcquisitionPoint)
        acq = next(iter(acqs)) if acqs else None

        lines = []
        lines += self._create_keyword_line('SIGNALTYPE', detector.signal_type)
        lines += self._create_keyword_line('XLABEL', detector.calibration.quantity)
#        lines += self._create_keyword_line('YLABEL', )

        if probe:
            if probe.beam_voltage is not None:
                beamkv = float(convert_unit('kV', probe.beam_voltage))
                lines += self._create_keyword_line('BEAMKV', beamkv)

            if probe.emission_current is not None:
                emission = float(convert_unit('uA', probe.emission_current))
                lines += self._create_keyword_line('EMISSION', emission)

            if probe.beam_current is not None:
                probecur = float(convert_unit('nA', probe.beam_current))
                lines += self._create_keyword_line('PROBECUR', probecur)

            if probe.beam_diameter is not None:
                beamdiam = float(convert_unit('nm', probe.beam_diameter))
                lines += self._create_keyword_line('BEAMDIAM', beamdiam)

            if probe.scan_magnification is not None:
                magcam = int(probe.scan_magnification)
                lines += self._create_keyword_line('MAGCAM', magcam)

            convangle = getattr(probe, 'convergence_angle', None)
            if convangle is not None:
                convangle = float(convert_unit('mrad', convangle))
                lines += self._create_keyword_line('CONVANGLE', convangle)

            opermode = getattr(probe, 'lens_mode', None)
            if opermode is not None:
                lines += self._create_keyword_line('OPERMODE', opermode)

        if acq and acq.position is not None:
            xposition = float(convert_unit('mm', acq.position.x))
            lines += self._create_keyword_line('XPOSITION', xposition)

            yposition = float(convert_unit('mm', acq.position.y))
            lines += self._create_keyword_line('YPOSITION', yposition)

            zposition = float(convert_unit('mm', acq.position.z))
            lines += self._create_keyword_line('ZPOSITION', zposition)

        if acq:
            if acq.dwell_time is not None:
                dwelltime = float(convert_unit('ms', acq.dwell_time))
                lines += self._create_keyword_line('DWELLTIME', dwelltime)

            if acq.total_time is not None:
                integtime = float(convert_unit('ms', acq.total_time))
                lines += self._create_keyword_line('INTEGTIME', integtime)

            if acq.dwell_time_live is not None:
                livetime = float(convert_unit('s', acq.dwell_time_live))
                lines += self._create_keyword_line('LIVETIME', livetime)

            if acq.total_time is not None:
                realtime = float(convert_unit('s', acq.total_time))
                lines += self._create_keyword_line('REALTIME', realtime)

        if detector.semi_angle is not None:
            collangle = float(convert_unit('mrad', detector.semi_angle))
            lines += self._create_keyword_line('COLLANGLE', collangle)

        if detector.collection_mode is not None:
            elsdet = detector.collection_mode
            lines += self._create_keyword_line('ELSDET', elsdet)

        if detector.elevation is not None:
            elevangle = float(convert_unit('degrees', detector.elevation))
            lines += self._create_keyword_line('ELEVANGLE', elevangle)

        if detector.azimuth is not None:
            azimangle = float(convert_unit('degrees', detector.azimuth))
            lines += self._create_keyword_line('AZIMANGLE', azimangle)

        if detector.solid_angle is not None:
            solidangle = float(convert_unit('sr', detector.solid_angle))
            lines += self._create_keyword_line('SOLIDANGLE', solidangle)

#        if acq and acq.window:
#            lines += self._create_keyword_line('TDEADLYR',)
#            lines += self._create_keyword_line('TACTLYR',)
#            lines += self._create_keyword_line('TBEWIND',)
#            lines += self._create_keyword_line('TAUWIND',)
#            lines += self._create_keyword_line('TALWIND',)
#            lines += self._create_keyword_line('TPYWIND',)
#            lines += self._create_keyword_line('TBNWIND',)
#            lines += self._create_keyword_line('TDIWIND',)
#            lines += self._create_keyword_line('THCWIND',)
        lines += self._create_keyword_line('EDSDET', getattr(detector, 'technology', None))
        return lines

    def _create_data_lines(self, datafile):
        lines = []

        lines += self._create_keyword_line('SPECTRUM')

        datum = next(iter(datafile.data.findvalues(Analysis1D)))
        for i in range(0, len(datum), self._NCOLUMNS):
            values = ['%e' % d \
                      for d in datum[i:i + self._NCOLUMNS]]
            lines.append(', '.join(values))

        lines += self._create_keyword_line('ENDOFDATA')

        return lines

    def _create_checkum_lines(self, lines):
        value = calculate_checksum(lines)
        return [self._create_keyword_line('CHECKSUM', value)]

class ExporterEMSA(_Exporter):

    SUPPORTED_EXTENSIONS = ('.emsa',)

    def _create_thread(self, datafile, filepath, *args, **kwargs):
        return _ExporterEMSAThread(datafile, filepath)

    def validate(self, datafile, filepath):
        _Exporter.validate(self, datafile, filepath)

        data = datafile.data.findkeys(Analysis1D)
        if not data:
            raise ValueError('Datafile must contain an Analysis1D datum')
        if len(data) > 1:
            raise ValueError('Datafile must contain only 1 Analysis1D datum')

        detectors = datafile.conditions.findkeys(DetectorSpectrometer)
        if not detectors:
            raise ValueError('Datafile must contain a DetectorSpectrometer')
        if len(detectors) > 1:
            raise ValueError('Datafile must contain only 1 DetectorSpectrometer')
