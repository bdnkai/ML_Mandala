import cv2 as cv
import numpy as np


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

