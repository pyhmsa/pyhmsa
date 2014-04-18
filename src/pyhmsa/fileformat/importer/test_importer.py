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

# Third party modules.

# Local modules.
from pyhmsa.fileformat.importer.importer import _Importer, _ImporterThread
from pyhmsa.datafile import DataFile

# Globals and constants variables.

class ImporterThreadMock(_ImporterThread):

    def _run(self, filepath, *args, **kwargs):
        datafile = DataFile(filepath)
        datafile.header.title = 'Imported'
        return datafile

class ImporterMock(_Importer):

    SUPPORTED_EXTENSIONS = ('.abc',)

    def _create_thread(self, filepath, *args, **kwargs):
        return ImporterThreadMock(filepath)

class TestImporter(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.imp = ImporterMock(search_home=False)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testimport_(self):
        self.imp.import_('file.abc')
        datafile = self.imp.get()
        self.assertEqual('Imported', datafile.header.title)

    def test_update_extra(self):
        extra_datafile = DataFile()
        extra_datafile.header.author = 'Me'
        imp = ImporterMock(extra_datafile, search_home=False)

        imp.import_('file.abc')
        datafile = imp.get()
        self.assertEqual('Imported', datafile.header.title)
        self.assertEqual('Me', datafile.header.author)

    def testcan_import(self):
        self.assertTrue(self.imp.can_import('file.abc'))
        self.assertFalse(self.imp.can_import('file.def'))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
