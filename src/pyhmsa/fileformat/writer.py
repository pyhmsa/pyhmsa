#!/usr/bin/env python
"""
================================================================================
:mod:`writer` -- Write HMSA HyperDimensional Data File
================================================================================

.. module:: writer
   :synopsis: Write HMSA HyperDimensional Data File

.. inheritance-diagram:: pyhmsa.fileformat.writer

"""

# Standard library modules.
import os
import xml.etree.ElementTree as etree
from xml.dom import minidom
import binascii

# Third party modules.
from pkg_resources import iter_entry_points

# Local modules.
from pyhmsa.spec.header import Header
from pyhmsa.spec.condition.conditions import Conditions
from pyhmsa.spec.datum.data import Data
from pyhmsa.type.uid import generate_uid
from pyhmsa.type.checksum import calculate_checksum_sha1
from pyhmsa.type.language import validate_language_tag
from pyhmsa.fileformat.xmlhandler.header import HeaderXMLHandler

# Globals and constants variables.

class HMSAWriter(object):

    VERSION = '1.0'

    def __init__(self, filepath):
        base, ext = os.path.splitext(filepath)
        if ext not in ['.xml', '.hmsa']:
            raise ValueError('File must be either a XML or HMSA')

        self._filepath_xml = base + '.xml'
        self._filepath_hmsa = base + '.hmsa'

        self._xml_file = None
        self._hmsa_file = None
        self._uid = None
        self._language = 'en-US'
        self._header = Header()
        self._conditions = Conditions()
        self._data = Data()

    def __enter__(self):
        # Open files
        self._xml_file = open(self._filepath_xml, 'wb')
        self._hmsa_file = open(self._filepath_hmsa, 'wb')

        # Generate UID
        self._uid = generate_uid()
        self._hmsa_file.write(self._uid)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._xml_file is not None:
            # Create XML
            root = etree.Element('MSAHyperDimensionalDataFile')
            self._write_root(root)
            self._write_header(root)
            self._write_conditions(root)
            self._write_data(root)

            # Close HMSA file
            if self._hmsa_file is not None:
                self._hmsa_file.close()
                self._hmsa_file = None

            # Calculate and add checksum
            with open(self._filepath_hmsa, 'rb') as fp:
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

            self._xml_file.write(output)

            # Close XML file
            self._xml_file.close()
            self._xml_file = None

        self._uid = None

        return False

    def _write_root(self, root):
        root.set('Version', self.version)
        root.set('UID', binascii.hexlify(self.uid).decode('utf-8').upper())
        root.set('{http://www.w3.org/XML/1998/namespace}lang', self.language)

    def _write_header(self, root):
        handler = HeaderXMLHandler(self.VERSION)
        element = handler.convert(self._header)
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

    def _write_data(self, root):
        # Load handlers
        handlers = set()
        for entry_point in iter_entry_points('pyhmsa.fileformat.xmlhandler.datum'):
            handler = entry_point.load()(self.version, self._hmsa_file, self.conditions)
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
        return self._header

    @property
    def conditions(self):
        return self._conditions

    @property
    def data(self):
        return self._data

    @property
    def version(self):
        return self.VERSION

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language):
        validate_language_tag(language)
        self._language = language

    @property
    def uid(self):
        if self._uid is None:
            raise RuntimeError('Write first')
        return self._uid
