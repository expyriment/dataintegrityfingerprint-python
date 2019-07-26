"""
Data Integrity Fingerprint

This module is the Python reference implementation of the Data Integrity
Fingerprint (DIF).

"""


__author__ = 'Oliver Lindemann <oliver@expyriment.org>, ' +\
             'Florian Krause <florian@expyriment.org>'


import os
import codecs
import multiprocessing

from .openssl_hash_algorithm import OpenSSLHashAlgorithm
from .zlib_hash_algorithm import ZlibHashAlgorithm
from .ignore_file import IgnoreFile

CHECKSUM_FILENAME_SEPARATOR = "  "


class DataIntegrityFingerprint:
    """A class representing a DataIntegrityFingerprint (DIF).

    Example
    -------
    dif = DataIntegrityFingerprint("~/Downloads")
    print(dif)
    print(dif.checksums)

    """

    CRYPTOGRAPHIC_ALGORITHMS = OpenSSLHashAlgorithm.SUPPORTED_ALGORITHMS
    NON_CRYPTOGRAPHIC_ALGORITHMS = ZlibHashAlgorithm.SUPPORTED_ALGORITHMS
    SEPARATOR = "."

    def __init__(self, data, from_checksums_file=False,
                 hash_algorithm="SHA-256", multiprocessing=True,
                 dif_ignore_file = None,
                 allow_non_cryptographic_algorithms=False):
        """Create a DataIntegrityFingerprint object.

        Parameters
        ----------
        data : str
            the path to the data
        from_checksums_file : bool
            data argument is a checksums file
        hash_algorithm : str
            the hash algorithm (optional, default: sha256)
        multiprocessing : bool
            using multi CPU cores (optional, default: True)
            speeds up creating of checksums for large data files
        allow_non_cryptographic_algorithms : bool
            set True only, if you need non cryptographic algorithms (see
            notes!)

        Note
        ----
        We do not suggest to use non-cryptographic algorithms.
        Non-cryptographic algorithms are, while much faster, not secure (e.g.
        can be tempered with). Only use these algorithms to check for technical
        file damage and in cases security is not of critical concern.

        """

        if not from_checksums_file:
            assert os.path.isdir(data)

        h = new_hash_instance(hash_algorithm,
                              allow_non_cryptographic_algorithms)
        self._hash_algorithm = h.hash_algorithm
        self._data = os.path.abspath(data)
        self._hash_list = []
        self.multiprocessing = multiprocessing
        self.allow_non_cryptographic_algorithms = \
            allow_non_cryptographic_algorithms

        if dif_ignore_file is not None:
            self._difignore = IgnoreFile(dif_ignore_file)
        else:
            self._difignore = None

    def __str__(self):
        return str(self.dif)

    def get_files(self):
        # get all files to be hashed

        rtn = []
        if os.path.isdir(self._data):
            if self._difignore is None:
                # no dif ignore defined
                for dir_, _, files in os.walk(self._data):
                    for filename in files:
                        rtn.append(os.path.join(dir_, filename))
            else:
                rtn = list(self._difignore.walk(self._data))
        return rtn

    @ property
    def hash_algorithm(self):
        return self._hash_algorithm

    @property
    def data(self):
        return self._data

    @property
    def file_hash_list(self):
        if len(self._hash_list) < 1:
            self.generate()
        return self._hash_list

    @property
    def checksums(self):
        rtn = ""
        for h, fl in self.file_hash_list:
            rtn += u"{0}{1}{2}\n".format(h, CHECKSUM_FILENAME_SEPARATOR, fl)
        return rtn

    @property
    def prefix(self):
        return "".join(x for x in self.hash_algorithm.lower() if x.isalnum())

    @property
    def postfix(self):
        if len(self.file_hash_list) < 1:
            return None

        hasher = new_hash_instance(self._hash_algorithm,
                                   self.allow_non_cryptographic_algorithms)
        hasher.update(self.checksums.encode("utf-8"))
        return hasher.checksum

    @property
    def dif(self):
        if self.postfix is not None:
            return self.prefix + self.SEPARATOR + self.postfix

    def _sort_hash_list(self):
        self._hash_list = sorted(self._hash_list, key=lambda x: x[0] + x[1])

    def generate(self, progress=None):
        """Generate the Data Integrity Fingerprint.

        Parameters
        ----------
        progress: function, optional
            a callback function for a progress reporting that takes the
            following parameters:
                count  -- the current count
                total  -- the total count
                status -- a string describing the status

        """

        self._hash_list = []

        if os.path.isfile(self._data):
            # from  checksum file
            with codecs.open(self._data, encoding="utf-8") as f:
                for line in f:
                    h, fl = line.split(CHECKSUM_FILENAME_SEPARATOR, maxsplit=1)
                    self._hash_list.append((h, fl.strip()))
        else:
            files = self.get_files()
            func_args = zip(files, [self._hash_algorithm] * len(files))
            if self.multiprocessing:
                imap = multiprocessing.Pool().imap_unordered
            else:
                imap = map

            for counter, rtn in enumerate(imap(_hash_file_content, func_args)):
                if progress is not None:
                    progress(counter + 1, len(files),
                             "{0}/{1}".format(counter + 1, len(files)))
                fl = os.path.relpath(rtn[1], self.data).replace(os.path.sep, "/")
                self._hash_list.append((rtn[0], fl))

        self._sort_hash_list()

    def save_checksums(self, filename=None):
        """Save the checksums to a file.

        Parameters
        ----------
        filename : str, optional
            the name of the file to save checksums to

        Returns
        -------
        success : bool
            whether saving was successful

        """

        if self.dif is not None:
            if filename is None:
                filename = os.path.split(self.data)[-1] + ".{0}".format(
                    self._hash_algorithm)

            with codecs.open(filename, 'w', "utf-8") as f:
                f.write(self.checksums)

            return True

    def diff_checksums(self, filename):
        """Calculate differences of checksums to checksums file.

        Parameters
        ----------
        filename : str
            the name of the checksums file

        Returns
        -------
        diff : str
            the difference of checksums to the checksums file
            (minus means checksums is missing something from checksums file,
            plus means checksums has something in addition to checksums file)

        """

        checksums = self.checksums.split("\n")
        other = DataIntegrityFingerprint(filename, from_checksums_file=True,
                                         hash_algorithm=self._hash_algorithm)
        checksums_other = other.checksums.split("\n")
        sub = ["- " + x for x in list(set(checksums_other) - set(checksums))]
        add = ["+ " + x for x in list(set(checksums) - set(checksums_other))]

        return "\n".join(["\n".join(sub), "\n".join(add)]).strip()


def new_hash_instance(hash_algorithm,
                      supported_non_cryptographic_algorithms=False):
    """Return a new instance of a hash object (similar to hashlib.new()).

    Each HashAlgorithm object has the methods `update` and the
    properties `hash_algorithm` (according the DIF naming convention),
    `checksum`

    Parameters
    ----------
    hash_algorithm : str
        one of `DataIntegrityFingerprint.CRYPTOGRAPHIC_ALGORITHMS`
        (or `DataIntegrityFingerprint.NON_CRYPTOGRAPHIC_ALGORITHMS`)
    supported_non_cryptographic_algorithms : bool
        if True, also allow hash algorithms from
        `DataIntegrityFingerprint.NON_CRYPTOGRAPHIC_ALGORITHMS`

    Returns
    -------
    hasher : `ZlibHashAlgorithm` or `OpenSSLHashAlgorithm` object

    """

    if supported_non_cryptographic_algorithms:
        try:
            return ZlibHashAlgorithm(hash_algorithm)
        except Exception:
            pass

    try:
        return OpenSSLHashAlgorithm(hash_algorithm)
    except Exception:
        pass

    raise ValueError("{0} is not a supported hash algorithm.".format(
        hash_algorithm))


def _hash_file_content(args):
    # args = (filename, hash_algorithm)
    # helper function for multi threading of file hashing
    hasher = new_hash_instance(hash_algorithm=args[1],
                               supported_non_cryptographic_algorithms=True)
    with open(args[0], 'rb') as f:
        for block in iter(lambda: f.read(64 * 1024), b''):
            hasher.update(block)

    return hasher.checksum, args[0]
