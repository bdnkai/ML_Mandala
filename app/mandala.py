import cv2 as cv
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
import re
import dxcam
import gym
from windowcapture import WindowCapture

# env = gym.make(environment_name)
# custom data structure to hold the state of an HSV filter

game_name = 'MIRMG(1)'

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



TRACKBAR_WINDOW = 'Trackbars'
case = ''
def init_control_gui():
    # cv.namedWindow(TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
    # cv.resizeWindow(TRACKBAR_WINDOW, 350, 700)



    def nothing(position):
        pass

    # create trackbars for bracketing.
    # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
    if case == 'trackbar':
        cv.createTrackbar('HMin', TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMin', TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMin', TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('HMax', TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMax', TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMax', TRACKBAR_WINDOW, 0, 255, nothing)

        # Set default value for Max HSV trackbars
        cv.setTrackbarPos('HMax', TRACKBAR_WINDOW, 179)
        cv.setTrackbarPos('SMax', TRACKBAR_WINDOW, 255)
        cv.setTrackbarPos('VMax', TRACKBAR_WINDOW, 255)

        # trackbars for increasing/decreasing saturation and value
        cv.createTrackbar('SAdd', TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('SSub', TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VAdd', TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VSub', TRACKBAR_WINDOW, 0, 255, nothing)


# returns an HSV filter object based on the control GUI values
def get_hsv_filter_from_controls(case, ratio):

    hsv_filter = HsvFilter()

    # Get current positions of all trackbars
    if(case == 'text_filter'):
        print('case = text filter')

        # text filter
        # hsv_filter.hMin = 2
        # hsv_filter.sMin = 0
        # hsv_filter.vMin = 0
        # hsv_filter.hMax = 176
        # hsv_filter.sMax = 255
        # hsv_filter.vMax = 255
        # hsv_filter.sAdd = 255
        # hsv_filter.sSub = 23
        # hsv_filter.vAdd = 69
        # hsv_filter.vSub = 71

        hsv_filter.hMin = 0
        hsv_filter.sMin = 0
        hsv_filter.vMin = 133
        hsv_filter.hMax = 180
        hsv_filter.sMax = 255
        hsv_filter.vMax = 255
        hsv_filter.sAdd = 0
        hsv_filter.sSub = 255
        hsv_filter.vAdd = 34
        hsv_filter.vSub = 0

        # hsv_filter.hMin = 0
        # hsv_filter.sMin = 0
        # hsv_filter.vMin = 51
        # hsv_filter.hMax = 179
        # hsv_filter.sMax = 255
        # hsv_filter.vMax = 250
        # hsv_filter.sAdd = 0
        # hsv_filter.sSub = 83
        # hsv_filter.vAdd = 141
        # hsv_filter.vSub = 126

        return hsv_filter

    if case == 'circle_filter':

        print('case = circle filter')
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

    else:

        hsv_filter.hMin = cv.getTrackbarPos('HMin', TRACKBAR_WINDOW)
        hsv_filter.sMin = cv.getTrackbarPos('SMin', TRACKBAR_WINDOW)
        hsv_filter.vMin = cv.getTrackbarPos('VMin', TRACKBAR_WINDOW)
        hsv_filter.hMax = cv.getTrackbarPos('HMax', TRACKBAR_WINDOW)
        hsv_filter.sMax = cv.getTrackbarPos('SMax', TRACKBAR_WINDOW)
        hsv_filter.vMax = cv.getTrackbarPos('VMax', TRACKBAR_WINDOW)
        hsv_filter.sAdd = cv.getTrackbarPos('SAdd', TRACKBAR_WINDOW)
        hsv_filter.sSub = cv.getTrackbarPos('SSub', TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv.getTrackbarPos('VAdd', TRACKBAR_WINDOW)
        hsv_filter.vSub = cv.getTrackbarPos('VSub', TRACKBAR_WINDOW)





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

def process_screen(mandala_screen):


    init_control_gui()



    # rois = []
    left, top = 0, 0
    right, bottom = 1, 1
    region = (left, top, right, bottom)


    camera = dxcam.create(output_idx=0, output_color="BGR")


    print(f'camera is start: {camera.is_capturing}')

    for i in range(100000):

        # fetch application size
        wincap = WindowCapture(mandala_screen)
        new_region = (left + 5, top + 55, wincap.w - top, wincap.h- top)
        new_camera = camera.start(region=new_region)
        image = camera.get_latest_frame()  # Will block until new frame available
        img = image

        # readjust size to 1200 max width ratio
        orig_height, orig_width = img.shape[:2]
        fixed_width = 2800
        ratio = fixed_width / float(orig_width)
        fixed_height = int(orig_height * ratio)
        img = cv.resize(img, (fixed_width, fixed_height))

        # pass image and scenario to hsv_filter
        case = 'text_filter'

        hsv_filter = get_hsv_filter_from_controls(case, ratio=1)
        filtered_img = apply_hsv_filter(img, hsv_filter=hsv_filter)

        gray = cv.cvtColor(filtered_img, cv.COLOR_BGR2GRAY)
        thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

        config = '-c char_whitelist= a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 1 2 3 4 5 6 7 8 9 % / --oem 3 --psm 12'

        if case == 'circle_filter':
            circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 1, param1=95, param2=35, minRadius=16, maxRadius=40)

            if circles is not None:
                # Convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")

                # Loop over the detected circles and draw them
                for (x, y, r) in circles:
                    cv.circle(gray, (x, y), r, (100, 255, 100), 10)

            cv.imshow('img', gray)
            cv.waitKey(5)

            if cv.waitKey(1) & 0xFF == ord('q'):
                camera.stop()
                new_camera.stop()
                break

            if camera:
                camera.stop()

            if new_camera:
                new_camera.stop()
                camerqqa.start()


        if case == 'text_filter':
            text_right_box = pytesseract.image_to_string(thresh,lang='eng', config=config)
            if text_right_box:

                text = re.sub('[^A-Za-z0-9-%-/]+', ' ', text_right_box).lower()
                # text = text_right_box

                spotted_strings = []
                lines = text.split('\n')
                for line in lines:
                    print(f'RAW... {line}')
                    if (int(len(line)) <= int(1)):
                        print(f'CLEANING SOME... {line}')
                    if lines and ' ' in lines[0]:
                        print(f'CLEANING SPACES... {line}')
                        if (int(len(line)) <= int(1)):
                            print(f'CLEANING MORE... {line}')


            # cv.imshow('img', gray)
            # cv.waitKey(1)

            # if cv.waitKey(1) & 0xFF == ord('q'):
            #     camera.stop()
            #     new_camera.stop()
            #     break

            if camera:
                camera.stop()

            if new_camera:
                new_camera.stop()
                camerqqa.start()

        # print(int(len(circles)))
            # plt.imshow(cv.cvtColor(gray, cv.COLOR_BGR2RGB))
            # plt.show()

        # cv.imshow('img', gray)
        # cv.waitKey(1)
        # if cv.waitKey(1) & 0xFF == ord('q'):
        #     camera.stop()
        #     new_camera.stop()
        #     break

        if camera:
            camera.stop()

        if new_camera:
            new_camera.stop()
            camerqqa.start()







            #Create a feature vector
            # feature_vector = [core_spot_points_fraction, activation_chance_decimal]

    # Feed the feature vector to your model
    # (You'll need to replace this with your actual model code)
    # model_output = model.predict(feature_vector)
    # print (model_output)
    # return model_output


    # cv.imshow('img', img)
    #
    # # Break the loop if 'q' key is pressed
    # if cv.waitKey(1) & 0xFF == ord('q'):
    #     break



    cv.destroyAllWindows()











