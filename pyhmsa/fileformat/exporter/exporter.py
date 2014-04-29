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

    def __init__(self, datafile, dirpath, *args, **kwargs):
        args = (datafile, dirpath,) + args
        _MonitorableThread.__init__(self, args=args, kwargs=kwargs)

    def _run(self, datafile, dirpath, *args, **kwargs):
        raise NotImplementedError

class _Exporter(_Monitorable):

    def _create_thread(self, datafile, dirpath, *args, **kwargs):
        args = (datafile, dirpath,) + args
        _Monitorable._create_thread(self, *args, **kwargs)

    def validate(self, datafile):
        pass

    def can_export(self, datafile):
        try:
            self.validate(datafile)
        except:
            return False
        else:
            return True

    def export(self, datafile, dirpath):
        self.validate(datafile)

        if not os.path.exists(dirpath):
            raise ValueError('Path does not exist: %s' % dirpath)
        if not os.path.isdir(dirpath):
            raise ValueError('Path is not a directory: %s' % dirpath)

        self._start(datafile, dirpath)
