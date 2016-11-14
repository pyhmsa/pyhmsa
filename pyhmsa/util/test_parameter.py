""" """

# Standard library modules.
import datetime
import logging
import unittest

from pyhmsa.type.checksum import Checksum
from pyhmsa.type.xrayline import NOTATION_IUPAC, NOTATION_SIEGBAHN
from pyhmsa.type.xrayline import xrayline
from pyhmsa.util.parameter import \
    (Parameter, _Attribute, FrozenAttribute, NumericalAttribute, TextAttribute,
     TextListAttribute, AtomicNumberAttribute, UnitAttribute, XRayLineAttribute,
     ObjectAttribute, EnumAttribute, BoolAttribute, NumericalRangeAttribute,
     OrderedNumericalAttribute, DateAttribute, TimeAttribute, ChecksumAttribute)


class MockParameter(Parameter):
    required = _Attribute(True, xmlname='XMLNAME')
    notrequired = _Attribute(False)
    frozen = FrozenAttribute(list)
    numerical = NumericalAttribute('m')
    text = TextAttribute()
    atomic_number = AtomicNumberAttribute()
    unit = UnitAttribute()
    line = XRayLineAttribute()
    object = ObjectAttribute(int)
    enum = EnumAttribute(['a', 'b', 'c'])
    numerical_range = NumericalRangeAttribute('s', -4.0, 4.0)
    date = DateAttribute()
    time = TimeAttribute()
    checksum = ChecksumAttribute()


class TestModule(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

        self.mock = MockParameter()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test__repr__(self):
        self.assertEqual('<MockParameter(', repr(self.mock)[:15])

    def test_attribute(self):
        self.mock.required = 'abc'
        self.assertEqual('abc', self.mock.required)

        self.mock.set_required('def')
        self.assertEqual('def', self.mock.get_required())

        self.assertRaises(ValueError, self.mock.set_required, None)
        self.assertRaises(ValueError, delattr, self.mock, 'required')

        self.assertEqual('required', self.mock.__class__.required.name)
        self.assertEqual('XMLNAME', self.mock.__class__.required.xmlname)
        self.assertTrue(self.mock.__class__.required.is_required())
        self.assertEqual('<_Attribute(required)>', repr(self.mock.__class__.required))

        self.mock.notrequired = 'hkl'
        del self.mock.notrequired
        self.assertIsNone(self.mock.notrequired)

    def testfrozen_attribute(self):
        self.assertIsInstance(self.mock.frozen, list)
        self.assertIsInstance(self.mock.get_frozen(), list)
        self.assertFalse(hasattr(self.mock, 'set_frozen'))

        self.assertRaises(AttributeError, setattr, self.mock, 'frozen', 'abc')

        self.assertTrue(self.mock.__class__.frozen.is_required())

    def testnumerical_attribute(self):
        self.mock.numerical = (9.0, 'nm')
        self.assertAlmostEqual(9.0, self.mock.numerical, 4)
        self.assertEqual('nm', self.mock.numerical.unit)

        self.mock.numerical = 11.0
        self.assertAlmostEqual(11.0, self.mock.numerical, 4)
        self.assertEqual('m', self.mock.numerical.unit)

    def testtext_attribute(self):
        self.assertTrue(True)

    def testatomic_number_attribute(self):
        self.mock.atomic_number = 25
        self.assertEqual(25, self.mock.atomic_number)

        self.mock.atomic_number = None
        self.assertIsNone(self.mock.atomic_number)

        self.assertRaises(ValueError, self.mock.set_atomic_number, 0)
        self.assertRaises(ValueError, self.mock.set_atomic_number, 119)

    def testunit_attribute(self):
        self.mock.unit = 'A'
        self.assertEqual('A', self.mock.unit)

        self.mock.unit = None
        self.assertIsNone(self.mock.unit)

        self.assertRaises(ValueError, self.mock.set_unit, 'mmHg')

    def testline_attribute(self):
        self.mock.line = 'Ma'
        self.assertEqual('Ma', self.mock.line)
        self.assertEqual(NOTATION_SIEGBAHN, self.mock.line.notation)

        self.mock.line = ('M5-N6,7', NOTATION_IUPAC)
        self.assertEqual('M5-N6,7', self.mock.line)
        self.assertEqual(NOTATION_IUPAC, self.mock.line.notation)

        self.mock.line = xrayline('Ma', NOTATION_SIEGBAHN, 'M5-N6,7')
        self.assertEqual('Ma', self.mock.line)
        self.assertEqual(NOTATION_SIEGBAHN, self.mock.line.notation)
        self.assertEqual('M5-N6,7', self.mock.line.alternative)
        self.assertEqual(NOTATION_IUPAC, self.mock.line.alternative.notation)

        self.mock.line = None
        self.assertIsNone(self.mock.line)

    def testobject_attribute(self):
        self.mock.object = 5
        self.assertEqual(5, self.mock.object)

        self.mock.object = None
        self.assertIsNone(self.mock.object)

        self.assertRaises(ValueError, self.mock.set_object, 5.0)

        self.assertIs(int, self.mock.__class__.object.type_)

    def testenum_attribute(self):
        self.mock.enum = 'b'
        self.assertEqual('b', self.mock.enum)

        self.mock.enum = None
        self.assertIsNone(self.mock.enum)

        self.assertRaises(ValueError, self.mock.set_enum, 'd')

    def testnumerical_range_attribute(self):
        self.mock.numerical_range = (2.0, 3.0)
        self.assertAlmostEqual(2.0, self.mock.numerical_range[0], 4)
        self.assertAlmostEqual(3.0, self.mock.numerical_range[1], 4)
        self.assertEqual('s', self.mock.numerical_range.unit)

        self.mock.set_numerical_range(-1.0, 2.0, 'A')
        self.assertAlmostEqual(-1.0, self.mock.numerical_range[0], 4)
        self.assertAlmostEqual(2.0, self.mock.numerical_range[1], 4)
        self.assertEqual('A', self.mock.numerical_range.unit)

        self.mock.numerical_range = None
        self.assertIsNone(self.mock.numerical_range)

        self.assertRaises(ValueError, self.mock.set_numerical_range, -5.0, 2.0)
        self.assertRaises(ValueError, self.mock.set_numerical_range, 1.0, 5.0)
        self.assertRaises(ValueError, self.mock.set_numerical_range, 3.0, 2.0)
        self.assertRaises(ValueError, setattr, self.mock, 'numerical_range', (1.0, 2.0, 3.0))

    def testdate_attribute(self):
        self.mock.date = '2013-12-24'
        self.assertEqual(2013, self.mock.date.year)
        self.assertEqual(12, self.mock.date.month)
        self.assertEqual(24, self.mock.date.day)

        self.mock.date = datetime.date(2013, 12, 25)
        self.assertEqual(2013, self.mock.date.year)
        self.assertEqual(12, self.mock.date.month)
        self.assertEqual(25, self.mock.date.day)

        self.mock.date = None
        self.assertIsNone(self.mock.date)

    def testtime_attribute(self):
        self.mock.time = '20:31:15'
        self.assertEqual(20, self.mock.time.hour)
        self.assertEqual(31, self.mock.time.minute)
        self.assertEqual(15, self.mock.time.second)

        self.mock.time = datetime.time(20, 31, 16)
        self.assertEqual(20, self.mock.time.hour)
        self.assertEqual(31, self.mock.time.minute)
        self.assertEqual(16, self.mock.time.second)

        self.mock.time = None
        self.assertIsNone(self.mock.time)

    def testchecksum_attribute(self):
        self.mock.checksum = Checksum('53AAD59C05D59A40AD746D6928EA6D2D526865FD', 'SHA-1')
        self.assertEqual('53AAD59C05D59A40AD746D6928EA6D2D526865FD', self.mock.checksum.value)
        self.assertEqual('SHA-1', self.mock.checksum.algorithm)

        self.mock.checksum = None
        self.assertIsNone(self.mock.checksum)

        self.assertRaises(ValueError, self.mock.set_checksum, object())

    def _generate_parameter(self, dif_list=None, req_list=None):

        if not dif_list:
            dif_list = []

        if not req_list:
            req_list = []

        # is an attribute required
        req_val = {'required': False,
                   'notrequired': False,
                   'frozen': False,
                   'numerical': False,
                   'text': False,
                   'textList': False,
                   'atomic_number': False,
                   'unit': False,
                   'line': False,
                   'object': False,
                   'enum': False,
                   'bool': False,
                   'numerical_range': False,
                   'ordered_numerical': False,
                   'date': False,
                   'time': False,
                   'checksum': False}

        # default values for attributes
        def_val = {'required': 'abc',
                   'notrequired': 'def',
                   'frozen': None,
                   'numerical': (1.1, 'nm'),
                   'text': 'hello world',
                   'textList': ['hello', 'world'],
                   'atomic_number': 25,
                   'unit': 'A',
                   'line': 'Ma',
                   'object': 5,
                   'enum': 'b',
                   'bool': True,
                   'numerical_range': [1.1, 2.2],
                   'ordered_numerical': [1, 2, 3, 4],
                   'date': '2013-12-24',
                   'time': '20:31:15',
                   'checksum': Checksum('53AAD59C05D59A40AD746D6928EA6D2D526865FD',
                                        'SHA-1')}

        # values that differ from defaults
        dif_val = {'required': 'def',
                   'notrequired': 'abc',
                   'frozen': None,
                   'numerical': (1.2, 'nm'),
                   'text': 'goodbye world',
                   'textList': ['goodbye', 'world'],
                   'atomic_number': 26,
                   'unit': 'm',
                   'line': ('M5-N6,7', NOTATION_IUPAC),
                   'object': 6,
                   'enum': 'c',
                   'bool': False,
                   'numerical_range': [1.001, 2.2007],
                   'ordered_numerical': [2, 3, 4, 5],
                   'date': '2013-12-25',
                   'time': '20:31:16',
                   'checksum': Checksum('63AAD59C05D59A40AD746D6928EA6D2D526865FD',
                                        'SHA-1')}

        # set attribute status to required
        for key in req_list:
            if key not in req_val:
                raise ValueError
            req_val[key] = True

        class MyParameter(Parameter):
            required = _Attribute(required=req_val['required'], xmlname='XMLNAME')
            notrequired = _Attribute(required=req_val['notrequired'])
            frozen = FrozenAttribute(list)
            numerical = NumericalAttribute('m', required=req_val['numerical'])
            text = TextAttribute(required=req_val['text'])
            textList = TextListAttribute(required=req_val['textList'])
            atomic_number = AtomicNumberAttribute(required=req_val['atomic_number'])
            unit = UnitAttribute(required=req_val['unit'])
            line = XRayLineAttribute(required=req_val['line'])
            object = ObjectAttribute(int, required=req_val['object'])
            enum = EnumAttribute(['a', 'b', 'c'], required=req_val['enum'])
            bool = BoolAttribute(required=req_val['bool'])
            numerical_range = NumericalRangeAttribute('s', -4.0, 4.0,
                                                      required=req_val['numerical_range'])
            ordered_numerical = OrderedNumericalAttribute(required=req_val['ordered_numerical'])
            date = DateAttribute(required=req_val['date'])
            time = TimeAttribute(required=req_val['time'])
            checksum = ChecksumAttribute(required=req_val['checksum'])

        m = MyParameter()

        # initialize attributes
        for key in m.__attributes__.keys():
            if key == 'frozen':
                continue
            if key in dif_list:
                m.__attributes__[key].__set__(m, dif_val[key])
            else:
                m.__attributes__[key].__set__(m, def_val[key])

        return m

    def test__eq__(self):

        attr_list = ['date', 'numerical', 'textList', 'enum', 'time', 'unit', 'notrequired',
                     'ordered_numerical', 'text', 'required', 'line', 'frozen', 'bool',
                     'numerical_range', 'atomic_number', 'object', 'checksum']

        m1 = self._generate_parameter(req_list=attr_list)
        m2 = self._generate_parameter(req_list=attr_list)
        m3 = self._generate_parameter(req_list=attr_list, dif_list=attr_list)

        self.assertEqual(m2, m1)
        self.assertNotEqual(m3, m1)

        del m2
        del m3

        for a1 in attr_list:
            for a2 in attr_list:
                if a1 != 'frozen' and a2 != 'frozen':
                    m4 = self._generate_parameter(req_list=[a1], dif_list=[a2])
                    if a1 == a2:
                        self.assertNotEqual(m4, m1)
                    else:
                        self.assertEqual(m4, m1)


if __name__ == '__main__':  # pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
