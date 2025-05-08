from enum import IntEnum
from ArducamUvcXU import Devices, i2cWriteReg, i2cReadReg
import numpy as np


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

    def read_eeprom(self):
        eeprom_addr = 0xA2
        inf_eeprom_data_reg = 0x3956
        mac_eeprom_data_reg = 0x4B56
        eeprom_data_len = 4608
        inf_eeprom_data = []
        mac_eeprom_data = []
        for i in range(eeprom_data_len):
            inf_eeprom_data.append(self.read_register(eeprom_addr, inf_eeprom_data_reg + i, i2c_mode.I2C_MODE_16_8))
            mac_eeprom_data.append(self.read_register(eeprom_addr, mac_eeprom_data_reg + i, i2c_mode.I2C_MODE_16_8))
        inf_eeprom_data = np.array(inf_eeprom_data, dtype=np.uint8)
        mac_eeprom_data = np.array(mac_eeprom_data, dtype=np.uint8)
        inf_eeprom_data.tofile("inf_eeprom_data.dat")
        mac_eeprom_data.tofile("mac_eeprom_data.dat")

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

if __name__ == "__main__":
    camera = CameraXU()
    camera_names = camera.refresh()
    print("all camera names: ", camera_names)
    print("open camera: ", camera_names[0])
    camera.open(camera_names[0])
    camera.read_eeprom()
    camera.close()
