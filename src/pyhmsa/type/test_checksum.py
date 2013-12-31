#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pyhmsa.type.checksum import \
    Checksum, calculate_checksum, calculate_checksum_sha1, calculate_checksum_sum32

# Globals and constants variables.
from pyhmsa.type.checksum import CHECKSUM_ALGORITHM_SHA1, CHECKSUM_ALGORITHM_SUM32

class TestChecksum(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.checksum = Checksum('aBc', CHECKSUM_ALGORITHM_SHA1)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual('ABC', self.checksum.value)
        self.assertEqual(CHECKSUM_ALGORITHM_SHA1, self.checksum.algorithm)

        self.assertRaises(ValueError, Checksum, 'aBc', 'Algorithm')

class TestModule(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.buffer = b'abcdefGhij'

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcalculate_checksum_sha1(self):
        checksum = calculate_checksum_sha1(self.buffer)
        self.assertEqual('B2AA57BA7FCC90905DA4DBA9175CF42A9A30C32F', checksum.value)
        self.assertEqual(CHECKSUM_ALGORITHM_SHA1, checksum.algorithm)

    def testcalculate_checksum_sum32(self):
        checksum = calculate_checksum_sum32(self.buffer)
        self.assertEqual('000000000000000000000000000003D7', checksum.value)
        self.assertEqual(CHECKSUM_ALGORITHM_SUM32, checksum.algorithm)

    def testcalculate_checksum(self):
        checksum = calculate_checksum(CHECKSUM_ALGORITHM_SHA1, self.buffer)
        self.assertEqual('B2AA57BA7FCC90905DA4DBA9175CF42A9A30C32F', checksum.value)
        self.assertEqual(CHECKSUM_ALGORITHM_SHA1, checksum.algorithm)

        checksum = calculate_checksum(CHECKSUM_ALGORITHM_SUM32, self.buffer)
        self.assertEqual('000000000000000000000000000003D7', checksum.value)
        self.assertEqual(CHECKSUM_ALGORITHM_SUM32, checksum.algorithm)

        self.assertRaises(ValueError, calculate_checksum, 'Algorithm', self.buffer)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
