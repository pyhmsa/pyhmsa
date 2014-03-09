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
import datetime
import tempfile
import shutil
import xml.etree.ElementTree as etree
import binascii
import struct

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.datafile import DataFile
from pyhmsa.spec.datum.analysis import Analysis0D, Analysis1D
from pyhmsa.spec.condition.elementalid import ElementalID
from pyhmsa.spec.condition.instrument import Instrument
from pyhmsa.spec.condition.probe import ProbeEM
from pyhmsa.spec.condition.detector import DetectorSpectrometerXEDS
from pyhmsa.spec.condition.calibration import CalibrationLinear
from pyhmsa.type.language import langstr

# Globals and constants variables.
from pyhmsa.spec.condition.probe import GUN_TYPE_SCHOTTKY_FEG
from pyhmsa.spec.condition.detector import XEDS_TECHNOLOGY_SDD, SIGNAL_TYPE_EDS

class TestDataFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.datafile = DataFile()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testadd_condition(self):
        self.datafile.conditions['cond'] = ElementalID(13)

        self.assertEqual(1, len(self.datafile.conditions))

    def testadd_datum_condition(self):
        datum = Analysis0D(1.0)
        datum.conditions['cond'] = ElementalID(13)
        self.datafile.data['datum'] = datum

        self.assertEqual(1, len(self.datafile.data['datum'].conditions))
        self.assertEqual(1, len(self.datafile.conditions))

    def testadd_datum_condition2(self):
        datum = Analysis0D(1.0)
        self.datafile.data['datum'] = datum
        self.datafile.data['datum'].conditions['cond'] = ElementalID(13)

        self.assertEqual(1, len(self.datafile.data['datum'].conditions))
        self.assertEqual(1, len(self.datafile.conditions))

    def testadd_datum_condition3(self):
        datum = Analysis0D(1.0)
        self.datafile.data['datum'] = datum

        self.datafile.conditions['cond'] = ElementalID(13)

        self.assertRaises(ValueError, self.datafile.data['datum'].conditions.__setitem__,
                          'cond', ElementalID(14))

    def testmodify_datum_condition(self):
        datum = Analysis0D(1.0, conditions={'cond': ElementalID(13)})
        self.datafile.data['datum'] = datum

        datum.conditions['cond'] = ElementalID(14)

        self.assertEqual(1, len(self.datafile.data['datum'].conditions))
        self.assertEqual(1, len(self.datafile.conditions))
        self.assertEqual(14, self.datafile.data['datum'].conditions['cond'].atomic_number)
        self.assertEqual(14, self.datafile.conditions['cond'].atomic_number)

    def testmodify_datum_condition2(self):
        datum = Analysis0D(1.0, conditions={'cond': ElementalID(13)})
        self.datafile.data['datum'] = datum

        self.datafile.conditions['cond'] = ElementalID(14)

        self.assertEqual(1, len(self.datafile.data['datum'].conditions))
        self.assertEqual(1, len(self.datafile.conditions))
        self.assertEqual(14, self.datafile.data['datum'].conditions['cond'].atomic_number)
        self.assertEqual(14, self.datafile.conditions['cond'].atomic_number)

    def testdelete_datum_condition(self):
        datum = Analysis0D(1.0, conditions={'cond': ElementalID(13)})
        self.datafile.data['datum'] = datum

        del datum.conditions['cond']

        self.assertEqual(0, len(self.datafile.data['datum'].conditions))
        self.assertEqual(0, len(self.datafile.conditions))

    def testdelete_datum_condition2(self):
        datum = Analysis0D(1.0, conditions={'cond': ElementalID(13)})
        self.datafile.data['datum'] = datum

        del self.datafile.conditions['cond']

        self.assertEqual(0, len(self.datafile.data['datum'].conditions))
        self.assertEqual(0, len(self.datafile.conditions))

    def testmodify_datum(self):
        datum = Analysis0D(1.0, conditions={'cond': ElementalID(13)})
        self.datafile.data['datum'] = datum

        datum2 = Analysis0D(2.0, conditions={'cond': ElementalID(14)})
        self.datafile.data['datum'] = datum2

        self.assertEqual(1, len(self.datafile.data))
        self.assertEqual(1, len(self.datafile.conditions))
        self.assertEqual(14, self.datafile.data['datum'].conditions['cond'].atomic_number)
        self.assertEqual(14, self.datafile.conditions['cond'].atomic_number)

    def testdelete_datum(self):
        datum = Analysis0D(1.0, conditions={'cond': ElementalID(13)})
        self.datafile.data['datum'] = datum

        del self.datafile.data['datum']

        self.assertEqual(0, len(self.datafile.data))
        self.assertEqual(0, len(self.datafile.conditions))

    def testread(self):
        # Read
        testdatadir = os.path.join(os.path.dirname(__file__), 'testdata')
        filepath = os.path.join(testdatadir, 'breccia_eds.xml')
        datafile = DataFile.read(filepath)

        # Test
        ## Root
        self.assertEqual('1.0', self.datafile.version)
        self.assertEqual('en-US', self.datafile.language)

        ## Header
        header = datafile.header
        self.assertEqual('Breccia - EDS sum spectrum', header.title)
        self.assertEqual(datetime.date(2013, 7, 29), header.date)
        self.assertEqual(datetime.time(14, 42, 10), header.time)
        self.assertEqual('Clayton Microbeam Laboratory; CSIRO Process Science and Engineering.', header.author)
        self.assertEqual('EpmxToHmsa', header['AuthorSoftware'])
        self.assertEqual('AUS Eastern Standard Time', header.timezone)

        ## Conditions
        conditions = datafile.conditions
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

        ## Data
        data = datafile.data
        self.assertEqual(1, len(data))

        analysis = data['EDS sum spectrum']
        self.assertEqual(4096, analysis.channels)
        self.assertEqual(0, len(analysis.conditions))
        self.assertEqual(np.int64, analysis.dtype.type)
        self.assertEqual(0, analysis[0])
        self.assertEqual(395, analysis[-1])

    def testwrite(self):
        # Create datafile
        datafile = DataFile()
        datafile.header.title = 'Breccia - EDS sum spectrum'
        datafile.header.date = datetime.date(2013, 7, 29)
        datafile.header.time = datetime.time(14, 42, 10)
        datafile.header.author = 'Clayton Microbeam Laboratory; CSIRO Process Science and Engineering.'
        datafile.header.timezone = 'AUS Eastern Standard Time'
        datafile.header['AuthorSoftware'] = 'EpmxToHmsa'

        manufacturer = langstr('JEOL Ltd.', {'ja': b'\xe6\x97\xa5\xe6\x9c\xac\xe9\x9b\xbb\xe5\xad\x90\xe6\xa0\xaa\xe5\xbc\x8f\xe4\xbc\x9a\xe7\xa4\xbe'.decode('utf-8')})
        instrument = Instrument(manufacturer, 'JXA 8500F-CL')
        datafile.conditions['Inst0'] = instrument

        probe = ProbeEM(15.0, beam_current=47.59, scan_magnification=2500.0,
                        gun_type=GUN_TYPE_SCHOTTKY_FEG)
        datafile.conditions['Probe0'] = probe

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
        datafile.conditions['EDS'] = detector

        analysis = Analysis1D(4096, np.int32,
                              buffer=np.arange(4096, dtype=np.int32))
        datafile.data['EDS sum spectrum'] = analysis

        # Write
        tmpdir = tempfile.mkdtemp()
        xmlfilepath = os.path.join(tmpdir, 'breccia_eds.xml')
        hmsafilepath = os.path.join(tmpdir, 'breccia_eds.hmsa')
        uid = datafile.write(xmlfilepath)

        # Test
        with open(xmlfilepath, 'rb') as fp:
            root = etree.parse(fp).getroot()
        hmsa = open(hmsafilepath, 'rb')

        ## Root
        self.assertEqual('1.0', root.get('Version'))
        self.assertEqual('en-US', root.get('{http://www.w3.org/XML/1998/namespace}lang'))
        self.assertEqual(uid, root.get('UID').encode('ascii'))

        ## Header
        element = root.find('Header')
        self.assertEqual('Breccia - EDS sum spectrum', element.find('Title').text)
        self.assertEqual('2013-07-29', element.find('Date').text)
        self.assertEqual('14:42:10', element.find('Time').text)
        self.assertEqual('Clayton Microbeam Laboratory; CSIRO Process Science and Engineering.', element.find('Author').text)
        self.assertEqual('EpmxToHmsa', element.find('AuthorSoftware').text)
        self.assertEqual('AUS Eastern Standard Time', element.find('Timezone').text)

        ## Conditions
        element = root.find('Conditions/Instrument')
        self.assertEqual('Inst0', element.get('ID'))
        self.assertEqual('JEOL Ltd.', element.find('Manufacturer').text)
        self.assertEqual(b'\xe6\x97\xa5\xe6\x9c\xac\xe9\x9b\xbb\xe5\xad\x90\xe6\xa0\xaa\xe5\xbc\x8f\xe4\xbc\x9a\xe7\xa4\xbe',
                         element.find('Manufacturer').get('alt-lang-ja').encode('utf-8'))
        self.assertEqual('JXA 8500F-CL', element.find('Model').text)

        element = root.find('Conditions/Probe')
        self.assertEqual('Probe0', element.get('ID'))
        self.assertEqual('15.0', element.find('BeamVoltage').text)
        self.assertEqual('kV', element.find('BeamVoltage').get('Unit'))
        self.assertEqual('47.59', element.find('BeamCurrent').text)
        self.assertEqual('nA', element.find('BeamCurrent').get('Unit'))
        self.assertEqual('2500.0', element.find('ScanMagnification').text)
        self.assertEqual('Schottky FEG', element.find('GunType').text)

        element = root.find('Conditions/Detector')
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

        ## Data
        element = root.find('Data/Analysis')
        self.assertEqual('EDS sum spectrum', element.get('Name'))
        self.assertEqual('8', element.find('DataOffset').text)
        self.assertEqual('16384', element.find('DataLength').text)
        self.assertEqual('int32', element.find('DatumType').text)
        self.assertEqual('4096', element.find('DatumDimensions/Dimension').text)
        self.assertEqual('Channel', element.find('DatumDimensions/Dimension').get('Name'))

        uid = binascii.hexlify(hmsa.read(8)).upper()
        self.assertEqual(uid, root.get('UID').encode('ascii'))

        buffer = hmsa.read()
        self.assertEqual(16384, len(buffer))

        self.assertEqual(0, struct.unpack('<i', buffer[:4])[0])
        self.assertEqual(4095, struct.unpack('<i', buffer[-4:])[0])

        # Close
        hmsa.close()
        shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
