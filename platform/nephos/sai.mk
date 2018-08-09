<<<<<<< HEAD
NEPHOS_SAI = libsainps_2.0.1-20171020_amd64.deb
$(NEPHOS_SAI)_URL = "https://github.com/NephosInc/SONiC/raw/v0.94/sai/libsainps_2.0.1-20171020_amd64.deb"

NEPHOS_SAI_DEV = libsainps-dev_2.0.1-20171020_amd64.deb
$(eval $(call add_derived_package,$(NEPHOS_SAI),$(NEPHOS_SAI_DEV)))
$(NEPHOS_SAI_DEV)_URL = "https://github.com/NephosInc/SONiC/raw/v0.94/sai/libsainps-dev_2.0.1-20171020_amd64.deb"
=======
NEPHOS_SAI = libsainps_2.0.2-20171204_amd64.deb
$(NEPHOS_SAI)_URL = "https://github.com/NephosInc/SONiC/raw/master/sai/libsainps_2.0.2-20171204_amd64.deb"

NEPHOS_SAI_DEV = libsainps-dev_2.0.2-20171124_amd64.deb
$(eval $(call add_derived_package,$(NEPHOS_SAI),$(NEPHOS_SAI_DEV)))
$(NEPHOS_SAI_DEV)_URL = "https://github.com/NephosInc/SONiC/raw/master/sai/libsainps-dev_2.0.2-20171124_amd64.deb"
>>>>>>> 6453b3ac1b961bbff5b608bc29f23708cabfcf70

SONIC_ONLINE_DEBS += $(NEPHOS_SAI) $(NEPHOS_SAI_DEV)
$(NEPHOS_SAI_DEV)_DEPENDS += $(NEPHOS_SAI)
