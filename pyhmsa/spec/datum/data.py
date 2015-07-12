"""
Dictionary of datum objects
"""

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.spec.datum.datum import _Datum
from pyhmsa.type.identifier import _IdentifierDict
from pyhmsa.spec.condition.conditions import Conditions, WeakConditions

# Globals and constants variables.

class Data(_IdentifierDict):

    def __init__(self, datafile):
        _IdentifierDict.__init__(self)
        self._datafile = datafile

    def __setitem__(self, identifier, datum):
        if not isinstance(datum, _Datum):
            raise ValueError("Value is not a datum")

        # Remove old datum
        if identifier in self:
            del self[identifier]

        # Reconstruct weak references to conditions
        conditions = WeakConditions(self._datafile)
        for cidentifier, condition in datum.conditions.items():
            if condition not in self._datafile.conditions.values():
                cidentifier = self._datafile.conditions.add(cidentifier, condition)
            else:
                for cidentifier2, condition2 in self._datafile.conditions.items():
                    if condition == condition2:
                        cidentifier = cidentifier2
                        break
            conditions[cidentifier] = condition

        datum._conditions = conditions

        _IdentifierDict.__setitem__(self, identifier, datum)

    def __delitem__(self, identifier):
        datum = self[identifier]

        conditions = Conditions()
        conditions.update(datum.conditions)
        datum._conditions = conditions

        _IdentifierDict.__delitem__(self, identifier)
