#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import pickle

# Third party modules.

# Local modules.
from pyhmsa.type.language import langstr

# Globals and constants variables.

class Testlangstr(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.s1 = langstr('Test1', {'en-US': 'TEST', 'en-CA': 'test'})

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual('Test1', self.s1)
        self.assertEqual(2, len(self.s1.alternatives))
        self.assertEqual('TEST', self.s1.alternatives['en-US'])
        self.assertEqual('test', self.s1.alternatives['en-CA'])

        self.assertRaises(ValueError, langstr, 'Test1', {'blah': 'abc'})
        self.assertRaises(ValueError, langstr, 'Test1', {'en-blah': 'abc'})

    def testpickle(self):
        s = pickle.dumps(self.s1)
        s1 = pickle.loads(s)

        self.assertEqual('Test1', s1)
        self.assertEqual(2, len(s1.alternatives))
        self.assertEqual('TEST', s1.alternatives['en-US'])
        self.assertEqual('test', s1.alternatives['en-CA'])

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
