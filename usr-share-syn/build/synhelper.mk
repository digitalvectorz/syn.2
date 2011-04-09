#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

configure::
ifdef PATCH_SOURCE
	sh_patch
endif
ifdef CFLAGS
	CONF_PREFIX=$(C_PREFIX) CFLAGS=$(CFLAGS)
endif
	$(CONF_PREFIX) $(CONFIGURE) $(CONFIG_FLAGS)

build::
	$(BUILD) $(BUILD_FLAGS)
ifdef BUILD_CHECK
	$(BUILD_CHECK) $(BUILD_CHECK_FLAGS)
endif

stage::
	$(STAGE) $(STAGE_FLAGS) DESTDIR=$(S_DESTDIR)
ifdef STRIP_SOURCE
	cd $(S_DESTDIR) && sh_strip
endif
