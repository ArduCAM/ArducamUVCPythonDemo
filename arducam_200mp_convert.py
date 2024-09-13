import argparse
import numpy as np
import cv2
import os
from arducam_200mp_convert_lib import convert_200mp
from utils import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', type=str, required=True, help='200mp raw images file path or directory path, if it is a directory, please set -b/--batch option')
    parser.add_argument('-c', '--color-order', type=int, required=False, default=1, choices=range(0, len(color_order_list)), help=opencv_color_order_api)
    parser.add_argument('-b', '--batch', action='store_true', required=False, help="if -f/--filepath is a directory, set this option to process all files in the directory")

    args = parser.parse_args()
    filepath = args.filepath
    batch = args.batch
    color_order = color_order_list[args.color_order]
    if not filepath.endswith(".RAW") and not batch:
        raise ValueError("if -b/--batch option is not set, -f/--filepath should be a 200mp raw image file path")

    if batch:
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for root, dirs, files in os.walk(filepath):
            for file in files:
                if file.endswith(".RAW"):
                    data = np.fromfile(os.path.join(root, file), dtype=np.uint8)
                    color = convert_200mp(data, color_order)
                    filename = os.path.basename(file).split(".")[0]
                    print(f"Saving {output_dir}/{filename}.jpg")
                    cv2.imwrite(f"{output_dir}/{filename}.jpg", color)
    else:
        data = np.fromfile(filepath, dtype=np.uint8)
        color = convert_200mp(data, color_order)
        filename = os.path.basename(filepath).split(".")[0]
        print(f"Saving {filename}.jpg")
        cv2.imwrite(f"{filename}.jpg", color)
