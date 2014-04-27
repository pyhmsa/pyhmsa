#!/usr/bin/env python
"""
================================================================================
:mod:`uid` -- Generate unique identifier id
================================================================================

.. module:: uid
   :synopsis: Generate unique identifier id

.. inheritance-diagram:: pyhmsa.uid

"""

# Standard library modules.
import hashlib
import time
import uuid
import getpass
import socket
import binascii

try:
    import winreg
except ImportError: # pragma: no cover
    try:
        import _winreg as winreg
    except ImportError:
        winreg = None

# Third party modules.

# Local modules.

# Globals and constants variables.

_REG_KEY = 'SOFTWARE\\HmsaUID'

def generate_uid():
    """
    Generates a unique identifier id.
    The method to generate the id was taken from the C implementation of the
    HMSA lib.
    """
    sha1 = hashlib.sha1()

    # Current date/time
    sha1.update(str(time.time()).encode('ascii'))

    # Tick count
    # Note: GetTickCount() not available in Python
    sha1.update(str(time.clock()).encode('ascii'))

    # Counter from registry (incremented here)
    # Only on Windows
    if winreg: # pragma: no cover
        key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, _REG_KEY,
                                 0, winreg.KEY_READ | winreg.KEY_WRITE)
        with key:
            try:
                lastuid, _ = winreg.QueryValueEx(key, "Counter")
                lastuid += 1
            except:
                lastuid = 0
            winreg.SetValueEx(key, 'Counter', 0, winreg.REG_DWORD, lastuid)

        sha1.update(str(lastuid).encode('ascii'))

    # MAC address
    sha1.update(str(uuid.getnode()).encode('ascii'))

    # User name
    sha1.update(getpass.getuser().encode('ascii'))

    # Computer name
    sha1.update(socket.gethostname().encode('ascii'))

    uid = sha1.hexdigest()
    uid = uid[:16] # Take only the first 16 characters

    return binascii.unhexlify(uid)
