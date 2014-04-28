#!/usr/bin/env python
"""
================================================================================
:mod:`cookbook` -- Utility functions taken from Python Cookbook
================================================================================

.. module:: cookbook
   :synopsis: Utility functions taken from Python Cookbook

.. inheritance-diagram:: cookbook

"""

# Standard library modules.
from collections import Iterable

# Third party modules.
import six

# Local modules.

# Globals and constants variables.

def flatten(items, ignore_types=(six.string_types, six.binary_type, six.text_type)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            for y in flatten(x):
                yield y
        else:
            yield x
