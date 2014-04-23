Extract a spectrum to a CSV file
================================

We show in this example how to extract a spectrum from a HMSA data file and
save it in a CSV file with Python.
As in the second :ref:`example <read_datafile>`, we use one of the example HMSA 
data files provided by the authors: Brecci EDS spectrum.
You can download the data file `here <http://www.csiro.au/luminescence/HMSA/examples/Breccia%20-%20EDS%20sum%20spectrum.zip>`_.

First, let's read the data file.

.. literalinclude:: /../../examples/04_extract_spectrum.py
   :language: python
   :lines: 3-4
   
Then, we must find the data set corresponding to our spectrum.
In this case, the data set is called *EDS sum spectrum* so we could retrieve
it from its ID.

.. literalinclude:: /../../examples/04_extract_spectrum.py
   :language: python
   :lines: 6
   
However, in some cases, we might not know the name of a data set or an 
only a portion of the name.
The library offers search methods to find both data sets and conditions.

For instance, we could search for all data sets containing the word *spectrum*
as follow:

.. literalinclude:: /../../examples/04_extract_spectrum.py
   :language: python
   :lines: 9-10
   
The **\*** in the search pattern are wild cards and indicates to match any 
character.

We could also search based on the type of data set.
In this case, we are looking for an :class:`.Analysis1D` data set.

.. literalinclude:: /../../examples/04_extract_spectrum.py
   :language: python
   :lines: 12-14
   
Once we have our data set, we can use the utility method 
:meth:`get_xy <.Analysis1D.get_xy>` to retrieve a two-dimensional array where
the first column contains *x* values and the second *y* values.
This method is particularly useful since it will search through the 
associated conditions to the data set to see if a calibration was defined for
the *x* values.
In this example, a linear calibration with an offset of *-237.098251* was 
defined.
The first *x* value should therefore be equal to this value.

.. literalinclude:: /../../examples/04_extract_spectrum.py
   :language: python
   :lines: 16-18

The :meth:`get_xy <.Analysis1D.get_xy>` can also returns labels for the *x*
and *y* values as defined in the conditions.

.. literalinclude:: /../../examples/04_extract_spectrum.py
   :language: python
   :lines: 20
   
Finally, we can use Python's :mod:`csv` module to create the CSV file.

.. literalinclude:: /../../examples/04_extract_spectrum.py
   :language: python
   :lines: 23-27
   
Full source code
----------------

.. literalinclude:: /../../examples/04_extract_spectrum.py
   :language: python
