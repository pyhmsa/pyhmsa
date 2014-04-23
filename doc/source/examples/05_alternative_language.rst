
.. _alternative_language:

Use alternative language
========================

Although ASCII characters are preferred throughout the HMSA specifications,
it is possible to provide information in Unicode character and alternative
spelling.

In pyHMSA, this is done through a special object type called :class:`.langstr`.
This object behaves exactly like the default Python's :class:`str` type with
the exception that alternative spelling can be provided.
Let's look at an example how to specify an author's name in two different
languages.

First we create a data file object and import the :class:`langstr` type.

.. literalinclude:: /../../examples/05_alternative_language.py
   :language: python
   :lines: 3-5

Then we create a new :class:`.langstr` object for the author's name.
The first argument of :class:`.langstr` is the name in English (i.e. ASCII 
characters).
The second argument is a dictionary where the key is a valid language code 
and/or country code, as specified by ISO 639-1 and ISO 3166, respectively.

.. literalinclude:: /../../examples/05_alternative_language.py
   :language: python
   :lines: 7-8
   
The alternative spellings of a string can be access using the attribute
:attr:`alternatives <.langstr.alternatives>` which returns a dictionary.
Note that once created a :class:`.langstr` object is immutable; it cannot be
modified.

.. literalinclude:: /../../examples/05_alternative_language.py
   :language: python
   :lines: 10
   
Full source code
----------------

.. literalinclude:: /../../examples/05_alternative_language.py
   :language: python
