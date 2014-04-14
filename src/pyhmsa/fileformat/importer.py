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

# Globals and constants variables.

class _Importer(object):

    def __init__(self, supported_extensions, extra_datafile=None):
        if not supported_extensions:
            raise ValueError('At least one extension is required')
        self._supported_extensions = frozenset(supported_extensions)

        if extra_datafile is None:
            filepath = os.path.expanduser('~/.pyhmsa/extra.xml')
            if os.path.exists(filepath):
                extra_datafile = DataFile.read(filepath)
            else:
                extra_datafile = DataFile()
        self._extra_datafile = extra_datafile

    def _update_extra(self, datafile):
        if self._extra_datafile is None:
            return

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

    def _import(self, filepath):
        raise NotImplementedError

    def can_import(self, filepath):
        return os.path.splitext(filepath)[1] in self.supported_extensions

    def import_(self, filepath):
        datafile = self._import(filepath)
        self._update_extra(datafile)
        return datafile

    @property
    def supported_extensions(self):
        return self._supported_extensions
