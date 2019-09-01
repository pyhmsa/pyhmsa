"""
Header element
"""

# Standard library modules.
from collections.abc import MutableMapping
from abc import ABCMeta
import datetime
import threading

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

    def __new__(cls, datafile=None,
                title=None, author=None, owner=None, date=None,
                time=None, timezone=None, checksum=None, **kwargs):
        obj = super().__new__(cls)

        obj._lock = datafile._lock if datafile else threading.Lock()

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
            with self._lock:
                setattr(self, key.lower(), value)
        else:
            validate_identifier(key)
            with self._lock:
                self._extras[key] = value

    def __getitem__(self, key):
        if key.lower() in self.__attributes__:
            return getattr(self, key.lower())
        else:
            return self._extras[key]

    def __delitem__(self, key):
        if key.lower() in self.__attributes__:
            with self._lock:
                delattr(self, key.lower())
        else:
            with self._lock:
                del self._extras[key]

    def __getstate__(self):
        # Required not to pickle lock
        return dict(self.items())

    def __setstate__(self, items):
        self.update(**items)

    def set_datetime(self, dt):
        self.date = dt.date()
        self.time = dt.time()

    def get_datetime(self):
        date = self.date
        time = self.time
        return datetime.datetime(date.year, date.month, date.day,
                                 time.hour, time.minute, time.second, time.microsecond)

    datetime = property(get_datetime, set_datetime)
