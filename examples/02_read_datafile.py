#!/usr/bin/env python

from pyhmsa.datafile import DataFile
datafile = DataFile.read('Breccia - EDS sum spectrum.xml')

# Advanced
import time
from pyhmsa.fileformat.datafile import DataFileReader

reader = DataFileReader()
reader.read('Breccia - EDS sum spectrum.xml')

while reader.is_alive():
    print('{0:n}% - {1}'.format(reader.progress * 100.0, reader.status))
    time.sleep(0.1)
print('{0:n}% - {1}'.format(reader.progress * 100.0, reader.status))

datafile = reader.get()