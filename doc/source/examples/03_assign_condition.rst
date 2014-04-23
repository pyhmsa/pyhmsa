Assign a condition to a data set
================================

In the first :ref:`example <new_datafile>`, we create an acquisition point
condition, but only added it to the conditions inside the data file object.
Conditions can also be, and in many cases, should be associated directly with
the data set(s) they are representing.
It is often the case that the same condition is shared between several
data sets.
For instance, the condition describing the instrument (:class:`.Instrument`)
is usually applicable to all collected data sets.
So, how to add conditions to data sets?

Let's assume we have a data set named ``datum`` and a condition named ``acq``
(as in the first :ref:`example <new_datafile>`):

.. literalinclude:: /../../examples/03_assign_condition.py
   :language: python
   :lines: 6-19
   
In the current state, the data set nor the condition are added to the data file
object.
Each data set object has a :attr:`conditions <._Datum.conditions>` attribute
that acts exactly as the :attr:`conditions <.DataFile.conditions>` attribute
of the :class:`DataFile` object.
We can then simply add the condition as we did before.

.. literalinclude:: /../../examples/03_assign_condition.py
   :language: python
   :lines: 22
   
Now let's add the datum to the data file object.

.. literalinclude:: /../../examples/03_assign_condition.py
   :language: python
   :lines: 25
   
That's all, but there is some magic that also happened when adding the data set
to the data file object.
If we list the data file's conditions, we will see that our condition, added
to the data set, is also present.

.. literalinclude:: /../../examples/03_assign_condition.py
   :language: python
   :lines: 28
   
The :attr:`conditions <.DataFile.conditions>` attribute of the data file object
contains all conditions of the whole data file object.
We can technically retrieve and modified the same condition from two locations: 
the data file or the data set.

.. literalinclude:: /../../examples/03_assign_condition.py
   :language: python
   :lines: 29
   
Note that the order of the operation is not important. 
The conditions added to a data set will always be added to the overall 
conditions of the data file.

Some precisions must be made regarding removing conditions.
If a condition is removed from the data file, it will **also** be removed from 
all data sets having this condition.

.. literalinclude:: /../../examples/03_assign_condition.py
   :language: python
   :lines: 32-34
   
However, if a condition is removed from a data set, it will **only** be removed
from this data set and not from the data file.

.. literalinclude:: /../../examples/03_assign_condition.py
   :language: python
   :lines: 37-40
   
This behavior may appear counter-intuiative but it is not possible to know
if that condition was added first to a data set or directly to the data file's
conditions.

Full source code
----------------

.. literalinclude:: /../../examples/03_assign_condition.py
   :language: python