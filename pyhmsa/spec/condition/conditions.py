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
        _IdentifierDict.__init__(self)
        self._lock = datafile._lock if datafile else threading.Lock()

    def __setitem__(self, identifier, condition):
        if not isinstance(condition, _Condition):
            raise ValueError("Value is not a condition")
        with self._lock:
            _IdentifierDict.__setitem__(self, identifier, condition)

    def __delitem__(self, identifier):
        with self._lock:
            _IdentifierDict.__delitem__(self, identifier)

class WeakConditions(_WeakValueIdentifierDict):

    def __init__(self, datafile):
        _WeakValueIdentifierDict.__init__(self)
        self._datafile = datafile
        self._lock = datafile._lock

    def __setitem__(self, identifier, condition):
        self._datafile.conditions[identifier] = condition
        with self._lock:
            _WeakValueIdentifierDict.__setitem__(self, identifier, condition)

    def __delitem__(self, key):
        with self._lock:
            _WeakValueIdentifierDict.__delitem__(self, key)
