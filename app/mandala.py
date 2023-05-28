import cv2 as cv
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
import re
import dxcam
import gym
from windowcapture import WindowCapture
from hsv_filter import *
from node_parser import parse_message, update_data



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


camera = dxcam.create(output_idx=0, output_color="BGR")

def mandala_node_position(img):


    mandala_left, mandala_top = (431, 230)
    mandala_right, mandala_bottom = (808, 450)

    mandala_node_region = (mandala_left, mandala_top , mandala_right , mandala_bottom)

    mandala_camera = camera.start(region= mandala_node_region)
    print(f'camera is activated for mandala_node: {camera.is_capturing}')

    region_x, region_y = mandala_left, mandala_top


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
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 50, param1=80, param2=30, minRadius=int(25), maxRadius=int(40))

    if circles is not None:
        # Convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        positions = []
        # Loop over the detected circles and draw them
        for (x, y, r) in circles:
            cv.circle(img, (x , y), r, (100, 255, 100), 2)
            cv_x, cv_y = x, y
            screen_x = region_x + cv_x
            screen_y = region_y + cv_y
            positions.append((screen_x, screen_y))
        camera.stop()


        return positions


    if action_type == 'node_actions':
        image = img
        pass
    img = image
    orig_height, orig_width = img.shape[:2]
    fixed_width = 1200
    ratio = fixed_width / float(orig_width)
    fixed_height = int(orig_height * ratio)
    img = cv.resize(img, (fixed_width, fixed_height))

def mandala_node_state(img, action):
    action_type = action
    print(action_type)

    if action_type != 'node_actions':
        wincap = WindowCapture(img)

        sector_left, sector_top = (wincap.w - (wincap.w - 835)), (wincap.h - (wincap.h - 180))
        sector_right, sector_bottom = (wincap.w - 40), (wincap.h - 10)
        sector_region = (sector_left, sector_top, sector_right, sector_bottom)

        node_camera = camera.start(region=sector_region)
        print(f'camera is activated for mandala_node_state: {camera.is_capturing}')
        image = camera.get_latest_frame()


    if action_type == 'fetch_current_node_image':
        camera.stop()
        return image


    if action_type == 'node_actions':
        image = img

    img = image





    image = camera.get_latest_frame()
    img = image
    orig_height, orig_width = img.shape[:2]
    fixed_width = 1200
    ratio = fixed_width / float(orig_width)
    fixed_height = int(orig_height * ratio)
    img = cv.resize(img, (fixed_width, fixed_height))

    orig_height, orig_width = img.shape[:2]
    fixed_width = 1200
    ratio = fixed_width / float(orig_width)
    fixed_height = int(orig_height * ratio)
    img = cv.resize(img, (fixed_width, fixed_height))

    hsv_filter = get_hsv_filter_from_controls('mandala_messages')
    filtered_img = apply_hsv_filter(img, hsv_filter=hsv_filter)

    gray = cv.cvtColor(filtered_img, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]


        self.proccessing = True if self.get_probability and self.get_sector_info and self.get_sector_position == True else False
        self.ready = True if self.proccessing == False else True
        self.probability_finished = False
        self. sector_finished = False

    config = '-c char_whitelist= --oem 3 --psm 4'
    text_right_box = pytesseract.image_to_string(gray, lang='eng', config=config)
    if text_right_box:

        text = re.sub('[^A-Za-z0-9-,%]+', ' ', text_right_box).lower()

        lines = text.split('\n')

        for line in lines:

            if lines and ' ' in lines[0]:

                camera.stop()
                for line in lines:
                    print(line)
                    # parsed_message = parse_message(line)
                    os_read = f'{line}'


                camera.stop()
                return (f'{line}')



    orig_height, orig_width = img.shape[:2]
    fixed_width = orig_width
    ratio = fixed_width / float(orig_width)
    fixed_height = int(orig_height * ratio)
    img = cv.resize(img, (fixed_width, fixed_height))



    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        positions = []
        for (x, y, r) in circles:
            cv.circle(img, (x , y), r, (100, 255, 100), 2)
            cv_x, cv_y = x, y
            screen_x = region_x + cv_x
            screen_y = region_y + cv_y
            positions.append((screen_x, screen_y))
        camera.stop()


words = []

def mandala_ring_state(img):

    wincap = WindowCapture(img)

    activation_left, activation_top = 25, 150
    activation_right, activation_bottom = (wincap.w - 970), (wincap.h - 280)
    activation_region = (activation_left, activation_top, activation_right, activation_bottom)

    ring_camera = camera.start(region= activation_region)

    if action_type == 'node_actions':
        image = img
        pass
    img = image
    orig_height, orig_width = img.shape[:2]
    fixed_width = 1200
    ratio = fixed_width / float(orig_width)
    fixed_height = int(orig_height * ratio)
    img = cv.resize(img, (fixed_width, fixed_height))

    print(f'camera is activated for mandala_ring_state: {camera.is_capturing}')

    image = camera.get_latest_frame()

    img = image


    orig_height, orig_width = img.shape[:2]
    fixed_width = 1200
    ratio = fixed_width / float(orig_width)
    fixed_height = int(orig_height * ratio)
    img = cv.resize(img, (fixed_width, fixed_height))

    hsv_filter = get_hsv_filter_from_controls('mandala_messages')
    filtered_img = apply_hsv_filter(img, hsv_filter=hsv_filter)

    gray = cv.cvtColor(filtered_img, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]


    config = '-c char_whitelist= --oem 3 --psm 4'
    text_right_box = pytesseract.image_to_string(gray, lang='eng', config=config)
    if text_right_box:

        text = re.sub('[^A-Za-z0-9-%,]+', ' ', text_right_box).lower()

        lines = text.split('\n')

        for line in lines:

            if lines and ' ' in lines[0]:

                camera.stop()
                for line in lines:
                    print(line)
                    # parsed_message = parse_message(line)


                camera.stop()
                return (f'{line}')


if camera.is_capturing:
    camera.stop()
















