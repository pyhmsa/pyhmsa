#!/usr/bin/env python
"""
================================================================================
:mod:`checksum` -- Check sum
================================================================================

.. module:: checksum
   :synopsis: Check sum

.. inheritance-diagram:: checksum

"""

# Standard library modules.
from collections import namedtuple
import hashlib

# Third party modules.

# Local modules.

# Globals and constants variables.

CHECKSUM_ALGORITHM_SHA1 = 'SHA-1'
CHECKSUM_ALGORITHM_SUM32 = 'SUM32'

class Checksum(namedtuple('Checksum', ['value', 'algorithm'])):

    def __new__(cls, value, algorithm):
        if algorithm not in _CHECKSUM_ALGORITHMS:
            raise ValueError('Unknown algorithm: %s' % algorithm)
        value = value.upper()
        return cls.__bases__[0].__new__(cls, value, algorithm)

def calculate_checksum_sha1(buffer):
    sha1 = hashlib.sha1()
    sha1.update(buffer)
    value = sha1.hexdigest()
    return Checksum(value, CHECKSUM_ALGORITHM_SHA1)

def calculate_checksum_sum32(buffer):
    try:
        sumbytes = sum(buffer)
    except: # Python 2
        sumbytes = sum(map(ord, buffer))
    value = hex(sumbytes)[2:34].zfill(32)
    return Checksum(value, CHECKSUM_ALGORITHM_SUM32)

_CHECKSUM_ALGORITHMS = {CHECKSUM_ALGORITHM_SHA1: calculate_checksum_sha1,
                        CHECKSUM_ALGORITHM_SUM32: calculate_checksum_sum32}

def calculate_checksum(algorithm, buffer):
    try:
        method = _CHECKSUM_ALGORITHMS[algorithm.upper()]
    except KeyError:
        raise ValueError('Unknown checksum algorithm: %s' % algorithm)
    else:
        return method(buffer)
