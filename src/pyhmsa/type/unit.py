#!/usr/bin/env python
"""
================================================================================
:mod:`unit` -- Allowable units
================================================================================

.. module:: unit
   :synopsis: Allowable units

.. inheritance-diagram:: pyhmsa.unit

"""

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
                               'Bq',
                               'C',
                               'Da', # March 2014: Changed symbols for atomic mass unit from 'u' to 'Da' (Dalton), to avoid conflict with use of 'u' for micro prefix.
                               u'\u00b0\u0043', # degC
                               'degreesC', # March 2014: Changed preference to ASCII over Unicode characters
                               'F',
                               'Gy',
                               'H',
                               'Hz',
                               'J',
                               'L',
                               'lm',
                               'lx'
                               'N',
                               u'\u03a9', # ohm
                               'Ohm', # March 2014: Changed preference to ASCII over Unicode characters
                               'Pa',
                               'rad',
                               'S',
                               'Sv',
                               'sr',
                               'T',
                               'V',
                               'W',
                               'Wb',
                               ])

_NON_SI_UNITS = frozenset([u'\u00b0', # deg,
                           'degrees', # March 2014: Changed preference to ASCII over Unicode characters
                           'atoms',
                           'counts',
                           'counts/s', # March 2014: 'c/s' and 'cps' was explicitly forbidden.
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
                      'm', u'\u00b5', 'u', 'n', 'p', 'f', 'a', 'z', 'y'])

_PREFIXES_VALUES = {'Y': 1e24, 'Z': 1e21, 'E': 1e18, 'P': 1e15, 'T': 1e12,
                    'G': 1e9, 'M': 1e6, 'k': 1e3, 'm': 1e-3, u'\u00b5': 1e-6,
                    'u': 1e-6, 'n': 1e-9, 'p': 1e-12, 'f': 1e-15, 'a': 1e-18,
                    'z': 1e-21, 'y': 1e-24}

_PATTERN = r'\A'
_PATTERN += '(?P<prefix>' + '|'.join(_PREFIXES) + ')?'
_PATTERN += '(?P<unit>' + '|'.join(_UNITS) + ')'
_PATTERN += '(?P<exponent>[+-]?\d+)?'
_PATTERN += r'\Z'

_RE_PATTERN = re.compile(_PATTERN, re.UNICODE)

def parse_unit(unit):
    match = _RE_PATTERN.match(unit)
    if match is None:
        raise ValueError('Invalid unit: %s' % unit)

    prefix = match.group('prefix')
    baseunit = match.group('unit')
    exponent = int(match.group('exponent') or 1)

    # Apply ASCII preference over Unicode characters
    if prefix is not None:
        prefix = prefix.replace(u'\u00b5', 'u')
    baseunit = baseunit.replace(u'\u00b0\u0043', 'degreesC')
    baseunit = baseunit.replace(u'\u03a9', 'Ohm')
    baseunit = baseunit.replace(u'\u00b0', 'degrees')

    return prefix, baseunit, exponent

def validate_unit(unit):
    prefix, baseunit, exponent = parse_unit(unit)

    # Special cases
    if baseunit == 'g' and prefix in ['Y', 'Z', 'E', 'P', 'T', 'G', 'M']:
        raise ValueError('Use kg to express mass greater than 1 kg')
    if baseunit == 's' and prefix in ['Y', 'Z', 'E', 'P', 'T', 'G', 'M', 'k']:
        raise ValueError('Use s to express time greater than 1 s')
    if baseunit == u'\u00c5' and prefix is not None:
        raise ValueError(u'Prefix are not allowed for \u00c5')

    return ''.join([prefix or '', baseunit, str(exponent) if exponent != 1 else ''])

