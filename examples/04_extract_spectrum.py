#!/usr/bin/env python

from pyhmsa.datafile import DataFile
datafile = DataFile.read('Breccia - EDS sum spectrum.xml')

spectrum = datafile.data['EDS sum spectrum']

# Search
results = datafile.data.findvalues('*spectrum*')
print(len(results)) # Returns: 1

from pyhmsa.spec.datum.analysis import Analysis1D
results = datafile.data.findvalues(Analysis1D)
print(len(results)) # Returns: 1

spectrum = next(iter(results)) # Take first result
xy = spectrum.get_xy()
print(xy[0, 0]) # Returns -237.098251

xlabel, ylabel, xy = spectrum.get_xy(with_labels=True)

# Save
import csv
with open('breccia.csv', 'w') as fp:
    writer = csv.writer(fp) # Create CSV writer
    writer.writerow([xlabel, ylabel]) # Header
    writer.writerows(xy)