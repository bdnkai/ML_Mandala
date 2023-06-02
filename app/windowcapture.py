import numpy as np
import win32gui, win32ui, win32con
from pywinauto.application import Application



class WindowCapture:
    # properties
    w = 0
    h = 0
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, window_name):
        # Connect to the application
        self.app = Application().connect(title=window_name)

        # Get the window
        self.window = self.app.window(title=window_name)

        # Get the window's rectangle
        self.rect = self.window.rectangle()

        # Print the size and position
        print(f"Left: {self.rect.left}, Top: {self.rect.top}, Right: {self.rect.right}, Bottom: {self.rect.bottom}")
        print(f"Width: {self.rect.width()}, Height: {self.rect.height()}")



        # # find the handle for the window we want to capture
        # self.hwnd = win32gui.FindWindow(None, window_name)
        # if not self.hwnd:
        #     raise Exception('Window not found: {}'.format(window_name))
        #
        # # get the window size
        # self.window_rect = win32gui.GetWindowRect(self.hwnd)
        #
        # self.w = self.window_rect[2] - self.window_rect[0]
        # self.h = self.window_rect[3] - self.window_rect[1]
        #
        # # account for the window border and titlebar and cut them off
        # border_pixels = 0
        # titlebar_pixels = 0
        # self.w = self.w - (border_pixels * 2)
        # self.h = self.h - titlebar_pixels - border_pixels
        # self.cropped_x = border_pixels
        # self.cropped_y = titlebar_pixels
        #
        # # set the cropped coordinates offset so we can translate screenshot
        # # images into actual screen positions
        # self.offset_x = self.window_rect[0] + self.cropped_x
        # self.offset_y = self.window_rect[1] + self.cropped_y
        #
        # self.size_w = self.w
        # self.size_h = self.h

