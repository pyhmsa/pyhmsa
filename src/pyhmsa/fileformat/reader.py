#!/usr/bin/env python
"""
================================================================================
:mod:`reader` -- Read HMSA HyperDimensional Data File
================================================================================

.. module:: reader
   :synopsis: Read HMSA HyperDimensional Data File

.. inheritance-diagram:: pyhmsa.reader

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os
import binascii
import xml.etree.ElementTree as etree
import logging

# Third party modules.
from pkg_resources import iter_entry_points

# Local modules.
from pyhmsa.fileformat.xmlhandler.header import HeaderXMLHandler
from pyhmsa.spec.condition.conditions import Conditions
from pyhmsa.spec.datum.data import Data
from pyhmsa.type.checksum import calculate_checksum

# Globals and constants variables.

class HMSAReader(object):

    VERSION = '1.0'

    def __init__(self, filepath):
        base, ext = os.path.splitext(filepath)
        if ext not in ['.xml', '.hmsa']:
            raise ValueError('File must be either a XML or HMSA')

        self._filepath_xml = base + '.xml'
        if not os.path.exists(self._filepath_xml):
            raise ValueError('XML file is missing')

        self._filepath_hmsa = base + '.hmsa'
        if not os.path.exists(self._filepath_hmsa):
            raise ValueError('HMSA file is missing')

        self._xml_file = None
        self._hmsa_file = None
        self._version = None
        self._uid = None
        self._language = None
        self._header = None
        self._conditions = None
        self._data = None

    def __enter__(self):
        # Open files
        self._xml_file = open(self._filepath_xml, 'rb')
        self._hmsa_file = open(self._filepath_hmsa, 'rb')

        root = etree.ElementTree(file=self._xml_file).getroot()
        self._read_root(root)
        self._read_header(root)
        self._read_conditions(root)
        self._read_data(root)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Close files
        if self._xml_file is not None:
            self._xml_file.close()
            self._xml_file = None
        if self._hmsa_file is not None:
            self._hmsa_file.close()
            self._hmsa_file = None

        return False

    def _read_root(self, root):
        self._version = root.attrib['Version']
        if self._version != self.VERSION:
            raise ValueError('Unknown version. Can only read version %s.' % self.VERSION)
        self._language = root.get('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        self._uid = root.attrib['UID'].encode('ascii')

    def _read_header(self, root):
        handler = HeaderXMLHandler(self.version)
        self._header = handler.parse(root.find('Header'))

    def _read_conditions(self, root):
        # Load handlers
        handlers = set()
        for entry_point in iter_entry_points('pyhmsa.fileformat.xmlhandler.condition'):
            handler = entry_point.load()(self.version)
            handlers.add(handler)

        # Parse conditions
        self._conditions = Conditions()

        for element in root.findall('Conditions/*'):
            key = element.get('ID', 'Inst%i' % len(self._conditions))

            for handler in handlers:
                if handler.can_parse(element):
                    self._conditions[key] = handler.parse(element)
                    break

    def _read_data(self, root):
        # Check UID
        xml_uid = self._uid
        hmsa_uid = binascii.hexlify(self._hmsa_file.read(8))
        if xml_uid.upper() != hmsa_uid.upper():
            raise ValueError('UID in XML (%s) does not match UID in HMSA (%s)' % \
                             (xml_uid, hmsa_uid))
        logging.debug('Check UID: %s == %s', xml_uid, hmsa_uid)

        # Check checksum
        if 'checksum' in self.header:
            xml_checksum = self.header.checksum

            self._hmsa_file.seek(0)
            buffer = self._hmsa_file.read()
            hmsa_checksum = calculate_checksum(xml_checksum.algorithm, buffer)

            if xml_checksum.value.upper() != hmsa_checksum.value.upper():
                raise ValueError('Checksum in XML (%s) does not match checksum in HMSA (%s)' % \
                                 (xml_checksum.value, hmsa_checksum.value))
            logging.debug('Check sum: %s == %s', xml_checksum.value, hmsa_checksum.value)

        # Load handlers
        handlers = set()
        for entry_point in iter_entry_points('pyhmsa.fileformat.xmlhandler.datum'):
            handler = entry_point.load()(self.version, self._hmsa_file, self.conditions)
            handlers.add(handler)

        # Parse data
        self._data = Data()

        for element in root.findall('Data/*'):
            key = element.get('Name', 'Inst%i' % len(self._data))

            for handler in handlers:
                if handler.can_parse(element):
                    self._data[key] = handler.parse(element)
                    break

    @property
    def header(self):
        if self._header is None:
            raise RuntimeError('Read first')
        return self._header

    @property
    def conditions(self):
        if self._conditions is None:
            raise RuntimeError('Read first')
        return self._conditions

    @property
    def data(self):
        if self._data is None:
            raise RuntimeError('Read first')
        return self._data

    @property
    def version(self):
        if self._version is None:
            raise RuntimeError('Read first')
        return self._version

    @property
    def language(self):
        if self._language is None:
            raise RuntimeError('Read first')
        return self._language

    @property
    def uid(self):
        if self._uid is None:
            raise RuntimeError('Read first')
        return self._uid
