
.. _read_datafile:

Read a data file
================

In this example, we will read one of the example HMSA data files provided
by the authors: Brecci EDS spectrum.
You can download the data file `here <http://www.csiro.au/luminescence/HMSA/examples/Breccia%20-%20EDS%20sum%20spectrum.zip>`_.

We first import the :class:`.DataFile` class.

.. literalinclude:: /../../examples/02_read_datafile.py
   :language: python
   :lines: 3
   
Then assuming that the Breccia EDS spectrum files are in the same folder as
this script, we simply called the class method :meth:`read <.DataFile.read>`.

.. literalinclude:: /../../examples/02_read_datafile.py
   :language: python
   :lines: 4

And that's all!

Advanced
--------

Reading a large data file may take a long time since all the information is
transfered in the memory.
To get a progress report or to prevent blocking operation, the pyHMSA API 
provides an advanced reader :class:`.DataFileReader` which operates 
inside a thread.
It can be used as follows:

.. literalinclude:: /../../examples/02_read_datafile.py
   :language: python
   :lines: 7-17
   
Note that the :meth:`read <.DataFileReader.read>` only initiates the reading
process, but does not any data file.
The method :meth:`get <.DataFileReader.get>` must be called to return the
data file.

Full source code
----------------

.. literalinclude:: /../../examples/02_read_datafile.py
   :language: python