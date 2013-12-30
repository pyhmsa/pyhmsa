#!/usr/bin/env python
"""
================================================================================
:mod:`header` -- Header element
================================================================================

.. module:: header
   :synopsis: Header element

.. inheritance-diagram:: pyemsa.header

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.type.identifier import validate_identifier
from pyhmsa.util.parameter import \
    Parameter, TextAttribute, DateAttribute, TimeAttribute, ChecksumAttribute

# Globals and constants variables.

class Header(Parameter):

    title = TextAttribute(False, 'Title', 'title')
    author = TextAttribute(False, 'Author', 'author')
    owner = TextAttribute(False, 'Owner', 'legal owner')
    date = DateAttribute(False, 'Date', 'date')
    time = TimeAttribute(False, 'Time', 'time')
    checksum = ChecksumAttribute(False, 'Checksum', 'checksum')

    def __init__(self, **kwargs):
        """
        Contains metadata that principally identifies the title of the document,
        the author/ownership of the data, and the date/time of collection.
        Header information shall not contain parameters that are required for
        the interpretation of the experimental data.
        """
        for key, value in kwargs.items():
            self[key] = value

    def __setitem__(self, key, value):
        key = key.lower()
        validate_identifier(key)

        if value is None:
            self.__dict__.pop(key, None)
            return

        method = getattr(self, 'set_%s' % key, None)
        if method:
            method(value)
        else:
            self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__.get(key.lower())

    def __delitem__(self, key):
        del self.__dict__[key.lower()]

    def __contains__(self, key):
        return key.lower() in self.__dict__
