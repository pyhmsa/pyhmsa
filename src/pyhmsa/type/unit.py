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

_PREFIXES_VALUES = {'Y': 1e24, 'Z': 1e21, 'E': 1e18, 'P': 1e15, 'T': 1e12,
                    'G': 1e9, 'M': 1e6, 'k': 1e3, 'm': 1e-3, u'\u00b5': 1e-6,
                    'n': 1e-9, 'p': 1e-12, 'f': 1e-15, 'a': 1e-18, 'z': 1e-21,
                    'y': 1e-24}

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
    exponent = float(match.group('exponent') or 1.0)

    return prefix, baseunit, exponent

def validate_unit(unit):
    prefix, baseunit, _ = parse_unit(unit)

    # Special cases
    if baseunit == 'g' and prefix in ['Y', 'Z', 'E', 'P', 'T', 'G', 'M']:
        raise ValueError('Use kg to express mass greater than 1 kg')
    if baseunit == 's' and prefix in ['Y', 'Z', 'E', 'P', 'T', 'G', 'M', 'k']:
        raise ValueError('Use s to express time greater than 1 s')
    if baseunit == u'\u00c5' and prefix is not None:
        raise ValueError(u'Prefix are not allowed for \u00c5')

    return True

