#!/usr/bin/env python

# Standard library modules.
import os
import re
import sys
import glob
import codecs
from distutils.core import Command
from subprocess import check_call

# Third party modules.
from setuptools import setup, find_packages

# Local modules.

# Globals and constants variables.
BASEDIR = os.path.abspath(os.path.dirname(__file__))

def find_version(*file_paths):
    """
    Read the version number from a source file.

    .. note::

       Why read it, and not import?
       see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion
    """
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(BASEDIR, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

class _bdist_fpm(Command):

    description = 'Build using fpm (Effing Package Management)'

    user_options = [('dist-dir=', 'd',
                     "directory to put final built distributions in "
                     "[default: dist]"), ]

    def initialize_options(self):
        self.dist_dir = None

    def finalize_options(self):
        if self.dist_dir is None:
            self.dist_dir = "dist"

    def _run(self, target):
        setup_filepath = os.path.join(BASEDIR, 'setup.py')

        python_bin = 'python3' if sys.version_info.major == 3 else 'python'
        version = '%i.%i' % (sys.version_info.major, sys.version_info.minor)

        args = ['fpm',
                '-s', 'python',
                '-t', target,
                '--force',
                '--verbose',
                '--maintainer', 'Philippe Pinard <philippe.pinard@gmail.com>',
                '--category', 'science',
                '--depends', "%s >= %s" % (python_bin, version),
                '--depends', python_bin + '-numpy',
                '--depends', python_bin + '-six',
                '--no-python-dependencies',
                '--python-bin', python_bin,
                '--name', python_bin + '-hmsa',
                setup_filepath]
        check_call(args)

        self.mkpath(self.dist_dir)
        for srcfilepath in glob.glob('*.%s' % target):
            self.move_file(srcfilepath, self.dist_dir)

class bdist_deb(_bdist_fpm):

    description = 'Build deb '

    def run(self):
        self._run('deb')

# Get the long description from the relevant file
with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

packages = find_packages()

setup(name='pyHMSA',
      version=find_version('pyhmsa', '__init__.py'),
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Physics',
        ],

      packages=packages,
      namespace_packages=packages,

      install_requires=['numpy', 'six'],
      setup_requires=['nose', 'coverage'],
      tests_require=['Pillow'],

      zip_safe=True,

      test_suite='nose.collector',

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
        },

      cmdclass={'bdist_deb': bdist_deb},
     )
