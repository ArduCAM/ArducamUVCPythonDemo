import cv2
import argparse
import time
from camera import Camera
from utils import validate_windows_size, selector_list, VideoCaptureAPIs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture a single photo from Arducam")
    parser.add_argument('-W', '--width', type=int, default=4656, help='set camera image width')
    parser.add_argument('-H', '--height', type=int, default=3496, help='set camera image height')
    parser.add_argument('-f', '--FrameRate', type=int, default=10, help='set camera frame rate')
    parser.add_argument('--focus', type=int, help='Set manual focus value (e.g., 850)')
    parser.add_argument('-i', '--index', type=int, default=0, help='set camera index')
    parser.add_argument('-v', '--VideoCaptureAPI', type=int, default=0, choices=range(len(selector_list)), help=VideoCaptureAPIs)
    parser.add_argument('-o', '--output', type=str, default=None, help='output filename (default: auto timestamped)')
    
    args = parser.parse_args()

    selector = selector_list[args.VideoCaptureAPI]
    cap = Camera(args.index, selector)
    cap.set_width(args.width)
    cap.set_height(args.height)
    cap.set_fps(args.FrameRate)
    cap.open()

    if not cap.isOpened():
        print("Failed to open camera.")
        exit(1)

    # Optional manual focus
    if args.focus is not None:
        cap.set_focus(args.focus)
        print(f"Set focus to {args.focus}")

    # Warm up camera
    for _ in range(5):
        cap.read()
        cap.set_focus(cap.get_focus())
        time.sleep(0.1)

    ret, frame = cap.read()
    if ret:
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
        filename = args.output or f"{args.width}x{args.height}_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Image saved to: {filename}")
    else:
        print("Failed to capture image.")

    cap.release()
