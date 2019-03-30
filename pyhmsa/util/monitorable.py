"""
Base class for monitorable classes
"""

# Standard library modules.
import sys
import threading
import logging
logger = logging.getLogger(__name__)

# Third party modules.

# Local modules.

# Globals and constants variables.

class _MonitorableThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None):
        super().__init__(group, target, name, args, kwargs)

        self._progress = 0.0
        self._status = ''
        self._exception = None
        self._cancel_event = threading.Event()
        self._result = None

    def _update_status(self, progress, status):
        logger.debug('In %s: %s (%s%%)', self.name, status, progress * 100.0)
        self._progress = progress
        self._status = status

    def _run(self, *args, **kwargs):
        super().run()

    def start(self):
        self._exception = None
        self._cancel_event.clear()
        self._result = None

        logger.debug('Starting %s' % self.name)
        super().start()

        self._progress = 0.0
        self._status = 'Running'

    def run(self):
        self._update_status(0.0, 'Running')
        if self.is_cancelled(): return

        try:
            result = self._run(*self._args, **self._kwargs)
        except Exception as ex:
            self._update_status(1.0, 'Error')
            self._cancel_event.set()
            if not hasattr(ex, '__traceback__'):
                ex.__traceback__ = sys.exc_info()[2]
            self._exception = ex
            return

        if self.is_cancelled(): return
        self._update_status(1.0, 'Completed')
        self._result = result

    def is_alive(self):
        if self._exception is not None:
            raise self._exception
        return super().is_alive()

    def is_cancelled(self):
        return self._cancel_event.is_set()

    def join(self, timeout=None):
        if self._exception is not None:
            raise self._exception

        super().join(timeout)

        if self._exception is not None:
            raise self._exception

    def cancel(self):
        self._update_status(1.0, 'Cancelled')
        self._cancel_event.set()

    def get(self):
        self.join()

        if self._exception is not None:
            raise self._exception

        if self._result is None:
            raise RuntimeError('No result')

        return self._result

    @property
    def progress(self):
        return self._progress

    @property
    def status(self):
        return self._status

class _Monitorable(object):

    def __init__(self):
        self._thread = _MonitorableThread() # Dummy

    def _create_thread(self, *args, **kwargs):
        raise NotImplementedError

    def _start(self, *args, **kwargs):
        if self._thread.is_alive():
            raise RuntimeError('Current thread running')
        self._thread = self._create_thread(*args, **kwargs)
        self._thread.start()

    def cancel(self, timeout=None):
        self._thread.cancel()
        self._thread.join(timeout)
        self._thread._update_status(1.0, 'Cancelled') # Require in case thread changed status

    def is_alive(self):
        return self._thread.is_alive()

    def join(self, timeout=None):
        return self._thread.join(timeout)

    def get(self):
        return self._thread.get()

    @property
    def progress(self):
        return self._thread.progress

    @property
    def status(self):
        return self._thread.status
