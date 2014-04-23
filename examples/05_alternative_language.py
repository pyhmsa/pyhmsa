#!/usr/bin/env python

from pyhmsa.datafile import DataFile
from pyhmsa.type.language import langstr
datafile = DataFile()

author = langstr('Fyodor Dostoyevsky', {'ru': u'Фёдор Миха́йлович Достое́вский'})
datafile.header.author = author

print(datafile.header.author.alternatives['ru']) # Returns ...