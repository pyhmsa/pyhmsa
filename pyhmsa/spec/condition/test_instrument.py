#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging
import pickle

# Third party modules.

# Local modules.
from pyhmsa.spec.condition.instrument import Instrument

# Globals and constants variables.

class TestInstrument(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.instrument = Instrument('Example Inc', 'Example Model 123')

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testmanufacturer(self):
        self.assertEqual('Example Inc', self.instrument.manufacturer)
        self.assertRaises(ValueError, self.instrument.set_manufacturer, None)

    def testmodel(self):
        self.assertEqual('Example Model 123', self.instrument.model)
        self.assertRaises(ValueError, self.instrument.set_model, None)

    def testserial_number(self):
        self.instrument.serial_number = '12345-abc-67890'
        self.assertEqual('12345-abc-67890', self.instrument.serial_number)

    def testpickle(self):
        self.instrument.serial_number = '12345-abc-67890'

        s = pickle.dumps(self.instrument)
        instrument = pickle.loads(s)

        self.assertEqual('Example Inc', instrument.manufacturer)
        self.assertEqual('Example Model 123', instrument.model)
        self.assertEqual('12345-abc-67890', instrument.serial_number)

if __name__ == '__main__': # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
