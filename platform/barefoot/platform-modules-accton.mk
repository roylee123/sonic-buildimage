# Accton Platform modules

ACCTON_WEDGE100BF_65X_PLATFORM_MODULE_VERSION = 1.1

export ACCTON_WEDGE100BF_65X_PLATFORM_MODULE_VERSION

ACCTON_WEDGE100BF_65X_PLATFORM_MODULE = sonic-platform-accton-wedge100bf-65x_$(ACCTON_WEDGE100BF_65X_PLATFORM_MODULE_VERSION)_amd64.deb
$(ACCTON_WEDGE100BF_65X_PLATFORM_MODULE)_SRC_PATH = $(PLATFORM_PATH)/sonic-platform-modules-accton
$(ACCTON_WEDGE100BF_65X_PLATFORM_MODULE)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON)
$(ACCTON_WEDGE100BF_65X_PLATFORM_MODULE)_PLATFORM = x86_64-accton_wedge100bf_65x-r0
SONIC_DPKG_DEBS += $(ACCTON_WEDGE100BF_65X_PLATFORM_MODULE)
