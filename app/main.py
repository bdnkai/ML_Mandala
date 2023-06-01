from mandala_actions import dispatch, game_name

if __name__ == '__main__':

    screen_img = game_name

    # dispatch('sector_left', screen_img)

    # found_position = dispatch('sector_position', screen_img)
    # click = dispatch('select_node', found_position)
    # if found_position:
    #  wow = dispatch('node_sector', screen_img)

    dispatch('node_sector', screen_img)



