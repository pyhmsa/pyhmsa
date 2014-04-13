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
import threading
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

# Globals and constants variables.

def _extract_filepath(filepath):
    base, ext = os.path.splitext(filepath)
    if ext not in ['.xml', '.hmsa']:
        raise IOError('File must be either a XML or HMSA')

    filepath_xml = base + '.xml'
    filepath_hmsa = base + '.hmsa'

    return filepath_xml, filepath_hmsa

class DataFileReader(object):

    def __init__(self):
        """
        Reads an existing MSA hyper dimensional data file.

        :arg filepath: either the location of the XML or HMSA file.
            Note that both have to be present.
        """
        self._datafile = None
        self._status = ''
        self._progress = 0.0
        self._exception = None
        self._cancel_event = threading.Event()
        self._thread = threading.Thread()

    def read(self, filepath):
        if self._thread.is_alive():
            raise RuntimeError('Already running')

        filepath_xml, filepath_hmsa = _extract_filepath(filepath)
        if not os.path.exists(filepath_xml):
            raise IOError('XML file is missing')
        if not os.path.exists(filepath_hmsa):
            raise IOError('HMSA file is missing')

        self._datafile = None
        self._status = ''
        self._progress = 0.0
        self._exception = None
        self._cancel_event.clear()
        self._thread = threading.Thread(target=self._run, args=(filepath,))
        self._thread.start()

    def _run(self, filepath):
        self._status = 'Running'
        self._progress = 0.0
        if self._cancel_event.is_set(): return

        try:
            filepath_xml, filepath_hmsa = _extract_filepath(filepath)
            xml_file = open(filepath_xml, 'rb')
            hmsa_file = open(filepath_hmsa, 'rb')

            # Read XML
            root = etree.ElementTree(file=xml_file).getroot()

            # Create object
            self._status = 'Creating data file'
            self._progress = 0.1
            if self._cancel_event.is_set(): return
            datafile = DataFile(filepath, root.attrib['Version'])

            # Read
            self._status = 'Reading XML'
            self._progress = 0.13
            if self._cancel_event.is_set(): return
            self._read_root(datafile, root)

            self._status = 'Reading header'
            self._progress = 0.16
            if self._cancel_event.is_set(): return
            self._read_header(datafile, root)

            self._status = 'Reading conditions'
            self._progress = 0.2
            if self._cancel_event.is_set(): return
            self._read_conditions(datafile, root)

            self._status = 'Reading data'
            self._progress = 0.6
            if self._cancel_event.is_set(): return
            self._read_data(datafile, root, hmsa_file)
        except Exception as ex:
            self._progress = 1.0
            self._status = 'Error'
            self._cancel_event.set()
            self._exception = ex
            return
        finally:
            xml_file.close()
            hmsa_file.close()

        # Close files
        self._status = 'Completed'
        self._progress = 1.0
        self._datafile = datafile

    def _read_root(self, obj, root):
        obj.language = root.get('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')

    def _read_header(self, obj, root):
        handler = HeaderXMLHandler(obj.version)
        obj.header.update(handler.parse(root.find('Header')))

    def _read_conditions(self, obj, root):
        # Load handlers
        handlers = set()
        for entry_point in iter_entry_points('pyhmsa.fileformat.xmlhandler.condition'):
            handler = entry_point.load()(obj.version)
            handlers.add(handler)

        # Parse conditions
        elements = root.findall('Conditions/*')
        count = len(elements)
        for i, element in enumerate(elements):
            key = element.get('ID', 'Inst%i' % len(obj.conditions))

            self._status = 'Reading condition %s' % key
            self._progress = 0.2 + i / count * 0.4
            if self._cancel_event.is_set(): return

            for handler in handlers:
                if handler.can_parse(element):
                    obj.conditions[key] = handler.parse(element)
                    break

    def _read_data(self, obj, root, hmsa_file):
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
        elements = root.findall('Data/*')
        count = len(elements)
        for i, element in enumerate(elements):
            key = element.get('Name', 'Inst%i' % len(obj.data))

            self._status = 'Reading datum %s' % key
            self._progress = 0.6 + i / count * 0.4
            if self._cancel_event.is_set(): return

            for handler in handlers:
                if handler.can_parse(element):
                    obj.data[key] = handler.parse(element)
                    break

    def cancel(self):
        self._cancel_event.set()
        self._progress = 1.0
        self._status = 'Cancelled'

    def get(self):
        self._thread.join()

        if self._exception is not None:
            raise self._exception

        if self._datafile is None:
            raise RuntimeError('Data file was not read')

        return self._datafile

    def is_alive(self):
        if self._exception is not None:
            raise self._exception
        return self._thread.is_alive()

    @property
    def progress(self):
        return self._progress

    @property
    def status(self):
        return self._status

class DataFileWriter(object):

    def __init__(self):
        """
        Writes this data file to disk.

        :arg filepath: either the location of the XML or HMSA file
        """
        self._status = ''
        self._progress = 0.0
        self._exception = None
        self._cancel_event = threading.Event()
        self._thread = threading.Thread()

    def write(self, datafile, filepath=None):
        if self._thread.is_alive():
            raise RuntimeError('Already running')

        if filepath is None:
            filepath = datafile.filepath

        self._status = ''
        self._progress = 0.0
        self._exception = None
        self._cancel_event.clear()
        self._thread = threading.Thread(target=self._run,
                                        args=(datafile, filepath))
        self._thread.start()

    def _run(self, datafile, filepath):
        self._status = 'Running'
        self._progress = 0.0
        if self._cancel_event.is_set(): return

        try:
            filepath_xml, filepath_hmsa = _extract_filepath(filepath)

            xml_file = open(filepath_xml, 'wb')
            hmsa_file = open(filepath_hmsa, 'wb')

            # Generate UID
            self._status = 'Generating UID'
            self._progress = 0.025
            if self._cancel_event.is_set(): return
            uid = generate_uid()
            hmsa_file.write(uid)

            # Create XML
            self._status = 'Writing XML'
            self._progress = 0.05
            if self._cancel_event.is_set(): return
            root = etree.Element('MSAHyperDimensionalDataFile')
            self._write_root(datafile, root, uid)

            self._status = 'Writing header'
            self._progress = 0.075
            if self._cancel_event.is_set(): return
            self._write_header(datafile, root)

            self._status = 'Writing conditions'
            self._progress = 0.1
            if self._cancel_event.is_set(): return
            self._write_conditions(datafile, root)

            self._status = 'Writing data'
            self._progress = 0.5
            if self._cancel_event.is_set(): return
            self._write_data(datafile, root, hmsa_file)

            # Close HMSA file
            hmsa_file.close()

            # Calculate and add checksum
            self._status = 'Calculating checksum'
            self._progress = 0.93
            if self._cancel_event.is_set(): return
            with open(filepath_hmsa, 'rb') as fp:
                checksum = calculate_checksum_sha1(fp.read())

            element = root.find('Header')
            subelement = etree.Element('Checksum')
            subelement.text = checksum.value
            subelement.set('Algorithm', checksum.algorithm)
            element.append(subelement)

            # Write XML file
            self._status = 'Writing XML'
            self._progress = 0.96
            if self._cancel_event.is_set(): return

            output = etree.tostring(root, encoding='UTF-8')
            document = minidom.parseString(output)
            output = document.toprettyxml(encoding='UTF-8')

            # Fix add stand-alone manually
            output = output.replace(b'<?xml version="1.0" encoding="UTF-8"?>',
                                    b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')

            xml_file.write(output)

            # Close XML file
            xml_file.close()
        except Exception as ex:
            self._progress = 1.0
            self._status = 'Error'
            self._cancel_event.set()
            self._exception = ex
            return
        finally:
            hmsa_file.close()
            xml_file.close()

        self._status = 'Completed'
        self._progress = 1.0

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

            self._status = 'Writing condition %s' % identifier
            self._progress = 0.1 + i / count * 0.4
            if self._cancel_event.is_set(): return

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

            self._status = 'Writing datum %s' % identifier
            self._progress = 0.5 + i / count * 0.4
            if self._cancel_event.is_set(): return

            for handler in handlers:
                if handler.can_convert(datum):
                    subelement = handler.convert(datum)
                    subelement.set('Name', identifier)
                    element.append(subelement)
                    break

        root.append(element)

    def wait(self):
        if self._exception is not None:
            raise self._exception
        self._thread.join()

    def cancel(self):
        self._cancel_event.set()
        self._progress = 1.0
        self._status = 'Cancelled'

    def is_alive(self):
        if self._exception is not None:
            raise self._exception
        return self._thread.is_alive()

    @property
    def progress(self):
        return self._progress

    @property
    def status(self):
        return self._status
