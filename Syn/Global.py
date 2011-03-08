#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

WORKDIR         = "/tmp/syn/" # where to unpack & build

# binary package root
ARCHIVE_FS_ROOT_NOSLASH = "syn"
ARCHIVE_FS_ROOT = ARCHIVE_FS_ROOT_NOSLASH + "/"

BUILD_FS_ROOT   = "build/"    # build build folder

INSTALL_ROOT_PATH = "/syn/"         # install all packages here
SYNDB = INSTALL_ROOT_PATH + "pkgdb" # "database"
LOCKF = INSTALL_ROOT_PATH + ".lock" # lock

SYN_BIN_PKG_XTN     = "syn"         # pkg-1.0.BIN_PKG
SYN_SRC_PKG_XTN     = "syn.tar.gz"  # pkg-1.0.SRC_PKG

SYN_SRC_DIR         = "synd/"

SYN_BUILDDIR_SCRIPT = "build"      # build "rules" file
SYN_BUILDDIR_CONFIG = "buildrc"    # build config file (flags)
SYN_BUILDDIR_META   = "meta"       # metafile (control file)
SYN_BUILDDIR_MPKG   = "multipkg"   # multipkg file for more then one
#                                    binary package

SYN_SRC_LOAD_ON_LOAD = [
	SYN_SRC_DIR + SYN_BUILDDIR_CONFIG,
	SYN_SRC_DIR + SYN_BUILDDIR_META,
	# SYN_SRC_DIR + SYN_BUILDDIR_MPKG
]

SYN_BINARY_FILESUMS  = ".filesums"  # MD5 sums
SYN_BINARY_META      = ".meta-syn"  # binary metafile package location
#                                    (in the archive)

SYN_BIN_LOAD_ON_LOAD = [
	SYN_BINARY_FILESUMS,
	SYN_BINARY_META
]

SYN_SRC_TO_BIN_FILESPEC = {
	SYN_SRC_DIR + SYN_BUILDDIR_META : ARCHIVE_FS_ROOT + SYN_BINARY_META
}

SYN_XTRACT_META      = "metainf"    # metainf in the filesystem
SYN_XTRACT_SUMS      = "filesums"   # filesums

SYN_BIN_TO_XTRACT = {
	ARCHIVE_FS_ROOT + SYN_BINARY_META     : SYN_XTRACT_META,
	ARCHIVE_FS_ROOT + SYN_BINARY_FILESUMS : SYN_XTRACT_SUMS
}

CONFIG_FLAGS = "CONFIG_FLAGS"
BUILD_FLAGS  = "BUILD_FLAGS"
STAGE_FLAGS  = "STAGE_FLAGS"
CONFIG       = "CONFIGURE"
BUILD        = "BUILD"
STAGE        = "STAGE"
DESTDIR      = "S_DESTDIR"

