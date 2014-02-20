#!/usr/bin/env python
"""
================================================================================
:mod:`cookbook` -- Utility functions taken from Python Cookbook
================================================================================

.. module:: cookbook
   :synopsis: Utility functions taken from Python Cookbook

.. inheritance-diagram:: cookbook

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
from collections import Iterable

# Third party modules.

# Local modules.

# Globals and constants variables.

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            for y in flatten(x):
                yield y
        else:
            yield x
