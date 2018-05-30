#!/usr/bin/env python

#############################################################################
# Accton
#
# Module contains an implementation of SONiC PSU Base API and
# provides the PSUs status which are available in the platform
#
#############################################################################
import commands
import time
import os.path

try:
    from sonic_psu.psu_base import PsuBase
except ImportError as e:
    raise ImportError (str(e) + "- required module not found")

class PsuUtil(PsuBase):
    """Platform-specific PSUutil class"""

    _present_read_time = 0
    def __init__(self):
        PsuBase.__init__(self)

        self.psu_read_cmd = "i2cget -y 1 0x32 0x10"
        self.psu_presence_bit = [0, 4]
        self.psu_good_bit = [2, 6]
        self.data_present = [0, 0]
        self.data_good = [0, 0]

    def get_num_psus(self):
        return len(self.psu_presence_bit)

    def read_cpld(self):
        start = time.time()
        elapsed = start - self._present_read_time
        if (elapsed < 3):    #not updated within 3 seconds
            return True;
        self._present_read_time = start
        ret, log = commands.getstatusoutput(self.psu_read_cmd)
        print ("log:%s" % log)
        if (ret):
            print("Failed to run cmd:\"%s\" with ret(%d)" % (cmd, ret))
            return ret                
        byte = int(log.rstrip(), 16)
        for i in range(0, len(self.psu_good_bit)):
	    #if powered, it is surely present.	
            bit = byte & (1<<self.psu_good_bit[i])
            self.data_good[i] = not (not bit)
            if (self.data_good[i]):
                self.data_present[i] = self.data_good[i]
            else:
		#0: present, 1: not present.
                bit = byte & (1<<self.psu_presence_bit[i])
                self.data_present[i] = not bit
        return True

    def get_psu_status(self, index):
        if index is None:
            return False

        if (False == self.read_cpld()):
            return False
        else:
            return self.data_good[index-1]

    def get_psu_presence(self, index):
        if index is None:
            return False

        if (False == self.read_cpld()):
            return False
        else:
            return self.data_present[index-1]
