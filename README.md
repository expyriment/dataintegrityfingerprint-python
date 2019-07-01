Data Integrity Fingerprint (DIF)
================================

*Released under the MIT License*

Oliver Lindemann (oliver@expyriment.org) & Florian Krause (florian@expyriment.org)

General Documentation: http://expyriment.github.io/DIF

Example using DIF package
```
from dataintegrityfingerprint import DataIntegrityFingerprint

dif = DataIntegrityFingerprint("/home/me/Downloads")
print(dif)
print(dif.checksums)
print(dif.master_hash)
```

DIF Command line interface
```
python3 -m dataintegrityfingerprint.cli -h
```


DIF GUI
```
python3 -m dataintegrityfingerprint.gui
```
