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

# Third party modules.

# Local modules.
from pyhmsa.datafile import DataFile
from pyhmsa.spec.datum.analysis import Analysis0D
from pyhmsa.spec.condition.elementalid import ElementalID

# Globals and constants variables.

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
        self.assertIs(self.datafile.conditions['cond'],
                      self.datafile.data['datum'].conditions['cond'])

    def testadd_datum_condition2(self):
        datum = Analysis0D(1.0)
        self.datafile.data['datum'] = datum
        self.datafile.data['datum'].conditions['cond'] = ElementalID(13)

        self.assertEqual(1, len(self.datafile.data['datum'].conditions))
        self.assertEqual(1, len(self.datafile.conditions))
        self.assertIs(self.datafile.conditions['cond'],
                      self.datafile.data['datum'].conditions['cond'])

    def testadd_datum_condition3(self):
        datum = Analysis0D(1.0)
        self.datafile.data['datum'] = datum

        self.datafile.conditions['cond'] = ElementalID(13)
        self.datafile.data['datum'].conditions['cond'] = ElementalID(14)

        self.assertEqual(14, self.datafile.conditions['cond'].atomic_number)
        self.assertEqual(14, self.datafile.data['datum'].conditions['cond'].atomic_number)

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

        self.assertEqual(0, len(self.datafile.data['datum'].conditions))
        self.assertEqual(1, len(self.datafile.conditions))
        self.assertEqual(14, self.datafile.conditions['cond'].atomic_number)

    def testdelete_datum_condition(self):
        datum = Analysis0D(1.0, conditions={'cond': ElementalID(13)})
        self.datafile.data['datum'] = datum

        del datum.conditions['cond']

        self.assertEqual(0, len(self.datafile.data['datum'].conditions))
        self.assertEqual(1, len(self.datafile.conditions))

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
        self.assertEqual(2, len(self.datafile.conditions))
        self.assertEqual(1, len(self.datafile.data['datum'].conditions))

        self.assertEqual(13, self.datafile.conditions['cond'].atomic_number)
        self.assertEqual(14, self.datafile.data['datum'].conditions['cond1'].atomic_number)
        self.assertEqual(14, self.datafile.conditions['cond1'].atomic_number)

    def testdelete_datum(self):
        datum = Analysis0D(1.0, conditions={'cond': ElementalID(13)})
        self.datafile.data['datum'] = datum

        del self.datafile.data['datum']

        self.assertEqual(0, len(self.datafile.data))
        self.assertEqual(1, len(self.datafile.conditions))

        self.datafile.conditions.clear()

        self.assertEqual(1, len(datum.conditions))

    def testread(self):
        # Read
        testdatadir = os.path.join(os.path.dirname(__file__), 'testdata')
        filepath = os.path.join(testdatadir, 'breccia_eds.xml')
        DataFile.read(filepath)

    def testwrite(self):
        tmpdir = tempfile.mkdtemp()
        xmlfilepath = os.path.join(tmpdir, 'breccia_eds.xml')

        self.datafile.write(xmlfilepath)

        shutil.rmtree(tmpdir, ignore_errors=True)

    def testupdate(self):
        datafile = DataFile()
        datafile.header.title = 'Update'
        datafile.conditions['cond'] = ElementalID(13)
        datafile.data['datum'] = Analysis0D(1.0)

        self.datafile.update(datafile)

        self.assertEqual('Update', datafile.header.title)
        self.assertEqual(13, datafile.conditions['cond'].atomic_number)
        self.assertAlmostEqual(1.0, float(datafile.data['datum']), 4)

    def testmerge(self):
        self.datafile.header.title = 'Update'
        self.datafile.data['datum'] = \
            Analysis0D(1.0, conditions={'cond': ElementalID(13)})

        datafile = DataFile()
        datafile.header.title = 'Update2'
        datafile.header.author = 'John Doe'
        datafile.conditions['cond'] = ElementalID(14)
        datafile.data['datum'] = Analysis0D(2.0, conditions={'cond': ElementalID(15)})

        self.datafile.merge(datafile)
#
        self.assertEqual('Update', self.datafile.header.title)
        self.assertEqual('John Doe', self.datafile.header.author)
        self.assertEqual(3, len(self.datafile.conditions))
        self.assertEqual(2, len(self.datafile.data))
        self.assertEqual(13, self.datafile.conditions['cond'].atomic_number)
        self.assertEqual(15, self.datafile.conditions['cond1'].atomic_number)
        self.assertEqual(14, self.datafile.conditions['cond2'].atomic_number)
        self.assertAlmostEqual(1.0, float(self.datafile.data['datum']), 4)
        self.assertAlmostEqual(2.0, float(self.datafile.data['datum1']), 4)
        self.assertIn('cond', self.datafile.data['datum'].conditions)
        self.assertIn('cond1', self.datafile.data['datum1'].conditions)
        self.assertIn('cond2', self.datafile.orphan_conditions)

    def testorphan_conditions(self):
        self.datafile.header.title = 'Update'
        self.datafile.data['datum'] = \
            Analysis0D(1.0, conditions={'cond': ElementalID(13)})
        self.assertEqual(0, len(self.datafile.orphan_conditions))

        self.datafile.data['datum'].conditions.clear()
        self.assertEqual(1, len(self.datafile.orphan_conditions))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
