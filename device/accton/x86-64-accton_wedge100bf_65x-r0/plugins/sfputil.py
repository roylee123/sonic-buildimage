# sfputil.py
#
# Platform-specific SFP transceiver interface for SONiC
#
import commands
import time

try:
    import time
    from sonic_sfp.sfputilbase import SfpUtilBase
except ImportError as e:
    raise ImportError("%s - required module not found" % str(e))


class SfpUtil(SfpUtilBase):
    """Platform-specific SfpUtil class"""

    PORT_START = 0
    PORT_END = 63
    PORTS_IN_BLOCK = 64
    QSFP_PORT_START = 64
    QSFP_PORT_END = 64

    BASE_VAL_PATH = "/sys/class/i2c-adapter/i2c-{0}/{1}-0050/"

    _port_to_is_present = {}

    _port_to_eeprom_mapping = {}
    _port_to_i2c_mapping = {
         0: [33,33],
         1: [34,34],
         2: [31,31],
         3: [32,32],
         4: [29,29],
         5: [30,30],
         6: [27,27],
         7: [28,28],
         8: [25,25],
         9: [26,26],
        10: [23,23],
        11: [24,24],
        12: [21,21],
        13: [22,22],
        14: [19,19],
        15: [20,20],
        16: [17,17],
        17: [18,18],
        18: [15,15],
        19: [16,16],
        20: [13,13],
        21: [14,14],
        22: [11,11],
        23: [12,12],
        24: [ 9, 9],
        25: [10,10],
        26: [ 7, 7],
        27: [ 8, 8],
        28: [ 5, 5],
        29: [ 6, 6],
        30: [ 3, 3],
        31: [ 4, 4],
        32: [73,73],
        33: [74,74],
        34: [71,71],
        35: [72,72],
        36: [69,69],
        37: [70,70],
        38: [67,67],
        39: [68,68],
        40: [65,65],
        41: [66,66],
        42: [63,63],
        43: [64,64],
        44: [61,61],
        45: [62,62],
        46: [59,59],
        47: [60,60],
        48: [57,57],
        49: [58,58],
        50: [55,55],
        51: [56,56],
        52: [53,53],
        53: [54,54],
        54: [51,51],
        55: [52,52],
        56: [49,49],
        57: [50,50],
        58: [47,47],
        59: [48,48],
        60: [45,45],
        61: [46,46],
        62: [43,43],
        63: [44,44] }

    _sfp_bitmap =  [             
		30, 31, 28, 29, 26, 27, 24, 25,
		22, 23, 20, 21, 18, 19, 16, 17,
		14, 15, 12, 13, 10, 11,  8,  9,
		 6,  7,  4,  5,  2,  3,  0,  1,
		62, 63, 60, 61, 58, 59, 56, 57,
		54, 55, 52, 53, 50, 51, 48, 49,
		46, 47, 44, 45, 42, 43, 40, 41,
		38, 39, 36, 37, 34, 35, 32, 33]
    _present_bits = 0
    _present_read_time = 0

    @property
    def port_start(self):
        return self.PORT_START

    @property
    def port_end(self):
        return self.PORT_END

    @property
    def qsfp_ports(self):
        return range(self.QSFP_PORT_START, self.PORTS_IN_BLOCK + 1)

    @property
    def port_to_eeprom_mapping(self):
        return self._port_to_eeprom_mapping

    @property
    def port_to_i2cbus_mapping(self):
        return self._port_to_i2c_mapping

    def __init__(self):
        eeprom_path = self.BASE_VAL_PATH + "eeprom"

        for x in range(0, self.port_end+1):
            self.port_to_eeprom_mapping[x] = eeprom_path.format(
                self._port_to_i2c_mapping[x][0], 
                self._port_to_i2c_mapping[x][1])

        SfpUtilBase.__init__(self)


    def get_pca9535(self):
        bit_array = 0
        pca535_cmds = [ 
                      "i2cget -y 78 0x23 0 w",
                      "i2cget -y 77 0x22 0 w", 
                      "i2cget -y 38 0x23 0 w", 
                      "i2cget -y 37 0x22 0 w",
    		  ]
        start = time.time()
	elapsed = start - self._present_read_time
        if (elapsed < 5):    #not updated within 5 seconds
	    return self._present_bits;

	self._present_read_time = start  
        for cmd in pca535_cmds:
            ret, log = commands.getstatusoutput(cmd)  
            if (ret):
                print("Failed to run cmd:\"%s\" with ret(%d)" % (cmd, ret))     
    	        return ret
            bit_array = bit_array << 16;
    	    bit_array = bit_array | int(log.rstrip(), 16)
    
	self._present_bits = bit_array
        return bit_array

    def get_presence(self, port_num):
        # Check for invalid port_num
        if port_num < self.port_start or port_num > self.port_end:
            return False
	bits = self.get_pca9535()
	#print("BIT: %x" % bit_array)

	pst =  (bits >> self._sfp_bitmap[port_num]) & 1
        pst = not pst      #present is low-active signal
        return pst

    def get_low_power_mode(self, port_num):
        raise NotImplementedError

    def set_low_power_mode(self, port_num, lpmode):
        raise NotImplementedError

    def reset(self, port_num):
        raise NotImplementedError
