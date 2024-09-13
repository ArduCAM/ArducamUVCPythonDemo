import time
import cv2

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
        
        if self.width and self.height:
            self.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        if self.fps:
            self.set(cv2.CAP_PROP_FPS, self.fps)
    
    def set_width(self, width):
        self.width = width
    
    def set_height(self, height):
        self.height = height
    
    def set_fps(self, fps):
        self.fps = fps

    def set_focus(self, val):
        self.set(cv2.CAP_PROP_FOCUS, val)

    def set(self, selector, val):
        self.cap.set(selector, val)

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

        