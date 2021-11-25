Data Integrity Fingerprint (DIF)
================================

![GitHub](https://img.shields.io/pypi/l/dataintegrityfingerprint?style=flat)
[![PyPI](https://img.shields.io/pypi/v/dataintegrityfingerprint?style=flat)](https://pypi.org/project/dataintegrityfingerprint/)
[![Automated test suite](https://github.com/expyriment/dataintegrityfingerprint-python/actions/workflows/automated_test_suite.yml/badge.svg)](https://github.com/expyriment/dataintegrityfingerprint-python/actions/workflows/automated_test_suite.yml)

**Reference Python implementation**
* Application (command line and graphical user interface)
* Programming library

_by [Oliver Lindemann](http://www.cognitive-psychology.eu/lindemann/) & [Florian Krause](https://floriankrause.org)_


## Introduction
This software calculates the [Data Integrity Fingerprint (DIF)](https://github.com/expyriment/DIF) of multi-file datasets. It can be used via the command line, via a graphical user interface, or as a Python library for embedding in other software. In either case, the user has the choice of calculating the DIF based on a variety of (cryptographic) algorithms using serial (single CPU core) or parallel (multiple CPU cores) computing. In addition, a checksums file with fingerprints of individual files in a dataset can be created. These files can also serve as the basis for calculating the DIF and, in addition, can be compared against a dataset in order to reveal content differences in case a DIF could not be verified.

**Note:** We strongly recommend to use SHA-256 or one of the other cryptographic algorithms for calculating the DIF. The non-cryptographic algorithms are significantly faster, but also significantly less secure (i.e. collisions are much more likely, breaking the uniqueness of a DIF, and opening a door for potential manipulation). They might hence only be an option for very large datasets in scenarios where a potential manipulation by a third party is not part of the threat model. The graphical user interface does not allow for selecting non-cryptographic algorithms.

## Installation
The quickest way to use the application is to install it with [pipx](https://pypa.github.io/pipx/):

```
pipx install dataintegrityfingerprint
```

To also make use of the programming library, a classical pip installation is of course also possible:

```
python -m pip install dataintegrityfingerprint
```


## Usage
### Application
After successfull installation, the command line interface is available as `dataintegrityfingerprint`:

```
dataintegrityfingerprint [-h] [-f] [-a ALGORITHM] [-C] [-D] [-G] [-L] [-s]
                         [-d CHECKSUMSFILE] [-n] [-p] [--non-cryptographic]
                         [PATH]
                         
positional arguments:
  PATH                  the path to the data directory

options:
  -h, --help            show this help message and exit
  -f, --from-checksums-file
                        Calculate dif from checksums file. PATH is a checksums
                        file
  -a ALGORITHM, --algorithm ALGORITHM
                        the hash algorithm to be used (default=SHA-256)
  -C, --checksums       print checksums only
  -D, --dif-only        print dif only
  -G, --gui             open graphical user interface
  -L, --list-available-algorithms
                        print available algorithms
  -s, --save-checksums-file
                        save checksums to file
  -d CHECKSUMSFILE, --diff-checksums-file CHECKSUMSFILE
                        Calculate differences of checksums to CHECKSUMSFILE
  -n, --no-multi-processing
                        switch of multi processing
  -p, --progress        show progressbar
  --non-cryptographic   allow non cryptographic algorithms (Not suggested,
                        please read documentation carefully!)

```

Alternatively, the graphical user interface is available as `dataintegrityfingerprint-gui`:

![image](https://user-images.githubusercontent.com/2971539/143326083-99d839a9-e653-4508-a549-edf001faa6f7.png)

* **Button "Browse"** - Opens a file browser for selecting a data directory.
  The selected data directory will be shown at the top of the interface.
* **Button "Generate DIF"** - Generates the DIF for the selected data
  directory. The DIF will be shown at the bottom of the interface. In addition,
  the main area in the middle of the interface will show the checksums
  (fingerprints) of individual files.
* **Button "Copy"** - Copies the DIF into the clipboard for pasting into other
  applications.
* **Menu item "File --> Open checksums"** - Opens a checksums file. The DIF of
  that checksums file will be shown at the bottom of the interface. In
  addition, the main area in the middle of the interface will show the
  checksums (fingerprints) of individual files.
* **Menu item "File --> Save checksums"** - Saves the checksums (fingerprints)
  of individual files to a file.
* **Menu item "File --> Quit"** - Quits the application.
* **Menu item "Edit --> Diff checksums"** - Opens a checksums file and shows
  differences of checksums (fingerprints) of individual files to those
  currently shown in the main area in the middle of the interface.
* **Menu item "Options --> Hash algorithm"** - Selects the cryptographic hash
  algorithm used as basis for DIF calculation.
* **Menu item "Progress updating"** - Enables/disables progress updating via a
  progress bar.
* **Menu item "Options --> Multi-core processing"** - Enables/disables parallel
  computing (usage of multiple CPU cores).
  
  
### Programming library
After successful installation, the Python package is available as `dataintegrityfingerprint`:

```python3
import dataintegrityfingerprint
```

It contains the class `DataIntegrityFingerprint` which can be used to instantiate a DIF object:

```python3
dif = dataintegrityfingerprint.DataIntegrityFingerprint("/home/me/Downloads")
print(dif)
print(dif.checksums)
```

The code is self-documented using docstrings. Use `help(dataintegrityfingerprint.DataIntegrityFingerprint)` for information on what this class can do and how to use it.
