""" """

# Standard library modules.
import unittest
import logging
import random

# Third party modules.

# Local modules.
from pyhmsa.type.identifier import \
    validate_identifier, sorted_identifier, _IdentifierDict

# Globals and constants variables.

class TestModule(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testvalidate_identifier(self):
        self.assertTrue(validate_identifier('abc'))
        self.assertTrue(validate_identifier('abc_asda-|(sadfa)'))
        self.assertRaises(ValueError, validate_identifier, '')
        self.assertRaises(ValueError, validate_identifier, u'\u00b0C')

    def testsorted_identifier(self):
        identifiers = ['abc10', 'abc2', 'abc20', 'abc1', 'abc100']
        random.shuffle(identifiers)
        self.assertEqual(['abc1', 'abc2', 'abc10', 'abc20', 'abc100'],
                         sorted_identifier(identifiers))

        identifiers = ['abc10', 'abc2', 'abc20', 'abc', 'def', 'abc1', 'abc100']
        random.shuffle(identifiers)
        self.assertEqual(['abc', 'abc1', 'abc2', 'abc10', 'abc20', 'abc100', 'def'],
                         sorted_identifier(identifiers))

class Test_IdentifierDict(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.d = _IdentifierDict()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testcopy(self):
        self.d['abc'] = 1
        d = self.d.copy()

        self.assertEqual(1, d['abc'])

        d['def'] = 2
        self.assertIn('def', d)
        self.assertNotIn('def', self.d)

    def testfindkeys(self):
        self.d['a'] = 1
        self.d['b'] = 2.0
        self.d['c'] = '3'

        keys = self.d.findkeys(int)
        self.assertEqual(1, len(keys))
        self.assertEqual('a', next(iter(keys)))

        keys = self.d.findkeys(float)
        self.assertEqual(1, len(keys))
        self.assertEqual('b', next(iter(keys)))

        keys = self.d.findkeys(str)
        self.assertEqual(1, len(keys))
        self.assertEqual('c', next(iter(keys)))

        keys = self.d.findkeys('a*')
        self.assertEqual(1, len(keys))
        self.assertEqual('a', next(iter(keys)))

        keys = self.d.findkeys('*')
        self.assertEqual(3, len(keys))

    def testfindvalues(self):
        self.d['a'] = 1
        self.d['b'] = 2.0
        self.d['c'] = '3'

        values = self.d.findvalues(int)
        self.assertEqual(1, len(values))
        self.assertEqual(1, next(iter(values)))

        values = self.d.findvalues(float)
        self.assertEqual(1, len(values))
        self.assertAlmostEqual(2.0, next(iter(values)), 4)

        values = self.d.findvalues(str)
        self.assertEqual(1, len(values))
        self.assertEqual('3', next(iter(values)))

        values = self.d.findvalues('a*')
        self.assertEqual(1, len(values))
        self.assertEqual(1, next(iter(values)))

        values = self.d.findvalues('*')
        self.assertEqual(3, len(values))

    def testfinditems(self):
        self.d['a'] = 1
        self.d['b'] = 2.0
        self.d['c'] = '3'

        items = self.d.finditems(int)
        self.assertEqual(1, len(items))
        self.assertEqual(('a', 1), next(iter(items)))

        items = self.d.finditems(float)
        self.assertEqual(1, len(items))
        self.assertEqual(('b', 2.0), next(iter(items)), 4)

        items = self.d.finditems(str)
        self.assertEqual(1, len(items))
        self.assertEqual(('c', '3'), next(iter(items)))

        items = self.d.finditems('a*')
        self.assertEqual(1, len(items))
        self.assertEqual(('a', 1), next(iter(items)))

        items = self.d.finditems('*')
        self.assertEqual(3, len(items))

    def testadd(self):
        self.d.add('a', 1)
        self.d.add('a', 2)
        self.assertEqual(2, len(self.d))
        self.assertIn('a', self.d)
        self.assertIn('a1', self.d)
        self.assertEqual(1, self.d['a'])
        self.assertEqual(2, self.d['a1'])

        identifier = self.d.add('a', 3)
        self.assertEqual('a2', identifier)

        identifier = self.d.add('a2', 4)
        self.assertEqual('a3', identifier)

    def testaddall(self):
        self.d.add('a', 1)
        self.d.addall({'a': 2})
        self.assertEqual(2, len(self.d))
        self.assertIn('a', self.d)
        self.assertIn('a1', self.d)
        self.assertEqual(1, self.d['a'])
        self.assertEqual(2, self.d['a1'])

        self.d.addall(a=3)
        self.assertIn('a2', self.d)
        self.assertEqual(3, self.d['a2'])

        self.d.addall([('a', 4), ('a', 5)])
        self.assertIn('a3', self.d)
        self.assertEqual(4, self.d['a3'])
        self.assertIn('a4', self.d)
        self.assertEqual(5, self.d['a4'])

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
