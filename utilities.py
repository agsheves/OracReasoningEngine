# Define available heuristics with descriptions
def list_all_heuristic_names():
    heuristic_list = "Available heuristics:"
    for heuristic_id, details in heuristics_data["heuristics"].items():
        heruistic_list += f"- {details['name']} (ID: {heuristic_id})"
    return heuristic_list


def list_all_heuristic_names_and_characteristics():
    heuristic_characteristics = "Available heuristics and characteristics:\n"
    for heuristic_id, details in heuristics_data["heuristics"].items():
        heuristic_characteristics += f"- {details['name']} (ID: {heuristic_id})"
        heuristic_characteristics += f"  Description: {details['description']}\n"
    return heuristic_characteristics


def get_heuristic_details(heuristic_id):
    if heuristic_id in heuristics_data["heuristics"]:
        return heuristics_data["heuristics"][heuristic_id]
    return None