#!/usr/bin/env python

try:
    import os
    import time
    import cPickle as pickle
    import pprint
    import fcntl
    import subprocess
    from sonic_sfp.sfputilbase import SfpUtilBase 
except ImportError, e:
    raise ImportError (str(e) + "- required module not found")

#from xcvrd
SFP_STATUS_INSERTED = '1'
SFP_STATUS_REMOVED = '0'
GET_HWSKU_CMD = "sonic-cfggen -d -v DEVICE_METADATA.localhost.hwsku"

class Lock(object):
    """File Locking class."""
    def __init__(self, filename):
        self.filename = filename
        self.handle = open(filename, 'w')

    def take(self):
        # logger.debug("taking lock %s" % self.filename)
        fcntl.flock(self.handle, fcntl.LOCK_EX)
        # logger.debug("took lock %s" % self.filename)

    def give(self):
        fcntl.flock(self.handle, fcntl.LOCK_UN)
        # logger.debug("released lock %s" % self.filename)

    def __enter__(self):
        self.take()

    def __exit__(self ,type, value, traceback):
        self.give()

    def __del__(self):
        self.handle.close()


class SfpUtil(SfpUtilBase):
    """Platform specific SfpUtill class"""

    _port_start = 0
    _port_end = 63
    ports_in_block = 64



    _port_to_eeprom_mapping = {}
    port_to_i2c_mapping = {
        61 : 25,
        62 : 26,
        63 : 27,
        64 : 28,
        55 : 29,
        56 : 30,
        53 : 31,
        54 : 32,
        9  : 33,
        10 : 34,
        11 : 35,
        12 : 36,
        1  : 37,
        2  : 38,
        3  : 39,
        4  : 40,
        6  : 41,
        5  : 42,
        8  : 43,
        7  : 44,
        13 : 45,
        14 : 46,
        15 : 47,
        16 : 48,
        17 : 49,
        18 : 50,
        19 : 51,
        20 : 52,
        25 : 53,
        26 : 54,
        27 : 55,
        28 : 56,
        29 : 57,
        30 : 58,
        31 : 59,
        32 : 60,
        21 : 61,
        22 : 62,
        23 : 63,
        24 : 64,
        41 : 65,
        42 : 66,
        43 : 67,
        44 : 68,
        33 : 69,
        34 : 70,
        35 : 71,
        36 : 72,
        45 : 73,
        46 : 74,
        47 : 75,
        48 : 76,
        37 : 77,
        38 : 78,
        39 : 79,
        40 : 80,
        57 : 81,
        58 : 82,
        59 : 83,
        60 : 84,
        49 : 85,
        50 : 86,
        51 : 87,
        52 : 88,}

    _qsfp_ports = range(0, ports_in_block + 1)

    @property
    def cache_file_name(self):
        p = subprocess.Popen(GET_HWSKU_CMD, shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()
        cache = os.path.join('/tmp/.sfputil.cache.%s' % out.rstrip())
        return cache

    @property
    def get_transceiver_status(self):
        node = "/sys/bus/i2c/devices/19-0060/module_present_all"
        try:
            reg_file = open(node)

        except IOError as e:
            print "Error: unable to open file: %s" % str(e)
            return False
        bitmap = reg_file.readline().rstrip()
        reg_file.close()
        rev = bitmap.split(" ")
        rev = "".join(rev[::-1])
        return int(rev,16)

    def _load_cache(self, cache):
        with Lock(cache + ".lock"):
           if os.path.exists(cache):
               #print("Loading from package cache %s" % cache)
               data = pickle.load(open(cache, "rb"))
               return data
        return

    def _save_cache(self, cache, data):
        with Lock(cache + ".lock"):
           pickle.dump(data, open(cache, "wb"))
           return


    def get_transceiver_change_event(self, timeout=3000):
        now = time.time()
        port_dict = {}
        port = self.port_start
        data = {'valid':0, 'last':0, 'present':0} 

        if timeout < 1000:
            timeout = 1000
        timeout = (timeout) / float(1000) # Convert to secs

        cache = self.cache_file_name
        if os.path.exists(cache):
            data = self._load_cache(cache)

        if now < (data['last'] + timeout) and data['valid']:
            return True, {}

        reg_value = self.get_transceiver_status
        changed_ports = data['present'] ^ reg_value
        if changed_ports:
            while port >= self.port_start and port <= self.port_end:
                # Mask off the bit corresponding to our port
                mask = (1 << port)
                if changed_ports & mask:
                    # ModPrsL is active low
                    if reg_value & mask == 0:
                        port_dict[port] = SFP_STATUS_INSERTED
                    else:
                        port_dict[port] = SFP_STATUS_REMOVED
                port += 1

            # Update cache 
            data['present'] = reg_value
            data['last'] = now
            data['valid'] = 1
            self._save_cache(cache, data)

            pprint.pprint(port_dict)
            return True, port_dict
        else:
            return True, {}
        return False, {}

    def __init__(self):
        eeprom_path = '/sys/bus/i2c/devices/{0}-0050/eeprom'
        for x in range(0, self._port_end + 1):
            port_eeprom_path = eeprom_path.format(self.port_to_i2c_mapping[x+1])
            self._port_to_eeprom_mapping[x] = port_eeprom_path
        SfpUtilBase.__init__(self)
        #self.modprs_register = self.get_transceiver_status
        #status, port_dict = self.get_transceiver_change_event()
	#print "s:%d"%(status)
        #pprint.pprint(port_dict)

    def reset(self, port_num):
        # Check for invalid port_num
        if port_num < self._port_start or port_num > self._port_end:
            return False

        path = "/sys/bus/i2c/devices/19-0060/module_reset_{0}"
        port_ps = path.format(port_num+1)
          
        try:
            reg_file = open(port_ps, 'w')
        except IOError as e:
            print "Error: unable to open file: %s" % str(e)
            return False

        #HW will clear reset after set.
        reg_file.seek(0)
        reg_file.write('1')
        reg_file.close()
        return True

    def set_low_power_mode(self, port_nuM, lpmode):
        raise NotImplementedError

    def get_low_power_mode(self, port_num):
        raise NotImplementedError
        
    def get_presence(self, port_num):
        # Check for invalid port_num
        if port_num < self._port_start or port_num > self._port_end:
            return False

        path = "/sys/bus/i2c/devices/19-0060/module_present_{0}"
        port_ps = path.format(port_num+1)
          
        try:
            reg_file = open(port_ps)
        except IOError as e:
            print "Error: unable to open file: %s" % str(e)
            return False

        reg_value = reg_file.readline().rstrip()
        if reg_value == '1':
            return True

        return False

    @property
    def port_start(self):
        return self._port_start

    @property
    def port_end(self):
        return self._port_end
        
    @property
    def qsfp_ports(self):
        return range(0, self.ports_in_block + 1)

    @property 
    def port_to_eeprom_mapping(self):
         return self._port_to_eeprom_mapping


