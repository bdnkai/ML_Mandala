import cv2 as cv
import numpy as np
import os
import time
import concurrent.futures
from mandala import mandala_node, mandala_message

game_name = 'MIRMG(1)'
def dispatch(mandala_action, img):
        match mandala_action:
            case "proc_text":
                #     -------------------------- START -----------------------------------
                print('proc test started')
                return

            case "proc_nodes":
                #     -------------------------- START -----------------------------------
                print('proc nodes started')


            case "sector_left":
                #     -------------------------- START -----------------------------------
                print('getting left block message...')

                message = mandala_message(img, 'left')

                print(f' Success Chance to Unlock is ... {message}')

                return message



            case "sector_position":
                #     -------------------------- START -----------------------------------
                print('fetching sector positions...')

                node = mandala_node(img)

                print(f'finished, sector position is {node}')

                return node

            case "sector_right":
                #     -------------------------- START -----------------------------------
                print('getting right block message...')
                message = mandala_message(img, 'right')

                print(f'Core Sector Block says : {message}')
                return message

            case default:
                return "something"



