Data Integrity Fingerprint (DIF)
================================

*Released under the MIT License*

Oliver Lindemann (oliver@expyriment.org) & Florian Krause (florian@expyriment.org)

Project homepage: https://github.com/expyriment/dataintegrityfingerprint-python
General Documentation: http://expyriment.github.io/DIF


Install
-------

```
python3 -m pip install --index-url https://test.pypi.org/simple/ dataintegrityfingerprint
```


Run DIF GUI
-----------

```
python3 -m dataintegrityfingerprint.gui
```

or if installed via pip:

```
dataintegrityfingerprint -G
```


DIF Command line interface
--------------------------

```
python3 -m dataintegrityfingerprint.cli
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
