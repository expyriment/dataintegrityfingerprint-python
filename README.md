Data Integrity Fingerprint (DIF)
================================

![GitHub](https://img.shields.io/pypi/l/dataintegrityfingerprint?style=flat)
[![PyPI](https://img.shields.io/pypi/v/dataintegrityfingerprint?style=flat)](https://pypi.org/project/dataintegrityfingerprint/)

**Reference Python implementation**
* Application (command line and graphical user interface)
* Programming library

Data Integrity Fingerprint (DIF) specification: https://github.com/expyriment/DIF

---

*Released under the MIT License*

Oliver Lindemann (oliver@expyriment.org) & Florian Krause (florian@expyriment.org)

---


## Install


```
python -m pip install dataintegrityfingerprint
```

## Usage
### Application

```
python -m dataintegrityfingerprint     # Command line interface
python -m dataintegrityfingerprint -G  # Graphical user interface
```

or if installed via pip:

```
dataintegrityfingerprint     # Command line interface
dataintegrityfingerprint -G  # Graphical user interface
```


### Programming library

```python3
from dataintegrityfingerprint import DataIntegrityFingerprint

dif = DataIntegrityFingerprint("/home/me/Downloads")
print(dif)
print(dif.checksums)
print(dif.master_hash)
```
