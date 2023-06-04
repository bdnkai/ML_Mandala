import csv
import time

def parse_message(node_info, state):
    state = state

    if state == 'unlocked':
        sector_info = node_info

        for info in sector_info:
            if info == 'stat_type' or sector_info[info] == None:
                pass
            else:
                try:
                    if sector_info[info] is not None:
                        sector_info[info] = [word for word in sector_info[info].split(' ') if sector_info[info] is not None]
                except:
                    sector_info[info] = None

        title = sector_info['title']
        stat_type = sector_info['stat_type']
        stat_value_length = int(len(sector_info['stat_value'])) - 2
        stat_value = sector_info['stat_value']
        current_node_level = sector_info['node_level']
        coin_price = sector_info['coin_price']
        orb_price = sector_info['orb_price']
        success_chance = sector_info['success_chance']

        coin_length = (int(len(coin_price)))
        coin_value = coin_length - 1


        ring = title[0]
        sector = title[2]
        node_title = f'{title[3]} {title[4]}' if len(title) >= 4 else f'{title[3]}'
        stat_type = stat_type
        stat_value = stat_value[stat_value_length]
        node_level = current_node_level[0]
        coin_price = coin_price[1] if coin_length <=3 else coin_price[coin_value]
        orb_price = orb_price[1] if len(orb_price) > 0 else orb_price[1]
        success_type = success_chance[0]
        success_chance = success_chance[3] if success_type == 'enhancement' else success_chance[2]

        return {
            "Ring": ring,
            "Sector": sector,
            "Node Title": node_title,
            "Stat Type": stat_type,
            "Stat Value": stat_value,
            "Level": node_level,
            "Required Dragon Orbs": orb_price,
            "Required Coins": coin_price,
            'Success Type': success_type,
            'Success Chance': success_chance
        }



    if state == 'locked':
        sector_info = node_info
        for info in sector_info:
            if info == 'invalid_stat_type' :
                pass
            else:
                try:
                    if sector_info[info] is not None:
                        sector_info[info] = [word for word in sector_info[info].split(' ') if
                                             sector_info[info] is not None]
                except:
                    sector_info[info] = None

        title = sector_info['title']
        stat_type = sector_info['invalid_stat_type']
        invalid_stat_value_length = int(len(sector_info['invalid_stat_value'])) - 2
        stat_value = sector_info['invalid_stat_value']
        current_node_level = 0
        coin_price = sector_info['coin_price']
        orb_price = sector_info['orb_price']
        success_chance = sector_info['success_chance']

        coin_length = (int(len(coin_price)))
        coin_value = coin_length - 1

        ring = title[0]
        sector = title[2]

        node_title = f'{title[3]} {title[4]}' if len(title) <= 6  else f'{title[3]} {title[4]} {title[5]}'
        stat_type = stat_type
        stat_value = stat_value[invalid_stat_value_length]
        node_level = current_node_level
        coin_price = coin_price[1] if coin_length <=3 else coin_price[coin_value]
        orb_price = orb_price[1]
        success_type = success_chance[0]
        success_chance = success_chance[3] if success_type == 'enhancement' else success_chance[2]


        return {
            "Ring": ring,
            "Sector": sector,
            "Node Title": node_title,
            "Stat Type": stat_type,
            "Stat Value": stat_value,
            "Level": node_level,
            "Required Dragon Orbs": orb_price,
            "Required Coins": coin_price,
            'Success Type': success_type,
            'Success Chance': success_chance
        }