
import pyautogui
import time
import concurrent.futures
from node_parser import parse_message
from mandala import mandala_node_position, mandala_node_state, mandala_ring_state
from node_actions import dispatch_node
import cv2 as cv

game_name = 'MIRMG(1)'

def dispatch(mandala_action, img):
    def node_img_parser(roi, img):
        result = mandala_node_state(dispatch_node(roi, img), 'node_actions')
        return result

    match mandala_action:
        case "sector_ring":
            print('fetching ring state..')
            message = mandala_ring_state(img)
            print(f' Success Chance to Unlock is ... {message}')
            return message

        case "sector_position":
            positions = mandala_node_position(img)
            print(f'finished, sector position is {positions}')
            return positions

        case "select_node":
            positions = img
            print(f'Clicking Sector... {positions[0]}')
            pyautogui.click(positions[0])
            time.sleep(1)
            return

        case "node_sector":
            node_status, node_image = dispatch('node_status', img)
            sector_node = dispatch('sector_unlocked', node_image) if node_status == True else dispatch('sector_locked', node_image) if node_status == False else None
            return sector_node

        case "sector_unlocked":
            sections = ['title', 'stat_type', 'stat_value', 'node_level', 'coin_price', 'orb_price', 'success_chance']
            futures = {}
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for section in sections:
                    future = executor.submit(node_img_parser, roi=section, img=img)
                    futures[future] = section
            sector_info = {}
            for f in concurrent.futures.as_completed(futures):
                sec = futures[f]
                sector_info[sec] = f.result()
            parsed_message = parse_message(sector_info,'unlocked')
            print([parsed_message])
            return parsed_message

        case "sector_locked":
            sections = ['title', 'invalid_node', 'invalid_stat_type', 'invalid_stat_value', 'coin_price', 'orb_price', 'success_chance']
            futures = {}
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for section in sections:
                    future = executor.submit(node_img_parser, roi=section, img=img)
                    futures[future] = section
            sector_info = {}
            for f in concurrent.futures.as_completed(futures):
                sec = futures[f]
                sector_info[sec] = f.result()
            parsed_message = parse_message(sector_info, 'locked')
            print([parsed_message])

            return parsed_message

        case "node_status":
            node_image = mandala_node_state(img, 'fetch_current_node_image')
            status = mandala_node_state(img, 'fetch_current_node_status')
            if "previous mandala has not been activated yet" in status:
                return False, node_image
            return True, node_image


        case default:
            pass

