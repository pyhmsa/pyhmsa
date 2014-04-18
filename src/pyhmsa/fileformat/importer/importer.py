#!/usr/bin/env python
"""
================================================================================
:mod:`importer` -- Base class for importers
================================================================================

.. module:: importer
   :synopsis: Base class for importers

.. inheritance-diagram:: pyhmsa.fileformat.importer

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
from pyhmsa.datafile import DataFile
from pyhmsa.util.monitorable import _Monitorable, _MonitorableThread

# Globals and constants variables.

class _ImporterThread(_MonitorableThread):

    def __init__(self, filepath, *args, **kwargs):
        args = (filepath,) + args
        _MonitorableThread.__init__(self, args=args, kwargs=kwargs)

    def _run(self, filepath, *args, **kwargs):
        raise NotImplementedError

class _Importer(_Monitorable):

    SUPPORTED_EXTENSIONS = ()

    def __init__(self, extra_datafile=None):
        _Monitorable.__init__(self)

        if extra_datafile is None:
            filepath = os.path.expanduser('~/.pyhmsa/importer_extra.xml')
            if os.path.exists(filepath):
                extra_datafile = DataFile.read(filepath)
            else:
                extra_datafile = DataFile()
        self._extra_datafile = extra_datafile

    def _update_extra(self, datafile):
        # Header
        for key, value in self._extra_datafile.header.items():
            if datafile.header[key] is None:
                datafile.header[key] = value

        # Conditions
        for extra_name, extra_condition in self._extra_datafile.conditions.items():
            conditions = datafile.conditions.findvalues(extra_name + '*')

            for condition in conditions:
                if type(condition) is not type(extra_condition):
                    continue

                for attr in condition.__attributes__.keys():
                    if getattr(condition, attr, None) is None:
                        value = getattr(extra_condition, attr, None)
                        setattr(condition, attr, value)

    def _create_thread(self, filepath, *args, **kwargs):
        args = (filepath,) + args
        _Monitorable._create_thread(self, *args, **kwargs)

    def validate(self, filepath):
        ext = os.path.splitext(filepath)[1]
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError('%s is not a supported extension' % ext)

    def can_import(self, filepath):
        try:
            self.validate(filepath)
        except:
            return False
        else:
            return True

    def import_(self, filepath):
        """
        Should create appropriate importer thread and starts it.
        """
        self._start(filepath)

    def get(self):
        datafile = _Monitorable.get(self)
        self._update_extra(datafile)
        return datafile
