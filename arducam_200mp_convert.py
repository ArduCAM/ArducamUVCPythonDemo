import argparse
import numpy as np
import cv2
import os
from utils.utils import *
import subprocess

def convert_200mp(filepath, color_order):
    width = 16320
    height = 12288
    convert_exe_path = r".\200mp_convert_lib\arducam_200mp_convert.exe"
    inf_eeprom_data_path = "inf_eeprom.dat"
    mac_eeprom_data_path = "mac_eeprom.dat"
    eeprom_data_len = 4608

    basename = os.path.splitext(filepath)[0]
    image_data_raw8 = np.fromfile(filepath, dtype=np.uint8)
    image_data_raw10 = (image_data_raw8.astype(np.uint16) << 2)
    out_raw_path = f"{basename}_raw10"
    image_data_raw10.tofile(f"{out_raw_path}.raw")
    command = [
        convert_exe_path,
        out_raw_path,
        str(width), str(height), str(width), str(height), str(color_order),
        inf_eeprom_data_path, str(eeprom_data_len),
        mac_eeprom_data_path, str(eeprom_data_len),
    ]

    try:
        print("Executing command: {}".format(" ".join(command)))
        start_time = time.time()
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        end_time = time.time()
        print("Command executed successfully!")
        print("Output:")
        print(result.stdout)
        print(f"Conversion time: {end_time - start_time:.2f} seconds")
    except subprocess.CalledProcessError as e:
        print("Error occurred while executing the command:")
        print(e.stderr)
        return -1
    
    out_raw_path = "out_normal.raw"
    data = np.fromfile(out_raw_path, dtype=np.uint8)
    arr = np.frombuffer(data, dtype=np.uint16)
    arr = arr >> 2
    arr = arr.astype(np.uint8)
    image = arr.reshape(height, width, 1)
    image = cv2.cvtColor(image, color_order_list[color_order])
    return image


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', type=str, required=True, help='200mp raw images file path')
    parser.add_argument('-c', '--color-order', type=int, required=False, default=0, choices=range(0, len(color_order_list)), help=opencv_color_order_api)

    args = parser.parse_args()
    filepath = args.filepath
    color_order = args.color_order

    image = convert_200mp(filepath, color_order)
    filename = os.path.basename(filepath).split(".")[0]
    print(f"Saving {filename}.jpg")
    cv2.imwrite(f"{filename}.jpg", image)
