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
from collections import MutableMapping
from abc import ABCMeta

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

    def __init__(self, title=None, author=None, owner=None, date=None,
                 time=None, timezone=None, checksum=None, **kwargs):
        """
        Contains metadata that principally identifies the title of the document,
        the author/ownership of the data, and the date/time of collection.
        Header information shall not contain parameters that are required for
        the interpretation of the experimental data.
        """
        self.title = title
        self.author = author
        self.owner = owner
        self.date = date
        self.time = time
        self.timezone = timezone
        self.checksum = checksum

        self._extras = {}
        self._extras.update(kwargs)

    def __hash__(self):
        return hash(tuple(self.items()))

    def __reduce__(self):
        return (self.__class__, ())

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
