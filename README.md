Data Integrity Fingerprint (Python implementation)
===================================================

*Released under the MIT License*

Oliver Lindemann (oliver@expyriment.org) & Florian Krause (florian@expyriment.org)

Documentation Data Integrity Fingerprint: http://expyriment.github.io/DIF

Python implementation: https://github.com/expyriment/dataintegrityfingerprint-python


Install
-------

```
python -m pip install --index-url https://test.pypi.org/simple/ dataintegrityfingerprint
```


Run DIF GUI
-----------

```
python -m dataintegrityfingerprint.gui
```

or if installed via pip:

```
dataintegrityfingerprint -G
```


DIF Command line interface
--------------------------

```
python -m dataintegrityfingerprint.cli
```

or if installed via pip:

```
dataintegrityfingerprint.cli
```

DIF Python library
-------------------

```
from dataintegrityfingerprint import DataIntegrityFingerprint
dif = DataIntegrityFingerprint("/home/me/Downloads")
print(dif)
print(dif.checksums)
print(dif.master_hash)
```
