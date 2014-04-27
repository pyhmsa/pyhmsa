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
        self._filepath = filepath

        self._version = version

        self._language = language

        self._header = Header()

        self._conditions = Conditions()
        self._conditions.item_deleted.connect(self._on_condition_deleted)
        self._conditions.item_modified.connect(self._on_condition_modified)

        self._data = Data()
        self._data.item_added.connect(self._on_datum_added)
        self._data.item_modified.connect(self._on_datum_modified)

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

    def _on_condition_deleted(self, identifier, oldcondition):
        for datum in self._data.values():
            for identifier2 in list(datum.conditions.keys()):
                if identifier == identifier2:
                    del datum.conditions[identifier]

    def _on_condition_modified(self, identifier, condition, oldcondition):
        for datum in self._data.values():
            for identifier2 in datum.conditions.keys():
                if identifier == identifier2 and condition != oldcondition:
                    datum.conditions[identifier] = condition

    def _on_datum_added(self, identifier, datum):
        datum.conditions.item_added.connect(self._on_datum_condition_added)
        datum.conditions.item_modified.connect(self._on_datum_condition_modified)

        # Re-add conditions (to allow signal to be propagated)
        conditions = datum.conditions.copy()
        datum.conditions.clear()
        datum.conditions.update(conditions)

    def _on_datum_modified(self, identifier, newdatum, olddatum):
        # Remove old conditions
        for condition_identifier in olddatum.conditions.keys():
            state = None
            for datum in self._data.values():
                if condition_identifier in datum.conditions:
                    if datum is newdatum: # Same object
                        state = 'replace'
                    else:
                        state = 'remove'

            if condition_identifier in self._conditions:
                if state == 'remove':
                    del self._conditions[condition_identifier]
                elif state == 'replace':
                    self._conditions[condition_identifier] = \
                        newdatum.conditions[condition_identifier]

        self._on_datum_added(identifier, newdatum)

    def _on_datum_condition_added(self, identifier, condition):
        if identifier not in self._conditions:
            self._conditions[identifier] = condition

        if condition != self._conditions[identifier]:
            raise ValueError('Condition with ID "%s" already exists' % identifier)

    def _on_datum_condition_modified(self, identifier, condition, oldcondition):
        self._conditions[identifier] = condition

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
        return self._filepath
