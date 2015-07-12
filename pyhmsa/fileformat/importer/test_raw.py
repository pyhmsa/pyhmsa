""" """

# Standard library modules.
import unittest
import logging
import os

# Third party modules.

# Local modules.
from pyhmsa.fileformat.importer.raw import ImporterRAW

# Globals and constants variables.

class TestImporterRAW(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.testdata = os.path.join(os.path.dirname(__file__),
                                     '..', '..', 'testdata', 'importer', 'raw')
        self.imp = ImporterRAW()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testimport_vector(self):
        filepath = os.path.join(self.testdata, 'bruker_bcf_fileformat_16x16.raw')
        self.imp.import_(filepath)
        datafile = self.imp.get()

        self.assertEqual(0, len(datafile.conditions))
        self.assertEqual(1, len(datafile.data))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
