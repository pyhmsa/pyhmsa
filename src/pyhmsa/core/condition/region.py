#!/usr/bin/env python
"""
================================================================================
:mod:`region` -- Region of interest condition
================================================================================

.. module:: region
   :synopsis: Region of interest condition

.. inheritance-diagram:: region

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.

# Third party modules.

# Local modules.
from pyhmsa.core.condition import _Condition
from pyhmsa.type.numerical import extract_value

# Globals and constants variables.

class RegionOfInterest(_Condition):
    
    def __init__(self, start_channel, end_channel):
        """
        Defines a region of a spectrum (or other one-dimensional datum), 
        as may be useful for defining start and end channels used for a region 
        of interest image.
        
        :arg start_channel: start channel (required)
        :arg end_channel: end channel (required)
        """
        _Condition.__init__(self)

        self.set_channel(start_channel, end_channel)

    def get_start_channel(self):
        """
        Returns the start channel.
        """
        return self._start_channel

    start_channel = property(get_start_channel, doc='Start channel')

    def get_end_channel(self):
        """
        Returns the end channel.
        """
        return self._end_channel

    end_channel = property(get_end_channel, doc='End channel')

    def set_channel(self, start, end):
        """
        Sets the start and end channel.
        
        :arg start: start channel
        :arg end: end channel
        """
        if start is None:
            raise ValueError('Start channel required')
        if end is None:
            raise ValueError('End channel required')
        if start < 0:
            raise ValueError('Start channel must be greater than 0')
        if start > end:
            raise ValueError('Start channel greater than end channel')
        self._start_channel = extract_value(start)
        self._end_channel = extract_value(end)
