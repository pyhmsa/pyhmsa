#!/usr/bin/env python

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2013 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import os
import zipfile
from distutils.cmd import Command

# Third party modules.
from setuptools import setup, find_packages

# Local modules.

# Globals and constants variables.

class TestDataCommand(Command):

    description = "create a zip of all files in the testData folder"
    user_options = [('dist-dir=', 'd',
                     "directory to put final built distributions in "
                     "[default: dist]"), ]

    def initialize_options(self):
        self.dist_dir = None

    def finalize_options(self):
        if self.dist_dir is None:
            self.dist_dir = "dist"

    def run(self):
        if not os.path.exists(self.dist_dir):
            os.makedirs(self.dist_dir)

        basepath = os.path.dirname(__file__)
        testdatapath = os.path.join(basepath, 'src', 'pyhmsa', 'testdata')

        zipfilename = self.distribution.get_fullname() + '-testdata.zip'
        zipfilepath = os.path.join(self.dist_dir, zipfilename)
        with zipfile.ZipFile(zipfilepath, 'w') as z:
            for root, _, files in os.walk(testdatapath):
                for file in files:
                    filename = os.path.join(root, file)
                    arcname = os.path.relpath(filename, basepath)
                    z.write(filename, arcname)

setup(name='pyHMSA',
      version='0.1',
      description='Python implementation of the MSA / MAS / AMAS Hyper-Dimensional Data File specification',
      author='Philippe Pinard',
      author_email='philippe.pinard@gmail.com',
      url='https://bitbucket.org/microanalysis/pyhmsa',
      license='MIT',
      keywords='microscopy microanalysis hmsa file format',

      packages=find_packages('src'),
      package_dir={'':'src'},

      install_requires=['numpy'],
      zip_safe=True,

      tests_require=['nose'],
      test_suite='nose.collector',

      cmdclass={'zip_testdata': TestDataCommand},

      entry_points=\
        {'pyhmsa.fileformat.xmlhandler.condition':
            ['AcquisitionPoint = pyhmsa.fileformat.xmlhandler.condition.acquisition:AcquisitionPointXMLHandler',
             'AcquisitionMultipoint = pyhmsa.fileformat.xmlhandler.condition.acquisition:AcquisitionMultipointXMLHandler',
             'AcquisitionRasterLinescan = pyhmsa.fileformat.xmlhandler.condition.acquisition:AcquisitionRasterLinescanXMLHandler',
             'AcquisitionRasterXY = pyhmsa.fileformat.xmlhandler.condition.acquisition:AcquisitionRasterXYXMLHandler',
             'AcquisitionRasterXYZ = pyhmsa.fileformat.xmlhandler.condition.acquisition:AcquisitionRasterXYZXMLHandler',

             'DetectorCamera = pyhmsa.fileformat.xmlhandler.condition.detector:DetectorCameraXMLHandler',
             'DetectorSpectrometer = pyhmsa.fileformat.xmlhandler.condition.detector:DetectorSpectrometerXMLHandler',
             'DetectorSpectrometerCL = pyhmsa.fileformat.xmlhandler.condition.detector:DetectorSpectrometerCLXMLHandler',
             'DetectorSpectrometerWDS = pyhmsa.fileformat.xmlhandler.condition.detector:DetectorSpectrometerWDSXMLHandler',
             'DetectorSpectrometerXEDS = pyhmsa.fileformat.xmlhandler.condition.detector:DetectorSpectrometerXEDSXMLHandler',

             'ElementID = pyhmsa.fileformat.xmlhandler.condition.elementid:ElementIDXMLHandler',
             'ElementIDXray = pyhmsa.fileformat.xmlhandler.condition.elementid:ElementIDXrayXMLHandler',

             'Instrument = pyhmsa.fileformat.xmlhandler.condition.instrument:InstrumentXMLHandler',

             'ProbeEM = pyhmsa.fileformat.xmlhandler.condition.probe:ProbeEMXMLHandler',
             'ProbeTEM = pyhmsa.fileformat.xmlhandler.condition.probe:ProbeTEMXMLHandler',

             'RegionOfInterest = pyhmsa.fileformat.xmlhandler.condition.region:RegionOfInterestXMLHandler',

             'SpecimenPosition = pyhmsa.fileformat.xmlhandler.condition.specimen:SpecimenPositionXMLHandler',
             'Specimen = pyhmsa.fileformat.xmlhandler.condition.specimen:SpecimenXMLHandler',
             'SpecimenMultilayer = pyhmsa.fileformat.xmlhandler.condition.specimen:SpecimenMultilayerXMLHandler',
             ],
         'pyhmsa.fileformat.xmlhandler.condition.calibration':
            [
             'CalibrationConstant = pyhmsa.fileformat.xmlhandler.condition.calibration:CalibrationConstantXMLHandler',
             'CalibrationLinear = pyhmsa.fileformat.xmlhandler.condition.calibration:CalibrationLinearXMLHandler',
             'CalibrationPolynomial = pyhmsa.fileformat.xmlhandler.condition.calibration:CalibrationPolynomialXMLHandler',
             'CalibrationExplicit = pyhmsa.fileformat.xmlhandler.condition.calibration:CalibrationExplicitXMLHandler',
             ],
         'pyhmsa.fileformat.xmlhandler.datum':
            [
            'Analysis0D = pyhmsa.fileformat.xmlhandler.datum.analysis:Analysis0DXMLHandler',
            'Analysis1D = pyhmsa.fileformat.xmlhandler.datum.analysis:Analysis1DXMLHandler',
            'Analysis2D = pyhmsa.fileformat.xmlhandler.datum.analysis:Analysis2DXMLHandler',

            'AnalysisList0D = pyhmsa.fileformat.xmlhandler.datum.analysislist:AnalysisList0DXMLHandler',
            'AnalysisList1D = pyhmsa.fileformat.xmlhandler.datum.analysislist:AnalysisList1DXMLHandler',
            'AnalysisList2D = pyhmsa.fileformat.xmlhandler.datum.analysislist:AnalysisList2DXMLHandler',

            'ImageRaster2D = pyhmsa.fileformat.xmlhandler.datum.imageraster:ImageRaster2DXMLHandler',
            'ImageRaster2DSpectral = pyhmsa.fileformat.xmlhandler.datum.imageraster:ImageRaster2DSpectralXMLHandler',
            'ImageRaster2DHyperimage = pyhmsa.fileformat.xmlhandler.datum.imageraster:ImageRaster2DHyperimageXMLHandler',
             ]},
     )
