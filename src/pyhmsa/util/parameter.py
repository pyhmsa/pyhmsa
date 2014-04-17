#!/usr/bin/env python
"""
================================================================================
:mod:`parameter` -- Generic definition of parameters
================================================================================

.. module:: parameter
   :synopsis: Generic definition of parameters

.. inheritance-diagram:: parameter

"""

# Standard library modules.
import inspect
import datetime
from collections import OrderedDict

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.type.numerical import convert_value
from pyhmsa.type.unit import validate_unit
from pyhmsa.type.checksum import Checksum
from pyhmsa.type.xrayline import xrayline, NOTATION_SIEGBAHN

# Globals and constants variables.

class _Attribute(object):

    def __init__(self, required=False, xmlname=None, doc=None):
        """
        Creates a new parameter.
        """
        self._name = None
        self._required = required
        self._xmlname = xmlname
        self.__doc__ = doc

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__, self.name)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        value = self._prepare_value(value)
        self._validate_value(value)
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        if self._required:
            raise ValueError("%s is required" % self.name)
        instance.__dict__.pop(self.name, None)

    def _new(self, cls, clsname, bases, methods, name):
        self._name = name

        # Attach get/set method
        methods['get_%s' % name] = lambda instance: self.__get__(instance)
        methods['set_%s' % name] = \
            lambda instance, value: self.__set__(instance, value)

    def _prepare_value(self, value):
        return value

    def _validate_value(self, value):
        if value is None and self.is_required():
            raise ValueError('%s is required' % self.name)

    def is_required(self):
        return self._required

    @property
    def name(self):
        return self._name

    @property
    def xmlname(self):
        return self._xmlname

class FrozenAttribute(_Attribute):

    def __init__(self, class_or_value, args=(), kwargs=None, xmlname=None, doc=None):
        _Attribute.__init__(self, True, xmlname, doc)

        self._value = class_or_value
        self._klass_args = args
        if kwargs is None: kwargs = {}
        self._klass_kwargs = kwargs

    def __get__(self, instance, owner=None):
        if instance is None:
            return self

        if self.name not in instance.__dict__:
            value = self._value
            if inspect.isclass(value):
                value = self._value(*self._klass_args, **self._klass_kwargs)

            value = self._prepare_value(value)
            self._validate_value(value)
            instance.__dict__[self.name] = value

        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        raise AttributeError("Frozen parameter (%s)" % self._name)

    def _new(self, cls, clsname, bases, methods, name):
        _Attribute._new(self, cls, clsname, bases, methods, name)

        methods.pop('set_%s' % name) # Remove set method

class NumericalAttribute(_Attribute):

    def __init__(self, default_unit=None, required=False, xmlname=None, doc=None):
        _Attribute.__init__(self, required, xmlname, doc)
        self._default_unit = default_unit

    def _prepare_value(self, value):
        if isinstance(value, tuple) and \
                len(value) == 2 and \
                (isinstance(value[1], str) or value[1] is None):
            unit = value[1] or self.default_unit
            value = value[0]
        else:
            unit = self.default_unit
        return convert_value(value, unit)

    def _new(self, cls, clsname, bases, methods, name):
        _Attribute._new(self, cls, clsname, bases, methods, name)

        # Change set method to allow unit input
        methods['set_%s' % name] = \
            lambda instance, value, unit = None: \
                self.__set__(instance, (value, unit or self.default_unit))

    @property
    def default_unit(self):
        return self._default_unit

class TextAttribute(_Attribute):

    def _validate_value(self, value):
        _Attribute._validate_value(self, value)

        if value is not None and len(value.strip()) == 0 and self.is_required():
            raise ValueError('%s is required' % self.name)

class AtomicNumberAttribute(NumericalAttribute):

    def __init__(self, required=False, xmlname=None, doc=None):
        NumericalAttribute.__init__(self, None, required, xmlname, doc)

    def _prepare_value(self, value):
        value = NumericalAttribute._prepare_value(self, value)
        if value is None:
            return None
        return np.uint8(value)

    def _validate_value(self, value):
        NumericalAttribute._validate_value(self, value)

        if value is not None and value < 1:
            raise ValueError('Atomic number cannot be less than Hydrogen')
        if value is not None and value > 118:
            raise ValueError('Atomic number cannot be greater than Uuo')

class UnitAttribute(TextAttribute):

    def __init__(self, default_unit=None, required=False, xmlname=None, doc=None):
        TextAttribute.__init__(self, required, xmlname, doc)
        self._default_unit = default_unit

    def _prepare_value(self, value):
        value = TextAttribute._prepare_value(self, value)
        value = value or self.default_unit
        try:
            value = validate_unit(value)
        except:
            pass
        return value

    def _validate_value(self, value):
        TextAttribute._validate_value(self, value)
        if value is not None:
            validate_unit(value)

    @property
    def default_unit(self):
        return self._default_unit

class XRayLineAttribute(_Attribute):

    def __init__(self, default_notation=NOTATION_SIEGBAHN,
                 required=False, xmlname=None, doc=None):
        _Attribute.__init__(self, required, xmlname, doc)
        self._default_notation = default_notation

    def _prepare_value(self, value):
        if isinstance(value, xrayline):
            return value

        if isinstance(value, tuple) and \
                len(value) == 2 and \
                (isinstance(value[1], str) or value[1] is None):
            notation = value[1] or self.default_notation
            value = value[0]
        else:
            notation = self.default_notation

        if value is None:
            return None

        return xrayline(value, notation)

    def _new(self, cls, clsname, bases, methods, name):
        _Attribute._new(self, cls, clsname, bases, methods, name)

        # Change set method to allow unit input
        methods['set_%s' % name] = \
            lambda instance, value, notation = None: \
                self.__set__(instance, (value, notation or self.default_notation))

    @property
    def default_notation(self):
        return self._default_notation

class ObjectAttribute(_Attribute):

    def __init__(self, type_, required=False, xmlname=None, doc=None):
        _Attribute.__init__(self, required, xmlname, doc)
        self._type = type_

    def _validate_value(self, value):
        _Attribute._validate_value(self, value)

        if value is not None and not isinstance(value, self._type):
            raise ValueError('Value must be of type "%s"' % self._type)

    @property
    def type_(self):
        return self._type

class EnumAttribute(TextAttribute):

    def __init__(self, values, required=False, xmlname=None, doc=None):
        TextAttribute.__init__(self, required, xmlname, doc)
        self._values = tuple(values)

    def _prepare_value(self, value):
        if value is not None and len(value.strip()) == 0:
            value = None
        return value

    def _validate_value(self, value):
        _Attribute._validate_value(self, value)

        if value is not None and value not in self._values:
            raise ValueError('Unknown %s: %s' % (self.name, value))

class NumericalRangeAttribute(NumericalAttribute):

    def __init__(self, default_unit=None, minvalue=-np.inf, maxvalue=np.inf,
                  required=False, xmlname=None, doc=None):
        NumericalAttribute.__init__(self, default_unit, required, xmlname, doc)
        if minvalue > maxvalue: # pragma: no cover
            raise ValueError('Minimum value greater than maximum value')
        self._limitmin = minvalue
        self._limitmax = maxvalue

    def _validate_value(self, value):
        NumericalAttribute._validate_value(self, value)

        if value is None:
            return

        try:
            vmin, vmax = value
        except:
            raise ValueError('Range must be made of 2 values')

        if vmin > vmax:
            raise ValueError('Lower value greater than upper value')
        if vmin < self._limitmin:
            raise ValueError("Lower value is smaller than limit")
        if vmax > self._limitmax:
            raise ValueError("Upper value is greater than limit")

    def _new(self, cls, clsname, bases, methods, name):
        NumericalAttribute._new(self, cls, clsname, bases, methods, name)

        # Change set method to allow two values and unit input
        methods['set_%s' % name] = \
            lambda instance, vmin, vmax, unit = None: \
                self.__set__(instance, ((vmin, vmax), unit or self._default_unit))

class DateAttribute(_Attribute):

    def _prepare_value(self, value):
        if value is not None and not isinstance(value, datetime.date):
            dt = datetime.datetime.strptime(value, '%Y-%m-%d')
            value = datetime.date(dt.year, dt.month, dt.day)
        return value

class TimeAttribute(_Attribute):

    def _prepare_value(self, value):
        if value is not None and not isinstance(value, datetime.time):
            dt = datetime.datetime.strptime(value, '%H:%M:%S')
            value = datetime.time(dt.hour, dt.minute, dt.second)
        return value

class ChecksumAttribute(_Attribute):

    def _validate_value(self, value):
        _Attribute._validate_value(self, value)

        if value is not None and not isinstance(value, Checksum):
            raise ValueError('Value must be a Checksum object')

class ParameterMetaclass(type):

    def __new__(cls, clsname, bases, methods):
        attributes = OrderedDict()

        # Parameters from parents
        parents = [b for b in bases if isinstance(b, ParameterMetaclass)]
        for base in parents:
            attributes.update(base.__attributes__)

        # Attach attribute names to parameters
        for key, value in list(methods.items()):
            if isinstance(value, _Attribute):
                value._new(cls, clsname, bases, methods, key)
                attributes[value.name] = value

        # Add __attributes__
        methods['__attributes__'] = attributes

        # Add __repr__ method
        def _repr(self):
            reprstr = []
            for name, attribute in self.__attributes__.items():
                value = getattr(self, name, None)
                if value is None and not attribute.is_required():
                    continue
                reprstr.append('%s=%s' % (name, value))
            return '<%s(%s)>' % (self.__class__.__name__, ', '.join(reprstr))
        methods['__repr__'] = _repr

        return type.__new__(cls, clsname, bases, methods)

Parameter = ParameterMetaclass('Parameter', (object,), {})
