
try:
	import json
except:
	import simplejson as json

class SynConfig:
	failed = False
	data = ""

	def readConfig( self, path ):
		try:
			file = open( path, 'r')
			self.data = json.load(file)
		except IOError:
			self.failToRead()

	def failToRead( self ):
		failed = True
