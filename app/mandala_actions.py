
import pyautogui
import time
import concurrent.futures
from mandala import mandala_node_position, mandala_node_state, mandala_ring_state
from node_actions import dispatch_node
import cv2 as cv

game_name = 'MIRMG(1)'

def dispatch(mandala_action, img):
        match mandala_action:
            case "sector_ring":
                # -------------------- START -----------------------------------
                print('fetching ring state..')
                message = mandala_ring_state(img)
                print(f' Success Chance to Unlock is ... {message}')

                return message

            case "sector_position":
                #     -------------------------- START -----------------------------------
                print('fetching sector positions...')
                positions = mandala_node_position(img)
                print(f'finished, sector position is {positions}')

                return positions

            case "select_node":
                #     -------------------------- START -----------------------------------
                positions = img

                print(f'Clicking Sector... {positions}')
                pyautogui.click(positions[0])

                time.sleep(2)
                return

            case "node_sector":
                #     -------------------------- START -----------------------------------
                print('checking node_sector...')
                node_status, node_image = dispatch('node_status', img)
                sector_node = dispatch('sector_unlocked', node_image) if node_status == True else dispatch('sector_locked', node_image)
                return sector_node

            case "sector_unlocked":
                #     -------------------------- START -----------------------------------
                print('Sector Node is unlocked!')

                def node_img_parser(section):
                    result = mandala_node_state(dispatch_node(section, img), 'node_actions')
                    return result

                title = node_img_parser('title')
                stat_type = node_img_parser('stat_type')
                stat_value = node_img_parser('stat_value')
                current_node_level = node_img_parser('node_level')
                coin_price = node_img_parser('coin_price')
                orb_price = node_img_parser('orb_price')
                success_chance = node_img_parser('success_chance')
                return

            case "sector_locked":
                #     -------------------------- START -----------------------------------
                print('Sector Node is locked!')
                def node_img_parser(section):
                    result = mandala_node_state(dispatch_node(section, img), 'node_actions')
                    return result

                title = node_img_parser('title')
                invalid_msg = node_img_parser('invalid_msg')
                stat_type = node_img_parser('stat_value')
                stat_value = node_img_parser('node_level')
                current_node_level = 0
                coin_price = node_img_parser('coin_price')
                orb_price = node_img_parser('orb_price')
                success_chance = node_img_parser('success_chance')
                return

            case "node_status":
                #     -------------------------- START -----------------------------------
                print('node status invoked, retrieving, current node img & status ..')

                node_image = mandala_node_state(img, 'fetch_current_node_image')
                status = mandala_node_state(img, 'fetch_current_node_status')

                if "previous mandala has not been activated yet" in status:
                    return False, node_image

                return True, node_image


            case default:
                pass


