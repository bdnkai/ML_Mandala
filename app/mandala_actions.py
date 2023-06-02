
import pyautogui
import time
import concurrent.futures
from node_parser import parse_message
from mandala import mandala_node_position, mandala_node_state, mandala_ring_state
from node_actions import dispatch_node
from dotenv import load_dotenv
import os


def get_variable():
    load_dotenv('../.env')
    application_name = os.getenv("APP_NAME")
    a_locked = os.getenv("AL_PATH")
    e_locked = os.getenv("EL_PATH")
    a_unlocked = os.getenv("AU_PATH")
    e_unlocked = os.getenv("EU_PATH")
    return application_name, a_unlocked, a_locked, e_unlocked, e_locked



def dispatch(mandala_action, img):
    def node_img_parser(roi, img):
        result = mandala_node_state(dispatch_node(roi, img), 'node_actions')
        return result

    match mandala_action:
        case "assign_action":
            print('taking action!..')
            message = mandala_ring_state(img)
            print(f'pressing action/ emhance')
            return message

        case "find_node_position":
            positions = mandala_node_position(img)
            print(f'finished, sector position is {positions}')
            return positions

        case "select_node_position":
            positions = img
            print(f'Clicking Sector... {positions[0]}')
            time.sleep(1)
            pyautogui.click(positions[0])
            time.sleep(1)
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
            status = mandala_node_state(img, 'fetch_current_node_status')

            if "previous mandala has not been activated yet" in status:
                return False, node_image

            else:
                return True, node_image

        case default:
            pass

