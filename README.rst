pyHMSA
======

.. image:: https://badge.fury.io/py/pyhmsa.svg
   :target: http://badge.fury.io/py/pyhmsa

.. image:: https://drone.io/bitbucket.org/microanalysis/pyhmsa/status.png
   :target: https://drone.io/bitbucket.org/microanalysis/pyhmsa

.. image:: https://readthedocs.org/projects/pyhmsa/badge/?version=latest
   :target: https://readthedocs.org/projects/pyhmsa/

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

The library is provided under the MIT license.

More information can be found at the website:

http://pyhmsa.readthedocs.org

The most current development version is always available from our
bitbucket repository:

https://bitbucket.org/microanalysis/pyhmsa