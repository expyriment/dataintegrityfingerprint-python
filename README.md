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
dataintegrityfingerprint
```
with the following options
```
usage: cli.py [-h] [-f] [-i DIFIGNOREFILE] [-a ALGORITHM] [-C] [-D] [-G] [-L]
              [-s] [-d CHECKSUMSFILE] [-n] [-p] [--non-crypthographic]
              [PATH]

Create a Data Integrity Fingerprint (DIF). v0.5.1

positional arguments:
  PATH                  the path to the data folder or file

optional arguments:
  -h, --help            show this help message and exit
  -f, --from-checksums-file
                        Calculate dif from checksums file. PATH is a checksums
                        file
  -i DIFIGNOREFILE, --dif-ignore-file DIFIGNOREFILE
                        'dif ignore file' specifies the to-be-ignored files
                        and folders. Otherwise the file `.difignore` in the
                        base data folder will be used, if it exists
  -a ALGORITHM, --algorithm ALGORITHM
                        the hash algorithm to be used (default=sha256)
  -C, --checksums       print checksums only
  -D, --dif-only        print dif only
  -G, --gui             open graphical user interface
  -L, --list-available-algorithms
                        print available algorithms
  -s, --save-checksums-file
                        save checksums to file
  -d CHECKSUMSFILE, --diff-checksums-file CHECKSUMSFILE
                        Calculate differences of checksums file to
                        CHECKSUMSFILE
  -n, --no-multi-processing
                        switch of multi processing
  -p, --progress        show progressbar
  --non-crypthographic  allow non crypthographic algorithms (Not suggested,
                        please read documentation carefully!)
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
