import threading
from mandala_actions import dispatch, get_variable, dispatch_craft
import time
import keyboard

if __name__ == '__main__':
    app, lazy = get_variable()
    plus, craft, okay_button, okay2_button = lazy

    def stop_script(e):
        print('Stopping script...')
        exit(e)
        quit()

    def perform_craft():
        plus_position = dispatch_craft("vision", app, plus, threshold=0.8)
        if plus_position == 'done':
            craft_position = dispatch_craft("press_once", app, craft, 0.6)
            if craft_position == 'done':
                okay_position = dispatch_craft("press_once", app, okay_button, 0.65)
                if okay_position == 'done':
                    okay2_position = dispatch_craft("press_once_wait", app, okay2_button, 0.95)

    def main_thread():
        while True:
            keyboard.on_press_key('q', stop_script)
            print('Running script...')
            # Create and start the craft thread
            craft_thread = threading.Thread(target=perform_craft)
            craft_thread.start()
            craft_thread.join()  # Wait for the craft thread to finish before proceeding to the next iteration

    main_thread()
