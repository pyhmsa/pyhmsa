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
from pyhmsa.fileformat.importer import _Importer
from pyhmsa.datafile import DataFile

# Globals and constants variables.

class ImporterMock(_Importer):

    def __init__(self, extra_datafile=None):
        _Importer.__init__(self, ('.abc',), extra_datafile)

    def _import(self, filepath):
        datafile = DataFile(filepath)
        datafile.header.title = 'Imported'
        return datafile

class TestImporter(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        extra_datafile = DataFile()
        self.imp = ImporterMock(extra_datafile)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testsupported_extensions(self):
        self.assertEqual(1, len(self.imp.supported_extensions))
        self.assertIn('.abc', self.imp.supported_extensions)

    def testimport_(self):
        datafile = self.imp.import_('file.abc')
        self.assertEqual('Imported', datafile.header.title)

    def test_update_extra(self):
        extra_datafile = DataFile()
        extra_datafile.header.author = 'Me'
        imp = ImporterMock(extra_datafile)

        datafile = imp.import_('file.abc')
        self.assertEqual('Imported', datafile.header.title)
        self.assertEqual('Me', datafile.header.author)

    def testcan_import(self):
        self.assertTrue(self.imp.can_import('file.abc'))
        self.assertFalse(self.imp.can_import('file.def'))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
