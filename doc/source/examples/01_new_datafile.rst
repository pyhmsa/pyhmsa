
.. _new_datafile:

Create a new data file
======================

This example shows how to create a new data file object from scratch and 
add one condition and one data set.

Create main object
------------------

First, we import the :class:`.DataFile` class and define a **datafile** object:

.. literalinclude:: /../../examples/01_new_datafile.py
   :language: python
   :lines: 3-4

From the **datafile** object, the header can be modified using the attribute 
:attr:`header <.DataFile.header>`, conditions can be added/modified/removed 
using the :attr:`conditions <.DataFile.conditions>` which acts as a 
Python's dictionary and data sets can be added/modified/removed in the same way 
as conditions using the :attr:`data <.DataFile.data>`.

Header
------

Let's personalize the data file and specify values from some of the default
header fields.
The default header fields are: :attr:`title <.Header.title>`, 
:attr:`author <.Header.author>`, :attr:`owner <.Header.owner>`, 
:attr:`date <.Header.date>`, :attr:`time <.Header.time>`, 
:attr:`timezone <.Header.timezone>` and :attr:`checksum <.Header.checksum>`.
The checksum field is automatically determined when saving a data file.
The default header fields can be set using their respective attributes or using
lowercase keys.
The instance setting the title as follows:

.. literalinclude:: /../../examples/01_new_datafile.py
   :language: python
   :lines: 7

is equivalent to this:

.. literalinclude:: /../../examples/01_new_datafile.py
   :language: python
   :lines: 8

The :attr:`date <.Header.date>` field of the header is stored as a 
:class:`datetime.date` object as specified in Python's standard library.
The same goes for the :attr:`time <.Header.time>`, stored as a 
:class:`datetime.time` object.
For more information on these objects, refer to Python's standard library.
For a new data file, the date and time will often correspond to the current
date and time.
A shortcut to set both is to use Python's :class:`datetime.datetime` object.

.. literalinclude:: /../../examples/01_new_datafile.py
   :language: python
   :lines: 10-11
   
Condition
---------
   
The next step is to create a condition.
For this example, we will create an acquisition point condition 
(:class:`.AcquisitionPoint`).
This condition requires to define a position.
Positions are specified by the :class:`.SpecimenPosition` class.
Note that per the HMSA specification, the specimen position could also be 
a condition on its own.
All arguments of the specimen position are optional.
We will define **x**, **y** and **z**.

.. literalinclude:: /../../examples/01_new_datafile.py
   :language: python
   :lines: 15-16

With this position we can create our acquisition condition object.
The optional arguments (:attr:`dwell_time <.AcquisitionPoint.dwell_time>`,
:attr:`total_time <.AcquisitionPoint.total_time>`,
:attr:`dwell_time_live <.AcquisitionPoint.dwell_time_live>`) can be defined 
later.

.. literalinclude:: /../../examples/01_new_datafile.py
   :language: python
   :lines: 19-20
   
Numerical attributes with a magnitude (i.e. unit) can be defined in three
different ways:

  * Using the set method and specify the unit as the second argument.
        
    .. literalinclude:: /../../examples/01_new_datafile.py
       :language: python
       :lines: 21
  
  * Using directly the attribute and a 2-item tuple where the first item is
    the value and the second the unit.
    
    .. literalinclude:: /../../examples/01_new_datafile.py
       :language: python
       :lines: 22
  
  * Not specifying the unit. The default unit will be used. Refer to the
    documentation to know which unit is assigned by default.
    
    .. literalinclude:: /../../examples/01_new_datafile.py
       :language: python
       :lines: 23
  
Note that regardless how a numerical attribute is set, all get methods will
return a special object called :class:`.arrayunit`. 
The details of this object is not important for the users, except that it
behaves as a regular number (i.e. Python's :class:`float`) and that it has
an extra attribute :attr:`unit <.arrayunit.unit>` to retrieve the unit.
For example,

.. literalinclude:: /../../examples/01_new_datafile.py
   :language: python
   :lines: 25-27
   
Finally, we can add our acquisition point condition to the **datafile** object.
We use the identifier *Acq0*.

.. literalinclude:: /../../examples/01_new_datafile.py
   :language: python
   :lines: 30

Data set
--------

All data set classes are derived from NumPy's arrays.
NumPy is a powerful Python library to handle multi-dimensional arrays.
It also allows to define the type of data (integer, float) and the number of
bytes.
Based on the HMSA specifications the following NumPy data types are allowed:
**uint8**, **int16**, **uint16**, **int32**, **uint32**, **int64**, **float32**
and **float64**.
If you want to perform advanced array manipulation, we refer you to the
NumPy's `documentation <http://docs.scipy.org/doc/numpy/reference/>`_.

For this example, we will create a 1D analysis data set (:class:`.Analysis1D`).
This data set is designed to store a measurement at a single point in space 
or time with one datum dimension.
It has no collection dimensions.
An example of such data set would be an EDS spectrum.

We create the data set with 1000 channels using the **int64** data type.

.. literalinclude:: /../../examples/01_new_datafile.py
   :language: python
   :lines: 34-37
   
At this point, the data set does not contain any values.
No assumption can be made on the initial values. 
For the purpose of this example, we will fill the array using random numbers
generated from 0 to 5000.

.. literalinclude:: /../../examples/01_new_datafile.py
   :language: python
   :lines: 40-41

As for the condition, we add the new data set to the **datafile** object.

.. literalinclude:: /../../examples/01_new_datafile.py
   :language: python
   :lines: 44
   
Saving
------

Now our data file is created, we obviously would like to save it.
The **datafile** object was an easy utility method 
:meth:`write <.DataFile.write>` which allows to save the object to disk.
The method takes one argument, the location (absolute or relative) where to
save the data file.
Note that the extension of the file can either be ``.xml`` or ``.hmsa``.
Both files will automatically be created as per the HMSA specifications.

.. literalinclude:: /../../examples/01_new_datafile.py
   :language: python
   :lines: 48
   
Once a **datafile** object has been saved, it can be saved again to the
same location by just calling :meth:`write` without any 
argument.

.. literalinclude:: /../../examples/01_new_datafile.py
   :language: python
   :lines: 49
   
Full source code
----------------

.. literalinclude:: /../../examples/01_new_datafile.py
   :language: python
