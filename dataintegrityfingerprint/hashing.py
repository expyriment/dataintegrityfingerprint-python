"""
This module provides wrapper for hash functions from different libraries
to have a unique interface for all types of hash algorithm.

Each HashAlgorithm class has the methods 
    update() & update_file() and
the properties 
    digest & digest_size.
    
"""

import hashlib
import zlib

# not support algorithm (so far):  "SHA-512/224", "SHA-512/256"  # TODO Florian, see slash in 'official' SHA name. might be a Problem?

CRYPTOGRAPHIC_ALGORITHMS = sorted(["MD5",
                                   "SHA-1",
                                   "SHA-224",
                                   "SHA-256",
                                   "SHA-384",
                                   "SHA-512",
                                   "SHA3-224",
                                   "SHA3-256",
                                   "SHA3-384",
                                   "SHA3-512"])
NON_CRYPTOGRAPHIC_ALGORITHMS = sorted(["CRC-32", "Adler-32"])

def new_hash_instance(hash_algorithm, allow_non_cryptographic_algorithms=False):
    """return a new instance of an hash object. (similar hashlib.new())

    Each HashAlgorithm object has the methods update & update_file and
    the properties hash_algorithm (according the DIF naming convention),
        checksum & digest_size.

    :param hash_algorithm:
    :param allow_non_cryptographic_algorithms:

    """

    if allow_non_cryptographic_algorithms:
        try:
            return ZlibHashAlgorithm(hash_algorithm)
        except:
            pass

    try:
        return OpenSSLHashAlgorithm(hash_algorithm)
    except:
        pass

    raise ValueError("{0} is a not support hash algorithm.".format(hash_algorithm))


class _HashAlgorithm(object):
    # abstract super class of a hash algorithms

    def update_file(self, filename):

        with open(filename, 'rb') as f:
            for block in iter(lambda: f.read(64 * 1024), b''):
                self.update(block)

    def update(self, data):
        pass


class OpenSSLHashAlgorithm(_HashAlgorithm):

    def __init__(self, hash_algorithm):
        """OpenSSLHashAlgorithm

        DIF algorithm naming convention and hashlib algorithm names are support.

        :param hash_algorithm:
        """

        self.hash_algorithm = hash_algorithm.upper().replace("_", "-")
        hashlib_name = self.hash_algorithm

        # check for deviation names
        deviating_names = [( "SHA-1", "SHA1"),
                              ("SHA-224", "SHA224"),
                              ("SHA-256", "SHA256"),
                              ("SHA-384", "SHA384"),
                              ("SHA-512", "SHA512")]
        for dif_name, lib_name in deviating_names:
            if self.hash_algorithm == dif_name or self.hash_algorithm == lib_name:
                self.hash_algorithm = dif_name
                hashlib_name = lib_name
                break

        if self.hash_algorithm not in CRYPTOGRAPHIC_ALGORITHMS:
            raise ValueError("{0} is a not support hash algorithm.".format(self.hash_algorithm))

        self.hasher = hashlib.new(hashlib_name)


    def update(self, data):
        self.hasher.update(data)

    @property
    def checksum(self):
        return self.hasher.hexdigest()

    @property
    def digest_size(self):
        return self.hasher.digest_size


class ZlibHashAlgorithm(_HashAlgorithm):

    digest_size = 8

    def __init__(self, hash_algorithm):
        hash_algorithm = hash_algorithm.upper()
        if hash_algorithm == "CRC-32":
            self._current = 0
            self._hasher = zlib.crc32
            self.hash_algorithm = "CRC-32"
        elif hash_algorithm == "ADLER-32":
            self._current = None
            self._hasher = zlib.adler32
            self.hash_algorithm = "Adler-32"
        else:
            raise ValueError("{0} is a not support hash algorithm.".format(hash_algorithm))
        self.hash_algorithm = hash_algorithm

    def update(self, data):
        try:
            self._current = self._hasher(data, self._current)
        except:
            self._current = self._hasher(data)

    @property
    def chechsum(self):
        return hex(self._current)[2:]
