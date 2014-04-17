#!/usr/bin/env python
"""
================================================================================
:mod:`exporter` -- Base class for exporters
================================================================================

.. module:: exporter
   :synopsis: Base class for exporters

.. inheritance-diagram:: pyhmsa.fileformat.exporter.exporter

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2014 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os

# Third party modules.

# Local modules.
from pyhmsa.util.monitorable import _Monitorable, _MonitorableThread

# Globals and constants variables.

class _ExporterThread(_MonitorableThread):

    def __init__(self, datafile, filepath, *args, **kwargs):
        args = (datafile, filepath,) + args
        _MonitorableThread.__init__(self, args=args, kwargs=kwargs)

    def _run(self, datafile, filepath, *args, **kwargs):
        raise NotImplementedError

class _Exporter(_Monitorable):

    SUPPORTED_EXTENSIONS = ()

    def _create_thread(self, datafile, filepath, *args, **kwargs):
        args = (datafile, filepath,) + args
        _Monitorable._create_thread(self, *args, **kwargs)

    def validate(self, datafile, filepath):
        ext = os.path.splitext(filepath)[1]
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError('%s is not a supported extension' % ext)

    def can_export(self, datafile, filepath):
        try:
            self.validate(datafile, filepath)
        except:
            return False
        else:
            return True

    def export(self, datafile, filepath):
        self._start(datafile, filepath)
