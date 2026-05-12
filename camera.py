import time
import subprocess
import cv2
import re


class Camera:

    def __init__(self, index=0, selector=cv2.CAP_ANY) -> None:
        self.index = index
        self.selector = selector
        self.cap = None
        self.width = None
        self.height = None
        self.fps = None

    def open(self):
        self.cap = cv2.VideoCapture(self.index, self.selector)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))


        if self.width and self.height:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        if self.fps:
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
    
    def set_width(self, width):
        self.width = width
    
    def set_height(self, height):
        self.height = height
    
    def set_fps(self, fps):
        self.fps = fps

    def set_focus(self, val):
        self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # turn off autofocus
        self.cap.set(cv2.CAP_PROP_FOCUS, val)
        self.cap.set(cv2.CAP_PROP_FOCUS, val + 1)  # give it a shake
        self.cap.set(cv2.CAP_PROP_FOCUS, val)      # Back to target focus value
    
    def get_focus(self):
        # Run the command to get current focus value
        result = subprocess.run(f"v4l2-ctl -d /dev/video0 --get-ctrl=focus_absolute",
                                shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            match = re.search(r"focus_absolute:\s*(\d+)", result.stdout)
            if match:
                return int(match.group(1))
        return None
    
    
    def read(self):
        return self.cap.read()

    def reStart(self):
        self.release()
        time.sleep(0.5)
        self.open()

    def release(self):
        self.cap.release()

    def isOpened(self):
        return self.cap.isOpened()

        
