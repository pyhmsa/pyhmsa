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
try:
    from collections import UserDict
except ImportError: # Python 2.7
    from UserDict import UserDict

import datetime
import time

# Third party modules.
try:
    import pytz
except ImportError:
    pytz = None

# Local modules.
from pyhmsa.type.checksum import Checksum

# Globals and constants variables.

class Header(UserDict):
    
    def __init__(self, checksum=None, title=None, author=None, owner=None,
                  date=None, time=None, timezone=None, client=None,
                  author_software=None, location=None, comment=None):
        """
        Contains metadata that principally identifies the title of the document, 
        the author/ownership of the data, and the date/time of collection. 
        Header information shall not contain parameters that are required for 
        the interpretation of the experimental data.
        """
        UserDict.__init__(self)

    def __setitem__(self, key, item):
        key = key.title()
        # TODO: Verify key

        if item is None:
            self.pop(key, None)
            return

        method = getattr(self, 'set_%s' % key.lower(), None)
        if method:
            method(item)
        else:
            UserDict.__setitem__(self, key, item)

    def __getitem__(self, key):
        return UserDict.__getitem__(self, key.title())
#        except KeyError:
#            return None

    def get_title(self):
        return self.get('Title')

    def set_title(self, value):
        UserDict.__setitem__(self, 'Title', value)

    title = property(get_title, set_title)

    def get_author(self):
        return self.get('Author')

    def set_author(self, value):
        UserDict.__setitem__(self, 'Author', value)

    author = property(get_author, set_author)

    def get_owner(self):
        return self.get('Owner')

    def set_owner(self, value):
        UserDict.__setitem__(self, 'Owner', value)

    owner = property(get_owner, set_owner)

    def get_date(self):
        return self.get('Date')

    def set_date(self, value):
        if not isinstance(value, datetime.date):
            dt = datetime.datetime.strptime(value, '%Y-%m-%d')
            value = datetime.date(dt.year, dt.month, dt.day)
        UserDict.__setitem__(self, 'Date', value)

    date = property(get_date, set_date)

    def get_time(self):
        return self.get('Time')

    def set_time(self, value):
        if not isinstance(value, datetime.time):
            dt = datetime.datetime.strptime(value, '%H:%M:%S')
            tzinfo = self.get('Timezone', pytz.timezone(time.tzname[0]) if pytz else None)
            value = datetime.time(dt.hour, dt.minute, dt.second, tzinfo=tzinfo)
        UserDict.__setitem__(self, 'Time', value)
        UserDict.__setitem__(self, 'Timezone', value.tzinfo)

    time = property(get_time, set_time)

    def get_timezone(self):
        return self.get('Timezone')

    def set_timezone(self, value):
        if not isinstance(value, datetime.tzinfo) and pytz is not None:
            value = pytz.timezone(value)
        UserDict.__setitem__(self, 'Timezone', value)

    timezone = property(get_timezone, set_timezone)

    def get_checksum(self):
        return self.get('Checksum')

    def set_checksum(self, value):
        if not isinstance(value, Checksum):
            raise ValueError('Only Checksum object are supported')
        UserDict.__setitem__(self, 'Checksum', value)

    checksum = property(get_checksum, set_checksum)
