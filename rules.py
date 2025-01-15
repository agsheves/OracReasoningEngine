## This is where you define the heuristics and the top-levle prompt to send to the model.
# Adjust these and amend the 'routing_and_logic.py / match_heuristic_with_llm' function to match the heuristic name.

heuristic1_rules = {
    "must_do": [
        "thing to do 1",
        "thing to do 2",
    ],
    "must_not_do": [
        "thing to not do 1",
        "thing to not do 1",
    ],
}

heuristic2_rules = {
    "must_do": [
        "thing to do 1",
        "thing to do 2",
    ],
    "must_not_do": [
        "thing to not do 1",
        "thing to not do 1",
    ],
}

HEURISTIC_LIST = {
    "heuristic1": f"Insert prompt guidance here. End by including {heuristic1_rules}",
    "heuristic2": f"Insert prompt guidance here. End by including {heuristic2_rules}",
}
