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
import tempfile
import shutil
import os
import xml.etree.ElementTree as etree

# Third party modules.

# Local modules.

# Globals and constants variables.

class BaseTestCaseDatum(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def save(self, handler_class, obj):
        hmsa_filepath = os.path.join(self.tmpdir, 'test.hmsa')
        with open(hmsa_filepath, 'wb') as fp:
            fp.write(b'\x60\x60\x6E\xE4\x85\xB4\x27\x36') # Write UID

            handler = handler_class(1.0, fp, {})

            self.assertTrue(handler.can_convert(obj))
            self.assertFalse(handler.can_convert(object()))

            element = handler.convert(obj)

        xml_filepath = os.path.join(self.tmpdir, 'test.xml')
        with open(xml_filepath, 'wb') as fp:
            element.set('Name', 'Test')

            fp.write(b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
            fp.write(b'<MSAHyperDimensionalDataFile Version="1.0" UID="60606EE485B42736" xml:lang="en-US">')
            fp.write(b'<Header/>')
            fp.write(b'<Conditions/>')
            fp.write(b'<Data>')
            fp.write(etree.tostring(element))
            fp.write(b'</Data>')
            fp.write(b'</MSAHyperDimensionalDataFile>')

        return xml_filepath, hmsa_filepath

    def load(self, handler_class, hmsa_filepath, tag):
        xml_filepath = os.path.splitext(hmsa_filepath)[0] + '.xml'

        with open(xml_filepath, 'rb') as fp:
            element = etree.parse(fp).getroot().find('Data/' + tag)

        with open(self.hmsa_filepath, 'rb') as fp:
            h = handler_class(1.0, fp, {})

            self.assertTrue(h.can_parse(element))
            self.assertFalse(h.can_parse(etree.Element(tag)))
            self.assertFalse(h.can_parse(etree.Element('Abc')))

            return h.parse(element)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
