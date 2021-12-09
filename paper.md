---
title: 'Data Integrity Fingerprint (DIF) - Reference Python implementation'
tags:
  - Python
  - Open Data
  - datasets
  - data integrity
  - checksum
  - hash
authors:
  - name: Oliver Lindemann^[corresponding author]
    orcid: 0000-0003-3789-5373
    affiliation: 1
  - name: Florian Krause
    orcid: 0000-0002-2754-3692
    affiliation: "2, 3"
affiliations:
 - name: Department of Psychology, Education and Child Studies, Erasmus University Rotterdam, The Netherlands
   index: 1
 - name: Donders Institute for Brain, Cognition and Behaviour, Radboud University Medical Center, Nijmegen, The Netherlands
   index: 2
 - name: Department of Psychiatry, Maastricht University Medical Center, The Netherlands
   index: 3
date: 06 December 2021
bibliography: paper.bib
---
  

# Summary

We here present the reference implementation of the _Data Integrity
Fingerprint (DIF)_ - a proposal for a human-readable fingerprint of scientific
datasets [@DIF]. The software can be used via the command line, via a graphical
user interface, or as a Python library for embedding in other software. In
either case, the user has the choice of calculating the DIF based on a variety
of (cryptographic) hash algorithms using serial (single CPU core) or parallel
(multiple CPU cores) computing. In addition, a checksums file with fingerprints
of individual files in a dataset can be created. These files can also serve as
the basis for calculating the DIF and, in addition, can be compared against a
dataset in order to reveal content differences in case a DIF could not be
verified.

# Statement of need

In recent years, publicly sharing scientific datasets has become good research
practice [@Wilkinson] and the concept of _Open Data_ has been incorporated
into international policies [@EU]. However, there currently seems to be no good
way to unmistakenly and indefinitely link these datasets to a corresponding
journal publication, without relying on storage providers [e.g. GitHub, Dryad,
Open Science Framework; @Tan] or other services [e.g. Digital Object
Identifier; @Liu] that need to be maintained [@Lin].

The DIF provides a simple solution to this problem wihtout relying on a third
party by extending the concept of file verification to multi-file datasets
(see also \autoref{fig:Fig1}):

* The author of a journal article calculates checksums of all the files in the
  dataset the article relates to
  
* From these checksums the author calculates a single "master checksum" (the
  DIF) that uniquly identifies the entire dataset
  
* The author reports the DIF in the journal article

* A reader of the journal article who obtained a copy of the dataset (from
  either the author or any other source) calculates the DIF of their copy of
  the dataset and compares it to the correct DIF as stated in the article
  
* If the list of checksums of individual files in the original dataset is
  available, the author can furthermore investigate in detail the differences
  between the datasets, in case of a DIF mismatch

![Schematic overview of verifying the integrity of a dataset using the DIF.\label{fig:Fig1}](https://user-images.githubusercontent.com/2971539/143914028-ea2b8570-6db4-4f82-9bec-b1770fda7df8.png)

Notably, previous efforts to solve this problem outside of the scientific
domain suffer from several shortcomings. Their implementations are either not
available cross-platform [i.e. Windows, MacOS, Linux; @DirHash], lack a
command line [@checksum; @Dirtools] or graphical [@checksumdir; @hashdir;
@checksum; @Dirtools; @DirHash; @dirhash-python; @filehash] user interface, or
are not meant to be used as a programming library [@checksum]. The here
presented software offers all of these features.
More importantly, however, previous efforts are incompatible with each other,
due to a lack of a formal specification of how to calculate the fingerprint.
The (to our knowledge) only attempt at defining a standard procedure of how to
calculate a fingerprint of a directory [@dirhash] is specifically designed to
be extendable and requires a user to make decicions on a priori variety of
options, which all affect the calculation (and the result) and hence also need
to be know by anyone wanting to verify the fingerprint. We believe that this
amount of degrees of freedom (and potential error) are not a good fit for a
scientific application, and is at odds with our goal of a simple human-readable
fingerprint that can be printed in a journal article.
The DIF, on the other hand, has only a single degree of freedom, which is the
hash algorithm chosen to base all calculations on. While we recommend to
use SHA-256, having a algorithm-independent DIF is crucial for being able to
adapt to future developments in the domain of cryptography and computer
security.

# Specification

The procedure for calculating the DIF is:

1. Choose a (cryptographic) hash function `Hash` (e.g. SHA-256)

2.  For every file `f` in the (potentially nested) subtree under the dataset root directory,

    * calculate the checksum `c` as the hexadecimal digest (lower case letters) of `Hash(f)` (i.e. the hashed _binary contents_ of the file)

    * get the file path `p` as the UTF-8 encoded relative path in Unix notation (i.e. U+002F slash character as separator) from the dataset root directory to `f`

    * create the string `cp` (i.e the concatenation of `c` and `p`)
    
    * add `cp` to a list `l`
    
3. Sort `l` in ascending Unicode code point order (i.e., byte- wise sorting, NOT based on the Unicode collation algorithm)

4. Create the string `l[0]l[1]...l[n]` (i.e. the concatenation of all elements of `l`)

5. Retrieve the DIF as the hexadecimal digest of `Hash(l[0]l[1]...l[n])`

Optionally, checksums of individual files and their file paths can be saved as a checksums file (lines of `c  p` for each `f).

# References
