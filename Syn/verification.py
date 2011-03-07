#!/usr/bin/env python

import tarfile
import hashlib
import sys

def sumfile(fobj):
	'''Returns an md5 hash for an object with read() method.'''
	m = hashlib.md5()
	while True:
		d = fobj.read(8096)
		if not d:
			break
		m.update(d)
	return m.hexdigest()


def md5sum(fname):
	'''Returns an md5 hash for file fname, or stdin if fname is "-".'''
	if fname == '-':
		ret = sumfile(sys.stdin)
	else:
		try:
			f = file(fname, 'rb')
		except:
			return 'Failed to open file'
		ret = sumfile(f)
		f.close()
	return ret

def md5sumtar(filezor):
	tarball_target = tarfile.open(filezor, "r")
	filelist = tarball_target.getmembers()
	sumlist = {}

	for tarinfo in filelist:
		if tarinfo.isfile():
			fd = tarball_target.extractfile(tarinfo)
			md5 = sumfile(fd)
			sumlist[tarinfo.name] = md5
	return sumlist

