#
# Copyright (c) Paul Tagliamonte
# GNU GPL-3+, 2011
#

configure::
	$(CONFIGURE) $(CONFIG_FLAGS)

build::
	$(BUILD) $(BUILD_FLAGS)
ifdef BUILD_CHECK
		$(BUILD_CHECK) $(BUILD_CHECK_FLAGS)
endif

stage::
	$(STAGE) $(STAGE_FLAGS) DESTDIR=$(S_DESTDIR)
