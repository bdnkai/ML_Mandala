from mandala_actions import dispatch, get_variable

if __name__ == '__main__':

    # captured_img = application_name
    app, a_unlock, a_lock, e_unlock, e_lock = get_variable()



    # dispatch('get_ring_information', screen_img)

    # found_position = dispatch('find_node_position', application)

    # click = dispatch('select_node_position', found_position)
    # if found_position:

    message =dispatch('get_node_information', app)
    print(message)


