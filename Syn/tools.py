"""
Old-school tools to make life easy.
"""

from Syn import output, constants

import os
import json


class filedb:
	def __init__(self, dbfile):
		self.dbfile = os.path.abspath(dbfile)
		self.failed = False
		self.data   = {}

	def read( self ):
		try:
			path = self.dbfile
			file = open( path, 'r')
			self.data = json.load(file)
		except IOError:
			output.log("IO Error when we are doing read", 3)
			if not self.init():
				self.failToRead()

	def setInfo( self, key, value ):
		filename = self.dbfile
		output.log( "Noting a metafile " + filename + ", " + str(key) + " = " + str(value), 3 )
		try:
			self.read()
			data = self.data
			data[key] = value
			PACK = json.dumps( data )

			f = open( filename, 'w' )
			f.write( PACK )
			f.write( "\n" )
			f.close()

		except IOError:
			output.log("IO Error when we are doing setInfo", 3)
			if not self.init():
				self.failToRead()

	def init(self):
		if not os.path.exists( self.dbfile ):
			output.log("Trying to create a file to write to", 3)
			attr = {"synj":"synj"}
			PACK = json.dumps(attr)
			f = open( self.dbfile, 'w' )
			f.write( PACK )
			f.write( "\n" )
			f.close()
			output.success("Created the base conf db file", 3)
			return True
		else:
			output.error("Failure to create file. Already there!", 3)
			return False


	def failToRead(self):
		output.error("Failed to read datastore: " + self.dbfile + ".", 0 )

def cd( path ):
	"""Change Working Directory"""
	os.chdir( path )
	output.log( "Changed dir to " + path, 3 )

def mkshit( DIRZ ):
	"""Make the folder structure given"""
	for key, value in DIRZ.items():
		if value == "dir":
			os.mkdir( key )
			output.log( "Created dir " + key, 3 )
		else:
			os.mkdir( key )
			output.log( "Created dir " + key, 3 )
			cd( key )
			mkshit( DIRZ[key] )
			cd( ".." )

def stripXtn( name ):
	"""Strip out Extentions"""
	success = False
	for key, value in constants.SYN_SRC_XTNS.items():
		index = name.find( value )
		if index > 0:
			name = name[:index]
			success = True
			break

	if not success:
		output.error( "Detection errors! Extention sucks!", 3 )
		return False

	return name

def figureOutName( name ):
	"""Figure out name / version"""
	base = os.path.basename( name )
	base = stripXtn( base )

	ret = {
		"pkg" : "",
		"ver" : ""
	}

	if base:
		delim_one = base.find("-")

		if delim_one > 0:

			package_name   = base[:delim_one]
			version_string = base[delim_one+1:]

			ret['pkg'] = package_name
			ret['ver'] = version_string

		return ret
	else:
		output.error("Yeah, we can't save this. Something is wrong with this file", 1)
		return ret

## 2004-01-30
##
## Nick Vargish

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

