#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import pickle

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

    def testpickle(self):
        s = pickle.dumps(self.checksum)
        checksum = pickle.loads(s)

        self.assertEqual('ABC', checksum.value)
        self.assertEqual(CHECKSUM_ALGORITHM_SHA1, checksum.algorithm)

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
