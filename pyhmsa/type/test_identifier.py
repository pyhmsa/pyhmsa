#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pyhmsa.type.identifier import validate_identifier, _IdentifierDict

# Globals and constants variables.

class Wrapper(object):

    def __init__(self, func):
        self.func = func
        self.called = False

    def __call__(self, *args, **kwargs):
        self.called = True
        return self.func(*args, **kwargs)

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

        w = Wrapper(handler)
        self.d.item_added.connect(w)

        self.d['abc'] = 1
        self.assertTrue(w.called)

    def test__setitem__modified(self):
        self.d['abc'] = 1

        def handler(key, value, oldvalue):
            self.assertEqual('abc', key)
            self.assertEqual(2, value)
            self.assertEqual(1, oldvalue)

        w = Wrapper(handler)
        self.d.item_modified.connect(w)

        self.d['abc'] = 2
        self.assertTrue(w.called)

    def test__delitem__(self):
        def handler(key, oldvalue):
            self.assertEqual('abc', key)
            self.assertEqual(1, oldvalue)

        w = Wrapper(handler)
        self.d.item_deleted.connect(w)

        self.d['abc'] = 1
        del self.d['abc']
        self.assertTrue(w.called)

    def testupdate(self):
        def handler(key, value):
            self.assertEqual('abc', key)
            self.assertEqual(1, value)

        w = Wrapper(handler)
        self.d.item_added.connect(w)

        self.d.update(abc=1)
        self.assertTrue(w.called)

    def testsetdefault(self):
        def handler(key, value):
            self.assertEqual('abc', key)
            self.assertEqual(1, value)

        w = Wrapper(handler)
        self.d.item_added.connect(w)

        self.d.setdefault('abc', 1)
        self.assertTrue(w.called)

    def testpop(self):
        def handler(key, oldvalue):
            self.assertEqual('abc', key)
            self.assertEqual(1, oldvalue)

        w = Wrapper(handler)
        self.d.item_deleted.connect(w)

        self.d['abc'] = 1
        self.d.pop('abc')
        self.assertTrue(w.called)

    def testpopitem(self):
        def handler(key, oldvalue):
            self.assertEqual('abc', key)
            self.assertEqual(1, oldvalue)

        w = Wrapper(handler)
        self.d.item_deleted.connect(w)

        self.d['abc'] = 1
        self.d.popitem()
        self.assertTrue(w.called)

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

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
