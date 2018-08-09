# Marvell SAI

export MRVL_SAI_VERSION = 1.0.1
<<<<<<< HEAD
export MRVL_SAI_TAG = SONiC.201709
=======
export MRVL_SAI_TAG = SONiC.201712
>>>>>>> 6453b3ac1b961bbff5b608bc29f23708cabfcf70
export MRVL_SAI = mrvllibsai_$(MRVL_SAI_VERSION).deb

$(MRVL_SAI)_SRC_PATH = $(PLATFORM_PATH)/sai
$(MRVL_SAI)_DEPENDS += $(MRVL_FPA)
SONIC_MAKE_DEBS += $(MRVL_SAI)
