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
from pyhmsa.fileformat.exporter.exporter import _Exporter, _ExporterThread

from pyhmsa.datafile import DataFile

# Globals and constants variables.

class ExporterThreadMock(_ExporterThread):

    def _run(self, datafile, dirpath, *args, **kwargs):
        filepath = os.path.join(dirpath, datafile.header.title + '.abc')
        with open(filepath, 'w') as fp:
            fp.write(datafile.header.title)
        return [filepath]

class ExporterMock(_Exporter):

    def _create_thread(self, datafile, dirpath, *args, **kwargs):
        return ExporterThreadMock(datafile, dirpath)

class Test_Exporter(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.tmpdir = tempfile.mkdtemp()
        self.exp = ExporterMock()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def testexport(self):
        datafile = DataFile()
        datafile.header.title = 'test'

        self.exp.export(datafile, self.tmpdir)
        filepaths = self.exp.get()

        # Test
        self.assertEqual(1, len(filepaths))
        with open(filepaths[0], 'r') as fp:
            self.assertEqual('test', fp.read())

    def testcan_export(self):
        datafile = DataFile()
        self.assertTrue(self.exp.can_export(datafile))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
