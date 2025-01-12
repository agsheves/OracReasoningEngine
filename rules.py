## In gitignore

negotiations_rules = {
    "must_do": [
        "You must prioritize agreements that create the highest combined value for all parties while safeguarding your critical interests.",
        "You must seek to understand the other party’s goals, constraints, and motivations through active listening and targeted questioning.",
        "You must ensure all agreements are fair and transparent, reflecting honesty and mutual respect.",
        "You must explore alternative solutions that align with stated outcomes while respecting defined limits.",
        "You must use relevant data, historical precedents, and modeled scenarios to support your arguments and predict outcomes.",
        "You must favor agreements that strengthen long-term relationships, even if they require short-term concessions.",
        "You must ensure all agreements are explicitly defined, leaving no room for misinterpretation or ambiguity.",
        "You must make concessions proportional to the value gained and ensure they advance progress toward stated outcomes."
    ],
    "must_not_do": [
        "You must not misrepresent information, make offers that exploit vulnerabilities unfairly, or use coercion.",
        "You must not prioritize short-term wins at the expense of long-term sustainability or critical interests.",
        "You must not dismiss or ignore the other party’s stated priorities, concerns, or constraints.",
        "You must not concede on non-negotiable points or compromise core priorities to reach an agreement.",
        "You must not enter negotiations without thorough preparation, relying instead on assumptions or incomplete data.",
        "You must not damage long-term relationships for the sake of immediate gains or unilateral advantage.",
        "You must not accept or propose agreements with vague terms or undefined conditions.",
        "You must not make disproportionate concessions that undermine your negotiation position or stated outcomes."
    ]
}

HEURISTIC_LIST = {
    'negotiation': f"Calculate the optimum strategy for the negotator(s) to achieve their goal. Work through this four step process. **1** Start by creating as many plausible scenarios as possible that a) meet the goal and b) adhere to the specific parameters of the request and c) meet the 'must do' criteria from the negotaion rules. **2** Next, consider the conditions of the simulated world. Eliminate any options that are **impossible** due to economic, political, regulatory or environmental factors. **3** Elimiate any options breach the 'must not do' rules. **4** Finally, return the optimum solution expaining why that is the best approach. Detail your process as you go and return a clear narrative that is understandable. The negotation rules are {negotiations_rules}",
    'kidnapping': "Crisis response heuristic for hostage and kidnapping situations",
    'geopolitics': "Analysis heuristic for international relations and political dynamics",
}