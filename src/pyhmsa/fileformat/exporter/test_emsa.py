#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2014 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import unittest
import logging
import os
import tempfile
import shutil
import datetime

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.fileformat.exporter.emsa import ExporterEMSA

from pyhmsa.datafile import DataFile
from pyhmsa.spec.condition.detector import DetectorSpectrometerXEDS
from pyhmsa.spec.condition.calibration import CalibrationLinear
from pyhmsa.spec.condition.probe import ProbeEM
from pyhmsa.spec.datum.analysis import Analysis1D

# Globals and constants variables.
from pyhmsa.spec.condition.detector import XEDS_TECHNOLOGY_SDD, SIGNAL_TYPE_EDS

class TestExporterEMSA(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.tmpdir = tempfile.mkdtemp()
        self.exp = ExporterEMSA()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _create_datafile(self):
        datafile = DataFile()

        datafile.header.title = 'Breccia - EDS sum spectrum'
        datafile.header.date = datetime.date(2013, 7, 29)
        datafile.header.time = datetime.time(14, 42, 10)
        datafile.header.author = 'Clayton Microbeam Laboratory; CSIRO Process Science and Engineering.'
        datafile.header.timezone = 'AUS Eastern Standard Time'
        datafile.header['AuthorSoftware'] = 'EpmxToHmsa'

        probe = ProbeEM(beam_voltage=(15000.0, 'V'),
                        beam_current=47.59,
                        scan_magnification=2500.0)
        datafile.conditions['Probe0'] = probe

        calibration = CalibrationLinear('Energy', 'eV', 2.49985, -237.098251)
        detector = DetectorSpectrometerXEDS(4096, calibration,
                                            technology=XEDS_TECHNOLOGY_SDD,
                                            nominal_throughput=(180.0, 'kcounts/s'),
                                            strobe_rate=2000.0,
                                            signal_type=SIGNAL_TYPE_EDS,
                                            manufacturer='Bruker AXS',
                                            model='XFLASH 4010',
                                            elevation=40.0,
                                            area=20.0)
        datafile.conditions['EDS'] = detector

        analysis = Analysis1D(1024, np.int32,
                              buffer=np.arange(1024, dtype=np.int32))
        datafile.data['EDS sum spectrum'] = analysis

        return datafile

    def testexport1(self):
        datafile = self._create_datafile()
        filepath = os.path.join(self.tmpdir, 'test.emsa')
        self.exp.export(datafile, filepath)
        self.exp.join()

        with open(filepath, 'r') as fp:
            lines = fp.readlines()

        self.assertEqual(278, len(lines))

    def testcan_export(self):
        datafile = self._create_datafile()
        filepath = os.path.join(self.tmpdir, 'test.emsa')
        self.assertTrue(self.exp.can_export(datafile, filepath))

        datafile = DataFile()
        filepath = os.path.join(self.tmpdir, 'test.emsa')
        self.assertFalse(self.exp.can_export(datafile, filepath))

        datafile = self._create_datafile()
        filepath = os.path.join(self.tmpdir, 'test.txt')
        self.assertFalse(self.exp.can_export(datafile, filepath))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
