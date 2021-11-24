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
This software calculates the [Data Integrity Fingerprint (DIF)](https://github.com/expyriment/DIF) of multi-file datasets. It can be used via the command line, via a graphical user interface, or as a Python library for embedding in other software. In either case, the user has the choice of calculating the DIF based on a variety of (cryptographic) algorithms using serial (single CPU) or parallel (multiple CPUs) computing. In addition, a checksums file with fingerprints of individual files in a dataset can be created. These files can also serve as the basis for calculating the DIF and, in addition, can be compared against a dataset in order to reveal content differences in case a DIF could not be verified.

**Note:** We strongly recommend to use SHA-256 or one of the other cryptographic algorithms for calculating the DIF. The non-cryptographic algorithms are significantly faster, but also significantly less secure (i.e. collisions are much more likely, breaking the uniqueness of a DIF, and opening a door for potential manipulation). They might hence only be an option for very large datasets in scenarios where a potential manipulation by a third party is not part of the threat model.

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
To start the command line intercae, run

```
dataintegrityfingerprint
```
Appending `-h` to the command will

To start the graphical user interface, run

```
dataintegrityfingerprint-gui
```

### Programming library
In order to use the Python library, import it in your code with

```python3
import dataintegrityfingerprint
```

The library exposes a class `DataIntegrityFingerprint` which can be used to instanciate a DIF object:

```python3
dif = dataintegrityfingerprint.DataIntegrityFingerprint("/home/me/Downloads")
print(dif)
print(dif.checksums)
```

The code uses docstrings for documentation. Use `help(dataintegrityfingerprint.DataIntegrityFingerprint)` for information on what this class can do and how to use it.
