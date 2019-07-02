__author__ = 'Oliver Lindemann <oliver@expyriment.org>, ' \
             'Florian Krause <florian@expyriment.org>'

__version__ = '0.3'

from sys import version_info as _vi
if _vi.major< 3:
    raise RuntimeError("Dataintegretyfinger requires Python 3 or larger.")

from .hashing import CRYPTOGRAPHIC_ALGORITHMS, NON_CRYPTOGRAPHIC_ALGORITHMS, \
                    new_hash_instance
from .dif import DataIntegrityFingerprint
