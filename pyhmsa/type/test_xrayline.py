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
import pickle

# Third party modules.

# Local modules.
from pyhmsa.type.xrayline import xrayline

# Globals and constants variables.
from pyhmsa.type.xrayline import NOTATION_SIEGBAHN, NOTATION_IUPAC

class Testxrayline(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.x = xrayline('Ma', NOTATION_SIEGBAHN, 'M5-N6,7')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testskeleton(self):
        self.assertEqual('Ma', self.x)
        self.assertEqual(NOTATION_SIEGBAHN, self.x.notation)
        self.assertEqual('M5-N6,7', self.x.alternative)
        self.assertEqual(NOTATION_IUPAC, self.x.alternative.notation)

    def testpickle(self):
        s = pickle.dumps(self.x)
        x = pickle.loads(s)

        self.assertEqual('Ma', x)
        self.assertEqual(NOTATION_SIEGBAHN, x.notation)
        self.assertEqual('M5-N6,7', x.alternative)
        self.assertEqual(NOTATION_IUPAC, x.alternative.notation)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
