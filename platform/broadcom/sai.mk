<<<<<<< HEAD
BRCM_SAI = libsaibcm_2.3.0.5-2_amd64.deb
$(BRCM_SAI)_URL = "https://sonicstorage.blob.core.windows.net/packages/libsaibcm_2.3.0.5-2_amd64.deb?sv=2015-04-05&sr=b&sig=5Q1rbpPp0EtyJtbb1Y5LM%2FBRAKmvy8moXAFuLj47xTM%3D&se=2031-06-05T21%3A50%3A55Z&sp=r"

BRCM_SAI_DEV = libsaibcm-dev_2.3.0.5-2_amd64.deb
$(eval $(call add_derived_package,$(BRCM_SAI),$(BRCM_SAI_DEV)))
$(BRCM_SAI_DEV)_URL = "https://sonicstorage.blob.core.windows.net/packages/libsaibcm-dev_2.3.0.5-2_amd64.deb?sv=2015-04-05&sr=b&sig=%2BaLb2myxvGPmhIVL%2FZGOEi%2FxW9nSMVB7ZTa%2BzSTufOc%3D&se=2031-06-05T21%3A52%3A24Z&sp=r"
=======
BRCM_SAI = libsaibcm_3.0.3.3-3_amd64.deb
$(BRCM_SAI)_URL = "https://sonicstorage.blob.core.windows.net/packages/libsaibcm_3.0.3.3-3_amd64.deb?sv=2015-04-05&sr=b&sig=A%2Bcq%2B8XL%2BZfhOV6zqwRWm1jQ31PN0t54H9abZSRwTVw%3D&se=2031-09-25T22%3A41%3A43Z&sp=r"

BRCM_SAI_DEV = libsaibcm-dev_3.0.3.3-3_amd64.deb
$(eval $(call add_derived_package,$(BRCM_SAI),$(BRCM_SAI_DEV)))
$(BRCM_SAI_DEV)_URL = "https://sonicstorage.blob.core.windows.net/packages/libsaibcm-dev_3.0.3.3-3_amd64.deb?sv=2015-04-05&sr=b&sig=XT0v%2B25LZ5whTwH%2FE%2FykQLV8Kzn%2FoDyLNXjmqNuiFPo%3D&se=2031-09-25T22%3A41%3A21Z&sp=r"
>>>>>>> 6453b3ac1b961bbff5b608bc29f23708cabfcf70

SONIC_ONLINE_DEBS += $(BRCM_SAI) $(BRCM_SAI_DEV)
$(BRCM_SAI_DEV)_DEPENDS += $(BRCM_SAI)
