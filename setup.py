#!/usr/bin/env python3
"""
Installer
"""

from setuptools import setup
import codecs
import os
from sys import version_info as _vi

package_name = "dataintegrityfingerprint"

install_requires = []

if _vi.major< 1:
    raise RuntimeError("{0} requires Python 3 or larger.".format(package_name))

def readme():
    directory = os.path.dirname(os.path.join(
        os.getcwd(), __file__, ))
    with codecs.open(
        os.path.join(directory, "README.md"),
        encoding="utf8",
        mode="r",
        errors="replace",
        ) as file:
        return file.read()

def get_version(package):
    """Get version number"""

    with open(os.path.join(package, "__init__.py")) as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("'")[1]
    return "None"


if __name__ == '__main__':
    print(readme())
    setup(
        name = package_name,
        version=get_version(package_name),
        description='Create a Data Integrity Fingerprint',
        author='Florian Krause, Oliver Lindemann',
        author_email='oliver@expyriment.org, florian@expyriment.org',
        license='MIT Licence',
        url='http://expyriment.github.io/DIF',
        packages=[package_name],
        include_package_data=True,
        setup_requires=[],
        install_requires=install_requires,
        entry_points={
            'console_scripts': ['dataintegrityfingerprint={0}.cli:run'.format(package_name)],
            },
        keywords = "", #ToDo
        classifiers=[ #ToDO
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Topic :: Scientific/Engineering"
        ],
        long_description=readme(),
        long_description_content_type='text/markdown'
    )
