#!/usr/bin/env python

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.

# Third party modules.
from setuptools import setup, find_packages

# Local modules.

# Globals and constants variables.

setup(name='pyHMSA',
      version='0.1',
      description='Python implementation of the MSA / MAS / AMAS Hyper-Dimensional Data File specification',
      author='Philippe Pinard',
      author_email='philippe.pinard@gmail.com',
      url='https://bitbucket.org/microanalysis/pyhmsa',
      license='MIT',
      keywords='microscopy microanalysis hmsa file format',

      packages=find_packages(),

      install_requires=['numpy'],
      zip_safe=True,

      entry_points=\
        {'pyhmsa.io.xmlhandler.condition':
            ['AcquisitionPoint = pyhmsa.io.xmlhandler.condition.acquisition:AcquisitionPointXMLHandler',
             'AcquisitionMultipoint = pyhmsa.io.xmlhandler.condition.acquisition:AcquisitionMultipointXMLHandler',
             'AcquisitionRasterLinescan = pyhmsa.io.xmlhandler.condition.acquisition:AcquisitionRasterLinescanXMLHandler',
             'AcquisitionRasterXY = pyhmsa.io.xmlhandler.condition.acquisition:AcquisitionRasterXYXMLHandler',
             'AcquisitionRasterXYZ = pyhmsa.io.xmlhandler.condition.acquisition:AcquisitionRasterXYZXMLHandler',

             'DetectorCamera = pyhmsa.io.xmlhandler.condition.detector:DetectorCameraXMLHandler',
             'DetectorSpectrometer = pyhmsa.io.xmlhandler.condition.detector:DetectorSpectrometerXMLHandler',
             'DetectorSpectrometerCL = pyhmsa.io.xmlhandler.condition.detector:DetectorSpectrometerCLXMLHandler',
             'DetectorSpectrometerWDS = pyhmsa.io.xmlhandler.condition.detector:DetectorSpectrometerWDSXMLHandler',
             'DetectorSpectrometerXEDS = pyhmsa.io.xmlhandler.condition.detector:DetectorSpectrometerXEDSXMLHandler',

             'ElementID = pyhmsa.io.xmlhandler.condition.elementid:ElementIDXMLHandler',
             'ElementIDXray = pyhmsa.io.xmlhandler.condition.elementid:ElementIDXrayXMLHandler',

             'Instrument = pyhmsa.io.xmlhandler.condition.instrument:InstrumentXMLHandler',

             'ProbeEM = pyhmsa.io.xmlhandler.condition.probe:ProbeEMXMLHandler',
             'ProbeTEM = pyhmsa.io.xmlhandler.condition.probe:ProbeTEMXMLHandler',

             'RegionOfInterest = pyhmsa.io.xmlhandler.condition.region:RegionOfInterestXMLHandler',

             'SpecimenPosition = pyhmsa.io.xmlhandler.condition.specimen:SpecimenPositionXMLHandler',
             'Specimen = pyhmsa.io.xmlhandler.condition.specimen:SpecimenXMLHandler',
             'SpecimenMultilayer = pyhmsa.io.xmlhandler.condition.specimen:SpecimenMultilayerXMLHandler',
             ],
         'pyhmsa.io.xmlhandler.condition.calibration':
            [
             'CalibrationConstant = pyhmsa.io.xmlhandler.condition.calibration:CalibrationConstantXMLHandler',
             'CalibrationLinear = pyhmsa.io.xmlhandler.condition.calibration:CalibrationLinearXMLHandler',
             'CalibrationPolynomial = pyhmsa.io.xmlhandler.condition.calibration:CalibrationPolynomialXMLHandler',
             'CalibrationExplicit = pyhmsa.io.xmlhandler.condition.calibration:CalibrationExplicitXMLHandler',
             ],
         'pyhmsa.io.xmlhandler.datum':
            [
            'Analysis0D = pyhmsa.io.xmlhandler.datum.analysis:Analysis0DXMLHandler',
            'Analysis1D = pyhmsa.io.xmlhandler.datum.analysis:Analysis1DXMLHandler',
            'Analysis2D = pyhmsa.io.xmlhandler.datum.analysis:Analysis2DXMLHandler',

            'AnalysisList0D = pyhmsa.io.xmlhandler.datum.analysislist:AnalysisList0DXMLHandler',
            'AnalysisList1D = pyhmsa.io.xmlhandler.datum.analysislist:AnalysisList1DXMLHandler',
            'AnalysisList2D = pyhmsa.io.xmlhandler.datum.analysislist:AnalysisList2DXMLHandler',

            'ImageRaster2D = pyhmsa.io.xmlhandler.datum.imageraster:ImageRaster2DXMLHandler',
            'ImageRaster2DSpectral = pyhmsa.io.xmlhandler.datum.imageraster:ImageRaster2DSpectralXMLHandler',
            'ImageRaster2DHyperimage = pyhmsa.io.xmlhandler.datum.imageraster:ImageRaster2DHyperimageXMLHandler',
             ]},
     )
