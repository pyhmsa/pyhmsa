#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import unittest
import logging
import os
import datetime

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.fileformat.reader import HMSAReader

# Globals and constants variables.

class TestHMSAReader(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        testdatadir = os.path.join(os.path.dirname(__file__), '..', 'testdata')
        filepath = os.path.join(testdatadir, 'breccia_eds.xml')
        self.reader = HMSAReader(filepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testroot(self):
        with self.reader:
            self.assertEqual('1.0', self.reader.version)
            self.assertEqual('en-US', self.reader.language)
            self.assertEqual(b'60606EE485B42736', self.reader.uid)

    def testheader(self):
        with self.reader:
            header = self.reader.header

        self.assertEqual('Breccia - EDS sum spectrum', header.title)
        self.assertEqual(datetime.date(2013, 7, 29), header.date)
        self.assertEqual(datetime.time(14, 42, 10), header.time)
        self.assertEqual('Clayton Microbeam Laboratory; CSIRO Process Science and Engineering.', header.author)
        self.assertEqual('EpmxToHmsa', header['AuthorSoftware'])
        self.assertEqual('AUS Eastern Standard Time', header.timezone)

    def testconditions(self):
        with self.reader:
            conditions = self.reader.conditions

        self.assertEqual(3, len(conditions))

        instrument = conditions['Inst0']
        self.assertEqual('JEOL Ltd.', instrument.manufacturer)
        self.assertEqual(b'\xe6\x97\xa5\xe6\x9c\xac\xe9\x9b\xbb\xe5\xad\x90\xe6\xa0\xaa\xe5\xbc\x8f\xe4\xbc\x9a\xe7\xa4\xbe',
                         instrument.manufacturer.alternatives['ja'].encode('utf-8'))
        self.assertEqual('JXA 8500F-CL', instrument.model)

        probe = conditions['Probe0']
        self.assertAlmostEqual(15.0, probe.beam_voltage, 4)
        self.assertEqual('kV', probe.beam_voltage.unit)
        self.assertAlmostEqual(47.59, probe.beam_current, 4)
        self.assertEqual('nA', probe.beam_current.unit)
        self.assertAlmostEqual(2500.0, probe.scan_magnification, 4)
        self.assertEqual('Schottky FEG', probe.gun_type)

        detector = conditions['EDS']
        self.assertEqual(4096, detector.channel_count)
        self.assertEqual("Energy", detector.calibration.quantity)
        self.assertEqual("eV", detector.calibration.unit)
        self.assertAlmostEqual(2.49985, detector.calibration.gain, 4)
        self.assertAlmostEqual(-237.098251, detector.calibration.offset, 4)
        self.assertEqual('EDS', detector.signal_type)
        self.assertEqual('Bruker AXS', detector.manufacturer)
        self.assertEqual('XFLASH 4010', detector.model)
        self.assertAlmostEqual(20.0, detector.area, 4)
        self.assertEqual('mm2', detector.area.unit)
        self.assertEqual('SDD', detector.technology)
        self.assertAlmostEqual(2000.0, detector.strobe_rate, 4)
        self.assertEqual('Hz', detector.strobe_rate.unit)
        self.assertAlmostEqual(180.0, detector.nominal_throughput, 4)
        self.assertEqual('kcps', detector.nominal_throughput.unit)
        self.assertAlmostEqual(40.0, detector.elevation, 4)
        self.assertEqual(u'\u00b0', detector.elevation.unit)

    def testdata(self):
        with self.reader:
            data = self.reader.data

        self.assertEqual(1, len(data))

        analysis = data['EDS sum spectrum']
        self.assertEqual(4096, analysis.channels)
        self.assertEqual(0, len(analysis.conditions))
        self.assertEqual(np.int64, analysis.dtype.type)
        self.assertEqual(0, analysis[0])
        self.assertEqual(395, analysis[-1])

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
