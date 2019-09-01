"""
Condition and datum identifier
"""

# Standard library modules.
from collections.abc import MutableMapping, Mapping, KeysView, ValuesView, ItemsView
import fnmatch
import inspect
import copy
import re
import weakref

# Third party modules.

# Local modules.

# Globals and constants variables.

def validate_identifier(identifier):
    if len(identifier.strip()) == 0:
        raise ValueError('Identifier cannot be an empty string')
    try:
        identifier.encode('ascii')
        return True
    except UnicodeEncodeError:
        raise ValueError('Identifier contains non-ascii characters')

def sorted_identifier(iterable, reverse=False):
    """
    Sorts identifiers while taking into consideration the numeric suffix.
    """
    def _key(item):
        match = re.match(r'(\d+)(.*)$', item[::-1])
        if not match:
            return (item,)
        else:
            number, prefix = match.groups()
            return (prefix[::-1], int(number[::-1]))
    return sorted(iterable, key=_key, reverse=reverse)

class _BaseIdentifierDict(object):

    def add(self, identifier, item):
        base_identifier = re.sub(r'\d*$', '', identifier)

        identifiers = self.findkeys(base_identifier + '*')
        if identifiers: # Identifier already exists
            index = 1
            while identifier in self:
                identifier = '{0}{1:d}'.format(base_identifier, index)
                index += 1

        self[identifier] = item
        return identifier

    def addall(*args, **kwds): #@NoSelf
        if len(args) > 2:
            raise TypeError("update() takes at most 2 positional "
                            "arguments ({} given)".format(len(args)))
        elif not args:
            raise TypeError("update() takes at least 1 argument (0 given)")
        self = args[0]
        other = args[1] if len(args) >= 2 else ()

        if isinstance(other, Mapping):
            for identifier in other:
                self.add(identifier, other[identifier])
        elif hasattr(other, "keys"):
            for identifier in other.keys():
                self.add(identifier, other[identifier])
        else:
            for identifier, datum in other:
                self.add(identifier, datum)
        for identifier, datum in kwds.items():
            self.add(identifier, datum)

    def _find(self, match):
        if isinstance(match, str):
            return dict((key, value) for key, value in self.items() \
                        if fnmatch.fnmatch(key, match))
        elif inspect.isclass(match):
            return dict((key, value) for key, value in self.items() \
                        if isinstance(value, match))
        else:
            raise ValueError("Specify an identifier or class")

    def findkeys(self, match):
        return KeysView(self._find(match))

    def findvalues(self, match):
        return ValuesView(self._find(match))

    def finditems(self, match):
        return ItemsView(self._find(match))


class _IdentifierDict(MutableMapping, _BaseIdentifierDict):

    def __init__(self):
        super().__init__()
        self._data = {}

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__,
                             ','.join(sorted(self.keys())))

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, identifier):
        return self._data[identifier]

    def __setitem__(self, identifier, item):
        validate_identifier(identifier)
        self._data[identifier] = item

    def __delitem__(self, identifier):
        del self._data[identifier]

    def copy(self):
        data = self._data
        try:
            self._data = {}
            c = copy.copy(self)
        finally:
            self._data = data
        c.update(self)
        return c

class _WeakValueIdentifierDict(weakref.WeakValueDictionary, _BaseIdentifierDict):

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__,
                             ','.join(sorted(self.keys())))

    def __setitem__(self, identifier, item):
        validate_identifier(identifier)
        super().__setitem__(identifier, item)
