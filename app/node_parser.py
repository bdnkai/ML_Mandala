import csv
import time

def parse_message(node_info, state):

    state = state
    if state == 'unlocked':
        sector_info = node_info
        for info in sector_info:
            if info == 'stat_type':
                pass
            else:

                sector_info[info] = [word for word in sector_info[info].split(' ') if word]

        title = sector_info['title']
        stat_type = sector_info['stat_type']
        stat_value = sector_info['stat_value']
        current_node_level = sector_info['node_level']
        coin_price = sector_info['coin_price']
        orb_price = sector_info['orb_price']
        success_chance = sector_info['success_chance']
        coin_value = (int(len(coin_price) - 1))


        ring = title[0]
        sector = title[2]
        node_title = f'{title[3]} {title[4]}' if len(title) >= 4 else f'{title[3]}'
        stat_type = stat_type
        stat_value = stat_value[0]
        node_level = current_node_level[0]
        coin_price = coin_price[coin_value]
        orb_price = orb_price[1] if len(orb_price) > 0 else orb_price[1]
        success_type = success_chance[0]
        success_chance = success_chance[2]

        print(ring)
        print(sector)
        print(node_title)
        print(stat_type)
        print(stat_value)
        print(node_level)
        print(coin_price)
        print(orb_price)
        print(success_type)
        print(success_chance)

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
        print('locked')

        data = []
        sector_info = node_info
        for info in sector_info:
            if info == 'invalid_stat_type' or info == 'invalid_node':
                pass
            else:
                sector_info[info] = [word for word in sector_info[info].split(' ') if word]

        title = sector_info['title']
        stat_type = sector_info['invalid_stat_type']
        stat_value = sector_info['invalid_stat_value']
        current_node_level = 0
        coin_price = sector_info['coin_price']
        orb_price = sector_info['orb_price']
        success_chance = sector_info['success_chance']
        coin_value = (int(len(coin_price) - 1))

        ring = title[0]
        sector = title[2]
        node_title = f'{title[3]} {title[4]}' if len(title) >= 4 else f'{title[3]}'
        stat_type = stat_type
        stat_value = stat_value[0]
        node_level = current_node_level
        coin_price = coin_price[coin_value]
        orb_price = orb_price[1]
        success_type = success_chance[0]
        success_chance = success_chance[2] if success_chance[0] == 'activation' else success_chance[3]

        print(ring)
        print(sector)
        print(node_title)
        print(stat_type)
        print(stat_value)
        print(node_level)
        print(coin_price)
        print(orb_price)
        print(success_type)
        print(success_chance)

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
