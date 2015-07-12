""" """

# Standard library modules.
import unittest
import logging
import os

# Third party modules.

# Local modules.
from pyhmsa.fileformat.importer.emsa import ImporterEMSA

# Globals and constants variables.

class TestImporterESMA(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.testdata = os.path.join(os.path.dirname(__file__),
                                     '..', '..', 'testdata', 'importer', 'emsa')
        self.imp = ImporterEMSA(search_extra=False)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testimport_1(self):
        self.imp.import_(os.path.join(self.testdata, 'spectrum1.emsa'))
        datafile = self.imp.get()

        self.assertEqual(3, len(datafile.conditions))
        self.assertEqual(1, len(datafile.data))

    def testimport_2(self):
        self.imp.import_(os.path.join(self.testdata, 'spectrum2.emsa'))
        datafile = self.imp.get()

        self.assertEqual(2, len(datafile.conditions))
        self.assertEqual(1, len(datafile.data))

    def testimport_3(self):
        self.imp.import_(os.path.join(self.testdata, 'spectrum3.emsa'))
        datafile = self.imp.get()

        self.assertEqual(3, len(datafile.conditions))
        self.assertEqual(1, len(datafile.data))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
