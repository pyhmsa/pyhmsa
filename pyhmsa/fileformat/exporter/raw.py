"""
Export to RAW/RPL file format

Based on:
http://www.nist.gov/lispix/doc/image-file-formats/raw-file-format.htm

"""

# Standard library modules.
import os

# Third party modules.

# Local modules.
from pyhmsa.fileformat.exporter.exporter import _Exporter, _ExporterThread
from pyhmsa.spec.datum.analysislist import AnalysisList2D
from pyhmsa.spec.datum.imageraster import ImageRaster2D, ImageRaster2DSpectral

# Globals and constants variables.

class _ExporterRAWThread(_ExporterThread):

    def _run(self, datafile, dirpath, *args, **kwargs):
        basefilename = datafile.header.title or 'Untitled'

        keys = set(datafile.data.findkeys(AnalysisList2D)) | \
            set(datafile.data.findkeys(ImageRaster2D)) | \
            set(datafile.data.findkeys(ImageRaster2DSpectral))
        length = len(keys)
        filepaths = []

        for i, identifier in enumerate(keys):
            datum = datafile.data[identifier]

            self._update_status(i / length, 'Exporting %s' % identifier)

            filename = basefilename + '_' + identifier
            lines = self._create_rpl_lines(identifier, datum)
            rpl_filepath = os.path.join(dirpath, filename + '.rpl')
            with open(rpl_filepath, 'w') as fp:
                fp.write('\n'.join(lines))

            raw_filepath = os.path.join(dirpath, filename + '.raw')
            with open(raw_filepath, 'wb') as fp:
                datum = datum.copy()
                datum.dtype.newbyteorder('<')
                fp.write(datum.tobytes())

            filepaths.append(raw_filepath)

        return filepaths

    def _create_rpl_lines(self, identifier, datum):
        lines = []
        lines.append('key\t%s' % identifier)
        lines.append('offset\t0')

        if isinstance(datum, ImageRaster2D):
            width, height = datum.shape
            depth = 1
            record_by = 'dont-care'
        elif isinstance(datum, ImageRaster2DSpectral):
            width, height, depth = datum.shape
            record_by = 'vector'
        elif isinstance(datum, AnalysisList2D):
            depth, width, height = datum.shape
            record_by = 'image'
        else:
            raise IOError('Unkmown datum type')
        lines.append('width\t%i' % width)
        lines.append('height\t%i' % height)
        lines.append('depth\t%i' % depth)
        lines.append('record-by\t%s' % record_by)

        dtype = datum.dtype
        lines.append('data-length\t%i' % dtype.itemsize)

        byteorder = 'little-endian' if dtype.itemsize > 1 else 'dont-care'
        lines.append('byte-order\t%s' % byteorder)

        if dtype.kind == 'f':
            data_type = 'float'
        elif dtype.kind == 'u':
            data_type = 'unsigned'
        else:
            data_type = 'signed'
        lines.append('data-type\t%s' % data_type)

        return lines

class ExporterRAW(_Exporter):

    def _create_thread(self, datafile, dirpath, *args, **kwargs):
        return _ExporterRAWThread(datafile, dirpath)

    def validate(self, datafile):
        _Exporter.validate(self, datafile)

        identifiers = set(datafile.data.findkeys(AnalysisList2D)) | \
            set(datafile.data.findkeys(ImageRaster2D)) | \
            set(datafile.data.findkeys(ImageRaster2DSpectral))
        if not identifiers:
            raise ValueError('Datafile must contain at least one ' + \
                             'AnalysisList2D, ImageRaster2D or ' + \
                             'ImageRaster2DSpectral datum')

