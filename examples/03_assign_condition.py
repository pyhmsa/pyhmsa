#!/usr/bin/env python

from pyhmsa.datafile import DataFile
datafile = DataFile()

# Condition
from pyhmsa.spec.condition.specimenposition import SpecimenPosition
from pyhmsa.spec.condition.acquisition import AcquisitionPoint
position = SpecimenPosition(x=0.0, y=1.0, z=2.0)
acq = AcquisitionPoint(position=position)
acq.set_dwell_time(5.0, 's')

# Dataset
import random
import numpy as np
from pyhmsa.spec.datum.analysis import Analysis1D
channels = 1000
datum = Analysis1D(channels, np.int64)
datum[:] = [random.randint(0, 5000) for _ in range(channels)]

# Assign condition
datum.conditions['Acq0'] = acq

# Add dataset
datafile.data['Spectrum'] = datum

# Check
print(list(datafile.conditions)) # Returns: ['Acq0']
assert datafile.conditions['Acq0'] is datafile.data['Spectrum'].conditions['Acq0']

# Removing globally
del datafile.conditions['Acq0']
print(list(datafile.conditions)) # Returns: []
print(list(datafile.data['Spectrum'].conditions)) # Returns: []

# Removing locally
datafile.data['Spectrum'].conditions['Acq0'] = acq # Reset
del datafile.data['Spectrum'].conditions['Acq0']
print(list(datafile.conditions)) # Returns: ['Acq0']
print(list(datafile.data['Spectrum'].conditions)) # Returns: []