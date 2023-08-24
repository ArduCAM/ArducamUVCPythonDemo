import argparse
import re
import cv2
import time

selector_list = [
    cv2.CAP_ANY,
    cv2.CAP_MSMF,
    cv2.CAP_DSHOW,
]

VideoCaptureAPIs = """opencv VideoCaptureAPIs
0: cv2.CAP_ANY
1: cv2.CAP_MSMF
2: cv2.CAP_DSHOW"""

def display_fps(frame):
    display_fps.frame_count += 1

    current = time.monotonic()
    if current - display_fps.start >= 1:
        print(f"width: {frame.shape[1]} height: {frame.shape[0]} fps: {display_fps.frame_count}")
        display_fps.frame_count = 0
        display_fps.start = current

def validate_windows_size(windows_size):
    pattern = r'^\d{3,4}:\d{3,4}$'
    if not re.match(pattern, windows_size):
        raise argparse.ArgumentTypeError("Invalid windows args. Expected format: <width>:<height>")
    return windows_size