## These are a set of demo heuristics or rules for negotiations.
# Adjust these and amend the 'routing_and_logic.py / match_heuristic_with_llm' function as you see fit.

negotiations_rules = {
    "must_do": [
        "You must prioritize agreements that create the highest combined value for all parties while safeguarding your critical interests.",
        "You must seek to understand the other party’s goals, constraints, and motivations through active listening and targeted questioning.",
        "You must ensure all agreements are fair and transparent, reflecting honesty and mutual respect.",
        "You must explore alternative solutions that align with stated outcomes while respecting defined limits.",
        "You must use relevant data, historical precedents, and modeled scenarios to support your arguments and predict outcomes.",
        "You must favor agreements that strengthen long-term relationships, even if they require short-term concessions.",
        "You must ensure all agreements are explicitly defined, leaving no room for misinterpretation or ambiguity.",
        "You must make concessions proportional to the value gained and ensure they advance progress toward stated outcomes.",
    ],
    "must_not_do": [
        "You must not misrepresent information, make offers that exploit vulnerabilities unfairly, or use coercion.",
        "You must not prioritize short-term wins at the expense of long-term sustainability or critical interests.",
        "You must not dismiss or ignore the other party’s stated priorities, concerns, or constraints.",
        "You must not concede on non-negotiable points or compromise core priorities to reach an agreement.",
        "You must not enter negotiations without thorough preparation, relying instead on assumptions or incomplete data.",
        "You must not damage long-term relationships for the sake of immediate gains or unilateral advantage.",
        "You must not accept or propose agreements with vague terms or undefined conditions.",
        "You must not make disproportionate concessions that undermine your negotiation position or stated outcomes.",
    ],
}

geopolitical_strategy_rules = {
   "must_do": [
       "You must maintain 3+ independent paths to all critical resources",
       "You must keep one friendly power between you and potential adversaries",
       "You must hold leverage worth 2x any requested concession",
       "You must maintain 3:1 advantage in at least one critical domain vs any adversary",
       "You must maintain three distinct partner levels (core, strategic, tactical)",
       "You must keep secondary partnerships at 50%+ value of primary alliances",
       "You must ensure strategic plans survive loss of any single alliance",
       "You must maintain ability to reverse any position within 2 strategic cycles",
       "You must plan resources for 2x expected timeline",
       "You must ensure benefits exceed costs by 3x for strategic moves",
       "You must keep position viable if 2 major assumptions fail"
   ],
   "must_not_do": [
       "You must not let single adversary control >40% of vital supply",
       "You must not let any alliance control >60% of strategic options", 
       "You must not allow adversary to achieve >50% control of strategic domain",
       "You must not accept single points of failure in critical systems",
       "You must not lose independent action capability",
       "You must not commit >30% resources to single strategy",
       "You must not commit >40% strategic resources to single theater",
       "You must not accept strategic damage >20% from single loss",
       "You must not take positions requiring 100% alliance compliance",
       "You must not accept timelines requiring perfect execution",
       "You must not assume adversary incompetence",
       "You must not assume permanent alignment of interests",
       "You must not assume technology will solve structural problems",
       "You must not plan without multiple contingencies",
       "You must not accept unverifiable intelligence about adversary capabilities"
   ]
}

HEURISTIC_LIST = {
    "negotiation":
    f"""
Calculate the optimum strategy for the negotiator(s) to achieve their goal. Work through this four step process. 
**1** Start by creating as many plausible scenarios as possible that a) meet the goal and b) adhere to the specific parameters of the request and c) meet the 'must do' criteria from the negotiation rules. 
**2** Next, consider the conditions of the simulated world. Eliminate any options that are **impossible** due to economic, political, regulatory or environmental factors. 
**3** Elimiate any options breach the 'must not do' rules. 
**4** Finally, return the optimum solution expaining why that is the best approach. 
Take your time and explain your thinking for each step so the user can understand the process followed and decisions made. Explicitly note where an option was rejected for breachiug a rule. Expain the final suggestion in a clear narrative that is understandable. The negotation rules are {negotiations_rules}
""",
    "geopolitics": f"""
Analyze geopolitical scenarios and develop strategic recommendations by following this structured process:

    1. SITUATION MAPPING
    - Map all relevant actors, capabilities, and relationships
    - Identify critical resources, chokepoints, and centers of gravity
    - Document key assumptions and intelligence confidence levels
    - List explicit constraints from scenario
    - Define success criteria and objectives

    2. OPPORTUNITY ANALYSIS
    Generate potential strategies that:
    a) Meet defined objectives
    b) Adhere to scenario constraints
    c) Comply with all 'must do' rules
    d) Account for likely responses from all major actors

    3. FEASIBILITY FILTERING
    Eliminate strategies that:
    a) Violate physical, economic, or political realities
    b) Breach any 'must not do' rules
    c) Rely on unrealistic assumptions
    d) Cannot survive likely countermoves
    Document elimination reasoning.

    4. OPTIMAL STRATEGY SELECTION
    - Evaluate remaining strategies for:
      * Success probability
      * Resource efficiency
      * Risk-reward balance
      * Long-term sustainability
    - Select and justify optimal approach
    - Identify key decision points

Take your time and explain your thinking for each step so the user can understand the process followed and decisions made. Explicitly note where an option was rejected for breachiug a rule. Expain the final suggestion in a clear narrative that is understandable. The strategic framework rules are: {geopolitical_strategy_rules}
    """
}
