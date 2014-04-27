#!/usr/bin/env python
"""
================================================================================
:mod:`header` -- Header element
================================================================================

.. module:: header
   :synopsis: Header element

.. inheritance-diagram:: pyemsa.header

"""

# Standard library modules.
from collections import MutableMapping, Mapping
from abc import ABCMeta
import datetime

# Third party modules.

# Local modules.
from pyhmsa.type.identifier import validate_identifier
from pyhmsa.util.parameter import \
    (ParameterMetaclass, Parameter, TextAttribute, DateAttribute,
     TimeAttribute, ChecksumAttribute)

# Globals and constants variables.

class _HeaderMetaclass(ABCMeta, ParameterMetaclass):
    pass

_BaseHeader = _HeaderMetaclass('_HeaderMetaclass', (MutableMapping, Parameter), {})

class Header(_BaseHeader):

    title = TextAttribute(False, 'Title', 'title')
    author = TextAttribute(False, 'Author', 'author')
    owner = TextAttribute(False, 'Owner', 'legal owner')
    date = DateAttribute(False, 'Date', 'date')
    time = TimeAttribute(False, 'Time', 'time')
    timezone = TextAttribute(False, 'Timezone', 'timezone')
    checksum = ChecksumAttribute(False, 'Checksum', 'checksum')

    def __new__(cls, title=None, author=None, owner=None, date=None,
                time=None, timezone=None, checksum=None, **kwargs):
        obj = _BaseHeader.__new__(cls)

        obj.title = title
        obj.author = author
        obj.owner = owner
        obj.date = date
        obj.time = time
        obj.timezone = timezone
        obj.checksum = checksum

        obj._extras = {}
        obj._extras.update(kwargs)

        return obj

    def __hash__(self):
        return hash(tuple(self.items()))

    def __len__(self):
        return len(self._extras) + len(self.__attributes__)

    def __iter__(self):
        for key in set(self._extras.keys()) | set(self.__attributes__.keys()):
            yield key

    def __setitem__(self, key, value):
        if key.lower() in self.__attributes__:
            setattr(self, key.lower(), value)
        else:
            validate_identifier(key)
            self._extras[key] = value

    def __getitem__(self, key):
        if key.lower() in self.__attributes__:
            return getattr(self, key.lower())
        else:
            return self._extras[key]

    def __delitem__(self, key):
        if key.lower() in self.__attributes__:
            delattr(self, key.lower())
        else:
            del self._extras[key]

    def update(*args, **kwds): #@NoSelf
        """"
        .. note::
           Override MutableMapping update method to prevent update of values
           which are equal to ``None``.
        """
        if len(args) > 2:
            raise TypeError("update() takes at most 2 positional "
                            "arguments ({} given)".format(len(args)))
        elif not args:
            raise TypeError("update() takes at least 1 argument (0 given)")
        self = args[0]
        other = args[1] if len(args) >= 2 else ()

        if isinstance(other, Mapping):
            for key in other:
                if other[key] is not None:
                    self[key] = other[key]
        elif hasattr(other, "keys"):
            for key in other.keys():
                if other[key] is not None:
                    self[key] = other[key]
        else:
            for key, value in other:
                if value is not None:
                    self[key] = value
        for key, value in kwds.items():
            if value is not None:
                self[key] = value

    def set_datetime(self, dt):
        self.date = dt.date()
        self.time = dt.time()

    def get_datetime(self):
        date = self.date
        time = self.time
        return datetime.datetime(date.year, date.month, date.day,
                                 time.hour, time.minute, time.second, time.microsecond)

    datetime = property(get_datetime, set_datetime)
