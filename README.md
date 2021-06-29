Data Integrity Fingerprint (Python implementation)
===================================================

*Released under the MIT License*

Oliver Lindemann (oliver@expyriment.org) & Florian Krause (florian@expyriment.org)

---

Documentation Data Integrity Fingerprint: http://expyriment.github.io/DIF

---


Install
-------

```
python -m pip install dataintegrityfingerprint
```


Run DIF GUI
-----------

```
python -m dataintegrityfingerprint -G
```

or if installed via pip:

```
dataintegrityfingerprint -G
```


DIF Command line interface
--------------------------

```
python -m dataintegrityfingerprint
```

or if installed via pip:

```
dataintegrityfingerprint
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
