#!/usr/bin/env python

from pyhmsa.type.xrayline import xrayline, NOTATION_SIEGBAHN
line = xrayline('Ka1', NOTATION_SIEGBAHN, 'K-L3')

from pyhmsa.spec.condition.elementalid import ElementalIDXray
condition = ElementalIDXray(29, line, (8047.82, 'eV'))
print(condition) # Returns: <ElementalIDXray(atomic_number=29, energy=8047.82 eV, line=Ka1)>