#!/usr/bin/env python

from pyhmsa.datafile import DataFile
datafile = DataFile()

# Header
datafile.header.title = 'Example'
datafile.header['title'] = 'Example'

import datetime
datafile.header.datetime = datetime.datetime.now()

# Condition
## Create a position
from pyhmsa.spec.condition.specimenposition import SpecimenPosition
position = SpecimenPosition(x=0.0, y=1.0, z=2.0)

## Create an acquisition condition
from pyhmsa.spec.condition.acquisition import AcquisitionPoint
acq = AcquisitionPoint(position=position)
acq.set_dwell_time(5.0, 's')
acq.dwell_time = (5.0, 's')
acq.dwell_time = 5.0

print(acq.dwell_time) # Returns: 5.0 s
print(acq.get_dwell_time()) # Returns: 5.0 s
print(acq.dwell_time.unit) # Returns: s

## Add condition to datafile with the ID = Acq0
datafile.conditions['Acq0'] = acq

# Dataset
## Create a dataset (NumPy array) of 1000 64-bit integers
import numpy as np
from pyhmsa.spec.datum.analysis import Analysis1D
channels = 1000
datum = Analysis1D(channels, np.int64)

## Assign values to the array by generating a random integer between 0 and 5000
import random
datum[:] = [random.randint(0, 5000) for _ in range(channels)]

## Add dataset to datafile with the ID = Spectrum0
datafile.data['Spectrum0'] = datum

# Save datafile to a file
## Only one of the two files need to be specified, either .xml or .hmsa
datafile.write('example1.xml')
datafile.write() # Save to the same location
