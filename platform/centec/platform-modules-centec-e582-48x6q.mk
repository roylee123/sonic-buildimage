# Centec E582-48X6Q Platform modules

CENTEC_E582_48X6Q_PLATFORM_MODULE_VERSION = 1.0

export CENTEC_E582_48X6Q_PLATFORM_MODULE_VERSION

CENTEC_E582_48X6Q_PLATFORM_MODULE = platform-modules-e582-48x6q_$(CENTEC_E582_48X6Q_PLATFORM_MODULE_VERSION)_amd64.deb
$(CENTEC_E582_48X6Q_PLATFORM_MODULE)_SRC_PATH = $(PLATFORM_PATH)/sonic-platform-modules-e582
$(CENTEC_E582_48X6Q_PLATFORM_MODULE)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON)
$(CENTEC_E582_48X6Q_PLATFORM_MODULE)_PLATFORM = x86_64-centec_e582_48x6q-r0
SONIC_DPKG_DEBS += $(CENTEC_E582_48X6Q_PLATFORM_MODULE)
