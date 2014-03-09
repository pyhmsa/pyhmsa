#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pyhmsa.type.identifier import validate_identifier, _IdentifierDict

# Globals and constants variables.

class TestModule(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testvalidate_identifier(self):
        self.assertTrue(validate_identifier('abc'))
        self.assertTrue(validate_identifier('abc_asda-|(sadfa)'))
        self.assertRaises(ValueError, validate_identifier, u'\u00b0C')

class Test_IdentifierDict(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.d = _IdentifierDict()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test__setitem__added(self):
        def handler(key, value):
            self.assertEqual('abc', key)
            self.assertEqual(1, value)
        self.d.item_added.connect(handler)

        self.d['abc'] = 1

    def test__setitem__modified(self):
        self.d['abc'] = 1

        def handler(key, value, oldvalue):
            self.assertEqual('abc', key)
            self.assertEqual(2, value)
            self.assertEqual(1, oldvalue)
        self.d.item_modified.connect(handler)

        self.d['abc'] = 2

    def test__delitem__(self):
        def handler(key, oldvalue):
            self.assertEqual('abc', key)
            self.assertEqual(1, oldvalue)
        self.d.item_deleted.connect(handler)

        self.d['abc'] = 1
        del self.d['abc']

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
