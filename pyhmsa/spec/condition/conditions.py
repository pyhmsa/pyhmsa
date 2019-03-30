"""
Dictionary of conditions
"""

# Standard library modules.
import threading

# Third party modules.

# Local modules.
from pyhmsa.type.identifier import _IdentifierDict, _WeakValueIdentifierDict
from pyhmsa.spec.condition.condition import _Condition

# Globals and constants variables.

class Conditions(_IdentifierDict):

    def __init__(self, datafile=None):
        super().__init__()
        self._lock = datafile._lock if datafile else threading.Lock()

    def __setitem__(self, identifier, condition):
        if not isinstance(condition, _Condition):
            raise ValueError("Value is not a condition")
        with self._lock:
            super().__setitem__(identifier, condition)

    def __delitem__(self, identifier):
        with self._lock:
            super().__delitem__(identifier)

class WeakConditions(_WeakValueIdentifierDict):

    def __init__(self, datafile):
        super().__init__()
        self._datafile = datafile
        self._lock = datafile._lock

    def __setitem__(self, identifier, condition):
        self._datafile.conditions[identifier] = condition
        with self._lock:
            super().__setitem__(identifier, condition)

    def __delitem__(self, key):
        with self._lock:
            super().__delitem__(key)
