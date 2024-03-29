Data Integrity Fingerprint (DIF)
================================
![License](https://img.shields.io/pypi/l/dataintegrityfingerprint?style=flat)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5866698.svg)](https://doi.org/10.5281/zenodo.5866698)
[![PyPI](https://img.shields.io/pypi/v/dataintegrityfingerprint?style=flat)](https://pypi.org/project/dataintegrityfingerprint/) 
[![Automated test suite](https://github.com/expyriment/dataintegrityfingerprint-python/actions/workflows/automated_test_suite.yml/badge.svg)](https://github.com/expyriment/dataintegrityfingerprint-python/actions/workflows/automated_test_suite.yml)

**A reference implementation in Python**

* Command line interface (CLI) application
* Graphical user interface (GUI) application
* Programming library (Python package)

_by [Oliver Lindemann](http://www.cognitive-psychology.eu/lindemann/) & [Florian Krause](https://floriankrause.org)_
 
## Table of contents

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
  * [Command line interface (CLI) application usage](#command-line-interface-cli-application-usage)
  * [Graphical user interface (GUI) application usage](#graphical-user-interface-gui-application-usage)
  * [Programming library (Python package) usage](#programming-library-python-package-usage)
* [Support and contribution](#support-and-contribution)
* [Citation](#citation)

## Introduction

This software calculates the [Data Integrity Fingerprint (DIF)](https://www.expyriment.org/dataintegrityfingerprint/) of multi-file datasets. It can be used via the command line, via a graphical user interface, or as a Python library for embedding in other software. In either case, the user has the choice of calculating the DIF based on a variety of (cryptographic) algorithms using serial (single CPU core) or parallel (multiple CPU cores) computing. In addition, a checksums file with fingerprints of individual files in a dataset can be created. These files can also serve as the basis for calculating the DIF and, in addition, can be compared against a dataset in order to reveal content differences in case a DIF could not be verified.

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

### Command line interface (CLI) application usage

After successful installation, the command line interface is available as `dataintegrityfingerprint`:

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


### Graphical user interface (GUI) application usage

After successful installation, the graphical user interface is available as `dataintegrityfingerprint-gui`:

![image](https://user-images.githubusercontent.com/2971539/143478538-6700a283-01db-4073-8692-2218d5a777c2.png)

* _Button "Browse..."_ - Opens a file browser for selecting a data directory.
  The selected data directory will be shown at the top of the interface.
* _Button "Generate DIF"_ - Generates the DIF for the selected data
  directory. The DIF will be shown at the bottom of the interface. In addition,
  the main area in the middle of the interface will show the checksums
  (fingerprints) of individual files.
* _Button "Copy"_ - Copies the DIF into the clipboard for pasting into other
  applications.
* _Menu item "File --> Open checksums"_ - Opens a checksums file. The DIF of
  that checksums file will be shown at the bottom of the interface. In
  addition, the main area in the middle of the interface will show the
  checksums (fingerprints) of individual files.
* _Menu item "File --> Save checksums"_ - Saves the checksums (fingerprints)
  of individual files to a file.
* _Menu item "File --> Quit"_ - Quits the application.
* _Menu item "Edit --> Diff checksums"_ - Opens a checksums file and shows
  differences of checksums (fingerprints) of individual files to those
  currently shown in the main area in the middle of the interface.
* _Menu item "Options --> Hash algorithm"_ - Selects the cryptographic hash
  algorithm used as basis for DIF calculation.
* _Menu item "Progress updating"_ - Enables/disables progress updating via a
  progress bar.
* _Menu item "Options --> Multi-core processing"_ - Enables/disables parallel
  computing (usage of multiple CPU cores).
  

### Programming library (Python package) usage

After successful installation, the Python package is available as `dataintegrityfingerprint`:

```python3
import dataintegrityfingerprint
```

A DIF can then be created in the following way:

```python3
dif = dataintegrityfingerprint.DataIntegrityFingerprint("/path/to/dataset")
print(dif)  # get the DIF
print(dif.checksums)  # get the list of checksums of individual files
```


### API documentation

The main functionality for usage in other code is made available via the class `DataIntegrityFingerprint`.

---


#### DataIntegrityFingerprint

Create a DataIntegrityFingerprint object.
```
DataIntegrityFingerprint(data,
                         from_checksums_file=False,
                         hash_algorithm='SHA-256',
                         multiprocessing=True,
                         allow_non_cryptographic_algorithms=False)
 
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
```

---

The `DataIntegrityFingerprint` class includes a set of global variables which
affect all instances.

#### CHECKSUM_FILENAME_SEPARATOR = '  '

Global variable.

Default value = `'␣␣'`  (i.e., two U+0020 whitespace characters)

#### CRYPTOGRAPHIC_ALGORITHMS

Global variable.

Default value = `['MD5', 'SHA-1', 'SHA-224', 'SHA-256', 'SHA-384', 'SHA-512',
                  'SHA3-224', 'SHA3-256', 'SHA3-384', 'SHA3-512']`

#### NON_CRYPTOGRAPHIC_ALGORITHMS

Global variable.

Default value = `['ADLER-32', 'CRC-32']`

---

Once initiated, a `DataIntegrityFingerprint` object provides several methods and
attributes.

#### dif_checksums

Calculate differences of checksums to checksums file.
```
diff_checksums(filename)
    
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
```

#### generate

Generate hash list to get Data Integrity Fingerprint.
```
generate(progress=None)
    
    Parameters
    ----------
    progress: function, optional
        a callback function for a progress reporting that takes the
        following parameters:
            count  -- the current count
            total  -- the total count
            status -- a string describing the status
```

#### get_files

Get all files to hash.
```
get_files(self)
   
   Returns
   -------
   files : list
       the list of files to hash
```

#### save_checksums

Save the checksums to a file.
```
save_checksums(filename=None)
   
   Parameters
   ----------
   filename : str, optional
       the name of the file to save checksums to
   
   Returns
   -------
   success : bool
       whether saving was successful
```

---

An initiated `DataIntegrityFingerprint` object also provides a set of
read-only properties.

#### allow_non_cryptographic_algorithms

Read-only property

#### checksums

Read-only property.

#### data

Read-only property.

#### dif

Read-only property.

#### file_count

Read-only property.

#### file_hash_list

Read-only property.

#### hash_algorithm

Read-only property.

#### multiprocessing

Read-only property.


## Support and contribution

For any questions, please use the [discussion](https://github.com/expyriment/dataintegrityfingerprint-python/discussions) section from the code repository. 
If you wish to contribute or report an issue, please use the [issue tracker](https://github.com/expyriment/dataintegrityfingerprint-python/issues) and 
[pull requests](https://github.com/expyriment/dataintegrityfingerprint-python/pulls).

## Citation

To cite this software conceptually, you can use the following general citation/DOI:

>Lindemann, O., & Krause, F. Data Integrity Fingerprint (DIF) - A reference implementation in Python [Computer software]. https://doi.org/10.5281/zenodo.5866698

**To cite a specific version (preferred), please see the corresponding citation/DOI under [releases](https://github.com/expyriment/dataintegrityfingerprint-python/releases)!**
