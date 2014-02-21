Detector
========

Conditions describing the type and configuration of a detector used to collect
the data.

Constants
---------

Signal types
^^^^^^^^^^^^

.. data:: pyhmsa.spec.condition.detector.SIGNAL_TYPE_EDS
.. data:: pyhmsa.spec.condition.detector.SIGNAL_TYPE_WDS
.. data:: pyhmsa.spec.condition.detector.SIGNAL_TYPE_ELS
.. data:: pyhmsa.spec.condition.detector.SIGNAL_TYPE_AES
.. data:: pyhmsa.spec.condition.detector.SIGNAL_TYPE_PES
.. data:: pyhmsa.spec.condition.detector.SIGNAL_TYPE_XRF
.. data:: pyhmsa.spec.condition.detector.SIGNAL_TYPE_CLS
.. data:: pyhmsa.spec.condition.detector.SIGNAL_TYPE_GAM
.. data:: pyhmsa.spec.condition.detector.SIGNAL_TYPE_EBSD
.. data:: pyhmsa.spec.condition.detector.SIGNAL_TYPE_BEI
.. data:: pyhmsa.spec.condition.detector.SIGNAL_TYPE_SEI

Collection modes
^^^^^^^^^^^^^^^^

.. data:: pyhmsa.spec.condition.detector.COLLECTION_MODE_PARALLEL
.. data:: pyhmsa.spec.condition.detector.COLLECTION_MODE_SERIAL

PHA modes (WDS signal)
^^^^^^^^^^^^^^^^^^^^^^

.. data:: pyhmsa.spec.condition.detector.PHA_MODE_INTEGRAL
.. data:: pyhmsa.spec.condition.detector.PHA_MODE_DIFFERENTIAL

XEDS technologies (EDS signal)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. data:: pyhmsa.spec.condition.detector.XEDS_TECHNOLOGY_GE
.. data:: pyhmsa.spec.condition.detector.XEDS_TECHNOLOGY_SILI
.. data:: pyhmsa.spec.condition.detector.XEDS_TECHNOLOGY_SDD
.. data:: pyhmsa.spec.condition.detector.XEDS_TECHNOLOGY_UCAL

Helper classes
--------------

Calibration
^^^^^^^^^^^

.. autoclass:: pyhmsa.spec.condition.calibration.CalibrationConstant
   :members:
   :inherited-members:

.. autoclass:: pyhmsa.spec.condition.calibration.CalibrationLinear
   :members:
   :inherited-members:
   
.. autoclass:: pyhmsa.spec.condition.calibration.CalibrationPolynomial
   :members:
   :inherited-members:
   
.. autoclass:: pyhmsa.spec.condition.calibration.CalibrationExplicit
   :members:
   :inherited-members:
   
Window
^^^^^^

.. autoclass:: pyhmsa.spec.condition.detector.WindowLayer
   :members:
   :inherited-members:
   
.. autoclass:: pyhmsa.spec.condition.detector.Window
   :members:
   :inherited-members:
   
PHA
^^^

.. autoclass:: pyhmsa.spec.condition.detector.PulseHeightAnalyser
   :members:
   :inherited-members:

Classes
-------

.. autoclass:: pyhmsa.spec.condition.detector.DetectorCamera
   :members:
   :inherited-members:
   
.. autoclass:: pyhmsa.spec.condition.detector.DetectorSpectrometer
   :members:
   :inherited-members:
   
.. autoclass:: pyhmsa.spec.condition.detector.DetectorSpectrometerCL
   :members:
   :inherited-members:
   
.. autoclass:: pyhmsa.spec.condition.detector.DetectorSpectrometerWDS
   :members:
   :inherited-members:
   
.. autoclass:: pyhmsa.spec.condition.detector.DetectorSpectrometerXEDS
   :members:
   :inherited-members: