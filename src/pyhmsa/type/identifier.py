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
from collections import MutableMapping, KeysView, ValuesView, ItemsView
import fnmatch
import inspect
import copy

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

class _IdentifierDict(MutableMapping):

    def __init__(self, adict=None, **kwargs):
        self._data = {}

        if adict is not None:
            self.update(adict)
        self.update(**kwargs)

        self.item_added = Signal()
        self.item_deleted = Signal()
        self.item_modified = Signal()

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, identifier):
        return self._data[identifier]

    def __setitem__(self, identifier, item):
        validate_identifier(identifier)

        new = identifier not in self
        if not new:
            olditem = self[identifier]

        self._data[identifier] = item

        if new:
            self.item_added.fire(identifier, item)
        else:
            self.item_modified.fire(identifier, item, olditem)

    def __delitem__(self, identifier):
        olditem = self[identifier]
        del self._data[identifier]
        self.item_deleted.fire(identifier, olditem)

    def copy(self):
        data = self._data
        try:
            self._data = {}
            c = copy.copy(self)
        finally:
            self._data = data
        c.update(self)
        return c

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
