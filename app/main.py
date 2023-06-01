from mandala_actions import dispatch, game_name

if __name__ == '__main__':

    screen_img = game_name

    # dispatch('get_ring_information', screen_img)

    # found_position = dispatch('find_node_position', screen_img)

    # click = dispatch('select_node_position', found_position)
    # if found_position:

    dispatch('get_node_information', screen_img)



