#!/usr/bin/env python
"""
================================================================================
:mod:`emsa` -- Importer from EMSA file format
================================================================================

.. module:: emsa
   :synopsis: Importer from EMSA file format

.. inheritance-diagram:: pyhmsa.fileformat.importer.emsa

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2014 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import datetime

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.fileformat.importer.importer import _Importer, _ImporterThread
from pyhmsa.fileformat.common.emsa import calculate_checksum

from pyhmsa.datafile import DataFile
from pyhmsa.spec.header import Header
from pyhmsa.spec.condition.probe import ProbeEM, ProbeTEM
from pyhmsa.spec.condition.acquisition import AcquisitionPoint
from pyhmsa.spec.condition.specimenposition import SpecimenPosition
from pyhmsa.spec.condition.detector import \
    (DetectorSpectrometer, DetectorSpectrometerXEDS, DetectorSpectrometerCL,
     Window)
from pyhmsa.spec.condition.calibration import CalibrationLinear
from pyhmsa.spec.datum.analysis import Analysis1D

from pyhmsa.util.parsedict import parsedict

# Globals and constants variables.
from pyhmsa.spec.condition.detector import \
    (COLLECTION_MODE_PARALLEL, COLLECTION_MODE_SERIAL,
     XEDS_TECHNOLOGY_GE, XEDS_TECHNOLOGY_SILI, XEDS_TECHNOLOGY_SDD,
     XEDS_TECHNOLOGY_UCAL,
     SIGNAL_TYPE_EDS, SIGNAL_TYPE_WDS, SIGNAL_TYPE_CLS)
from pyhmsa.fileformat.common.emsa import \
    (EMSA_ELS_DETECTOR_SERIAL, EMSA_ELS_DETECTOR_PARALL,
     EMSA_EDS_DETECTOR_SIBEW, EMSA_EDS_DETECTOR_SIUTW, EMSA_EDS_DETECTOR_SIWLS,
     EMSA_EDS_DETECTOR_GEBEW, EMSA_EDS_DETECTOR_GEUTW, EMSA_EDS_DETECTOR_GEWLS,
     EMSA_EDS_DETECTOR_SDBEW, EMSA_EDS_DETECTOR_SDUTW, EMSA_EDS_DETECTOR_SDWLS,
     EMSA_EDS_DETECTOR_UCALUTW)

_ELSDET_TO_COLLECTION_MODE = \
    {EMSA_ELS_DETECTOR_PARALL: COLLECTION_MODE_PARALLEL,
     EMSA_ELS_DETECTOR_SERIAL: COLLECTION_MODE_SERIAL}
_EDSDET_TO_XEDS_TECHNOLOGY = \
    {EMSA_EDS_DETECTOR_SIBEW: XEDS_TECHNOLOGY_SILI,
     EMSA_EDS_DETECTOR_SIUTW: XEDS_TECHNOLOGY_SILI,
     EMSA_EDS_DETECTOR_SIWLS: XEDS_TECHNOLOGY_SILI,
     EMSA_EDS_DETECTOR_GEBEW: XEDS_TECHNOLOGY_GE,
     EMSA_EDS_DETECTOR_GEUTW: XEDS_TECHNOLOGY_GE,
     EMSA_EDS_DETECTOR_GEWLS: XEDS_TECHNOLOGY_GE,
     EMSA_EDS_DETECTOR_SDBEW: XEDS_TECHNOLOGY_SDD,
     EMSA_EDS_DETECTOR_SDUTW: XEDS_TECHNOLOGY_SDD,
     EMSA_EDS_DETECTOR_SDWLS: XEDS_TECHNOLOGY_SDD,
     EMSA_EDS_DETECTOR_UCALUTW: XEDS_TECHNOLOGY_UCAL}

class _ImporterEMSAThread(_ImporterThread):

    def _run(self, filepath, *args, **kwargs):
        emsa_file = None
        try:
            # Parse EMSA file
            emsa_file = open(filepath, 'rt')
            lines = emsa_file.readlines()

            self._update_status(0.1, 'Verify checksum')
            self._verify_checksum(lines)

            self._update_status(0.2, 'Parse keywords')
            keywords = self._parse_keywords(lines)

            self._update_status(0.3, 'Parse data')
            buffer = self._parse_data(lines, keywords)

            # Create data file
            datafile = DataFile()

            self._update_status(0.4, 'Extracting header')
            datafile.header.update(self._extract_header(keywords))

            self._update_status(0.5, 'Extracting probe')
            datafile.conditions.update(self._extract_probe(keywords))

            self._update_status(0.6, 'Extracting acquisition')
            datafile.conditions.update(self._extract_acquisition(keywords))

            self._update_status(0.7, 'Extracting detector')
            datafile.conditions.update(self._extract_detector(keywords))

            datum = Analysis1D(len(buffer), dtype=buffer.dtype,
                               buffer=np.ravel(buffer),
                               conditions=datafile.conditions)
            datafile.data['Spectrum'] = datum
        finally:
            if emsa_file is not None:
                emsa_file.close()

        return datafile

    def _is_line_keyword(self, line):
        try:
            return line.strip()[0] == '#'
        except:
            return False

    def _verify_checksum(self, lines):
        for line in lines:
            if not self._is_line_keyword(line):
                continue

            tag, _comment, expected_checksum = self._parse_keyword_line(line)
            if tag == 'ENDOFDATA':
                return # No checksum

            if tag == 'CHECKSUM':
                break

        actual_checksum = calculate_checksum(lines)
        if actual_checksum != expected_checksum:
            raise IOError("The checksums don't match: %i != %i " % \
                          (actual_checksum, expected_checksum))

    def _parse_keywords(self, lines):
        keywords = parsedict()

        # First pass
        for line in lines:
            if not self._is_line_keyword(line):
                break

            tag, _comment, value = self._parse_keyword_line(line)
            if tag == 'SPECTRUM':
                break

            keywords.setdefault(tag, []).append(value)

        # Second pass (remove list if only one value)
        for tag, values in keywords.items():
            if len(values) == 1:
                keywords[tag] = values[0]
            else:
                keywords[tag] = tuple(values)

        return keywords

    def _parse_keyword_line(self, line):
        line = line.strip("#") # Strip keyword character

        tag, value = line.split(":", 1)

        tag = tag.strip()
        value = value.strip()

        try:
            tag, comment = tag.split()
        except:
            comment = ""

        tag = tag.upper()
        comment = comment.strip("-")

        return tag, comment, value

    def _parse_data(self, lines, keywords):
        # Filter to get only data lines
        lines = filter(lambda line: not self._is_line_keyword(line), lines)

        # Read based on data type
        datatype = keywords.get('DATATYPE')
        if datatype is None:
            raise ValueError('No DATATYPE specified')

        datatype = datatype.upper()
        if datatype == 'XY':
            data = self._parse_data_xy(lines, keywords)
        elif datatype == 'Y':
            data = self._parse_data_y(lines, keywords)
        else:
            raise ValueError('Unknown data type')

        # Check number of points
        npoints = int(float(keywords.get('NPOINTS', len(data))))
        if npoints != len(data):
            raise ValueError('Inconsistent number of points. NPOINTS=%i != len(data)=%i' % \
                             (npoints, len(data)))

        return data

    def _parse_data_xy(self, lines, keywords):
        data = []

        for line in lines:
            data.append(self._parse_data_line(line))

        return np.array(data)[:, 1]

    def _parse_data_y(self, lines, keywords):
        ydata = []
        for line in lines:
            ydata.extend(self._parse_data_line(line))

        return np.array(ydata)

    def _parse_data_line(self, line):
        # Split values separated by a comma
        tmprow = [value.strip() for value in line.split(',')]

        # Split values separated by a space
        row = []
        for value in tmprow:
            row.extend(value.split())

        # Convert to float
        row = list(map(float, row))

        return row

    def _extract_header(self, keywords):
        header = Header()

        header.title = keywords['TITLE']
        header.date = \
            datetime.datetime.strptime(keywords['DATE'], '%d-%b-%Y').date()
        header.time = \
            datetime.datetime.strptime(keywords['TIME'], '%H:%M').time()
        header.author = keywords['OWNER']

        return header

    def _extract_probe(self, keywords):
        if 'BEAMKV' not in keywords:
            return {}

        kwargs = {}
        kwargs['beam_voltage'] = (keywords.getfloat('BEAMKV'), 'kV')
        kwargs['beam_current'] = (keywords.getfloat('PROBECUR'), 'nA')
        kwargs['emission_current'] = (keywords.getfloat('EMISSION'), 'uA')
        kwargs['beam_diameter'] = (keywords.getfloat('BEAMDIAM'), 'nm')
        kwargs['scan_magnification'] = keywords.getint('MAGCAM')

        if 'OPERMODE' in keywords:
            kwargs['lens_mode'] = keywords.get('OPERMODE') # Enums are identical
            kwargs['convergence_angle'] = (keywords.getfloat('CONVANGLE'), 'mrad')
            c = ProbeTEM(**kwargs)
        else:
            c = ProbeEM(**kwargs)

        return {'Probe0': c}

    def _extract_acquisition(self, keywords):
        if 'XPOSITION' not in keywords or \
                'YPOSITION' not in keywords or \
                'ZPOSITION' not in keywords:
            return {}

        position = SpecimenPosition(x=keywords.getfloat('XPOSITION'),
                                    y=keywords.getfloat('YPOSITION'),
                                    z=keywords.getfloat('ZPOSITION')) #FIXME: Handle XTILTSTGE and YTILTSTGE
        dwell_time = (keywords.get('DWELLTIME'), 'ms')
        if 'INTEGTIME' in keywords:
            total_time = (keywords.getfloat('INTEGTIME'), 'ms')
        else:
            total_time = (keywords.getfloat('REALTIME'), 's')
        dwell_time_live = (keywords.getfloat('LIVETIME'), 's')

        c = AcquisitionPoint(position, dwell_time, total_time, dwell_time_live)

        return {'Acq0': c}

    def _extract_detector(self, keywords):
        if 'SIGNALTYPE' not in keywords:
            return {}

        signal_type = keywords.get('SIGNALTYPE') # Enums is identical

        kwargs = {}

        kwargs['signal_type'] = signal_type
        kwargs['channel_count'] = keywords.getint('NPOINTS')

        quantity = keywords.get('XLABEL', 'x')
        unit = keywords.get('XUNITS')
        gain = keywords.getfloat('XPERCHAN')
        offset = keywords.getfloat('OFFSET')
        kwargs['calibration'] = CalibrationLinear(quantity, unit, gain, offset)

        kwargs['measurement_unit'] = keywords.get('yunits')
        kwargs['elevation'] = (keywords.getfloat('ELEVANGLE'), 'degrees')
        kwargs['azimuth'] = (keywords.getfloat('AZIMANGLE'), 'degrees')
        kwargs['solid_angle'] = (keywords.getfloat('SOLIDANGLE'), 'sr')
        kwargs['semi_angle'] = (keywords.getfloat('COLLANGLE'), 'mrad')

        kwargs['collection_mode'] = \
                _ELSDET_TO_COLLECTION_MODE.get(keywords.get('ELSDET'))

        if signal_type in [SIGNAL_TYPE_EDS, SIGNAL_TYPE_WDS]:
            window = Window()
            if 'TDEADLYR' in keywords:
                window.append_layer('Dead layer', (keywords.getfloat('TDEADLYR') * 1e4, 'um'))
            if 'TACTLYR' in keywords:
                window.append_layer('Active Layer', (keywords.getfloat('TACTLYR') * 1e4, 'um'))
            if 'TBEWIND' in keywords:
                window.append_layer('Be window', (keywords.getfloat('TBEWIND') * 1e4, 'um'))
            if 'TAUWIND' in keywords:
                window.append_layer('Au window', (keywords.getfloat('TAUWIND') * 1e4, 'um'))
            if 'TALWIND' in keywords:
                window.append_layer('Al window', (keywords.getfloat('TALWIND') * 1e4, 'um'))
            if 'TPYWIND' in keywords:
                window.append_layer('Pyrolene window', (keywords.getfloat('TPYWIND') * 1e4, 'um'))
            if 'TBNWIND' in keywords:
                window.append_layer('Boron-Nitride window', (keywords.getfloat('TBNWIND') * 1e4, 'um'))
            if 'TDIWIND' in keywords:
                window.append_layer('Diamond window', (keywords.getfloat('TDIWIND') * 1e4, 'um'))
            if 'THCWIND' in keywords:
                window.append_layer('HydroCarbon window', (keywords.getfloat('TDIWIND') * 1e4, 'um'))
            if window.layers:
                kwargs['window'] = window

        if signal_type == SIGNAL_TYPE_EDS:
            kwargs['technology'] = \
                _EDSDET_TO_XEDS_TECHNOLOGY.get(keywords.get('EDSDET'))
            c = DetectorSpectrometerXEDS(**kwargs)
        elif signal_type == SIGNAL_TYPE_CLS:
            c = DetectorSpectrometerCL(**kwargs)
        else:
            c = DetectorSpectrometer(**kwargs)

        return {signal_type: c}

class ImporterEMSA(_Importer):

    SUPPORTED_EXTENSIONS = ('.emsa',)

    def _create_thread(self, filepath, *args, **kwargs):
        return _ImporterEMSAThread(filepath)
