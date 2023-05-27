

def dispatch_node(action_type, image):
        match action_type:
            case "title":
                #     -------------------------- START -----------------------------------
                print('fetching title...')
                s1_top, s1_left, s1_right, s1_bottom = 0, 10, 225, 40
                sector_section = image[s1_top:s1_bottom, s1_left:s1_right]

                return sector_section

            case "stat_type":
                #     -------------------------- START -----------------------------------
                print('fetching stat_type...')
                s2_top, s2_left, s2_right, s2_bottom = 40, 10, 274, 80
                sector_section = image[s2_top:s2_bottom, s2_left:s2_right]

                return sector_section

            case "invalid_msg":
                #     -------------------------- START -----------------------------------
                print('fetching invalid msg...')
                s2_top, s2_left, s2_right, s2_bottom = 40, 10, 274, 80
                sector_section = image[s2_top:s2_bottom, s2_left:s2_right]

                return sector_section

            case "stat_value":
                #     -------------------------- START -----------------------------------
                print('fetching stat_value...')
                s3_top, s3_left, s3_right, s3_bottom = 80, 10, 276, 100
                sector_section = image[s3_top:s3_bottom, s3_left:s3_right]

                return sector_section

            case "node_level":
                #     -------------------------- START -----------------------------------
                print('fetching node_level...')
                s4_top, s4_left, s4_right, s4_bottom = 95, 70, 160, 125
                sector_section = image[s4_top:s4_bottom, s4_left:s4_right]

                return sector_section

            case "coin_price":
                #     -------------------------- START -----------------------------------
                print('fetching coin_price...')
                s5_top, s5_left, s5_right, s5_bottom = 325, 10, 260, 355
                sector_section = image[s5_top:s5_bottom, s5_left:s5_right]

                return sector_section

            case "orb_price":
                #     -------------------------- START -----------------------------------
                print('fetching orb_price...')
                s6_top, s6_left, s6_right, s6_bottom = 280, 80, 170, 325
                sector_section = image[s6_top:s6_bottom, s6_left:s6_right]

                return sector_section

            case "success_chance":
                #     -------------------------- START -----------------------------------
                s7_top, s7_left, s7_right, s7_bottom = 350, 10, 260, 375
                sector_section = image[s7_top:s7_bottom, s7_left:s7_right]

                print('fetching success_chance...')

                return sector_section


            case default:
                return "something"



