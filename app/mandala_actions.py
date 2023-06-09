
import pyautogui
import time
import concurrent.futures

import pywinauto.mouse

from node_parser import parse_message
from mandala import mandala_node_position, mandala_node_state, mandala_ring_state, assign
from node_actions import dispatch_split_node
from dotenv import load_dotenv
import os


load_dotenv('../.env')
def get_variable():
    application_name = os.getenv("APP_NAME")
    a_locked = os.getenv("AL_PATH")
    e_locked = os.getenv("EL_PATH")
    a_unlocked = os.getenv("AU_PATH")
    e_unlocked = os.getenv("EU_PATH")
    plus = os.getenv("PLUS")
    craft = os.getenv("CRAFT")
    okay_button = os.getenv('OKAY')
    okay2_button = os.getenv('OKAY2')

    mandala = a_unlocked, a_locked, e_unlocked, e_locked
    lazy = plus, craft, okay_button, okay2_button

    return application_name, lazy


def dispatch_craft(mandala_action, app_name, match_img, threshold):
    match mandala_action:
        case "vision":

            vision_position = assign(app_name, match_img, threshold=threshold)

            if vision_position:
                print('found position for  + sign')

                for press in range(10):
                    pyautogui.click(vision_position, duration=0.01)
                print('done')

            return 'done'

        case "press_once":

            vision_position = assign(app_name, match_img, threshold=threshold)

            if vision_position:
                print('found position for 1 action')

                pyautogui.click(vision_position, duration=0.01)
                print('done')
            return 'done'

        case "press_once_wait":
            time.sleep(4)
            vision_position = assign(app_name, match_img, threshold=threshold)

            if vision_position:
                print('found position for 1 action')

                pyautogui.click(vision_position, duration=0.01)
                print('done')
            return

        case default:
            return None


def dispatch(mandala_action, img):
    def node_img_parser(roi, img):
        result = mandala_node_state(dispatch_split_node(roi, img), f'{roi}')
        return result

    match mandala_action:
        case "find_node_position":
            positions = mandala_node_position(img)
            print(f'finished, sector position is {positions[0]}')
            return positions

        case "select_node_position":
            positions = img
            print(f'Clicking Sector... {positions[0]}')
            pyautogui.click(positions, duration=0.01)
            return

        case "get_ring_information":
            print('fetching ring state..')
            message = mandala_ring_state(img)
            print(f' Success Chance to Unlock is ... {message}')
            return message

        case "get_node_information":
            node_status, node_image = dispatch('node_status', img)
            sector_node = dispatch('sector_unlocked', node_image) if node_status == True else dispatch('sector_locked', node_image) if node_status == False else print('SOMETHINGS WRONG')
            return sector_node

        case "sector_unlocked":
            sections = ['title', 'stat_type', 'stat_value', 'node_level', 'coin_price', 'orb_price', 'success_chance']
            futures = {}
            sector_info = {}
            print('sector unlocked')

            with concurrent.futures.ThreadPoolExecutor() as executor:
                for section in sections:
                    future = executor.submit(node_img_parser, roi=section, img=img)
                    futures[future] = section

            for f in concurrent.futures.as_completed(futures):
                sec = futures[f]
                sector_info[sec] = f.result()
            parsed_message = parse_message(sector_info,'unlocked')
            return parsed_message

        case "sector_locked":
            sections = ['title', 'invalid_node', 'invalid_stat_type', 'invalid_stat_value', 'coin_price', 'orb_price', 'success_chance']
            futures = {}
            sector_info = {}
            print('sector locked')

            with concurrent.futures.ThreadPoolExecutor() as executor:
                for section in sections:
                    future = executor.submit(node_img_parser, roi=section, img=img)
                    futures[future] = section

            for f in concurrent.futures.as_completed(futures):
                sec = futures[f]
                sector_info[sec] = f.result()
                print(sector_info[sec])
            parsed_message = parse_message(sector_info, 'locked')

            return parsed_message

        case "node_status":
            node_image = mandala_node_state(img, 'fetch_current_node_image')
            status = mandala_node_state(node_image, 'fetch_current_node_status')

            if "previous mandala has not been activated yet" in status:
                return False, node_image

            else:
                return True, node_image

        case default:
            pass

