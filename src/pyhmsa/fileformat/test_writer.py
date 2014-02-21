#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import os
import tempfile
import shutil
import datetime
import xml.etree.ElementTree as etree
import binascii
import struct

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.fileformat.writer import HMSAWriter
from pyhmsa.spec.condition.instrument import Instrument
from pyhmsa.spec.condition.probe import ProbeEM
from pyhmsa.spec.condition.detector import DetectorSpectrometerXEDS
from pyhmsa.spec.condition.calibration import CalibrationLinear
from pyhmsa.spec.datum.analysis import Analysis1D
from pyhmsa.type.language import langstr

# Globals and constants variables.
from pyhmsa.spec.condition.probe import GUN_TYPE_SCHOTTKY_FEG
from pyhmsa.spec.condition.detector import XEDS_TECHNOLOGY_SDD, SIGNAL_TYPE_EDS

class TestHMSAWriter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestHMSAWriter, cls).setUpClass()

        cls.tmpdir = tempfile.mkdtemp()
        filepath = os.path.join(cls.tmpdir, 'breccia_eds.xml')

        with HMSAWriter(filepath) as writer:
            writer.header.title = 'Breccia - EDS sum spectrum'
            writer.header.date = datetime.date(2013, 7, 29)
            writer.header.time = datetime.time(14, 42, 10)
            writer.header.author = 'Clayton Microbeam Laboratory; CSIRO Process Science and Engineering.'
            writer.header.timezone = 'AUS Eastern Standard Time'
            writer.header['AuthorSoftware'] = 'EpmxToHmsa'

            manufacturer = langstr('JEOL Ltd.', {'ja': b'\xe6\x97\xa5\xe6\x9c\xac\xe9\x9b\xbb\xe5\xad\x90\xe6\xa0\xaa\xe5\xbc\x8f\xe4\xbc\x9a\xe7\xa4\xbe'.decode('utf-8')})
            instrument = Instrument(manufacturer, 'JXA 8500F-CL')
            writer.conditions['Inst0'] = instrument

            probe = ProbeEM(15.0, beam_current=47.59, scan_magnification=2500.0,
                            gun_type=GUN_TYPE_SCHOTTKY_FEG)
            writer.conditions['Probe0'] = probe

            calibration = CalibrationLinear('Energy', 'eV', 2.49985, -237.098251)
            detector = DetectorSpectrometerXEDS(4096, calibration,
                                                technology=XEDS_TECHNOLOGY_SDD,
                                                nominal_throughput=(180.0, 'kcps'),
                                                strobe_rate=2000.0,
                                                signal_type=SIGNAL_TYPE_EDS,
                                                manufacturer='Bruker AXS',
                                                model='XFLASH 4010',
                                                elevation=40.0,
                                                area=20.0)
            writer.conditions['EDS'] = detector

            analysis = Analysis1D(4096, np.int32,
                                  buffer=np.arange(4096, dtype=np.int32))
            writer.data['EDS sum spectrum'] = analysis

            cls.uid = binascii.hexlify(writer.uid).upper()

    @classmethod
    def tearDownClass(cls):
        super(TestHMSAWriter, cls).tearDownClass()
        shutil.rmtree(cls.tmpdir, ignore_errors=True)

    def setUp(self):
        unittest.TestCase.setUp(self)

        filepath = os.path.join(self.tmpdir, 'breccia_eds.xml')
        with open(filepath, 'rb') as fp:
            self.root = etree.parse(fp).getroot()

        filepath = os.path.join(self.tmpdir, 'breccia_eds.hmsa')
        self.hmsa = open(filepath, 'rb')

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.hmsa.close()

    def testroot(self):
        self.assertEqual('1.0', self.root.get('Version'))
        self.assertEqual('en-US', self.root.get('{http://www.w3.org/XML/1998/namespace}lang'))
        self.assertEqual(self.uid, self.root.get('UID').encode('ascii'))

    def testheader(self):
        element = self.root.find('Header')
        self.assertEqual('Breccia - EDS sum spectrum', element.find('Title').text)
        self.assertEqual('2013-07-29', element.find('Date').text)
        self.assertEqual('14:42:10', element.find('Time').text)
        self.assertEqual('Clayton Microbeam Laboratory; CSIRO Process Science and Engineering.', element.find('Author').text)
        self.assertEqual('EpmxToHmsa', element.find('AuthorSoftware').text)
        self.assertEqual('AUS Eastern Standard Time', element.find('Timezone').text)
#
    def testconditions(self):
        element = self.root.find('Conditions/Instrument')
        self.assertEqual('Inst0', element.get('ID'))
        self.assertEqual('JEOL Ltd.', element.find('Manufacturer').text)
        self.assertEqual(b'\xe6\x97\xa5\xe6\x9c\xac\xe9\x9b\xbb\xe5\xad\x90\xe6\xa0\xaa\xe5\xbc\x8f\xe4\xbc\x9a\xe7\xa4\xbe',
                         element.find('Manufacturer').get('alt-lang-ja').encode('utf-8'))
        self.assertEqual('JXA 8500F-CL', element.find('Model').text)

        element = self.root.find('Conditions/Probe')
        self.assertEqual('Probe0', element.get('ID'))
        self.assertEqual('15.0', element.find('BeamVoltage').text)
        self.assertEqual('kV', element.find('BeamVoltage').get('Unit'))
        self.assertEqual('47.59', element.find('BeamCurrent').text)
        self.assertEqual('nA', element.find('BeamCurrent').get('Unit'))
        self.assertEqual('2500.0', element.find('ScanMagnification').text)
        self.assertEqual('Schottky FEG', element.find('GunType').text)

        element = self.root.find('Conditions/Detector')
        self.assertEqual('EDS', element.get('ID'))
        self.assertEqual('4096', element.find('ChannelCount').text)
        self.assertEqual("Energy", element.find('Calibration/Quantity').text)
        self.assertEqual("eV", element.find('Calibration/Unit').text)
        self.assertEqual('2.49985', element.find('Calibration/Gain').text)
        self.assertEqual('-237.098251', element.find('Calibration/Offset').text)
        self.assertEqual('EDS', element.find('SignalType').text)
        self.assertEqual('Bruker AXS', element.find('Manufacturer').text)
        self.assertEqual('XFLASH 4010', element.find('Model').text)
        self.assertEqual('20.0', element.find('Area').text)
        self.assertEqual('mm2', element.find('Area').get('Unit'))
        self.assertEqual('SDD', element.find('Technology').text)
        self.assertEqual('2000.0', element.find('StrobeRate').text)
        self.assertEqual('Hz', element.find('StrobeRate').get('Unit'))
        self.assertEqual('180.0', element.find('NominalThroughput').text)
        self.assertEqual('kcps', element.find('NominalThroughput').get('Unit'))
        self.assertEqual('40.0', element.find('Elevation').text)
        self.assertEqual(u'\u00b0', element.find('Elevation').get('Unit'))

    def testdata_xml(self):
        element = self.root.find('Data/Analysis')
        self.assertEqual('EDS sum spectrum', element.get('Name'))
        self.assertEqual('8', element.find('DataOffset').text)
        self.assertEqual('16384', element.find('DataLength').text)
        self.assertEqual('int32', element.find('DatumType').text)
        self.assertEqual('4096', element.find('DatumDimensions/Dimension').text)
        self.assertEqual('Channel', element.find('DatumDimensions/Dimension').get('Name'))

    def testdata_binary(self):
        uid = binascii.hexlify(self.hmsa.read(8)).upper()
        self.assertEqual(uid, self.root.get('UID').encode('ascii'))

        buffer = self.hmsa.read()
        self.assertEqual(16384, len(buffer))

        self.assertEqual(0, struct.unpack('<i', buffer[:4])[0])
        self.assertEqual(4095, struct.unpack('<i', buffer[-4:])[0])

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
