import cv2
import argparse

import numpy as np
from camera import Camera
from isp import arducam108mp_isp
from utils import *
import json
from rich import print

display_fps.start = time.monotonic()
display_fps.frame_count = 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-W', '--width', type=int, required=False, default=0, help='set camera image width')
    parser.add_argument('-H', '--height', type=int, required=False, default=0, help='set camera image height')
    parser.add_argument('-d', '--DisplayWindow', type=validate_windows_size, required=False, default="800:600", help='Set the display window size, <width>:<height>')
    parser.add_argument('-f', '--FrameRate', type=int, required=False, default=0, help='set camera frame rate')
    parser.add_argument('-F', '--Focus', action='store_true', required=False, help='Add focus control on the display interface')
    parser.add_argument('-i', '--index', type=int, required=False, default=0, help='set camera index')
    parser.add_argument('-v', '--VideoCaptureAPI', type=int, required=False, default=0, choices=range(0, len(selector_list)), help=VideoCaptureAPIs)
    parser.add_argument('-o', '--OutputPath', type=str, required=False, help="set save image path")
    parser.add_argument('-t', '--reStartTimes', type=int, required=False, default=5, help="restart camera times")
    parser.add_argument('--ccm', action='store_true', required=False, help="add color correction")
    parser.add_argument('--tuning-file', type=str, required=False, help="tuning file path")
    parser.add_argument('--wait-frames', type=int, required=False, default=5, help="Wait a few frames to save 108mp image")

    args = parser.parse_args()
    width = args.width
    height = args.height
    view_window = [int(i) for i in args.DisplayWindow.split(":")]
    index = args.index
    fps = args.FrameRate
    focus = args.Focus
    output_path = args.OutputPath
    restart_times = args.reStartTimes
    ccm = args.ccm
    tuning_file_path = args.tuning_file
    selector = selector_list[args.VideoCaptureAPI]
    wait_frames = args.wait_frames


    cap = Camera(index, selector)
    cap.set_width(width)
    cap.set_height(height)
    cap.set_fps(fps)
    cap.open()

    if not cap.isOpened():
        print("Can't open camera")
        exit()

    cv2.namedWindow("video", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("video", view_window[0], view_window[1])
    
    if focus:
        cv2.createTrackbar('Focus', 'video', 187, 1023, cap.set_focus)

    if width == 6000 and height == 9000:
        cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)

    ccm_list = []
    if tuning_file_path:
        tuning_file = json.load(open(tuning_file_path, "r"))
        ccm_list = tuning_file["ccms"]
    
    if not output_path:
        output_path = f"{width}x{height}.jpg"

    while True:
        ret, frame = cap.read()

        if not ret:
            if restart_times != 0:
                print("Unable to read video frame")
                success = False
                for i in range(1, restart_times + 1):
                    print(f"reopen {i} times")
                    try:
                        cap.reStart()
                        success = True
                        break
                    except:
                        continue
                if success:
                    continue
                else:
                    print("reopen failed")
        
        if width == 6000 and height == 9000:
            frame = arducam108mp_isp(frame.reshape(9000, 12000), ccm, ccm_list)

        display_fps(frame)
        cv2.imshow("video", frame)

        key = cv2.waitKey(1)                                            
        if key == ord("q"):
            break
        elif key == ord("s"):
            cv2.imwrite(f"{output_path}", frame)
            print("save success")
        elif key == ord("a"):
            cap.set_width(6000)
            cap.set_height(9000)
            cap.reStart()
            cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)

            for i in range(wait_frames):
                print(f"wait {i + 1}")
                ret, frame = cap.read()
            if ret:
                frame = arducam108mp_isp(frame.reshape(9000, 12000), ccm, ccm_list)
                cv2.imwrite(f"108MP_{time.strftime('%Y-%m-%d') + time.strftime('_%H_%M_%S')}.jpg", frame)
                print("save success")
            else:
                print("none frame, save failed")

            cap.set_width(width)
            cap.set_height(height)
            cap.set_fps(fps)
            cap.reStart()

    cap.release()

    cv2.destroyAllWindows()
