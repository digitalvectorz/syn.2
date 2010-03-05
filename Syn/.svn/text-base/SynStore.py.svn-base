try:
	import json
except:
	import simplejson as json

import Syn.SynGlobals


class SynStore:
	failed = False
	data = ""

	def failToRead( self ):
		self.failed = True

	def readConfig( self, path ):
		try:
			file = open( path, 'r')
			self.data = json.load(file)
		except IOError:
			self.failToRead()

	def setInfo( self, filename, key, value ):
		Syn.SynGlobals.note( 4, "Noting a metafile " + filename + ", " + str(key) + " = " + str(value) )
		try:
			self.read( filename )
			if not self.failed:
				data = self.data
				data[key] = value
				PACK = json.dumps( data )
			else:
				PACK = json.dumps({ key : value } )

			f = open( filename, 'w' )
			f.write( PACK )
			f.write( "\n" )
			f.close()

		except IOError:
			self.failToRead()

	def read( self, filename ):
		try:
			self.failed = False
			file = open( filename, 'r')
			self.data = json.load(file)
		except IOError:
			self.failToRead()


