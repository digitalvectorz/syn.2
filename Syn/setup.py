"""
All the routeines to take care of setting up a
package template etc.
"""

import Syn
from Syn import output, tools, constants, errors

import os, shutil
import urllib2, urllib


def Dir( path ):
	"""Check if a directory exists"""
	if os.path.exists(path):
		output.log( "Whoh! " + path + " already exists!", 3 )
		return True
	else:
		output.log( path + " does not exist!", 3 )
		return False


def initTemplate(path):
	"""Create a template directory"""
	if Dir( path ):
		output.error( "Whoh! " + path + " already exists! Can't set up template!", 1 )		
	else:
		os.mkdir( path )
		output.success( "Created " + path , 2 )
		tools.cd( path )
		tools.mkshit( constants.SYN_TEMPLATE_LS )
		tools.cd( ".." )

		db = tools.filedb( constants.SYN_TEMPLATE_DIR + constants.SYN_INIT_INFO)
		db.init()

		# SETUP DEM SHIT

		return True

def importFromURL( path ):
	"""`wget` a file"""

	hacker = constants.SYN_DEFAULT_NAME
	email  = constants.SYN_DEFAULT_EMAIL

	output.log("default name / email -- " + hacker + ", " + email, 4 )

	rc = constants.SYN_RC_FILE
	rcfile = os.path.expanduser(rc)
	output.log("Using the RC: " + rcfile, 4)
	if os.path.exists( rcfile ):
		output.log("Found rc file " + rcfile, 3)
		db = tools.filedb( rcfile )
		db.read()
		rcdata = db.data

		hackeroverride = False
		emailoverride  = False
		
		try:
			foo = rcdata['hacker']
			foo = rcdata['email']
		except KeyError:
			output.error( "We have a crap conf file", 3 )
			raise errors.ShittyConfException(rcfile + " sucks ass. Failed loading hacker / email")

		if rcdata['hacker']:
			hacker = rcdata['hacker']
			hackeroverride = True

		if rcdata['email']:
			email = rcdata['email']
			emailoverride = True
	else:
		output.log("MISSING! " + rcfile, 3)

	ids = tools.figureOutName( path )
	package = ids['pkg']
	cont = True;

	if package != "":
		output.log( "Detected package: " + package, 2 )
	else:
		output.log( "Package Detection Failure! Fix the package name!", 2 )
		package = "default"
		cont = False

	version = ids['ver']
	if version != "":
		output.log( "Detected version: " + version, 2 )
	else:
		output.log( "Version Detection Failure! Fix the package name!", 2 )
		version = "0.0"
		cont = False
	if cont:
		if Dir( package ):
			output.error( "Whoh! " + package + " already exists! Can't contiue with " + package, 1 )		
			return False
		else:
			package     = output.query("Package Name   ", package, 1 )
			version     = output.query("Package Version", version, 1 )

			maintainer  = output.query("Packager Name  ", hacker,  3 )
			maint_email = output.query("Packager Email ", email,   3 )

			output.log( "Setting up pkg directory", 2 )
			os.mkdir( package )
			tools.cd( package )

			if initTemplate( constants.SYN_TEMPLATE_DIR ):
				output.success( "Created template", 2 )

				db = tools.filedb(constants.SYN_TEMPLATE_DIR + constants.SYN_PKG_INFO )
				db.init()

				db.setInfo( "pkg",   package     )
				db.setInfo( "ver",   version     )
				db.setInfo( "maint", maintainer  )
				db.setInfo( "email", maint_email )

				output.log( "getting remote file",  2 )
				try:
					opener = urllib2.build_opener()
					page = opener.open( path )
					tgz = page.read()
					outout = os.path.basename( path ).strip()
					output.log( "Writing file out to " + outout, 2 )
					archive = file( outout, "w" )
					archive.write( tgz )
					archive.close()

					db = tools.filedb(constants.SYN_TEMPLATE_DIR + constants.SYN_DOWNLOAD_INFO )
					db.init()
					db.setInfo( "filename", os.path.basename( path ).strip() )
					db.setInfo( "md5sum",   tools.md5sum( os.path.basename( path ).strip() ) )

					rc = constants.SYN_RC_FILE
					rcfile = os.path.expanduser(rc)
					db = tools.filedb( rcfile )
					db.read()
					rcinfo = db.data

					try:
						foo = rcinfo['env']
					except KeyError:
						output.error( "We have a crap conf file", 3 )
						raise ShittyConfException(rcfile + " sucks ass. Failed loading ENV")

					db = tools.filedb(constants.SYN_TEMPLATE_DIR + constants.SYN_BUILD_INFO  )
					db.init()

					if rcinfo != None:
						output.log( "Moving over build defauls from RC ", 2 )
						db.setInfo( "env",         rcinfo['env']           )
						db.setInfo( "ConfigFlags", rcinfo['ConfigFlags']   )
						db.setInfo( "BuildFlags",  rcinfo['BuildFlags']    )

					output.success( "Downloaded: " + package, 1 )

				except urllib2.URLError:
					output.error( "Failed to fetch " + package + "!", 0 )
			else:
				output.error( "Template creation failed!", 0 )
			tools.cd( ".." )
			return package
	else:
		return False

