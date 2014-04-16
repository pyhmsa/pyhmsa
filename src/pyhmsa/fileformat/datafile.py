#!/usr/bin/env python
"""
================================================================================
:mod:`datafile` -- Reader and writer of data file
================================================================================

.. module:: datafile
   :synopsis: Reader and writer of data file

.. inheritance-diagram:: pyhmsa.fileformat.datafile

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2014 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os
import logging
import binascii
import xml.etree.ElementTree as etree
import xml.dom.minidom as minidom

# Third party modules.
from pkg_resources import iter_entry_points

# Local modules.
from pyhmsa.datafile import DataFile

from pyhmsa.fileformat.xmlhandler.header import HeaderXMLHandler

from pyhmsa.type.checksum import calculate_checksum, calculate_checksum_sha1
from pyhmsa.type.uid import generate_uid

from pyhmsa.util.monitorable import _Monitorable, _MonitorableThread

# Globals and constants variables.

def _extract_filepath(filepath):
    base, ext = os.path.splitext(filepath)
    if ext not in ['.xml', '.hmsa']:
        raise IOError('File must be either a XML or HMSA')

    filepath_xml = base + '.xml'
    filepath_hmsa = base + '.hmsa'

    return filepath_xml, filepath_hmsa

class _DataFileReaderThread(_MonitorableThread):

    def __init__(self, filepath):
        filepath_xml, filepath_hmsa = _extract_filepath(filepath)
        if not os.path.exists(filepath_xml):
            raise IOError('XML file is missing')
        if not os.path.exists(filepath_hmsa):
            raise IOError('HMSA file is missing')

        _MonitorableThread.__init__(self, args=(filepath,))

    def _run(self, filepath, *args, **kwargs):
        self._update_status(0.0, 'Running')
        if self.is_cancelled(): return

        xml_file = None
        hmsa_file = None
        try:
            filepath_xml, filepath_hmsa = _extract_filepath(filepath)

            xml_file = open(filepath_xml, 'rb')
            hmsa_file = open(filepath_hmsa, 'rb')

            # Read XML
            root = etree.ElementTree(file=xml_file).getroot()

            # Create object
            self._update_status(0.1, 'Creating data file')
            if self.is_cancelled(): return
            datafile = DataFile(filepath, root.attrib['Version'])

            # Read
            self._update_status(0.13, 'Reading XML')
            if self.is_cancelled(): return
            self._read_root(datafile, root)

            self._update_status(0.16, 'Reading header')
            if self.is_cancelled(): return
            self._read_header(datafile, root)

            self._update_status(0.2, 'Reading conditions')
            if self.is_cancelled(): return
            self._read_conditions(datafile, root)

            self._update_status(0.6, 'Reading data')
            if self.is_cancelled(): return
            self._read_data(datafile, root, hmsa_file)
        finally:
            if hmsa_file is not None:
                hmsa_file.close()
            if xml_file is not None:
                xml_file.close()

        self._update_status(1.0, 'Completed')
        return datafile

    def _read_root(self, datafile, root):
        datafile.language = \
            root.get('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')

    def _read_header(self, datafile, root):
        handler = HeaderXMLHandler(datafile.version)
        datafile.header.update(handler.parse(root.find('Header')))

    def _read_conditions(self, datafile, root):
        # Load handlers
        handlers = set()
        for entry_point in iter_entry_points('pyhmsa.fileformat.xmlhandler.condition'):
            handler = entry_point.load()(datafile.version)
            handlers.add(handler)

        # Parse conditions
        elements = root.findall('Conditions/*')
        count = len(elements)
        for i, element in enumerate(elements):
            key = element.get('ID', 'Inst%i' % len(datafile.conditions))

            self._update_status(0.2 + i / count * 0.4,
                                'Reading condition %s' % key)
            if self.is_cancelled(): return

            for handler in handlers:
                if handler.can_parse(element):
                    datafile.conditions[key] = handler.parse(element)
                    break

    def _read_data(self, datafile, root, hmsa_file):
        # Check UID
        xml_uid = root.attrib['UID'].encode('ascii')
        hmsa_uid = binascii.hexlify(hmsa_file.read(8))
        if xml_uid.upper() != hmsa_uid.upper():
            raise ValueError('UID in XML (%s) does not match UID in HMSA (%s)' % \
                             (xml_uid, hmsa_uid))
        logging.debug('Check UID: %s == %s', xml_uid, hmsa_uid)

        # Check checksum
        xml_checksum = getattr(datafile.header, 'checksum', None)
        if xml_checksum is not None:
            xml_checksum = datafile.header.checksum

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
            handler = entry_point.load()(datafile.version, hmsa_file,
                                         datafile.conditions)
            handlers.add(handler)

        # Parse data
        elements = root.findall('Data/*')
        count = len(elements)
        for i, element in enumerate(elements):
            key = element.get('Name', 'Inst%i' % len(datafile.data))

            self._update_status(0.6 + i / count * 0.4, 'Reading datum %s' % key)
            if self.is_cancelled(): return

            for handler in handlers:
                if handler.can_parse(element):
                    datafile.data[key] = handler.parse(element)
                    break

class DataFileReader(_Monitorable):

    def _create_thread(self, filepath, *args, **kwargs):
        return _DataFileReaderThread(filepath)

    def read(self, filepath):
        """
        Reads an existing MSA hyper dimensional data file.

        :arg filepath: either the location of the XML or HMSA file.
            Note that both have to be present.
        """
        self._start(filepath)

class _DataFileWriterThread(_MonitorableThread):

    def __init__(self, datafile, filepath=None):
        if filepath is None:
            filepath = datafile.filepath
        if filepath is None:
            raise ValueError('No filepath given and none defined in datafile')
        _MonitorableThread.__init__(self, args=(datafile, filepath))

    def _run(self, datafile, filepath, *args, **kwargs):
        self._update_status(0.0, 'Running')
        if self.is_cancelled(): return

        xml_file = None
        hmsa_file = None
        try:
            filepath_xml, filepath_hmsa = _extract_filepath(filepath)

            xml_file = open(filepath_xml, 'wb')
            hmsa_file = open(filepath_hmsa, 'wb')

            # Generate UID
            self._update_status(0.025, 'Generating UID')
            if self.is_cancelled(): return
            uid = generate_uid()
            hmsa_file.write(uid)

            # Create XML
            self._update_status(0.05, 'Writing XML')
            if self.is_cancelled(): return
            root = etree.Element('MSAHyperDimensionalDataFile')
            self._write_root(datafile, root, uid)

            self._update_status(0.075, 'Writing header')
            if self.is_cancelled(): return
            self._write_header(datafile, root)

            self._update_status(0.1, 'Writing conditions')
            if self.is_cancelled(): return
            self._write_conditions(datafile, root)

            self._update_status(0.5, 'Writing data')
            if self.is_cancelled(): return
            self._write_data(datafile, root, hmsa_file)

            # Close HMSA file
            hmsa_file.close()

            # Calculate and add checksum
            self._update_status(0.93, 'Calculating checksum')
            if self.is_cancelled(): return
            with open(filepath_hmsa, 'rb') as fp:
                checksum = calculate_checksum_sha1(fp.read())

            element = root.find('Header')
            subelement = etree.Element('Checksum')
            subelement.text = checksum.value
            subelement.set('Algorithm', checksum.algorithm)
            element.append(subelement)

            # Write XML file
            self._update_status(0.96, 'Writing XML to file')
            if self.is_cancelled(): return

            output = etree.tostring(root, encoding='UTF-8')
            document = minidom.parseString(output)
            output = document.toprettyxml(encoding='UTF-8')

            # Fix add stand-alone manually
            output = output.replace(b'<?xml version="1.0" encoding="UTF-8"?>',
                                    b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')

            xml_file.write(output)

            # Close XML file
            xml_file.close()
        finally:
            if hmsa_file is not None:
                hmsa_file.close()
            if xml_file is not None:
                xml_file.close()

        self._update_status(1.0, 'Completed')
        datafile._filepath = filepath

        return datafile

    def _write_root(self, datafile, root, uid):
        root.set('Version', datafile.version)
        root.set('UID', binascii.hexlify(uid).decode('utf-8').upper())
        root.set('{http://www.w3.org/XML/1998/namespace}lang', datafile.language)

    def _write_header(self, datafile, root):
        handler = HeaderXMLHandler(datafile.version)
        element = handler.convert(datafile.header)
        root.append(element)

    def _write_conditions(self, datafile, root):
        # Load handlers
        handlers = set()
        for entry_point in iter_entry_points('pyhmsa.fileformat.xmlhandler.condition'):
            handler = entry_point.load()(datafile.version)
            handlers.add(handler)

        # Convert conditions
        element = etree.Element('Conditions')

        count = len(datafile.conditions)
        for i, item in enumerate(datafile.conditions.items()):
            identifier, condition = item

            self._update_status(0.1 + i / count * 0.4,
                                'Writing condition %s' % identifier)
            if self.is_cancelled(): return

            for handler in handlers:
                if handler.can_convert(condition):
                    subelement = handler.convert(condition)
                    subelement.set('ID', identifier)
                    element.append(subelement)
                    break

        root.append(element)

    def _write_data(self, datafile, root, hmsa_file):
        # Load handlers
        handlers = set()
        for entry_point in iter_entry_points('pyhmsa.fileformat.xmlhandler.datum'):
            handler = entry_point.load()(datafile.version, hmsa_file,
                                         datafile.conditions)
            handlers.add(handler)

        # Parse data
        element = etree.Element('Data')

        count = len(datafile.data)
        for i, item in enumerate(datafile.data.items()):
            identifier, datum = item

            self._update_status(0.5 + i / count * 0.4,
                                'Writing datum %s' % identifier)
            if self.is_cancelled(): return

            for handler in handlers:
                if handler.can_convert(datum):
                    subelement = handler.convert(datum)
                    subelement.set('Name', identifier)
                    element.append(subelement)
                    break

        root.append(element)

class DataFileWriter(_Monitorable):

    def _create_thread(self, datafile, filepath, *args, **kwargs):
        return _DataFileWriterThread(datafile, filepath)

    def write(self, datafile, filepath=None):
        """
        Writes a data file to disk.

        :arg datafile: data file
        :arg filepath: either the location of the XML or HMSA file
        """
        self._start(datafile, filepath)
