import dxcam
from hsv_filter import *
from pywinauto.application import Application



camera = dxcam.create(output_idx=0, output_color="BGR")




def get_window(app_name):
    # Connect to the application
    app = Application().connect(title=app_name)

    # Get the window
    window = app.window(title=app_name)


    rect = window.rectangle()
    print(rect.width(), rect.height())
    if rect.width() != 1435:
        window.move_window(x=0, y=0, width=1435, height=755)
    else:
        pass
    return app, window, rect


def assign(app_name, vision_image_file,  threshold):
    app, window, rect = get_window(app_name)

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