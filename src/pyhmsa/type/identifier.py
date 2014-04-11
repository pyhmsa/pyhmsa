#!/usr/bin/env python
"""
================================================================================
:mod:`identifier` -- Condition and datum identifier
================================================================================

.. module:: identifier
   :synopsis: Condition and datum identifier

.. inheritance-diagram:: pyhmsa.format.identifier

"""

# Standard library modules.
try:
    from collections import UserDict
except ImportError: # pragma: no cover
    from UserDict import UserDict
import fnmatch
import inspect

# Third party modules.

# Local modules.
from pyhmsa.util.signal import Signal

# Globals and constants variables.

def validate_identifier(identifier):
    if len(identifier.strip()) == 0:
        raise ValueError('Identifier cannot be an empty string')
    try:
        identifier.encode('ascii')
        return True
    except UnicodeEncodeError:
        raise ValueError('Identifier contains non-ascii characters')

class _IdentifierDict(UserDict):

    def __init__(self, adict=None, **kwargs):
        UserDict.__init__(self, adict, **kwargs)

        self.item_added = Signal()
        self.item_deleted = Signal()
        self.item_modified = Signal()

    def __setitem__(self, identifier, item):
        validate_identifier(identifier)

        new = identifier not in self
        if not new:
            olditem = self[identifier]

        UserDict.__setitem__(self, identifier, item)

        if new:
            self.item_added.fire(identifier, item)
        else:
            self.item_modified.fire(identifier, item, olditem)

    def __delitem__(self, identifier):
        olditem = self[identifier]
        UserDict.__delitem__(self, identifier)
        self.item_deleted.fire(identifier, olditem)

    def findkeys(self, match):
        if isinstance(match, str):
            return frozenset(key for key, value in self.items() \
                             if fnmatch.fnmatch(key, match))
        elif inspect.isclass(match):
            return frozenset(key for key, value in self.items() \
                             if isinstance(value, match))
        else:
            raise ValueError("Specify an identifier or class")

    def findvalues(self, match):
        if isinstance(match, str):
            return frozenset(value for key, value in self.items() \
                             if fnmatch.fnmatch(key, match))
        elif inspect.isclass(match):
            return frozenset(value for value in self.values() \
                             if isinstance(value, match))
        else:
            raise ValueError("Specify an identifier or class")

    def finditems(self, match):
        if isinstance(match, str):
            return frozenset((key, value) for key, value in self.items() \
                             if fnmatch.fnmatch(key, match))
        elif inspect.isclass(match):
            return frozenset((key, value) for key, value in self.items() \
                             if isinstance(value, match))
        else:
            raise ValueError("Specify an identifier or class")
