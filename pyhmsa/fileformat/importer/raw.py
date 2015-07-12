"""
Import from RAW/RPL file format

Based on:
http://www.nist.gov/lispix/doc/image-file-formats/raw-file-format.htm

"""

# Standard library modules.
import os
import logging
logger = logging.getLogger(__name__)

# Third party modules.
import numpy as np

# Local modules.
from pyhmsa.fileformat.importer.importer import _Importer, _ImporterThread
from pyhmsa.datafile import DataFile
from pyhmsa.spec.datum.imageraster import ImageRaster2D, ImageRaster2DSpectral
from pyhmsa.spec.datum.analysislist import AnalysisList2D

# Globals and constants variables.

class _ImporterRAWThread(_ImporterThread):

    def __init__(self, raw_filepath):
        rpl_filepath = os.path.splitext(raw_filepath)[0] + '.rpl'
        _ImporterThread.__init__(self, raw_filepath, rpl_filepath)

    def _run(self, raw_filepath, rpl_filepath, *args, **kwargs):
        # Read RPL
        self._update_status(0.1, 'Reading RPL')

        rpl = {}
        with open(rpl_filepath, 'r') as fp:
            for line in fp:
                line = line.strip()
                if line.startswith(';'): continue

                parts = line.split('\t')
                name = parts[0].strip().lower()
                value = parts[1].strip()

                if name == 'key' and 'key' in rpl: continue # only read once
                rpl[name] = value

        # Read RAW
        ## Find dtype
        self._update_status(0.2, 'Finding dtype')

        if 'data-type' not in rpl:
            raise IOError('Missing "data-type" parameter in rpl file')
        data_type = rpl['data-type']
        logger.debug('Data type: %s', data_type)

        if 'data-length' not in rpl:
            raise IOError('Missing "data-length" parameter in rpl file')
        data_length = int(rpl['data-length'])
        logger.debug('Data length: %i', data_length)

        if data_type == 'float':
            if data_length == 4:
                dtype = np.dtype(np.float32)
            elif data_length == 8:
                dtype = np.dtype(np.float64)
            else:
                raise IOError('Invalid data length: %i' % data_length)
        else:
            if data_length == 1:
                dtype = np.dtype(np.int8 if data_type == 'signed' else np.uint8)
            elif data_length == 2:
                dtype = np.dtype(np.int16 if data_type == 'signed' else np.uint16)
            elif data_length == 4:
                dtype = np.dtype(np.int32 if data_type == 'signed' else np.uint32)
            elif data_length == 8:
                dtype = np.dtype(np.int64 if data_type == 'signed' else np.uint64)
            else:
                raise IOError('Invalid data length: %i' % data_length)

        logger.debug('Numpy dtype: %s', dtype)

        ## Adjust byte order
        self._update_status(0.3, 'Adjust byte order')

        if 'byte-order' not in rpl:
            raise IOError('Missing "byte-order" parameter in rpl file')
        byte_order = rpl['byte-order']
        logger.debug('Byte order: %s' % byte_order)

        if byte_order != 'dont-care':
            dtype = dtype.newbyteorder('>' if byte_order == 'big-endian' else '<')

        ## Find dimensions
        self._update_status(0.4, 'Finding dimensions')

        if 'width' not in rpl:
            raise IOError('Missing "width" parameter in rpl file')
        width = int(rpl['width'])
        logger.debug('Width: %i', width)

        if 'height' not in rpl:
            raise IOError('Missing "height" parameter in rpl file')
        height = int(rpl['height'])
        logger.debug('Height: %i', height)

        if 'depth' not in rpl:
            raise IOError('Missing "depth" parameter in rpl file')
        depth = int(rpl['depth'])
        logger.debug('Depth: %i', depth)

        count = width * height * depth * dtype.itemsize

        ## Extract values
        self._update_status(0.5, 'Extract values')

        offset = int(rpl.get('offset', 0))
        logger.debug('Offset: %i', offset)

        fp = open(raw_filepath, 'rb')
        fp.seek(offset)
        values = np.fromfile(fp, dtype, count)
        fp.close()

        ## Reshape
        self._update_status(0.6, 'Reshape datum')

        if depth == 1:
            datum = ImageRaster2D(width, height, dtype, buffer=values)
        else:
            record_by = rpl['record-by']
            logger.debug('Record by: %s', record_by)

            if record_by == 'vector':
                datum = ImageRaster2DSpectral(width, height, depth, dtype,
                                              buffer=values)
            elif record_by == 'image':
                datum = AnalysisList2D(depth, width, height, dtype,
                                       buffer=values)
            else:
                raise IOError('Unknown "record-by" parameter')

        # Create datafile
        self._update_status(0.7, 'Create datafile')

        datafile = DataFile()

        datafile.header.title = \
            os.path.splitext(os.path.basename(raw_filepath))[0]

        datafile.data.add(rpl.get('key', 'Datum0'), datum)

        return datafile

class ImporterRAW(_Importer):

    SUPPORTED_EXTENSIONS = ('.raw',)

    def _create_thread(self, filepath, *args, **kwargs):
        return _ImporterRAWThread(filepath)

    def validate(self, filepath):
        _Importer.validate(self, filepath)

        rpl_filepath = os.path.splitext(filepath)[0] + '.rpl'
        if not os.path.exists(rpl_filepath):
            raise IOError('Raw parameter list file "%s" is missing' % rpl_filepath)
