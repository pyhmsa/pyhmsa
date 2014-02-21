About
=====

pyHMSA is a pure Python implementation of the MSA / MAS / AMAS HyperDimensional 
Data File (HMSA, for short) specifications. 
This file format is intended to be a common exchange format for microscopy and 
microanalysis data. 
More information about the file format and its specifications can be found 
`here <http://www.csiro.au/luminescence/HMSA/index.html>`_.

API
===

The API follows closely the name convention, hierarchy and parameter names of
the HMSA specifications. 
The type of conditions and datasets available can be found below.

.. toctree::
   :maxdepth: 2

   spec/header.rst
   spec/condition.rst
   spec/datum.rst

The API also provides reader and writer classes to read and write HMSA files, 
respectively.
Examples on how to use these classes are given in the documentation.

.. toctree::

   fileformat/reader.rst
   fileformat/writer.rst
   

Download
========

The source code of the library can be viewed/forked/downloaded on 
`bitbucket <https://bitbucket.org/microanalysis/pyhmsa>`_.
