import cv2 as cv
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
import re
import dxcam

from pywinauto import mouse
from vision import Vision
from windowcapture import WindowCapture
from hsv_filter import *
from node_parser import parse_message

from pywinauto.application import Application




camera = dxcam.create(output_idx=0, output_color="BGR")



def get_window(app_name):
    # Connect to the application
    app = Application().connect(title=app_name)

    # Get the window
    window = app.window(title=app_name)
    # Get the window's rectangle
    # print(dir(window.child_window()))


    rect = window.rectangle()
    print(rect.width(), rect.height())
    if rect.width() != 1435:
        window.move_window(x=0, y=0, width=1435, height=755)
    else:
        pass

    return app, window, rect


def assign(app_name, vision_image_file,  threshold):
    app, window, rect = get_window(app_name=app_name)

    # Grab Size and Specs from targetted app
    app_width = rect.width()
    app_height = rect.height()
    app_left, app_top, app_right, app_bottom = rect.left, rect.top, rect.right, rect.bottom

    app_region = app_left, app_top, app_right, app_bottom

    app_camera = camera.start(region=app_region)

    print(f'{app_region}')

    # Grab screen shot of last frame
    screenshot = camera.get_latest_frame()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    screenshot = screenshot.astype('float32')

    template = cv.imread(vision_image_file, 0)
    template = template.astype('float32')



    control = app.window(title=app_name).wrapper_object()

    # Perform template matching

    res = cv.matchTemplate(screenshot, template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    print(min_val, max_val, min_loc, max_loc)

    print(threshold)

    if max_val <= threshold:
        return None

    # Calculate the center of the matching image
    center_x = max_loc[0] + template.shape[1] // 2
    center_y = max_loc[1] + template.shape[0] // 2

    # Click on the center of the image
    # Move the mouse to the center of the image without physically moving the cursor


    if camera.start:
        camera.stop()
    return center_x,center_y



def mandala_node_position(img):

    mandala_left, mandala_top = (385, 320)
    mandala_right, mandala_bottom = (830, 560)

    mandala_node_region = (mandala_left, mandala_top , mandala_right , mandala_bottom)

    mandala_camera = camera.start(region= mandala_node_region)
    region_x, region_y = mandala_left, mandala_top

    image = camera.get_latest_frame()

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
        circles = np.round(circles[0, :]).astype("int")
        positions = []
        for (x, y, r) in circles:
            cv.circle(img, (x , y), r, (100, 255, 100), 2)
            cv_x, cv_y = x, y
            screen_x = region_x + cv_x
            screen_y = region_y + cv_y
            positions.append((screen_x, screen_y))

        camera.stop()
        return positions






def mandala_node_state(app_name, action):
    action_type = action

    if action_type == 'fetch_current_node_image':
        app, window, rect = get_window(app_name=app_name)

        app_width = rect.width()
        app_height = rect.height()
        app_left, app_top, app_right, app_bottom = rect.left, rect.top, rect.right, rect.bottom
        print(f"Left: {app_left}, Top: {app_top}, Right: {app_right}, Bottom: {app_bottom}")
        print(f"Width: {app_width}, Height: {app_height}")

        successful_sec_left = 835
        successful_sec_top = 180
        successful_sec_right = 1140
        successful_sec_bottom = 604
        successful_sec_width = successful_sec_right - successful_sec_left
        successful_sec_height = successful_sec_bottom - successful_sec_top

        roi_left_ratio = (successful_sec_left - app_left) / app_width
        roi_top_ratio = (successful_sec_top - app_top) / app_height
        roi_width_ratio = successful_sec_width / app_width
        roi_height_ratio = successful_sec_height / app_height

        sec_left = int(app_width * roi_left_ratio) + app_left
        sec_top = int(app_height * roi_top_ratio) + app_top
        sec_right = sec_left + int(app_width * roi_width_ratio)
        sec_bottom = sec_top + int(app_height * roi_height_ratio)

        sector_region = (sec_left, sec_top, sec_right, sec_bottom)

        print(roi_height_ratio,roi_width_ratio,roi_top_ratio,roi_top_ratio)


        node_camera = camera.start(region=sector_region)

        print(f'{sector_region}')

        image = camera.get_latest_frame()

        return image

    if action_type == 'split_node' or action_type == 'fetch_current_node_status' or action_type != 'fetch_current_node_image':
        pass
        img = app_name

    orig_height, orig_width = img.shape[:2]
    fixed_width = 600
    ratio = fixed_width / float(orig_width)
    fixed_height = int(orig_height * ratio)
    img = cv.resize(img, (fixed_width, fixed_height))

    print({f'{action_type}:  {orig_height} {orig_width} {orig_width} {orig_height}'})


    hsv_filter = get_hsv_filter_from_controls('mandala_messages')
    filtered_img = apply_hsv_filter(img, hsv_filter=hsv_filter)

    gray = cv.cvtColor(filtered_img, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    config = '-c char_whitelist= --oem 3 --psm 4'
    text_right_box = pytesseract.image_to_string(gray, lang='eng', config=config)
    if text_right_box:
        text = re.sub('[^A-Za-z0-9-.,%]+', ' ', text_right_box).lower()
        lines = text.split('\n')
        for line in lines:
            if lines and ' ' in lines[0]:
                for line in lines:
                    os_read = f'{line}'
                if camera.start:
                    camera.stop()

                return os_read

    if camera.start:
        camera.stop()


def mandala_ring_state(img):

    wincap = WindowCapture(img)

    activation_left, activation_top = 25, 150
    activation_right, activation_bottom = (wincap.w - 970), (wincap.h - 280)
    activation_region = (activation_left, activation_top, activation_right, activation_bottom)
    ring_camera = camera.start(region= activation_region)

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
                for line in lines:
                    os_read = f'{line}'
                    return os_read
                if camera.start:
                    camera.stop()

                return os_read

if camera.start:
    camera.stop()

















