# python-saithrift package

PYTHON_SAITHRIFT_BFN = python-saithrift_0.9.4_amd64.deb
$(PYTHON_SAITHRIFT_BFN)_SRC_PATH = $(SRC_PATH)/SAI
$(PYTHON_SAITHRIFT_BFN)_DEPENDS += $(BFN_SAI_DEV) $(BFN_SAI) $(THRIFT_COMPILER) $(PYTHON_THRIFT) $(LIBTHRIFT_DEV)
#SONIC_DPKG_DEBS += $(PYTHON_SAITHRIFT_BFN)
