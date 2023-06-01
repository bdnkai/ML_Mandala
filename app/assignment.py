import time
import threading
import cv2 as cv
import numpy as np
from vision import Vision
from windowcapture import WindowCapture



def assign(vision_image_file, name,  threshold):
    # sends adjusted img dimension to Vision Module
        adjusted_vision_image = Vision(vision_image_file)
        image_data = adjusted_vision_image

    # returns the (x, y) location at which the image is found
        tap_location = image_data.find( screenshot, threshold, 'points')

        if .tap_location is not None:
                tap(device, tap_location)

