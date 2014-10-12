#!/usr/bin/env python

from pyhmsa.datafile import DataFile
from pyhmsa.type.language import langstr
datafile = DataFile()

author = langstr('Wilhelm Conrad Roentgen', {'de': u'Wilhelm Conrad Röntgen'})
datafile.header.author = author

print(datafile.header.author.alternatives['de']) # Returns ...