# Marvell FPA

export MRVL_FPA_VERSION = 1.0.1
<<<<<<< HEAD
export MRVL_FPA_TAG = SONiC.201709
=======
export MRVL_FPA_TAG = SONiC.201712
>>>>>>> 6453b3ac1b961bbff5b608bc29f23708cabfcf70
export MRVL_FPA = mrvllibfpa_$(MRVL_FPA_VERSION).deb

$(MRVL_FPA)_SRC_PATH = $(PLATFORM_PATH)/sdk
SONIC_MAKE_DEBS += $(MRVL_FPA)
