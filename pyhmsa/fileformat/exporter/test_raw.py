""" """

# Standard library modules.
import unittest
import logging
import os
import tempfile
import shutil

# Third party modules.

# Local modules.
from pyhmsa.fileformat.exporter.raw import ExporterRAW
from pyhmsa.fileformat.importer.raw import ImporterRAW

# Globals and constants variables.

class TestExporterRAW(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.testdata = os.path.join(os.path.dirname(__file__),
                                     '..', '..', 'testdata', 'importer', 'raw')
        self.tmpdir = tempfile.mkdtemp()
        self.exp = ExporterRAW()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def testexport_vector(self):
        filepath = os.path.join(self.testdata, 'bruker_bcf_fileformat_16x16.raw')
        imp = ImporterRAW()
        imp.import_(filepath)
        datafile = imp.get()

        self.exp.export(datafile, self.tmpdir)
        filepaths = self.exp.get()

        with open(filepath, 'rb') as fp1, open(filepaths[0], 'rb') as fp2:
            self.assertEqual(fp1.read(), fp2.read())

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
