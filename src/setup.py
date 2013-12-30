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
        {'pyhmsa.condition': ['AcquisitionPoint = pyhmsa.core.condition.acquisition:AcquisitionPoint',
                              'AcquisitionMultipoint = pyhmsa.core.condition.acquisition:AcquisitionMultipoint',
                              'AcquisitionRasterLinescan = pyhmsa.core.condition.acquisition:AcquisitionRasterLinescan',
                              'AcquisitionRasterXY = pyhmsa.core.condition.acquisition:AcquisitionRasterXY',
                              'AcquisitionRasterXYZ = pyhmsa.core.condition.acquisition:AcquisitionRasterXYZ',

                              'DetectorCamera = pyhmsa.core.condition.detector:DetectorCamera',
                              'DetectorSpectrometer = pyhmsa.core.condition.detector:DetectorSpectrometer',
                              'DetectorSpectrometerCL = pyhmsa.core.condition.detector:DetectorSpectrometerCL',
                              'DetectorSpectrometerWDS = pyhmsa.core.condition.detector:DetectorSpectrometerWDS',
                              'DetectorSpectrometerXEDS = pyhmsa.core.condition.detector:DetectorSpectrometerXEDS',

                              'ElementID = pyhmsa.core.condition.elementid:ElementID',
                              'ElementIDXray = pyhmsa.core.condition.elementid:ElementIDXray',

                              'Instrument = pyhmsa.core.condition.instrument:Instrument',

                              'ProbeEM = pyhmsa.core.condition.probe:ProbeEM',
                              'ProbeTEM = pyhmsa.core.condition.probe:ProbeTEM',

                              'RegionOfInterest = pyhmsa.core.condition.region:RegionOfInterest',

                              'SpecimenPosition = pyhmsa.core.condition.specimen:SpecimenPosition',
                              'Specimen = pyhmsa.core.condition.specimen:Specimen',
                              'SpecimenMultilayer = pyhmsa.core.condition.specimen:SpecimenMultilayer',
                              ],
         'pyhmsa.datum': ['Analysis0D = pyhmsa.core.datum.analysis:Analysis0D',
                          'Analysis1D = pyhmsa.core.datum.analysis:Analysis1D',
                          'Analysis2D = pyhmsa.core.datum.analysis:Analysis2D',

                          'AnalysisList0D = pyhmsa.core.datum.analysislist:AnalysisList0D',
                          'AnalysisList1D = pyhmsa.core.datum.analysislist:AnalysisList1D',
                          'AnalysisList2D = pyhmsa.core.datum.analysislist:AnalysisList2D',

                          'ImageRaster2D = pyhmsa.core.datum.imageraster:ImageRaster2D',
                          'ImageRaster2DSpectral = pyhmsa.core.datum.imageraster:ImageRaster2DSpectral',
                          'ImageRaster2DHyperimage = pyhmsa.core.datum.imageraster:ImageRaster2DHyperimage',
                          ]},
     )
