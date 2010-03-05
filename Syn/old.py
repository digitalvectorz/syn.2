import commands
import tarfile
import os
import shutil
from Syn.SynConfig import SynConfig
from Syn.SynInfo   import SynInfo
import time

def handleRemoveReadonly(func, path, exc):
	excvalue = exc[1]
	if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
		os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
		func(path)
	else:
		raise
class SynManager:

	CONF_TEMPLATE_EXTN = ".synt" # Synthetic Template

	CONF_ROOT_FILENAME  = "syn"
	CONF_METADATA       = "/metadata.sync"
	USER_CONFIG_FILE    = "config.sync" # Synthetic Config
	USER_CONFIG_ROOT    = "~/.syn/" + USER_CONFIG_FILE
	DEFAULT_VERSION_MOD = "syn"
	DEFAULT_BUILD_PRE   = CONF_ROOT_FILENAME + "/pkg/"
	DEFAULT_BUILD_ROOT  = "syn/"
	DEFAULT_BUILD_TREE  = DEFAULT_BUILD_PRE + DEFAULT_BUILD_ROOT
	CONF_BINARY_BUILD_EXTN = "syn"

	LastPackageName    = ""
	LastPackageVersion = ""

	verbosity = 0
	errors = 0
	ohshit = False
	
	def printGood( self, msg ):
	        print "[  ok  ]    " + msg
	def printBad( self, msg ):
	        print "[  no  ]    " + msg
		self.errors += 1
	def note( self, level, msg ):
		if self.verbosity >= level:
		        print "[ note ]    " + msg

	def decompressArchive(self,packpath):
		try:
			self.note( 3, "Attempting to open " + packpath )
			tar = tarfile.open( packpath )
			self.note( 3, "Opened " + packpath )
			tar.extractall()
			self.note( 2, "Extracted " + packpath )
			tar.close()
			self.note( 3, "Closing " + packpath )
		except IOError:
			self.printBad( "That's not an archive!" )
		except EOFError:
			self.printBad( "Looks like a corrupt download!" )

	def setup( self, path ):
		basename, filename = os.path.split(path)
		version = filename.split( '-' )
		if len( version ) < 2:
			self.printBad( "Archive Name is Invalid!" );
		else:
			for f in [".gz",".tgz",".tar",".bz2"]:
				version[1] = version[1].replace(f,"")

			vid = version[1]
			pak = version[0]

			self.LastPackageName    = pak
			self.LastPackageVersion = vid

			self.note( 1, "Package: " + pak );
			self.note( 1, "Version: " + vid );

                        conf_root = pak + "-" + vid + "/"

                        if os.path.exists( conf_root ):
				self.note( 2, "Stale tree here. Removing it." )
				shutil.rmtree( conf_root, ignore_errors=False, onerror=handleRemoveReadonly)
			if self.errors > 0:
				self.printBad( "Halting. I don't want to play this game." )
				self.ohshit = True
			else:
				self.decompressArchive( path )

				if os.path.exists( conf_root ):
					self.note( 3, "Directory in the right format! Huzzah!" )
					if os.path.exists( conf_root + "/" + self.CONF_ROOT_FILENAME ):
						self.printBad( "Crap! There is a " + self.CONF_ROOT_FILENAME + " direcotry in there." )
					else:
						os.makedirs( conf_root + "/" + self.CONF_ROOT_FILENAME )
						os.makedirs( conf_root + "/" + self.CONF_ROOT_FILENAME + "/patches" )
						os.makedirs( conf_root + "/" + self.CONF_ROOT_FILENAME + "/logs" )
						if os.path.exists(os.path.expanduser(self.USER_CONFIG_ROOT)):
							shutil.copy(os.path.expanduser(self.USER_CONFIG_ROOT), conf_root + "/" + self.CONF_ROOT_FILENAME )
						else:
							self.printBad( "Uh oh. We can't find your Syn conf file " + self.USER_CONFIG_ROOT + "!" )
							self.ohshit = True

						si = SynInfo()
						SynInfoFile = pak + "-" + vid + "/" + self.CONF_ROOT_FILENAME + self.CONF_METADATA
						si.write( SynInfoFile, pak, vid, filename )

						self.note( 3, "Wrote metadata to " + SynInfoFile )

						if not si.failed:
							si.read( SynInfoFile )
							for var in si.data:
								self.note( 3, "Info Verify SI Write: " + var + " = " + si.data[var] )
						else:
							self.printBad( "Oh crap. Bad stuff. Can't write syn meta file" )

				else:
					self.printBad( "Directory is in an invalid format!" )
					self.ohshit = True
			if self.errors > 0:
				self.note( 1, "Finished with %d error(s)" % ( self.errors ) )
			else:
				self.printGood( "Finished with no errors! Archive unziped and set up" )
	def make( self ):
		b = SynConfig()
		b.readConfig( self.CONF_ROOT_FILENAME + "/" + self.USER_CONFIG_FILE )
		if b.failed:
			self.printBad( "We failed to load the config" )
			self.ohshit = True
		else:
			self.note( 2, "Loaded the config" )
			for var in b.data[u"env"]:
				self.note( 3, var + " = " + b.data[u"env"][var] )
				os.putenv( var, b.data[u"env"][var] )
			flags = ""
			for var in b.data[u"BuildFlags"]:
				self.note( 3, var + " = " + b.data[u"BuildFlags"][var] )
				flags += b.data[u"BuildFlags"][var] + " "
			self.note( 2, "Our build string: " + flags )
			if os.path.exists("Makefile"):
				self.note( 1, "Running the build" )

				si = SynInfo()
				SynInfoFile = self.CONF_ROOT_FILENAME + self.CONF_METADATA
				si.setInfo( SynInfoFile, "MakeStart", time.time() )
				stat, output = commands.getstatusoutput( "make " + flags )
				si.setInfo( SynInfoFile, "MakeFinish", time.time() )

				if stat != 0:
					self.printBad( "Oh crap. Make went bad. check the logs." )
				else:
					self.note( 2, "Saving log of the build" )
					f = open( self.CONF_ROOT_FILENAME + "/logs/make.log", 'w')
					f.write( output )
					f.write( "\n" )
					f.close()
					self.printGood( "Built OK!" )
			else:
				self.printBad( "There is no Makefile! Great scott!" )
				self.ohshit = True

	def config( self ):
		b = SynConfig()
		b.readConfig( self.CONF_ROOT_FILENAME + "/" + self.USER_CONFIG_FILE )
		if b.failed:
			self.printBad( "We failed to load the config" )
			self.ohshit = True
		else:
			self.note( 2, "Loaded the config " )
			for var in b.data[u"env"]:
				self.note( 3, var + " = " + b.data[u"env"][var] )
				os.putenv( var, b.data[u"env"][var] )
			flags = ""
			for var in b.data[u"ConfigFlags"]:
				self.note( 3, var + " = " + b.data[u"ConfigFlags"][var] )
				flags += b.data[u"ConfigFlags"][var] + " "
			self.note( 2, "Our conf string: " + flags )
			if os.path.exists("./configure"):
				self.note( 1, "Running the configure" )
				stat, output = commands.getstatusoutput( "./configure " + flags )
				if stat != 0:
					self.printBad( "Oh crap. Configure went bad check the logs." )
				else:
					self.note( 2, "Saving log of configure" )
					f = open( self.CONF_ROOT_FILENAME + "/logs/configure.log", 'w')
					f.write( output )
					f.write( "\n" )
					f.close()
					self.printGood( "Configured OK!" )
			else:
				self.printBad( "There is no configure! Great scott!" )
				self.ohshit = True
	def template( self ):
		if os.path.exists( self.CONF_ROOT_FILENAME ):
			self.note( 3, "Found the conf root. Starting a template" )
			si = SynInfo()
			SynInfoFile = self.CONF_ROOT_FILENAME + "/" + self.CONF_METADATA
			si.read( SynInfoFile )
			PN =  si.data['PackageName']
			PV =  si.data['PackageVersion']

			SYNT_PATH = "../" + PN + "-" + PV + self.CONF_TEMPLATE_EXTN
			try:
				self.note( 3, "Using " + SYNT_PATH + " to write" )
				synt = tarfile.open( SYNT_PATH, 'w' )
				self.note( 3, "Adding in the conf dir" )
				synt.add( self.CONF_ROOT_FILENAME )
				self.note( 3, "Closing template file" )
				synt.close()
				self.note( 1, "Template created" )
			except:
				self.printBad( "Template Failed!" )
				self.ohshit = True
		else:
			self.printBad( "No conf root. We can't template. This is bad. Ensure Syn set this pkg up." )
			self.ohshit = True

	def createBinaryPackage( self ):
		b = SynConfig()
		b.readConfig( self.CONF_ROOT_FILENAME + "/" + self.USER_CONFIG_FILE )
		if b.failed:
			self.printBad( "We failed to load the config" )
			self.ohshit = True
		else:
			self.note( 2, "Loaded the config" )
			for var in b.data[u"env"]:
				self.note( 3, var + " = " + b.data[u"env"][var] )
				os.putenv( var, b.data[u"env"][var] )
				if var == "VERSION_MODIFIER":
					self.note( 3, "Found a version modifier. using " + b.data[u"env"][var] )
					VERSION_MOD = b.data[u"env"][var]

			self.note( 2, "Our version modifier: " + VERSION_MOD )
			if os.path.exists("Makefile"):
				self.note( 1, "Running the Install" )
				si = SynInfo()
				SynInfoFile = self.CONF_ROOT_FILENAME + self.CONF_METADATA

				buildtree = self.DEFAULT_BUILD_TREE

	                        if os.path.exists( buildtree ):
					self.note( 2, "Stale install tree here. Removing it." )
					shutil.rmtree( buildtree, ignore_errors=False, onerror=handleRemoveReadonly)
				if self.errors > 0:
					self.printBad( "Halting. I don't want to play this game." )
					self.ohshit = True
				else:
					os.makedirs( buildtree )

					si = SynInfo()
					SynInfoFile = self.CONF_ROOT_FILENAME + self.CONF_METADATA
					si.setInfo( SynInfoFile, "BinaryStart", time.time() )
					stat, output = commands.getstatusoutput( "make install DESTDIR=" + buildtree )
					si.setInfo( SynInfoFile, "BinaryFinish", time.time() )

					if stat != 0:
						self.printBad( "Oh crap. Binary build went bad. check the logs." )
					else:
						self.note( 2, "Saving log of the build" )
						f = open( self.CONF_ROOT_FILENAME + "/logs/binary.log", 'w')
						f.write( output )
						f.write( "\n" )
						f.close()
						self.printGood( "Binary build OK!" )

						si.read( SynInfoFile )
						PN =  si.data['PackageName']
						PV =  si.data['PackageVersion']

						os.chdir( self.DEFAULT_BUILD_PRE )
						holdme = os.getcwd()

						SYNT_PATH = PN + "-" + PV + "." + self.CONF_BINARY_BUILD_EXTN

						try:
							self.note( 3, "Using " + self.DEFAULT_BUILD_ROOT + " to write build" )
							synt = tarfile.open( holdme + "/../../../" + SYNT_PATH, 'w' )s
							self.note( 3, "Adding in the package dir to " )
							synt.add( self.DEFAULT_BUILD_ROOT, "syn" )
							self.note( 3, "Adding in the metadata" )
							synt.add( "../" + self.CONF_METADATA, "metadata" )
							self.note( 3, "Closing binary blob file" )
							synt.close()
							self.note( 1, "Binary blob created" )
							shutil.rmtree( self.DEFAULT_BUILD_ROOT, ignore_errors=False, onerror=handleRemoveReadonly)
						except:
							self.printBad( "Blob Failed!" )
							self.ohshit = True

