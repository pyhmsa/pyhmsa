"""
Base class for importers
"""

# Standard library modules.
import os
import sys
import logging
logger = logging.getLogger(__name__)

# Third party modules.
from pkg_resources import iter_entry_points

# Local modules.
from pyhmsa.datafile import DataFile
from pyhmsa.util.monitorable import _Monitorable, _MonitorableThread

# Globals and constants variables.

class _ImporterThread(_MonitorableThread):

    def __init__(self, filepath, *args, **kwargs):
        args = (filepath,) + args
        _MonitorableThread.__init__(self, args=args, kwargs=kwargs)

    def _run(self, filepath, *args, **kwargs):
        raise NotImplementedError

class _Importer(_Monitorable):

    SUPPORTED_EXTENSIONS = ()

    def __init__(self, extra_datafile=None, search_extra=True):
        _Monitorable.__init__(self)

        if extra_datafile is None:
            extra_datafile = DataFile()

        if search_extra:
            logger.debug('Searching for extras')

            for filepath in self._glob_extra_filepaths():
                logger.debug('Found %s' % filepath)
                extra_datafile.update(DataFile.read(filepath))

        self._extra_datafile = extra_datafile

    def _glob_extra_filepaths(self, suffix=''):
        dirpaths = []
        dirpaths.append(os.path.expanduser('~/.pyhmsa'))
        if getattr(sys, "frozen", False):
            dirpaths.append(os.path.dirname(os.path.abspath(sys.executable)))

        filepaths = []
        for dirpath in dirpaths:
            filename = 'importer_extra%s.xml' % suffix
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                filepaths.append(filepath)

        return filepaths

    def _update_extra(self, datafile):
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

    def _create_thread(self, filepath, *args, **kwargs):
        args = (filepath,) + args
        _Monitorable._create_thread(self, *args, **kwargs)

    def validate(self, filepath):
        ext = os.path.splitext(filepath)[1]
        if ext.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError('%s is not a supported extension' % ext)

    def can_import(self, filepath):
        try:
            self.validate(filepath)
        except:
            return False
        else:
            return True

    def import_(self, filepath):
        """
        Should create appropriate importer thread and starts it.
        """
        self.validate(filepath)
        self._start(filepath)

    def get(self):
        datafile = _Monitorable.get(self)
        self._update_extra(datafile)
        return datafile

def find_importers(filepath, extra_datafile=None, search_extra=True, *args, **kwargs):
    # Load importers
    importers = {}
    for entry_point in iter_entry_points('pyhmsa.fileformat.importer'):
        importer_class = entry_point.load(require=False)
        importer = importer_class(extra_datafile=extra_datafile,
                                  search_extra=search_extra,
                                  *args, **kwargs)
        for ext in importer.SUPPORTED_EXTENSIONS:
            importers.setdefault(ext, []).append(importer)

    # Find importers
    ext = os.path.splitext(filepath)[1]
    return list(filter(lambda v: v.can_import(filepath), importers.get(ext, [])))

def import_(filepath, extra_datafile=None, search_extra=True, *args, **kwargs):
    importers = find_importers(filepath, extra_datafile, search_extra, *args, **kwargs)

    if not importers:
        raise ValueError('No possible importer for %s' % filepath)
    if len(importers) > 1:
        raise ValueError('Too many importers for %s' % filepath)

    importer = importers[0]
    importer.import_(filepath)
    return importer.get()

