Create an Elemental ID x-ray condition
======================================

Specifying the x-ray line in an :class:`.ElementalIDXray` condition is slightly
different than other attributes, so this example shows how to do it.
In microanalysis, there exists two common types of nomenclature for x-ray line:
the one proposed by the IUPAC (e.g. *K-L3*) and the traditional Siegbahn 
notation (*Ka1*).
HMSA specifications does not enforce one notation over the other and encourage
the users to specify the x-ray line in both notations.

In a similar way as for alternative languages (see the example on 
:ref:`alternative_language`), a new type is defined for x-ray lines: 
:class:`.xrayline`.
The type takes two required arguments (the x-ray line and its notation) and
an optional argument for the x-ray line express in the other notation.
For example, we can specify the *Ka1* line as follows:

.. literalinclude:: /../../examples/06_xrayline.py
   :language: python
   :lines: 3-4
   
The alternative value is automatically interpreted to be expressed in the 
IUPAC notation.

This new **line** object can then be used to create a new 
:class:`.ElementalIDXray` condition.

.. literalinclude:: /../../examples/06_xrayline.py
   :language: python
   :lines: 6-8
   
Full source code
----------------

.. literalinclude:: /../../examples/06_xrayline.py
   :language: python

