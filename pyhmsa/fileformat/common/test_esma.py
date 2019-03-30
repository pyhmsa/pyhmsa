#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pyhmsa.fileformat.common.emsa import calculate_checksum

# Globals and constants variables.

class TestModule(unittest.TestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testcalculate_checksum(self):
        lines = ['abc']
        self.assertEqual(294, calculate_checksum(lines))

        lines = ['abc', '#CHECKSUM : 294']
        self.assertEqual(294, calculate_checksum(lines))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
