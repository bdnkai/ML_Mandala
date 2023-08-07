from ppadb.client import Client as AdbClient
import threading
import time
import os
from dotenv import load_dotenv
import keyboard
from auction import get_window


load_dotenv('../.env')
client = AdbClient(host="127.0.0.1", port=5037)
print(client.version())
device = client.device("R52N90C8DWA")
print(device)
adb = device

if __name__ == '__main__':

    adb.shell('input tap 59 560')
    print('done')

    application_name = os.getenv("APP_NAME")
    application_name2 = os.getenv(('APP_TWO_NAME'))

    a_locked = os.getenv("AL_PATH")
    e_locked = os.getenv("EL_PATH")
    a_unlocked = os.getenv("AU_PATH")
    e_unlocked = os.getenv("EU_PATH")

    plus = os.getenv("PLUS")
    craft = os.getenv("CRAFT")
    okay_button = os.getenv('OKAY')
    okay2_button = os.getenv('OKAY2')

    waitres = os.getenv('WR')
    flicker1 = os.getenv('F1')
    flicker2 = os.getenv('F2')

    # def stop_script(q):
    #     quit()
    #     print('Stopping script...')
    #     exit(q)
    #
    #
    # get_window(app_name=application_name2)

    # # def perform_craft():
    #
    # print(waitres)
    #
    # wait_response = dispatch_norm("vision", app, waitres, threshold=0.8)
    #
    # start = time.time()
    # while start:
    #     print('timer started')
    #     if start > 0:
    #         flicker_one = dispatch_norm("vision", app, flicker1, threshold=0.94)
    #
    #         if flicker_one == 'done':
    #             flicker_two = dispatch_norm("vision", app, flicker2, threshold=0.9)
    #
    # print('no mroe WResponse')
    # end = time.time()
    #
    # print(end - start)


        # if plus_position == 'done':
        # craft_position = dispatch_norm_craft("press_once", app, craft, 0.6)
        # if craft_position == 'done':
        #     okay_position = dispatch_norm_craft("press_once", app, okay_button, 0.65)
        #     if okay_position == 'done':
        #         okay2_position = dispatch_norm_craft("press_once_wait", app, okay2_button, 0.95)
        #
        #
        #
        #
        #
        # def main_thread():
        # keyboard.on_press_key('q', stop_script)
        #
        # while True:
        #     print('Running script...')
        #     # Create and start the craft thread
        #     craft_thread = threading.Thread(target=perform_craft)
        #     craft_thread.start()
        #     craft_thread.join()  # Wait for the craft thread to finish before proceeding to the next iteration
        #
        #
        #
        # main_thread()
