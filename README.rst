pyHMSA
======

.. image:: https://badge.fury.io/py/pyhmsa.svg
   :target: http://badge.fury.io/py/pyhmsa

.. image:: https://readthedocs.org/projects/pyhmsa/badge/?version=latest
   :target: https://readthedocs.org/projects/pyhmsa/

.. image:: https://travis-ci.org/pyhmsa/pyhmsa.svg?branch=master
   :target: https://travis-ci.org/pyhmsa/pyhmsa
   
.. image:: https://codecov.io/github/pyhmsa/pyhmsa/coverage.svg?branch=master
   :target: https://codecov.io/github/pyhmsa/pyhmsa?branch=master

.. image:: https://zenodo.org/badge/doi/10.5281/zenodo.46773.svg
   :target: http://dx.doi.org/10.5281/zenodo.46773

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

pyHMSA is written to support both Python 3.6+.

The library is provided under the MIT license.

More information can be found at the website:

http://pyhmsa.readthedocs.org

The most current development version is always available from our
GitHub repository:

https://github.com/pyhmsa/pyhmsa

Release notes
=============

0.2
---

- Drop Python 2 support

Contributors
============

* `@nkipi <https://github.com/nkipi>`_
* `@silrichter <https://github.com/silrichter>`_

License
=======

The library is provided under the MIT license.

*pyxray* was partially developed as part of the doctorate thesis project of
Philippe T. Pinard at RWTH Aachen University (Aachen, Germany) under the
supervision of Dr. Silvia Richter.

Copyright (c) 2015-2016/06 Philippe Pinard and Silvia Richter

Copyright (c) 2016/06-2019 Philippe Pinard