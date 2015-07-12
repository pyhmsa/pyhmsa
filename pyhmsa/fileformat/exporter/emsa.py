"""
Exporter to EMSA file format.
"""

# Standard library modules.
import os

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

def _create_keyword_line(tag, value=''):
    if value is None:
        return []
    tag = tag.ljust(12)
    assert len(tag) == 12
    return ["#%s: %s" % (tag, value)]

class _ExporterEMSAThread(_ExporterThread):

    _NCOLUMNS = 4

    def _run(self, datafile, dirpath, *args, **kwargs):
        basefilename = datafile.header.title or 'Untitled'

        items = datafile.data.finditems(Analysis1D)
        length = len(items)
        filepaths = []

        for i, item in enumerate(items):
            identifier, datum = item
            detector = next(iter(datum.conditions.findvalues(DetectorSpectrometer)))

            self._update_status(i / length, 'Exporting %s' % identifier)
            lines = self._create_lines(datafile, datum, detector)

            filename = basefilename + '_' + identifier + '.emsa'
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'w') as fp:
                fp.write('\n'.join(lines))

            filepaths.append(filepath)

        return filepaths

    def _create_lines(self, datafile, datum, detector):
        lines = []
        lines += self._create_header_lines(datafile, datum, detector)
        lines += self._create_required_keywords_lines(datafile, datum, detector)
        lines += self._create_optional_keywords_lines(datafile, datum, detector)
        lines += self._create_data_lines(datafile, datum, detector)
        return lines

    def _create_header_lines(self, datafile, datum, detector):
        lines = []
        lines += _create_keyword_line('FORMAT', 'EMSA/MAS Spectral Data File')
        lines += _create_keyword_line('VERSION', '1.0')
        return lines

    def _create_required_keywords_lines(self, datafile, datum, detector):
        header = datafile.header

        lines = []
        lines += _create_keyword_line('TITLE', header.title)
        lines += _create_keyword_line('DATE', header.date.strftime('%d-%b-%Y'))
        lines += _create_keyword_line('TIME', header.time.strftime('%H:%M'))
        lines += _create_keyword_line('OWNER', header.author)
        lines += _create_keyword_line('NPOINTS', len(datum))
        lines += _create_keyword_line('NCOLUMNS', self._NCOLUMNS)
        lines += _create_keyword_line('XUNITS', detector.calibration.unit)
        lines += _create_keyword_line('YUNITS', detector.measurement_unit)
        lines += _create_keyword_line('DATATYPE', 'Y')
        lines += _create_keyword_line('XPERCHAN', detector.calibration.gain)
        lines += _create_keyword_line('OFFSET', detector.calibration.offset)
        return lines

    def _create_optional_keywords_lines(self, datafile, datum, detector):
        probes = datafile.conditions.findvalues(_Probe)
        probe = next(iter(probes)) if probes else None
        acqs = datafile.conditions.findvalues(AcquisitionPoint)
        acq = next(iter(acqs)) if acqs else None

        lines = []
        lines += _create_keyword_line('SIGNALTYPE', detector.signal_type)
        lines += _create_keyword_line('XLABEL', detector.calibration.quantity)
#        lines += _create_keyword_line('YLABEL', )

        if probe:
            if probe.beam_voltage is not None:
                beamkv = float(convert_unit('kV', probe.beam_voltage))
                lines += _create_keyword_line('BEAMKV', beamkv)

            if probe.emission_current is not None:
                emission = float(convert_unit('uA', probe.emission_current))
                lines += _create_keyword_line('EMISSION', emission)

            if probe.beam_current is not None:
                probecur = float(convert_unit('nA', probe.beam_current))
                lines += _create_keyword_line('PROBECUR', probecur)

            if probe.beam_diameter is not None:
                beamdiam = float(convert_unit('nm', probe.beam_diameter))
                lines += _create_keyword_line('BEAMDIAM', beamdiam)

            if probe.scan_magnification is not None:
                magcam = int(probe.scan_magnification)
                lines += _create_keyword_line('MAGCAM', magcam)

            convangle = getattr(probe, 'convergence_angle', None)
            if convangle is not None:
                convangle = float(convert_unit('mrad', convangle))
                lines += _create_keyword_line('CONVANGLE', convangle)

            opermode = getattr(probe, 'lens_mode', None)
            if opermode is not None:
                lines += _create_keyword_line('OPERMODE', opermode)

        if acq and acq.position is not None:
            xposition = float(convert_unit('mm', acq.position.x))
            lines += _create_keyword_line('XPOSITION', xposition)

            yposition = float(convert_unit('mm', acq.position.y))
            lines += _create_keyword_line('YPOSITION', yposition)

            zposition = float(convert_unit('mm', acq.position.z))
            lines += _create_keyword_line('ZPOSITION', zposition)

        if acq:
            if acq.dwell_time is not None:
                dwelltime = float(convert_unit('ms', acq.dwell_time))
                lines += _create_keyword_line('DWELLTIME', dwelltime)

            if acq.total_time is not None:
                integtime = float(convert_unit('ms', acq.total_time))
                lines += _create_keyword_line('INTEGTIME', integtime)

            if acq.dwell_time_live is not None:
                livetime = float(convert_unit('s', acq.dwell_time_live))
                lines += _create_keyword_line('LIVETIME', livetime)

            if acq.total_time is not None:
                realtime = float(convert_unit('s', acq.total_time))
                lines += _create_keyword_line('REALTIME', realtime)

        if detector.semi_angle is not None:
            collangle = float(convert_unit('mrad', detector.semi_angle))
            lines += _create_keyword_line('COLLANGLE', collangle)

        if detector.collection_mode is not None:
            elsdet = detector.collection_mode
            lines += _create_keyword_line('ELSDET', elsdet)

        if detector.elevation is not None:
            elevangle = float(convert_unit('degrees', detector.elevation))
            lines += _create_keyword_line('ELEVANGLE', elevangle)

        if detector.azimuth is not None:
            azimangle = float(convert_unit('degrees', detector.azimuth))
            lines += _create_keyword_line('AZIMANGLE', azimangle)

        if detector.solid_angle is not None:
            solidangle = float(convert_unit('sr', detector.solid_angle))
            lines += _create_keyword_line('SOLIDANGLE', solidangle)

#        if acq and acq.window:
#            lines += _create_keyword_line('TDEADLYR',)
#            lines += _create_keyword_line('TACTLYR',)
#            lines += _create_keyword_line('TBEWIND',)
#            lines += _create_keyword_line('TAUWIND',)
#            lines += _create_keyword_line('TALWIND',)
#            lines += _create_keyword_line('TPYWIND',)
#            lines += _create_keyword_line('TBNWIND',)
#            lines += _create_keyword_line('TDIWIND',)
#            lines += _create_keyword_line('THCWIND',)
        lines += _create_keyword_line('EDSDET', getattr(detector, 'technology', None))
        return lines

    def _create_data_lines(self, datafile, datum, detector):
        lines = []

        lines += _create_keyword_line('SPECTRUM')

        for i in range(0, len(datum), self._NCOLUMNS):
            values = ['%e' % d \
                      for d in datum[i:i + self._NCOLUMNS]]
            lines.append(', '.join(values))

        lines += _create_keyword_line('ENDOFDATA')

        return lines

    def _create_checkum_lines(self, lines):
        value = calculate_checksum(lines)
        return [_create_keyword_line('CHECKSUM', value)]

class ExporterEMSA(_Exporter):

    def _create_thread(self, datafile, dirpath, *args, **kwargs):
        return _ExporterEMSAThread(datafile, dirpath)

    def validate(self, datafile):
        _Exporter.validate(self, datafile)

        items = datafile.data.finditems(Analysis1D)
        if not items:
            raise ValueError('Datafile must contain at least one Analysis1D datum')

        for identifier, datum in items:
            detectors = datum.conditions.findkeys(DetectorSpectrometer)
            if not detectors:
                raise ValueError('Datum "%s" does not have a DetectorSpectrometer' % identifier)
