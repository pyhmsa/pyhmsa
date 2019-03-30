#!/usr/bin/env python

# Standard library modules.
import os
import codecs

# Third party modules.
from setuptools import setup, find_packages

# Local modules.
import versioneer

# Globals and constants variables.
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

PACKAGES = find_packages()

CMDCLASS = versioneer.get_cmdclass()

INSTALL_REQUIRES = ['numpy', 'six']
EXTRAS_REQUIRE = {'develop': ['pillow', 'nose', 'coverage']}

ENTRY_POINTS = \
        {'pyhmsa.fileformat.xmlhandler.condition':
            ['AcquisitionPoint = pyhmsa.fileformat.xmlhandler.condition.acquisition:AcquisitionPointXMLHandler',
             'AcquisitionMultipoint = pyhmsa.fileformat.xmlhandler.condition.acquisition:AcquisitionMultipointXMLHandler',
             'AcquisitionRasterLinescan = pyhmsa.fileformat.xmlhandler.condition.acquisition:AcquisitionRasterLinescanXMLHandler',
             'AcquisitionRasterXY = pyhmsa.fileformat.xmlhandler.condition.acquisition:AcquisitionRasterXYXMLHandler',
             'AcquisitionRasterXYZ = pyhmsa.fileformat.xmlhandler.condition.acquisition:AcquisitionRasterXYZXMLHandler',

             'CalibrationConstant = pyhmsa.fileformat.xmlhandler.condition.calibration:CalibrationConstantXMLHandler',
             'CalibrationLinear = pyhmsa.fileformat.xmlhandler.condition.calibration:CalibrationLinearXMLHandler',
             'CalibrationPolynomial = pyhmsa.fileformat.xmlhandler.condition.calibration:CalibrationPolynomialXMLHandler',
             'CalibrationExplicit = pyhmsa.fileformat.xmlhandler.condition.calibration:CalibrationExplicitXMLHandler',

             'DetectorCamera = pyhmsa.fileformat.xmlhandler.condition.detector:DetectorCameraXMLHandler',
             'DetectorSpectrometer = pyhmsa.fileformat.xmlhandler.condition.detector:DetectorSpectrometerXMLHandler',
             'DetectorSpectrometerCL = pyhmsa.fileformat.xmlhandler.condition.detector:DetectorSpectrometerCLXMLHandler',
             'DetectorSpectrometerWDS = pyhmsa.fileformat.xmlhandler.condition.detector:DetectorSpectrometerWDSXMLHandler',
             'DetectorSpectrometerXEDS = pyhmsa.fileformat.xmlhandler.condition.detector:DetectorSpectrometerXEDSXMLHandler',

             'ElementalID = pyhmsa.fileformat.xmlhandler.condition.elementalid:ElementalIDXMLHandler',
             'ElementalIDXray = pyhmsa.fileformat.xmlhandler.condition.elementalid:ElementalIDXrayXMLHandler',

             'Instrument = pyhmsa.fileformat.xmlhandler.condition.instrument:InstrumentXMLHandler',

             'ProbeEM = pyhmsa.fileformat.xmlhandler.condition.probe:ProbeEMXMLHandler',
             'ProbeTEM = pyhmsa.fileformat.xmlhandler.condition.probe:ProbeTEMXMLHandler',

             'RegionOfInterest = pyhmsa.fileformat.xmlhandler.condition.region:RegionOfInterestXMLHandler',

             'SpecimenPosition = pyhmsa.fileformat.xmlhandler.condition.specimenposition:SpecimenPositionXMLHandler',

             'CompositionElemental = pyhmsa.fileformat.xmlhandler.condition.composition:CompositionElementalXMLHandler',

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
             ],
         'pyhmsa.fileformat.importer':
            ['EMSA = pyhmsa.fileformat.importer.emsa:ImporterEMSA',
             'RAW = pyhmsa.fileformat.importer.raw:ImporterRAW'],
         'pyhmsa.fileformat.exporter':
            ['EMSA = pyhmsa.fileformat.exporter.emsa:ExporterEMSA',
             'RAW = pyhmsa.fileformat.exporter.raw:ExporterRAW'],
        }

setup(name='pyHMSA',
      version=versioneer.get_version(),
      description='Python implementation of the MSA / MAS / AMAS Hyper-Dimensional Data File specification',
      long_description=long_description,

      author='Philippe Pinard',
      author_email='philippe.pinard@gmail.com',
      maintainer='Philippe Pinard',
      maintainer_email='philippe.pinard@gmail.com',

      url='http://pyhmsa.readthedocs.org',
      license='MIT',
      keywords='microscopy microanalysis hmsa file format',

      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Physics',
        ],

      packages=PACKAGES,

      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,

      zip_safe=False,

      test_suite='nose.collector',

      cmdclass=CMDCLASS,

      entry_points=ENTRY_POINTS,
     )
