About
=====

pyHMSA is a pure Python implementation of the MSA / MAS / AMAS HyperDimensional 
Data File (HMSA, for short) specifications. 
This file format is intended to be a common exchange format for microscopy and 
microanalysis data. 
More information about the file format and its specifications can be found 
`here <http://www.csiro.au/luminescence/HMSA/index.html>`_.

The library is designed to be minimalist, leaving post-processing of the data
to the user's script.
The only dependency of pyHMSA is to `NumPy <http://www.numpy.org>`_, in order
to represent the multi-dimensional data.

pyHMSA is written to support both Python 2 and 3.

The library is provided under the MIT :ref:`license`.

Examples
========

A few examples from the pyHMSA library.

.. toctree::
   :maxdepth: 1
   :glob:
   
   examples/*

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
   
The main object of the library is the :class:`.DataFile` which regroups in a
single object the :ref:`header`, :ref:`conditions` and :ref:`datasets <data>`.
HMSA files can be created, read and written from this object.

.. toctree::
   :maxdepth: 1
   
   datafile.rst

Other classes of the library used to define data types, to read and write 
HMSA files as well as some utilities can be found here:

.. toctree::
   :maxdepth: 2
   
   fileformat.rst
   type.rst
   util.rst

Download
========

The source code of the library can be viewed/forked/downloaded on 
`GitHub <https://github.com/pyhmsa/pyhmsa>`_.

.. toctree::
   :hidden:
   
   license.rst