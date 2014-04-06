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
import binascii
import xml.etree.ElementTree as etree
from xml.dom import minidom
import logging

# Third party modules.
from pkg_resources import iter_entry_points

# Local modules.
from pyhmsa.spec.header import Header
from pyhmsa.spec.condition.conditions import Conditions
from pyhmsa.spec.datum.data import Data
from pyhmsa.type.language import validate_language_tag
from pyhmsa.fileformat.xmlhandler.header import HeaderXMLHandler
from pyhmsa.type.checksum import calculate_checksum, calculate_checksum_sha1
from pyhmsa.type.uid import generate_uid

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

    @staticmethod
    def _extract_filepath(filepath):
        base, ext = os.path.splitext(filepath)
        if ext not in ['.xml', '.hmsa']:
            raise IOError('File must be either a XML or HMSA')

        filepath_xml = base + '.xml'
        filepath_hmsa = base + '.hmsa'

        return filepath_xml, filepath_hmsa

    @classmethod
    def read(cls, filepath):
        """
        Reads an existing MSA hyper dimensional data file and returns an
        object of this class.

        :arg filepath: either the location of the XML or HMSA file.
            Note that both have to be present.
        """

        # Open files
        filepath_xml, filepath_hmsa = cls._extract_filepath(filepath)
        if not os.path.exists(filepath_xml):
            raise IOError('XML file is missing')
        if not os.path.exists(filepath_hmsa):
            raise IOError('HMSA file is missing')

        xml_file = open(filepath_xml, 'rb')
        hmsa_file = open(filepath_hmsa, 'rb')

        # Read XML
        root = etree.ElementTree(file=xml_file).getroot()

        # Create object
        obj = cls(filepath, root.attrib['Version'])

        # Read
        cls._read_root(obj, root)
        cls._read_header(obj, root)
        cls._read_conditions(obj, root)
        cls._read_data(obj, root, hmsa_file)

        # Close files
        xml_file.close()
        hmsa_file.close()

        return obj

    @classmethod
    def _read_root(cls, obj, root):
        obj.language = root.get('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')

    @classmethod
    def _read_header(cls, obj, root):
        handler = HeaderXMLHandler(obj.version)
        obj.header.update(handler.parse(root.find('Header')))

    @classmethod
    def _read_conditions(cls, obj, root):
        # Load handlers
        handlers = set()
        for entry_point in iter_entry_points('pyhmsa.fileformat.xmlhandler.condition'):
            handler = entry_point.load()(obj.version)
            handlers.add(handler)

        # Parse conditions
        for element in root.findall('Conditions/*'):
            key = element.get('ID', 'Inst%i' % len(obj.conditions))

            for handler in handlers:
                if handler.can_parse(element):
                    obj.conditions[key] = handler.parse(element)
                    break

    @classmethod
    def _read_data(cls, obj, root, hmsa_file):
        # Check UID
        xml_uid = root.attrib['UID'].encode('ascii')
        hmsa_uid = binascii.hexlify(hmsa_file.read(8))
        if xml_uid.upper() != hmsa_uid.upper():
            raise ValueError('UID in XML (%s) does not match UID in HMSA (%s)' % \
                             (xml_uid, hmsa_uid))
        logging.debug('Check UID: %s == %s', xml_uid, hmsa_uid)

        # Check checksum
        xml_checksum = getattr(obj.header, 'checksum', None)
        if xml_checksum is not None:
            xml_checksum = obj.header.checksum

            hmsa_file.seek(0)
            buffer = hmsa_file.read()
            hmsa_checksum = calculate_checksum(xml_checksum.algorithm, buffer)

            if xml_checksum.value.upper() != hmsa_checksum.value.upper():
                raise ValueError('Checksum in XML (%s) does not match checksum in HMSA (%s)' % \
                                 (xml_checksum.value, hmsa_checksum.value))
            logging.debug('Check sum: %s == %s', xml_checksum.value, hmsa_checksum.value)

        # Load handlers
        handlers = set()
        for entry_point in iter_entry_points('pyhmsa.fileformat.xmlhandler.datum'):
            handler = entry_point.load()(obj.version, hmsa_file, obj.conditions)
            handlers.add(handler)

        # Parse data
        for element in root.findall('Data/*'):
            key = element.get('Name', 'Inst%i' % len(obj.data))

            for handler in handlers:
                if handler.can_parse(element):
                    obj.data[key] = handler.parse(element)
                    break

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
        if filepath is None:
            filepath = self._filepath

        # Open files
        filepath_xml, filepath_hmsa = self._extract_filepath(filepath)

        xml_file = open(filepath_xml, 'wb')
        hmsa_file = open(filepath_hmsa, 'wb')

        # Generate UID
        uid = generate_uid()
        hmsa_file.write(uid)

        # Create XML
        root = etree.Element('MSAHyperDimensionalDataFile')
        self._write_root(root, uid)
        self._write_header(root)
        self._write_conditions(root)
        self._write_data(root, hmsa_file)

        # Close HMSA file
        hmsa_file.close()

        # Calculate and add checksum
        with open(filepath_hmsa, 'rb') as fp:
            checksum = calculate_checksum_sha1(fp.read())

        element = root.find('Header')
        subelement = etree.Element('Checksum')
        subelement.text = checksum.value
        subelement.set('Algorithm', checksum.algorithm)
        element.append(subelement)

        # Write XML file
        output = etree.tostring(root, encoding='UTF-8')
        document = minidom.parseString(output)
        output = document.toprettyxml(encoding='UTF-8')

        # Fix add standalone manually
        output = output.replace(b'<?xml version="1.0" encoding="UTF-8"?>',
                                b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')

        xml_file.write(output)

        # Close XML file
        xml_file.close()

        # Update internal file path
        self._filepath = filepath

        return binascii.hexlify(uid).upper()

    def _write_root(self, root, uid):
        root.set('Version', self.version)
        root.set('UID', binascii.hexlify(uid).decode('utf-8').upper())
        root.set('{http://www.w3.org/XML/1998/namespace}lang', self.language)

    def _write_header(self, root):
        handler = HeaderXMLHandler(self.version)
        element = handler.convert(self.header)
        root.append(element)

    def _write_conditions(self, root):
        # Load handlers
        handlers = set()
        for entry_point in iter_entry_points('pyhmsa.fileformat.xmlhandler.condition'):
            handler = entry_point.load()(self.version)
            handlers.add(handler)

        # Convert conditions
        element = etree.Element('Conditions')

        for identifier, condition in self.conditions.items():
            for handler in handlers:
                if handler.can_convert(condition):
                    subelement = handler.convert(condition)
                    subelement.set('ID', identifier)
                    element.append(subelement)
                    break

        root.append(element)

    def _write_data(self, root, hmsa_file):
        # Load handlers
        handlers = set()
        for entry_point in iter_entry_points('pyhmsa.fileformat.xmlhandler.datum'):
            handler = entry_point.load()(self.version, hmsa_file, self.conditions)
            handlers.add(handler)

        # Parse data
        element = etree.Element('Data')

        for name, datum in self.data.items():
            for handler in handlers:
                if handler.can_convert(datum):
                    subelement = handler.convert(datum)
                    subelement.set('Name', name)
                    element.append(subelement)
                    break

        root.append(element)

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
