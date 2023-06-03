
import cv2 as cv
def dispatch_split_node(action_type, image):
        match action_type:
            case "title":
                s1_top, s1_left, s1_right, s1_bottom = 0, 10, 245, 40
                sector1_section = image[s1_top:s1_bottom, s1_left:s1_right]
                return sector1_section

            case "stat_type":
                s2_top, s2_left, s2_right, s2_bottom = 40, 10, 264, 80
                sector2_section = image[s2_top:s2_bottom, s2_left:s2_right]
                return sector2_section

            case "stat_value":
                s3_top, s3_left, s3_right, s3_bottom = 70, 20, 260, 105
                sector3_section = image[s3_top:s3_bottom, s3_left:s3_right]
                return sector3_section

            case "node_level":
                s4_top, s4_left, s4_right, s4_bottom = 95, 70, 160, 125
                sector4_section = image[s4_top:s4_bottom, s4_left:s4_right]

                return sector4_section

            case "invalid_node":
                s2_top, s2_left, s2_right, s2_bottom = 40, 10, 274, 80
                sector5_section = image[s2_top:s2_bottom, s2_left:s2_right]

                return sector5_section

            case "invalid_stat_type":
                s3_top, s3_left, s3_right, s3_bottom = 80, 10, 276, 100
                sector6_section = image[s3_top:s3_bottom, s3_left:s3_right]
                return sector6_section

            case "invalid_stat_value":
                s4_top, s4_left, s4_right, s4_bottom = 95, 10, 255, 120
                sector7_section = image[s4_top:s4_bottom, s4_left:s4_right]
                return sector7_section

            case "coin_price":
                s5_top, s5_left, s5_right, s5_bottom = 325, 20, 260, 355
                sector8_section = image[s5_top:s5_bottom, s5_left:s5_right]

                return sector8_section

            case "orb_price":
                s6_top, s6_left, s6_right, s6_bottom = 280, 80, 170, 325
                sector9_section = image[s6_top:s6_bottom, s6_left:s6_right]
                return sector9_section

            case "success_chance":
                s7_top, s7_left, s7_right, s7_bottom = 350, 10, 260, 375
                sector0_section = image[s7_top:s7_bottom, s7_left:s7_right]
                return sector0_section

            case default:
                return "something"



