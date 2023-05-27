

def dispatch_parse(action_type, message):
        match action_type:
            case "invalid node":
                #     -------------------------- START -----------------------------------
                print('node is invalid to level')


                return

            case "proc_nodes":
                #     -------------------------- START -----------------------------------
                print('proc nodes started')
                positions = img
                pyautogui.click(positions[0])
                time.sleep(2)

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



