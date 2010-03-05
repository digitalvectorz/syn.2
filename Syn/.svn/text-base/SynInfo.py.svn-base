
import time
import os

try:
	import json
except:
	import simplejson as json

class SynInfo:

	failed = False
	data = ""

	def setInfo( self, filename, key, value ):
		try:
			self.read( filename )
			if not self.failed:
				data = self.data;
				data[key] = value
				PACK = json.dumps( data )
				f = open( filename, 'w' )
				f.write( PACK )
				f.write( "\n" )
				f.close()

		except IOError:
			self.failToRead()

	def write( self, fileName, name, version, filename ):
		try:
			PACK = json.dumps(
		{
			'PackageName' : name,
			'PackageVersion' : version,
			'TarFile' : filename,
			'Hacker' : os.getlogin(),
			'SetupAt' : str(time.time())
		}
			)
			f = open( fileName, 'w')
			f.write( PACK )
			f.write( "\n" )
			f.close()
		except IOError:
			self.failToRead()

	def read( self, filename ):
		try:
			file = open( filename, 'r')
			self.data = json.load(file)
		except IOError:
			self.failToRead()


