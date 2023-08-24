import cv2
import argparse
from camera import Camera
from utils import *

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
    parser.add_argument('-o', '--OutputPath', type=str, required=False, default="test.jpg", help="set save image path")
    parser.add_argument('-t', '--reStartTimes', type=int, required=False, default=5, help="restart camera times")

    args = parser.parse_args()
    width = args.width
    height = args.height
    view_window = [int(i) for i in args.DisplayWindow.split(":")]
    index = args.index
    fps = args.FrameRate
    focus = args.Focus
    output_path = args.OutputPath
    restart_times = args.reStartTimes
    selector = selector_list[args.VideoCaptureAPI]

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

        display_fps(frame)
        cv2.imshow("video", frame)

        key = cv2.waitKey(1)                                            
        if key == ord("q"):
            break
        elif key == ord("s"):
            cv2.imwrite(f"{output_path}", frame)

    cap.release()

    cv2.destroyAllWindows()