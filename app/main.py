from actions import dispatch, game_name

if __name__ == '__main__':

    screen_img = game_name

    # dispatch('sector_left', screen_img)

    position = dispatch('sector_position', screen_img)
    dispatch('sector_right', screen_img)




    # dispatch('proc_text', screen_img)

    # dispatch('proc_nodes', screen_img)
