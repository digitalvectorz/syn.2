import time
import os
import tarfile
import Syn.SynGlobals
import shutil

from Syn.SynStore import SynStore

class SynManager:
	ICanRecover = True

	synStore = Syn.SynStore()

	def setup( self, path ):

		if not os.path.exists( path ):
			Syn.SynGlobals.noteBad( "" )
			Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
			Syn.SynGlobals.noteBad( "|                      That's not an archive, silly!!!                   |" )
			Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
			Syn.SynGlobals.noteBad( "  * Stop being silly. Give me a real archive!!" )
			Syn.SynGlobals.noteBad( "" )
			return;

		WhereTo = "./"
		name, version = Syn.SynGlobals.parsePkgName( path )
		ExpectedExtract = WhereTo + name + "-" + version

		Syn.SynGlobals.note( 3, "We are expecting extract to " + ExpectedExtract )
		Syn.SynGlobals.note( 3, "Checking for existing tree" )

		if Syn.SynGlobals.dirExists( ExpectedExtract ):
			Syn.SynGlobals.note( 2, "Removing the old build." )
			Syn.SynGlobals.rmdashrf( ExpectedExtract )
			Syn.SynGlobals.note( 3, "Removed." )

		if not Syn.SynGlobals.extractArchive( path, WhereTo ):
			Syn.SynGlobals.noteBad( "" )
			Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
			Syn.SynGlobals.noteBad( "|                      Archive could not be extracted!!!                 |" )
			Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
			Syn.SynGlobals.noteBad( "  * Dunno. This should be failsafe. Check it out, rick!" )
			Syn.SynGlobals.noteBad( "  * Read spew above this line. This is usually an IO or EOF error." )
			Syn.SynGlobals.noteBad( "" )
			return

		if Syn.SynGlobals.dirExists( ExpectedExtract ):

			Syn.SynGlobals.note( 3, "Directory extracted just right." )
			os.chdir( ExpectedExtract )

			ConfigRoot = Syn.SynGlobals.SYN_METAFOLDER

			if not Syn.SynGlobals.dirExists( ConfigRoot ):
				MakingANote = os.getcwd()
				Syn.SynGlobals.note( 3, "I am at this dir:  " + os.getcwd() )
				Syn.SynGlobals.note( 3, "Creating config root" )
				Syn.SynGlobals.createDir( ConfigRoot )
				os.chdir( ConfigRoot )
				Syn.SynGlobals.note( 3, "I am at this dir:  " + os.getcwd() )

				for f in Syn.SynGlobals.SYN_FOLDERS:
					Syn.SynGlobals.note( 3, "Creating dir: " + f )
					Syn.SynGlobals.createDir( f )

				Syn.SynGlobals.noteGood( "Extracted and setup. Looking nice." )

				root = "../../"

				for foo in os.listdir(root):
					idz = os.path.splitext( foo )
					if idz[1] == ".patch":
						Syn.SynGlobals.note( 2, "I found a patch! Adding it in! ( " + foo + " )" )
						shutil.copy( root + foo, Syn.SynGlobals.SYN_PATCH_F )
						Syn.SynGlobals.note( 3, "Marking that patches exist. " +  Syn.SynGlobals.SYN_PATCH_E )
						open(Syn.SynGlobals.SYN_PATCH_E, 'w').close()

				if Syn.SynGlobals.importConfig( "./" + Syn.SynGlobals.SYN_CONFIG ):

					# Let's write some metadata.

					self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFILE, "SynVersion", Syn.SynGlobals.SYN_VERSION )
					self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFILE, "SetupBy",   os.getlogin() )
					self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFILE, "SetupTime", time.time()   )
					self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFILE, "Name", name )
					self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFILE, "Version", version )

					os.chdir( MakingANote )
					Syn.SynGlobals.note( 3, "I am at this dir:  " + os.getcwd() )
			else:
				Syn.SynGlobals.noteBad( "" )
				Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
				Syn.SynGlobals.noteBad( "|                       Syn Directory Already Exists!                    |" )
				Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
				Syn.SynGlobals.noteBad( "  * Is the gal or guy who made this a syn hacker? Do they have " )
				Syn.SynGlobals.noteBad( "     their changes already in there? If so just extract it!" )
				Syn.SynGlobals.noteBad( "     Otherwise, you are boned. Good luck." )
				Syn.SynGlobals.noteBad( "" )
				return
		else:
			Syn.SynGlobals.noteBad( "" )
			Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
			Syn.SynGlobals.noteBad( "|                     Root that we want does not exist                   |" )
			Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
			Syn.SynGlobals.noteBad( "  * We need the extract target to be package-version/. " )
			Syn.SynGlobals.noteBad( "  * See if you can't patch around the shoddy packaging. " )
			Syn.SynGlobals.noteBad( "  * Expected: " + ExpectedExtract )
			Syn.SynGlobals.noteBad( "" )
			return

	def config( self ):
		Syn.SynGlobals.note( 3, "Make sure we are patched up" )
		self.applyPatches();

		flags = Syn.SynGlobals.recoverConfigEnv()
		Syn.SynGlobals.preConfig()
		self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFOLDER + "/" + Syn.SynGlobals.SYN_METAFILE, "ConfigStartTime", time.time()   )
		if not Syn.SynGlobals.runRules( "config" ):
			path = "./configure" # check for configure
			if not os.path.exists( path ):
				Syn.SynGlobals.noteBad( "" )
				Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
				Syn.SynGlobals.noteBad( "|                 Configure File is not Found! This sucks!               |" )
				Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
				Syn.SynGlobals.noteBad( "  * This package might not need a configure." )
				Syn.SynGlobals.noteBad( "  * Try rolling your own build method. Look into hooks. ( rules section )" )
				Syn.SynGlobals.noteBad( "" )
				return;
			else:
				Syn.SynGlobals.note( 1, "Running the configure file" )
				if not Syn.SynGlobals.runCommand( path + " " + flags, "configure" ):
					Syn.SynGlobals.noteBad( "" )
					Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
					Syn.SynGlobals.noteBad( "|                       Configure File Failed!! Crap!                    |" )
					Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
					Syn.SynGlobals.noteBad( "  * Running the ./config bombed out. Full path: " + path + "." )
					Syn.SynGlobals.noteBad( "  * We tried to save what we could to logs." )
					Syn.SynGlobals.noteBad( "" )
					return;
				else:
					self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFOLDER + "/" + Syn.SynGlobals.SYN_METAFILE, "ConfigType", "Distrub" )
		else:
			Syn.SynGlobals.note( 1, "Rules configure finished." )
			self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFOLDER + "/" + Syn.SynGlobals.SYN_METAFILE, "ConfigType", "Rules" )

		self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFOLDER + "/" + Syn.SynGlobals.SYN_METAFILE, "ConfigTime", time.time()   )
		Syn.SynGlobals.postConfig()
		Syn.SynGlobals.noteGood( "Configure Finished!" )

	def applyPatches( self ):
		Syn.SynGlobals.note( 3, "Attempting to apply patches" )
		if Syn.SynGlobals.dirExists( Syn.SynGlobals.SYN_METAFOLDER + "/" + Syn.SynGlobals.SYN_PATCH_E ):
			Syn.SynGlobals.note( 2, "Found the patch signal! Let's patch dis bitch!" )
			if not Syn.SynGlobals.runCommand( "patch -Np1 -i " + "./" + Syn.SynGlobals.SYN_METAFOLDER + "/" + Syn.SynGlobals.SYN_PATCH_F + "/*", "patch" ):
				Syn.SynGlobals.noteBad( "" )
				Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
				Syn.SynGlobals.noteBad( "|                               Patches Failed!!                         |" )
				Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
				Syn.SynGlobals.noteBad( "  * Running the patches failed!" )
				Syn.SynGlobals.noteBad( "  * Remove the signal if patches don't exist! ( " + Syn.SynGlobals.SYN_PATCH_E + ")" )
				Syn.SynGlobals.noteBad( "" )
				return;
			else:
				Syn.SynGlobals.noteGood( "Patches Applied!" )
		else:
			Syn.SynGlobals.note( 3, "Patch file is not found. Skipping patching the source." )
	
	def build( self ):
		flags = Syn.SynGlobals.recoverBuildEnv()
		Syn.SynGlobals.preBuild()
		self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFOLDER + "/" + Syn.SynGlobals.SYN_METAFILE, "MakeStartTime", time.time()   )

		if not Syn.SynGlobals.runRules( "build" ):
			path = "Makefile" # check for make
			if not os.path.exists( path ):
				Syn.SynGlobals.noteBad( "" )
				Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
				Syn.SynGlobals.noteBad( "|                     Makefile is not Found! This sucks!                 |" )
				Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
				Syn.SynGlobals.noteBad( "  * This package might not need a make." )
				Syn.SynGlobals.noteBad( "  * Try rolling your own build method. Look into hooks. ( rules section )" )
				Syn.SynGlobals.noteBad( "" )
				return;
			else:
				Syn.SynGlobals.note( 1, "Running the makefile" )
				path = "make" # We checked for "Makefile"
				if not Syn.SynGlobals.runCommand( path + " " + flags, "build" ):
					Syn.SynGlobals.noteBad( "" )
					Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
					Syn.SynGlobals.noteBad( "|                          Makefile Failed!! Crap!                       |" )
					Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
					Syn.SynGlobals.noteBad( "  * Running the Makefile shat." )
					Syn.SynGlobals.noteBad( "  * You might be missing some build deps, or need to tweek your config" )
					Syn.SynGlobals.noteBad( "" )
					return;
				else:
					self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFOLDER + "/" + Syn.SynGlobals.SYN_METAFILE, "Maketype", "Distrub" )
		else:
			Syn.SynGlobals.note( 1, "Rules make finished." )
			self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFOLDER + "/" + Syn.SynGlobals.SYN_METAFILE, "Maketype", "Rules" )

		self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFOLDER + "/" + Syn.SynGlobals.SYN_METAFILE, "MakeTime", time.time()   )
		Syn.SynGlobals.postBuild()
		Syn.SynGlobals.noteGood( "Build Finished!" )

	def package( self ):
		Syn.SynGlobals.prePackage()
		stage_dir = Syn.SynGlobals.SYN_METAFOLDER + "/" + Syn.SynGlobals.SYN_PACK_F
		flags = "DESTDIR=" + stage_dir

		if not os.path.exists( stage_dir ):
			Syn.SynGlobals.createDir( stage_dir )
		else:
			Syn.SynGlobals.noteBad( "" )
			Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
			Syn.SynGlobals.noteBad( "|                       Package Failed to Create!                        |" )
			Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
			Syn.SynGlobals.noteBad( "  * Running the Makefile shat." )
			Syn.SynGlobals.noteBad( "  * Make sure it can use DESTDIR. This should not be run root." )
			Syn.SynGlobals.noteBad( "" )
			return;
		self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFOLDER + "/" + Syn.SynGlobals.SYN_METAFILE, "PackStartTime", time.time()   )
		if not Syn.SynGlobals.runRules( "pack" ):
			path = "Makefile" # check for make
			if not os.path.exists( path ):
				Syn.SynGlobals.noteBad( "" )
				Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
				Syn.SynGlobals.noteBad( "|                     Makefile is not Found! This sucks!                 |" )
				Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
				Syn.SynGlobals.noteBad( "  * This package might not need a make." )
				Syn.SynGlobals.noteBad( "  * Try rolling your own build method. Look into hooks. ( rules section )" )
				Syn.SynGlobals.noteBad( "" )
				return;
			else:
				Syn.SynGlobals.note( 1, "Running the makefile" )
				path = "make install" # We checked for "Makefile"
				if not Syn.SynGlobals.runCommand( path + " " + flags, "pack" ):
					Syn.SynGlobals.noteBad( "" )
					Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
					Syn.SynGlobals.noteBad( "|                      Packing this app blew a hard one                  |" )
					Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
					Syn.SynGlobals.noteBad( "  * Running the Makefile shat." )
					Syn.SynGlobals.noteBad( "  * Make sure it can use DESTDIR. This should not be run root." )
					Syn.SynGlobals.noteBad( "" )
					return;
				else:
					self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFOLDER + "/" + Syn.SynGlobals.SYN_METAFILE, "Packtype", "Distrub" )
		else:
			Syn.SynGlobals.note( 1, "Rules make finished." )
			self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFOLDER + "/" + Syn.SynGlobals.SYN_METAFILE, "Packtype", "Rules" )

		name = Syn.SynGlobals.getPackageName()
		vers = Syn.SynGlobals.getPackageVID()

		os.chdir( Syn.SynGlobals.SYN_METAFOLDER )
		Syn.SynGlobals.note( 3, "I am at this dir:  " + os.getcwd() )

		path = name + "-" + vers + "." + Syn.SynGlobals.SYN_TOKEN

		archive = tarfile.open( path, mode='w:gz' )
		archive.add( Syn.SynGlobals.SYN_PACK_F, "root", recursive=True )
		archive.add( Syn.SynGlobals.SYN_METAFILE )
		archive.add( Syn.SynGlobals.SYN_CONFIG )
		archive.close()

		Syn.SynGlobals.postPackage()
		self.synStore.setInfo( "./" + Syn.SynGlobals.SYN_METAFOLDER + "/" + Syn.SynGlobals.SYN_METAFILE, "PackTime", time.time()   )
		Syn.SynGlobals.noteGood( "Package Finished!" )

	def template( self ):
		Syn.SynGlobals.preTemplate()
		TempFolder = Syn.SynGlobals.SYN_METAFOLDER

		if os.path.exists( TempFolder ):
			name = Syn.SynGlobals.getPackageName()
			vers = Syn.SynGlobals.getPackageVID()

			path = name + "-" + vers + "." + Syn.SynGlobals.SYNT_TOKEN

			archive = tarfile.open( path, mode='w:gz' )
			archive.add( TempFolder )
			archive.close()

			shutil.move( path, Syn.SynGlobals.SYN_METAFOLDER )
		else:
			Syn.SynGlobals.noteBad( "" )
			Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
			Syn.SynGlobals.noteBad( "|                      Template Failed to Create!                        |" )
			Syn.SynGlobals.noteBad( "+------------------------------------------------------------------------+" )
			Syn.SynGlobals.noteBad( "  * Making a template failed! Set me up first!" )
			Syn.SynGlobals.noteBad( "" )
			return;
		Syn.SynGlobals.postTemplate()
		Syn.SynGlobals.noteGood( "Template Finished!" )

	def install( self, path ):
		tar = tarfile.open( path, "r:gz")
		member_info = tar.getmember( Syn.SynGlobals.SYN_METAFILE )
		if member_info != None:
			f = tar.extractfile(member_info)
			read = Syn.SynGlobals.getPackageMetadata( f )
			vid  = read["Version"]
			name = read["Name"]
			Syn.SynGlobals.note( 1, "Installing " + name + ", version " + vid )

			install_path = Syn.SynGlobals.SYN_ROOT + "/" + name + "/" + vid + "/"

			if not os.path.exists( Syn.SynGlobals.SYN_ROOT ):
				Syn.SynGlobals.noteBad( "Whoh! You don't have a package root! Crap!" )
				Syn.SynGlobals.noteBad( "Path Expected: " + Syn.SynGlobals.SYN_ROOT )
				return

			if not os.path.exists( Syn.SynGlobals.SYN_ROOT + "/" + name ):
				Syn.SynGlobals.note( 3, "Fist package of type " + name + ", making it's root" )
				Syn.SynGlobals.createDir( Syn.SynGlobals.SYN_ROOT + "/" + name )
				Syn.SynGlobals.note( 3, "Directory Created" )

			if os.path.exists( install_path ):
				# Oh FFFFFFFFFFFUUUUUUUUUUUU
				Syn.SynGlobals.noteBad( "Not installing. Already installed!" )
			else:
				Syn.SynGlobals.note(3, "Installing to " + install_path )
				Syn.SynGlobals.note( 3, "Directory Created" )

				tar.extractall( install_path )

		tar.close()
		Syn.SynGlobals.noteGood( "Install Finished!" )


	def link( self, name, vid ):
		install_path = Syn.SynGlobals.SYN_ROOT + "/" + name + "/" + vid + "/"
		if os.path.exists( install_path ):
			Syn.SynGlobals.note(3, "OK. Package exists. Let's do dis." )
			Syn.SynGlobals.note(3, "ID = " + name )
			Syn.SynGlobals.note(3, "VD = " + vid )

			install_path += "root/"

			link_path = "/syn/fake-rootski/"

			if os.path.exists( install_path ):
				Syn.SynGlobals.note(3, "OK. Root exists. Whuut! " + install_path )
				os.chdir( install_path )

				for root, dirs, files in os.walk( "." ): # rel paths ftw
					Syn.SynGlobals.note(4, "processing " + root )
					for f in files:
						Syn.SynGlobals.note(4, "linking " + root + f + " to " + link_path + root + f )
						if not os.path.exists( link_path + root ):
							Syn.SynGlobals.note(4, "no dir yet. creatking " + link_path + root )
							Syn.SynGlobals.createDir( link_path + root )
						os.symlink( install_path + root + "/" + f, link_path + root + "/" + f )
			else:
				Syn.SynGlobals.noteBad( "No root, what kind of fucking .syn file is that?" )
		else:
			Syn.SynGlobals.noteBad( "Install the package first, dummy!" )

