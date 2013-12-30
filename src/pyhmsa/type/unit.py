#!/usr/bin/env python
"""
================================================================================
:mod:`unit` -- Allowable units
================================================================================

.. module:: unit
   :synopsis: Allowable units

.. inheritance-diagram:: pyhmsa.unit

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import re

# Third party modules.

# Local modules.

# Globals and constants variables.

_SI_UNITS = frozenset(['m',
                       'g', # should kg, but causes problem with prefixes
                       's',
                       'A',
                       'K',
                       'mol',
                       'Cd'])

_SI_DERIVED_UNITS = frozenset([u'\u00c5', # Angstrom
                               'C',
                               u'\u00b0\u0043', # degC
                               'Hz',
                               'J',
                               'L',
                               'N',
                               'Pa',
                               'rad',
                               'sr',
                               'u',
                               'V',
                               'W',
                               u'\u03a9'])

_NON_SI_UNITS = frozenset([u'\u00b0', # deg,
                           'atoms',
                           'counts',
                           'c/s', # counts per second
                           'cps', # counts per second
                           'eV',
                           '%',
                           'mol%',
                           'vol%',
                           'wt%',
                           'mol_ppm',
                           'vol_ppm',
                           'wt_ppm',
                           'mol_ppb',
                           'vol_ppb',
                           'wt_ppb'])

_UNITS = _SI_UNITS | _SI_DERIVED_UNITS | _NON_SI_UNITS

_PREFIXES = frozenset(['Y', 'Z', 'E', 'P', 'T', 'G', 'M', 'k',
                      'm', u'\u00b5', 'n', 'p', 'f', 'a', 'z', 'y'])

_PATTERN = r'\A'
_PATTERN += '(?P<prefix>' + '|'.join(_PREFIXES) + ')?'
_PATTERN += '(?P<unit>' + '|'.join(_UNITS) + ')'
_PATTERN += '(?P<exponent>[+-]?\d+)?'
_PATTERN += r'\Z'

_RE_PATTERN = re.compile(_PATTERN, re.UNICODE)

def validate_unit(unit):
    match = _RE_PATTERN.match(unit)
    if match is None:
        raise ValueError('Invalid unit: %s' % unit)

    prefix = match.group('prefix')
    baseunit = match.group('unit')
#    exponent = match.group('exponent')

    # Special cases
    if baseunit == 'g' and prefix in ['Y', 'Z', 'E', 'P', 'T', 'G', 'M']:
        raise ValueError('Use kg to express mass greater than 1 kg')
    if baseunit == 's' and prefix in ['Y', 'Z', 'E', 'P', 'T', 'G', 'M', 'k']:
        raise ValueError('Use s to express time greater than 1 s')
    if baseunit == u'\u00c5' and prefix is not None:
        raise ValueError(u'Prefix are not allowed for \u00c5')

    return True

