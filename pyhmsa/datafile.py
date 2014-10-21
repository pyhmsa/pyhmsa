#!/usr/bin/env python
"""
================================================================================
:mod:`datafile` -- MSA hyper dimensional data file
================================================================================

.. module:: datafile
   :synopsis: MSA hyper dimensional data file

.. inheritance-diagram:: pyhmsa.spec.datafile

"""

# Standard library modules.
import os

# Third party modules.

# Local modules.
from pyhmsa.spec.header import Header
from pyhmsa.spec.condition.conditions import Conditions
from pyhmsa.spec.datum.data import Data

from pyhmsa.type.language import validate_language_tag

# Globals and constants variables.

class DataFile(object):

    VERSION = '1.0'

    def __init__(self, filepath=None, version=VERSION, language='en-US'):
        """
        Creates a new MSA hyper dimensional data file.

        Conditions and data objects can be added using the attributes
        :attr:`conditions <.DataFile.conditions>` and
        :attr:`data <.DataFile.data>`, respectively.
        Note that conditions part of any datum object will also appear in the
        global conditions dictionary.

        :arg version: version of the data file
            (default: to most up-to-date version)
        :arg language: language of the data file (default and recommended
            language is ``en-US``)
        """
        if filepath is not None:
            filepath = os.path.splitext(filepath)[0] + '.hmsa'
        self._filepath = filepath

        self._version = version

        self._language = language

        self._header = Header()

        self._conditions = Conditions()
        self._data = Data(self)

    @classmethod
    def read(cls, filepath):
        """
        Reads an existing MSA hyper dimensional data file and returns an
        object of this class.

        :arg filepath: either the location of the XML or HMSA file.
            Note that both have to be present.
        """
        from pyhmsa.fileformat.datafile import DataFileReader
        reader = DataFileReader()
        reader.read(filepath)
        return reader.get()

    def write(self, filepath=None):
        """
        Writes this data file to disk.

        :arg filepath: either the location of the XML or HMSA file
        """
        from pyhmsa.fileformat.datafile import DataFileWriter
        writer = DataFileWriter()
        writer.write(self, filepath)
        writer.join()

    def update(self, datafile):
        self._header.update(datafile.header)
        self._conditions.update(datafile.conditions)
        self._data.update(datafile.data)

    def merge(self, datafile):
        for key, value in datafile.header.items():
            if self.header.get(key) is None:
                self.header[key] = value

        self._data.addall(datafile.data)
        self._conditions.addall(datafile.orphan_conditions)

    @property
    def header(self):
        """
        Header
        """
        return self._header

    @property
    def conditions(self):
        """
        Conditions
        """
        return self._conditions

    @property
    def orphan_conditions(self):
        """
        Conditions that are not associated to any data sets (read-only).
        """
        conditions = {}

        for identifier, condition in self.conditions.items():
            orphan = True
            for datum in self.data.values():
                if condition in datum.conditions.values():
                    orphan = False
                    break
            if orphan:
                conditions[identifier] = condition

        return conditions

    @property
    def data(self):
        """
        Data
        """
        return self._data

    @property
    def version(self):
        """
        Version
        """
        return self._version

    @property
    def language(self):
        """
        Language
        """
        return self._language

    @language.setter
    def language(self, language):
        validate_language_tag(language)
        self._language = language

    @property
    def filepath(self):
        """
        Path where the data file was last saved. Always .hmsa extension used.
        """
        return self._filepath
