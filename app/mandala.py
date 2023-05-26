import cv2 as cv
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
import re
import dxcam
import gym
from windowcapture import WindowCapture



class Action_State:
    def __init__(self):
        super(Action_State, self).__init__()

        self.start = False

        self.get_probability = False
        self.get_sector_position = False
        self.get_sector_info =False

        self.proc_text = True if self.get_probability == True or self.get_sector_info == True else False
        self.proc_nodes = True if self.get_sector_position == True else False

        self.debug = False


        self.proccessing = True if self.get_probability and self.get_sector_info and self.get_sector_position == True else False
        self.ready = True if self.proccessing == False else True
        self.probability_finished = False
        self. sector_finished = False

        self.end = True if self.probability_finished and self.get_sector_info == True else False

class HsvFilter:
    def __init__(hMin=None, sMin=None, vMin=None, hMax=None, sMax=None, vMax=None,
                 sAdd=None, sSub=None, vAdd=None, vSub=None):
        hMin = hMin
        sMin = sMin
        vMin = vMin
        hMax = hMax
        sMax = sMax
        vMax = vMax
        sAdd = sAdd
        sSub = sSub
        vAdd = vAdd
        vSub = vSub

def init_control_gui():


    def nothing(position):
        pass

def get_hsv_filter_from_controls(scenario):

    scenario = scenario
    hsv_filter = HsvFilter()


    if scenario == 'mandala_messages':
        print('HSV for TEXT pulling ACTIVATED')

        hsv_filter.hMin = 0
        hsv_filter.sMin = 0
        hsv_filter.vMin = 133
        hsv_filter.hMax = 180
        hsv_filter.sMax = 255
        hsv_filter.vMax = 255
        hsv_filter.sAdd = 0
        hsv_filter.sSub = 255
        hsv_filter.vAdd = 65
        hsv_filter.vSub = 0

        return hsv_filter

    if scenario == 'mandala_middle':

        print('HSV for NODE pulling ACTIVATED')
        # circle filtering
        hsv_filter.hMin = 0
        hsv_filter.sMin = 58
        hsv_filter.vMin = 0
        hsv_filter.hMax = 115
        hsv_filter.sMax = 255
        hsv_filter.vMax = 255
        hsv_filter.sAdd = 0
        hsv_filter.sSub = 0
        hsv_filter.vAdd = 0
        hsv_filter.vSub = 0

        return hsv_filter


def apply_hsv_filter(original_image, hsv_filter=None):
    # convert image to HSV
    hsv = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)

    # if we haven't been given a defined filter, use the filter values from the GUI
    if not hsv_filter:
        hsv_filter = get_hsv_filter_from_controls()

    # add/subtract saturation and value
    h, s, v = cv.split(hsv)
    s = shift_channel(s, hsv_filter.sAdd)
    s = shift_channel(s, -hsv_filter.sSub)
    v = shift_channel(v, hsv_filter.vAdd)
    v = shift_channel(v, -hsv_filter.vSub)
    hsv = cv.merge([h, s, v])

    # Set minimum and maximum HSV values to display
    lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
    upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
    # Apply the thresholds
    mask = cv.inRange(hsv, lower, upper)
    result = cv.bitwise_and(hsv, hsv, mask=mask)

    # convert back to BGR for imshow() to display it properly
    img = cv.cvtColor(result, cv.COLOR_HSV2BGR)

    return img


def shift_channel(c, amount):
    if amount > 0:
        lim = 255 - amount
        c[c >= lim] = 255
        c[c < lim] += amount
    elif amount < 0:
        amount = -amount
        lim = amount
        c[c <= lim] = 0
        c[c > lim] -= amount
    return c



camera = dxcam.create(output_idx=0, output_color="BGR")

def mandala_node(img):
    wincap = WindowCapture(img)

    activation_left, activation_top = 10, 110
    activation_right, activation_bottom = (wincap.w - 1000), (wincap.h - 350)

    sector_left, sector_top = (wincap.w - (wincap.w - 925)), (wincap.h - (wincap.h - 210))
    sector_right, sector_bottom = (wincap.w - 20), (wincap.h - 95)

    mandala_left, mandala_top = (activation_right, activation_top)
    mandala_right, mandala_bottom = (sector_left, sector_bottom)

    mandala_region = (mandala_left + 240, mandala_top + 50, mandala_right - 200, mandala_bottom - 50)
    activation_region = (activation_left, activation_top, activation_right, activation_bottom)
    sector_region = (sector_left, sector_top, sector_right, sector_bottom)

    mandala_camera = camera.start(region= mandala_region)
    print(f'camera is activated for mandala_node: {camera.is_capturing}')

    image = camera.get_latest_frame()  # Will block until new frame available

    img = image

    orig_height, orig_width = img.shape[:2]
    fixed_width = orig_width
    ratio = fixed_width / float(orig_width)
    fixed_height = int(orig_height * ratio)
    img = cv.resize(img, (fixed_width, fixed_height))

    hsv_filter = get_hsv_filter_from_controls('mandala_middle')
    filtered_img = apply_hsv_filter(img, hsv_filter=hsv_filter)

    gray = cv.cvtColor(filtered_img, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 50, param1=95, param2=35, minRadius=int(20), maxRadius=int(40))

    if circles is not None:
        # Convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # Loop over the detected circles and draw them
        for (x, y, r) in circles:
            cv.circle(img, (x, y), r, (100, 255, 100), 2)
            print(x,y)

        camera.stop()
        return (x,y)





case = 'text'
words = []
def mandala_message(img, location):
    position = location

    wincap = WindowCapture(img)

    activation_left, activation_top = 10, 110
    activation_right, activation_bottom = (wincap.w - 1000), (wincap.h - 350)

    sector_left, sector_top = (wincap.w - (wincap.w - 925)), (wincap.h - (wincap.h - 210))
    sector_right, sector_bottom = (wincap.w - 20), (wincap.h - 95)

    mandala_left, mandala_top = (activation_right, activation_top)
    mandala_right, mandala_bottom = (sector_left, sector_bottom)

    mandala_region = (mandala_left + 240, mandala_top + 50, mandala_right - 200, mandala_bottom - 50)
    activation_region = (activation_left, activation_top, activation_right, activation_bottom)
    sector_region = (sector_left, sector_top, sector_right, sector_bottom)

    text_camera = camera.start(region=sector_region) if position == 'right' else camera.start(region= activation_region)

    print(f'camera is activated for mandala_text: {camera.is_capturing}')

    image = camera.get_latest_frame()

    img = image

    orig_height, orig_width = img.shape[:2]
    fixed_width = 1600
    ratio = fixed_width / float(orig_width)
    fixed_height = int(orig_height * ratio)
    img = cv.resize(img, (fixed_width, fixed_height))

    hsv_filter = get_hsv_filter_from_controls('mandala_messages')
    filtered_img = apply_hsv_filter(img, hsv_filter=hsv_filter)

    gray = cv.cvtColor(filtered_img, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

    config = '-c char_whitelist= --oem 3 --psm 4'
    text_right_box = pytesseract.image_to_string(thresh, lang='eng', config=config)
    if text_right_box:

        text = re.sub('[^A-Za-z0-9-%-/]+', ' ', text_right_box).lower()
        # text = text_right_box
        # print(text)
        spotted_strings = []
        lines = text.split('\n')
        for line in lines:

            if lines and ' ' in lines[0]:

                camera.stop()

                return (f'{lines}')


if camera.is_capturing:
    camera.stop()
















