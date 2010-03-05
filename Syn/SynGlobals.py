import commands
import os
import tarfile
import shutil
from Syn.SynStore import SynStore

SYN_VERSION     = 1

SYN_TOKEN       = "syn"
SYNT_TOKEN      = "synt"
SYN_METAFOLDER  = SYN_TOKEN

SYN_ROOT        = "/" + SYN_TOKEN

SYN_METAFILE    = "metadata.synm"
SYN_CONFIG      = "build.sync"

SYN_USERSPACE   = "~/.syn/"
SYN_USERSPACE_F = SYN_CONFIG

SYN_GLOBAL      = "/etc/syn/"
SYN_GLOBAL_F    = SYN_CONFIG

SYN_USER_PATH   = SYN_USERSPACE + SYN_USERSPACE_F
SYN_GLOBAL_PATH = SYN_GLOBAL + SYN_GLOBAL_F

SYN_HOOK_F      = "hooks"
SYN_LOG_F       = "logs"
SYN_PATCH_F     = "patches"
SYN_PATCH_E     = "apply-patch"
SYN_CONFIG_F    = "configs"
SYN_PACK_F      = "pack-tree"
SYN_PACK_AF     = SYN_METAFOLDER

SYN_FOLDERS     = [ SYN_LOG_F, SYN_PATCH_F, SYN_CONFIG_F, SYN_HOOK_F ]

SYN_HOOK_RULES    = "rules"

SYN_HOOK_PRECONF  = "preconf"
SYN_HOOK_POSTCONF = "postconf"

SYN_HOOK_PREBUILD  = "prebuild"
SYN_HOOK_POSTBUILD = "postbuild"

SYN_HOOK_PREINST   = "preinst"
SYN_HOOK_POSTINST  = "postinst"

SYN_HOOK_PRETEMP   = "pretemp"
SYN_HOOK_POSTTEMP  = "posttemp"

SYN_HOOK_PREPACK   = "prepack"
SYN_HOOK_POSTPACK  = "postpack"

SYN_HOOK_PRELINK   = "prelink"
SYN_HOOK_POSTLINK  = "postlink"

SYN_HOOK_OVERRIDECONF  = "configure"
SYN_HOOK_OVERRIDEBUILD = "make"
SYN_HOOK_OVERRIDEPACK  = "package"

VERBOSE_LEVEL   = 0
FAILURE_COUNT   = 0

INDENT_LINE     = "     "
NOTE_PREFIX     = "[ note ]" + INDENT_LINE
BAD_PREFIX      = "[ fail ]" + INDENT_LINE
GOOD_PREFIX     = "[  ok  ]" + INDENT_LINE

def note( level, message ):
	if level <= VERBOSE_LEVEL:
		print NOTE_PREFIX + message

def noteGood( message ):
	if VERBOSE_LEVEL >= 0:
		print GOOD_PREFIX + message

def noteBad( message ):
	print BAD_PREFIX + message

def extractArchive( path, WhereTo ):
	try:
		note( 2, "Attempting to open " + path )
		tar = tarfile.open( path )
		note( 3, "Opened Archive:    " + path )
		MakingANote = os.getcwd()
		note( 3, "I am at this dir:  " + os.getcwd() )
		os.chdir( WhereTo )
		note( 3, "I am at this dir:  " + os.getcwd() )
		tar.extractall()
		note( 1, "Extracted Archive: " + path )
		os.chdir( MakingANote )
		note( 3, "I am at this dir:  " + os.getcwd() )
		tar.close()
		note( 3, "Closing Archive:   " + path )
		return True
	except IOError:
		noteBad( "" )
		noteBad( "+------------------------------------------------------------------------+" )
		noteBad( "|                Input / Output Error Reading the archive file.          |" )
		noteBad( "+------------------------------------------------------------------------+" )
		noteBad( "  * Looks like an IO error to my humble logic." )
		noteBad( "" )
		return False
	except EOFError:
		noteBad( "" )
		noteBad( "+------------------------------------------------------------------------+" )
		noteBad( "|                  End of File Error Reading the archive file.           |" )
		noteBad( "+------------------------------------------------------------------------+" )
		noteBad( "  * Bad archive to my humble logic." )
		noteBad( "" )
		return False

def handleRemoveReadonly(func, path, exc):
	excvalue = exc[1]
	if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
		os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
		func(path)
	else:
		raise

def dirExists( path ):
	if os.path.exists( path ):
		return True
	else:
		return False

def rmdashrf( path ):
	shutil.rmtree(
		path,
		ignore_errors = False,
		onerror = handleRemoveReadonly
	)
	return dirExists( path )

def createDir( path ):
	os.makedirs( path )
	return dirExists( path )

def importConfig( path ):
	if os.path.exists(os.path.expanduser(SYN_USER_PATH)):
		# We prefer their config
		note( 2, "Found user sync file." )
		shutil.copy( os.path.expanduser(SYN_USER_PATH), path )
	elif os.path.exists( SYN_GLOBAL_PATH ):
		# We can fall back on this.
		shutil.copy( SYN_GLOBAL_PATH, path )
		note( 2, "Falling back on global sync file." )
	else:
		# FAILBOAT
		noteBad( "" )
		noteBad( "+------------------------------------------------------------------------+" )
		noteBad( "| No sync files ANYWHERE. This is BAD. Ensure everything is setup right. |" )
		noteBad( "+------------------------------------------------------------------------+" )
		noteBad( "  * We looked locally for:   " + SYN_USER_PATH )
		noteBad( "  * Also globally at:        " + SYN_GLOBAL_PATH )
		noteBad( "" )
		return False
	return True

def parsePkgName( path ):

	basename, filename = os.path.split(path)
	version = filename.split( '-' )

	if len( version ) < 2:
		noteBad( "" )
		noteBad( "+------------------------------------------------------------------------+" )
		noteBad( "|                  Archive Name is Invalid. This is not cool.            |" )
		noteBad( "+------------------------------------------------------------------------+" )
		noteBad( "  * The prototype for an archive is foo-1.0.[tgz|tar|tar.gz|bz2]" )
		noteBad( "  * Any other format then name-version.xtn will throw syn off." )
		noteBad( "  * Fix this for me, please. Chances are if this is wrong, the extract" )
		noteBad( "     will be wrong as well. See if you can't patch it." ) 
		noteBad( "" )
	else:
		for f in [".gz",".tgz",".tar",".bz2"]:
			version[1] = version[1].replace(f,"")

		vid = version[1]
		pak = version[0]
		note( 3, "Package: " + pak );
		note( 3, "Version: " + vid );

		return pak, vid

def recoverConfigEnv():
	b = SynStore()
	b.readConfig( SYN_METAFOLDER + "/" + SYN_CONFIG )

	if b.failed:
		noteBad( "We failed to load the config" )# ToDo: Fixme
		return ""
	else:
		note( 2, "Loaded the config " )
		for var in b.data[u"env"]:
			note( 3, var + " = " + b.data[u"env"][var] )
			os.putenv( var, b.data[u"env"][var] )
		flags = ""
		for var in b.data[u"ConfigFlags"]:
			note( 3, var + " = " + b.data[u"ConfigFlags"][var] )
			flags += b.data[u"ConfigFlags"][var] + " "
		note( 2, "Our conf string: " + flags )
		return flags

def getPackageName():
	b = SynStore()
	b.readConfig( SYN_METAFOLDER + "/" + SYN_METAFILE )

	if b.failed:
		noteBad( "We failed to load the config" )# ToDo: Fixme
		return ""
	else:
		name = b.data[u"Name"]
		note( 3, "name    = " + name )
		return name

def getPackageVID():
	b = SynStore()
	b.readConfig( SYN_METAFOLDER + "/" + SYN_METAFILE )

	if b.failed:
		noteBad( "We failed to load the config" )# ToDo: Fixme
		return ""
	else:
		name = b.data[u"Version"]
		note( 3, "version = " + name )
		return name

def recoverBuildEnv():
	b = SynStore()
	b.readConfig( SYN_METAFOLDER + "/" + SYN_CONFIG )

	if b.failed:
		noteBad( "We failed to load the config" )# ToDo: Fixme
		return ""
	else:
		note( 2, "Loaded the config " )
		for var in b.data[u"env"]:
			note( 3, var + " = " + b.data[u"env"][var] )
			os.putenv( var, b.data[u"env"][var] )
		flags = ""
		for var in b.data[u"BuildFlags"]:
			note( 3, var + " = " + b.data[u"BuildFlags"][var] )
			flags += b.data[u"BuildFlags"][var] + " "
		note( 2, "Our build string: " + flags )
		return flags


def runCommand( command, log ):
	LOG_PATH = SYN_METAFOLDER + "/" + SYN_LOG_F + "/" + log

	note( 3, "Running Command `" + command + "`" )

	stat, output = commands.getstatusoutput( command )

	if stat != 0:
		noteBad( "Run Command of `" + command + "` Failed. This is not good." )
		return False

	note( 2, "Saving log of command `" + command + "`" )
	f = open( LOG_PATH, 'w')
	f.write( output )
	f.write( "\n" )
	f.close()
	return True

def runRules( flag ):
	path = SYN_METAFOLDER + "/" + SYN_HOOK_F + "/" + SYN_HOOK_RULES
	if os.path.exists( path ):
		note( 1, "Running rules for `" + flag + "`" )
		return runCommand( path + " " + flag, "rules-" + flag )
	else:
		note( 3, "No rules file" )
		return False


def runHook( flag ):
	path = SYN_METAFOLDER + "/" + SYN_HOOK_F + "/" + flag
	if os.path.exists( path ):
		note( 1, "Running: " + path )
		return runCommand( path + " " + flag, "rules-" + flag )
	else:
		note( 3, flag + " not found" )
		return False


def preConfig():
	flag = SYN_HOOK_PRECONF;
	runHook( flag );

def postConfig():
	flag = SYN_HOOK_POSTCONF;
	runHook( flag );

def preBuild():
	flag = SYN_HOOK_PREBUILD;
	runHook( flag );

def postBuild():
	flag = SYN_HOOK_POSTBUILD;
	runHook( flag );

def prePackage():
	flag = SYN_HOOK_PREPACK;
	runHook( flag );

def postPackage():
	flag = SYN_HOOK_POSTPACK;
	runHook( flag );

def preTemplate():
	flag = SYN_HOOK_PRETEMP;
	runHook( flag );

def postTemplate():
	flag = SYN_HOOK_POSTTEMP;
	runHook( flag );

