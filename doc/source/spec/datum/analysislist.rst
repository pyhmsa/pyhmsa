Analysis list
=============

Dataset used to store a sequence of point measurements collected under the same 
conditions, but in an irregular pattern (line scan, time sequence, sparsely 
scanned image).

Classes
-------

.. autoclass:: pyhmsa.spec.datum.analysislist.AnalysisList0D
   :members: conditions, datum_dimensions, collection_dimensions, toanalysis
   
.. autoclass:: pyhmsa.spec.datum.analysislist.AnalysisList1D
   :members: conditions, datum_dimensions, collection_dimensions, toanalysis, channels
   
.. autoclass:: pyhmsa.spec.datum.analysislist.AnalysisList2D
   :members: conditions, datum_dimensions, collection_dimensions, toanalysis, u, v
