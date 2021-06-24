__author__ = 'Oliver Lindemann <oliver@expyriment.org>, ' \
             'Florian Krause <florian@expyriment.org>'

__version__ = '0.6.1'

from sys import version_info as _vi
if _vi.major< 3:
    raise RuntimeError("Dataintegretyfinger requires Python 3 or larger.")

from .dif import DataIntegrityFingerprint
