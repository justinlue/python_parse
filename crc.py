#!/usr/bin/env python
"""
@author: Elijah Luo
@file: parse.py
@time: 2018/08/31
"""
from hashlib import md5, sha1
from zlib import crc32
import sys

def getMd5(filename):
    mdfive = md5()
    with open(filename, 'rb') as f:
        mdfive.update(f.read())
    return mdfive.hexdigest()

def getSha1(filename):
    sha1Obj = sha1()
    with open(filename, 'rb') as f:
        sha1Obj.update(f.read())
    return sha1Obj.hexdigest()

def getCrc32(filename):
    with open(filename, 'rb') as f:
        return crc32(f.read())

if len(sys.argv) < 2:
    print('You must enter the file')
    exit(1)
elif len(sys.argv) > 2:
    print('Only one file is permitted')
    exit(1)

filename = sys.argv[1]

print('{:8} {}'.format('md5:', getMd5(filename)))
print('{:8} {}'.format('sha1:', getSha1(filename)))
print('{:8} {:x}'.format('crc32:', getCrc32(filename)))
