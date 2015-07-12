"""
Common constants and functions for EMSA.
"""

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

EMSA_ELS_DETECTOR_SERIAL = "SERIAL" # Serial ELS Detector
EMSA_ELS_DETECTOR_PARALL = "PARALL" # Parallel ELS Detector

EMSA_EDS_DETECTOR_SIBEW = 'SIBEW' # Si(Li) with Be Window
EMSA_EDS_DETECTOR_SIUTW = 'SIUTW' # Si(Li) with Ultra Thin Window
EMSA_EDS_DETECTOR_SIWLS = 'SIWLS' # Si(Li) Windowless
EMSA_EDS_DETECTOR_GEBEW = 'GEBEW' # Ge with Be Window
EMSA_EDS_DETECTOR_GEUTW = 'GEUTW' # Ge with Ultra Thin Window
EMSA_EDS_DETECTOR_GEWLS = 'GEWLS' # Ge Windowless
EMSA_EDS_DETECTOR_SDBEW = 'SDBEW' # SDD with Be Window (from DTSA-II)
EMSA_EDS_DETECTOR_SDUTW = 'SDUTW' # SDD with Ultra Thin Window (from DTSA-II)
EMSA_EDS_DETECTOR_SDWLS = 'SDWLS' # SDD Windowless (from DTSA-II)
EMSA_EDS_DETECTOR_UCALUTW = 'UCALUTW' # Micro-calorimeter with Ultra Thin Window (from DTSA-II)

def calculate_checksum(lines):
    checksum = 0

    for line in lines:
        if line.startswith('#CHECKSUM'):
            continue
        for character in line:
            checksum += ord(character)

    return checksum
