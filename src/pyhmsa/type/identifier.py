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

# Third party modules.

# Local modules.

# Globals and constants variables.

def validate_identifier(identifier):
    try:
        identifier.encode('ascii')
        return True
    except UnicodeEncodeError:
        raise ValueError('Identifier contains non-ascii characters')

class _IdentifierDict(UserDict):

    def __setitem__(self, identifier, item):
        validate_identifier(identifier)
        UserDict.__setitem__(self, identifier, item)