#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

POLICY_VERSION = 2

META_REQUIRED = [
	"package",
	"version",
	"build-deps",
	"deps",
	"description",
	"download",
	"local",
	"policy",
	"maintainer"
]

META_NEEDED = [
	"license",
	"vcs"
]

META_GOODTOHAVE = [
	"upstream-vcs",
	"upstream-bugtracker"
]

LICENSE_CLEAN = [
	"GPL",
	"GPL-1",
	"GPL-2",
	"GPL-3",
	"X11",
	"MIT",
	"PSFL-2"
]

LICENSE_TAINT = [
	"nonfree"
]


# Do *not* let messages get longer then this handy ruler.
# Please. I'll kill you.
# |---------------------------------------------------------------------------|

DESCRS = {
	"package"             :
"""
This field is the Package name.
 Given the source tarball `fluxbox-1.0', the package name is simply `fluxbox'.
 This field is required as it is used internally to generate tarball names
 and the like. Bear in mind that if (in the case of Python) the tarball does
 not match the package name, it's not the end of the world. Python may have
 `Python-n.m.tar.gz' as the source, but the package name is `python'.

 Please keep this field in line with the standards (and unique!).
""",
	"version"             :
"""
This field is the Package version number.
 Given the source tarball `fluxbox-1.0', the package version is just `1.0'.
 This field is required as it is used internally to generate tarball names
 and the like. Please keep this version number identical to the upstream
 source's ID. This is unlike the `package' attribute, which may differ.
""",
	"build-deps"          :
"""
This field tells syn which packages are needed to build the sourceball.
 The base development package will be installed before a build, so please
 don't worry about packages such as `gcc' or `make'. These should be unique
 to your package, such as `ncurses' or `x11'.

 Just because a package is in the build-deps does not mean it's put into the
 deps. Remember, you might have packages only used in setting up the package
 (such as `sed' or `awk'). 
""",
	"deps"                :
"""
This field tells syn which packages are needed to run the package on the host.
 By defining a package in this field, you are declaring that it must be
 installed and linked before this package. These should be runtime dependencies
 only, what is needed to run the package.
""",
	"description"         :
"""
This field is a human-readable description of what the package does.
 It's required to have a description for a package. This is because even the
 most hardcore UNIX nerd needs to look up exactly what a package does on
 occasion.

 This field must be one complete sentience in American English. Stupid
 conventions, such as putting the punctuation out of order may be ignored
 if the author feels it prudent. The following example is OK:
   I think that using punctuation outside of parenthesis is dumb (like this).

 That, however, is optional.
""",
	"download"            :
"""
This field is the *full* URL of an authoritative host, hosting the package.
 If, as example, you have downloaded the package `nullop-1.0' from pault.ag
 (the author of the package, so his domain is clearly trusted), one valid
 URL (if this URL is valid, of course) would be:
   http://nullop.pault.ag/download/nullop-1.0.tar.gz

 This field is used internally to resolve the source tarball name.
""",
	"local"               :
"""
This field is the local version of the package.
 This is the local syn version of the package. Since most packages are external
 to the syn development cycle, it makes sense to keep track of changes to the
 synd folder in this version ID. When you make a change to the synd (e.g. 
 maintainer, build steps, policy updates), this should be incremented to 
 ensure that the new package overrides the old one (without klobbering
 upstream's version IDs). Please reset this to '1' after every new release.
""",
	"policy"              :
"""
This field is the version of the standards in place. 
 Syn changes policy as often as needs to be done to maintain a sane build system
 for package maintainers. Fields are added, removed, and scripts get changed. As
 a result, we need to version the policy version ID of the system. You need this
 field to ensure that you are:
  * Following the up-to-date standards
  * Getting error messages on new fields or features
  * Ready for migration to new tools without backwards compatibility
  * Active ;)
""",
	"policy-outofdate"    :
"""
The policy version in this package is out of date.
 Please check to see what the changes are since the last policy version, and
 update your package accordingly. This is critical! Keep up to date and get
 virtual hugs!
""",
	"policy-missing-version"    :
"""
The policy version tag is missing a value.
 This sucks ass. We can't even check to see what version of the policy that this
 package is to adhere to. Please add the tag. Most of the time, this is also
 showing up below a policy missing error. Fix this, plox.
""",
	"maintainer"          :
"""
This field is used to maintain a record of who is currently in charge of it.
 This field needs to be composed of a dict, with two members, when combined
 with angle brackets compose a valid RFC822 email address.

 If, as example, the hacker "John Q. Hacker" with the email address of
 jhacker@example.com submits a package, the maintainer field should be in the
 following format (JSON, as all fields in the metafile are):

   "maintainer": {
       "email" : "jhacker@example.com",
       "name"  : "John Q. Hacker"
   }

 The order and spacing may vary. As you can see, when composed, the valid
 address "John Q. Hacker <jhacker@example.com>" is composed.
""",
	"vcs"                 :
"""
This field is to maintain a record of where the maintainer's branch is kept.
 This field needs to be composed of three fields in a simple dict. 

 The three fields are `type', `co-url' and `browse'. 
  * type   dictates what flavor of VCS is being used.
  * co-url is a valid anonymous checkout URL
  * browse is a valid URL to browse the contents of the VCS
    in a sane way. Apps like `gitweb' are great for this.

   "vcs" : {
     "type" : "git",
     "co-url" : "git://example.com/repo.git",
     "browse" : "http://git.example.com/?a=summary&p=repo"
   }
""",
	"license"             :
"""
Arguably the most complex field in the metainf, this field tracks licensing.
 Here's an example of a sane entry.

 "license" : {
   "*" : {
     "terms"  : "GPL-3",
     "author" : "Joe Shmo, et. al"
   },
   "synd/*" : {
     "terms"  : "GPL-3",
     "author" : "John Q. Hacker"
   }
 }

 keep in mind that this is for the source extract layout:
  package-1.0/    package-1.0.tar.gz    synd/

 This will cause (because it's processed from the top down) Joe Shmo to
 own license to all code, except synd/*, since that is the work of
 John Q. Hacker.

 In the event that there is more then one author, use "et. al". In the event
 that a package has no primary author, please use either "Package Team", or
 a list of all the authors. Using "Package Team" is much preferred.
""",
	"upstream-vcs"        :
"""
This field is the location of the upstream Version Control system.
 This field should be in the same format as the `vcs' attribute. 
""",
	"upstream-bugtracker" :
"""
This field is the homepage location of the upstream bugtracker.
 If the package uses a big ole' bugtracker like Launchpad, please
 include the full path to it's homepage.
"""
}
