#!/bin/bash

ABSPATH=$(realpath ${1})

echo "Python2"
time python2 -m dataintegrityfingerprint.cli ${ABSPATH}

echo "Python3"
time python3 -m dataintegrityfingerprint.cli  ${ABSPATH}
#python3 -m dataintegrityfingerprint.cli -f checksums.bash 
#python3 -m dataintegrityfingerprint.gui
