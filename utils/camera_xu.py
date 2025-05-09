from enum import IntEnum
from lib.ArducamUvcXU import Devices, i2cWriteReg, i2cReadReg
import numpy as np
import time
from progress.bar import IncrementalBar


class i2c_mode(IntEnum):
    I2C_MODE_8_8 = 1
    I2C_MODE_8_16 = 2
    I2C_MODE_16_8 = 3
    I2C_MODE_16_16 = 4


class CameraXU:
    def __init__(self) -> None:
        self.fd = -1
        self.Device = Devices()
        self.i2c_addr = 0x20
    
    def open(self, device_name):
        for i in self.Device:
            if i["name"] == device_name:
                self.fd = self.Device.open(i["id"])

    def read_eeprom(self, inf_eeprom_data_path="inf_eeprom_data.dat", mac_eeprom_data_path="mac_eeprom_data.dat", eeprom_data_len=4608):
        eeprom_addr = 0xA2
        inf_eeprom_data_reg = 0x3956
        mac_eeprom_data_reg = 0x4B56
        inf_eeprom_data = []
        mac_eeprom_data = []
        bar = IncrementalBar('reading eeprom data ...', max=eeprom_data_len)
        start_time = time.time()
        for i in range(eeprom_data_len):
            inf_eeprom_data.append(self.read_register(eeprom_addr, inf_eeprom_data_reg + i, i2c_mode.I2C_MODE_16_8))
            mac_eeprom_data.append(self.read_register(eeprom_addr, mac_eeprom_data_reg + i, i2c_mode.I2C_MODE_16_8))
            bar.next()
        bar.finish()
        inf_eeprom_data = np.array(inf_eeprom_data, dtype=np.uint8)
        mac_eeprom_data = np.array(mac_eeprom_data, dtype=np.uint8)
        inf_eeprom_data.tofile(inf_eeprom_data_path)
        mac_eeprom_data.tofile(mac_eeprom_data_path)
        print("save eeprom data to file {0} and {1}".format(inf_eeprom_data_path, mac_eeprom_data_path))
        end_time = time.time()
        print("read eeprom data time: {0:.2f}s".format(end_time - start_time))

    def refresh(self):
        self.Device.refresh()
        return ["{0}".format(i["name"]) for i in self.Device]

    def read_register(self, i2c_addr, addr, mode):
        ret, val = i2cReadReg(self.fd, mode, i2c_addr, addr)
        if ret != 0:
            print("Error reading register: ", ret)
            return None
        return val

    def write_register(self, i2c_addr, addr, value, mode):
        i2cWriteReg(self.fd, mode, i2c_addr, addr, value)

    def close(self):
        self.Device.close()
        self.fd = -1