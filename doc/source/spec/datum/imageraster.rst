Image raster
============

Dataset used to store rastered results over regularly spaced intervals in one 
or more dimensions, such as a 1D linescan, a 2D image or a 3D serial section.

Classes
-------

.. autoclass:: pyhmsa.spec.datum.imageraster.ImageRaster2D
   :members: conditions, datum_dimensions, collection_dimensions, toanalysis
   
.. autoclass:: pyhmsa.spec.datum.imageraster.ImageRaster2DSpectral
   :members: conditions, datum_dimensions, collection_dimensions, toanalysis, channels
   
.. autoclass:: pyhmsa.spec.datum.imageraster.ImageRaster2DHyperimage
   :members: conditions, datum_dimensions, collection_dimensions, toanalysis, u, v
