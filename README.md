Data Integrity Fingerprint (DIF)
================================

![GitHub](https://img.shields.io/pypi/l/dataintegrityfingerprint?style=flat)
[![PyPI](https://img.shields.io/pypi/v/dataintegrityfingerprint?style=flat)](https://pypi.org/project/dataintegrityfingerprint/)

**Reference Python implementation**
* GUI and command line tool
* Python library

Data Integrity Fingerprint (DIF) specification: https://github.com/expyriment/DIF

---

*Released under the MIT License*

Oliver Lindemann (oliver@expyriment.org) & Florian Krause (florian@expyriment.org)

---


## Install


```
python -m pip install dataintegrityfingerprint
```

## Usage DIF tools
### GUI

```
python -m dataintegrityfingerprint -G
```

or if installed via pip:

```
dataintegrityfingerprint -G
```


### Command line interface

```
python -m dataintegrityfingerprint
```

or if installed via pip:

```
dataintegrityfingerprint
```

## DIF Python library

```
from dataintegrityfingerprint import DataIntegrityFingerprint
dif = DataIntegrityFingerprint("/home/me/Downloads")
print(dif)
print(dif.checksums)
print(dif.master_hash)
```
