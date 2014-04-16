#!/usr/bin/env python
"""
================================================================================
:mod:`parsedict` -- Add utility function to Python's dict to help parsing
================================================================================

.. module:: parsedict
   :synopsis: Add utility function to Python's dict to help parsing

.. inheritance-diagram:: pyhmsa.util.parsedict

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2014 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

class parsedict(dict):

    BOOLEAN_STATES = {'1': True, 'yes': True, 'true': True, 'on': True,
                      '0': False, 'no': False, 'false': False, 'off': False}

    def _convert_to_boolean(self, value):
        """Return a boolean value translating from other types if necessary.
        """
        if value.lower() not in self.BOOLEAN_STATES:
            raise ValueError('Not a boolean: %s' % value)
        return self.BOOLEAN_STATES[value.lower()]

    def _get(self, key, conv, default=None):
        try:
            value = self[key]
        except KeyError:
            return default
        else:
            return conv(value)

    def getint(self, key, default=None):
        return self._get(key, lambda s: int(float(s)), default)

    def getfloat(self, key, default=None):
        return self._get(key, float, default)

    def getboolean(self, key, default=None):
        return self._get(key, self._convert_to_boolean, default)

    def getmany(self, keys, conv=str, default=None):
        for key in keys:
            try:
                value = self[key]
                return conv(value)
            except KeyError:
                continue
        return default