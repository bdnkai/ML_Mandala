import csv


def parse_message(message):
    data = []
    # Split the message into words

    words = message.split()
    ring = words[0]
    sector = words[2]
    node_title = f'{words[3]} { words[4]}'
    stat_type = f'{words[5]}'
    stat_value = words[6]
    level = words[7][0]
    required_dragon_orbs = words[12]
    required_coins = f'{words[15]}{words[16]}'

    # Return the information as a dictionary
    return {
        "Ring": ring,
        "Sector": sector,
        "Node Title": node_title,
        "Stat Type": stat_type,
        "Stat Value": stat_value,
        "Level": level,
        "Required Dragon Orbs": required_dragon_orbs,
        "Required Coins": required_coins
    }

def update_data(data, parsed_message):
    # Check if this node already exists in the data
    existing_node = next((item for item in data if item["Node Title"] == parsed_message["Node Title"]), None)

    if existing_node is None:
        # This is a new node, so create a new dictionary for it
        node_data = {
            "Ring": parsed_message["Ring"],
            "Sector": parsed_message["Sector"],
            "Node Title": parsed_message["Node Title"],
            # Initialize the levels with placeholder values
            "Level 1": None,
            "Level 2": None,
            "Level 3": None,
            "Level 4": None,
            "Level 5": None,
            "Required Dragon Orbs": parsed_message["Required Dragon Orbs"],
            "Required Coins": parsed_message["Required Coins"]
        }
        data.append(node_data)
    else:
        # This node already exists, so update the existing dictionary
        node_data = existing_node

    # Update the level information
    node_data[f"Level {parsed_message['Level']}"] = parsed_message["Stat Value"]

    # Your data


    # Column headers
    headers = ["Ring", "Sector", "Node Title", "Stat Type", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5",
               "Required Dragon Orbs", "Required Coins"]


    # Write data to CSV file
    with open("data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)