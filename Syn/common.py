#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

import time
import os

import Syn.tarball
import Syn.Global as g
import Syn.log

import tarfile
import os.path
import shutil
import json
import os


def processFullID(identifier):
	try:
		split = identifier.index("-")
		package_id = identifier[:split]
		version_id = identifier[split+1:]
		return [ package_id, version_id ]
	except ValueError:
		return [ identifier, None ]

def getTempLocation():
	timestamp = time.time()
	unpack_dir = Syn.Global.WORKDIR + str(timestamp) + "/"
	return unpack_dir

def createWorkDir(location):
	Syn.log.l(Syn.log.PEDANTIC, "creating work dir " + location)
	global _CUR_WORK_DIR
	_CUR_WORK_DIR = location
	os.makedirs(_CUR_WORK_DIR)

def mkdir(location):
	Syn.log.l(Syn.log.PEDANTIC, "creating dir " + location)
	os.makedirs(location)

def removeWorkDir():
	global _CUR_WORK_DIR
	Syn.log.l(Syn.log.PEDANTIC, "removing work dir " + _CUR_WORK_DIR)
	os.rmdir(_CUR_WORK_DIR)

def cd(work_dir):
	os.chdir(work_dir)
	Syn.log.l(Syn.log.PEDANTIC, "chdir to " + work_dir)

KEYNOTFOUND = '<KEYNOTFOUND>'       # KeyNotFound for dictDiff

def dict_diff(first, second):
	diff = {}
	# Check all keys in first dict
	for key in first.keys():
		if (not second.has_key(key)):
			diff[key] = (first[key], KEYNOTFOUND)
		elif (first[key] != second[key]):
			diff[key] = (first[key], second[key])
	# Check all keys in second dict to find missing
	for key in second.keys():
		if (not first.has_key(key)):
			diff[key] = (KEYNOTFOUND, second[key])
	return diff
