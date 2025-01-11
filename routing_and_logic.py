import anthropic
import os
import json
import logging
from typing import Tuple, Optional, Dict
from scenario_parser import ScenarioParser

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Anthropic client
api_key = os.environ.get('ANTHROPIC_API_KEY')
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

client = anthropic.Client(api_key=api_key)
scenario_parser = ScenarioParser()

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


# Define available heuristics with descriptions
HEURISTIC_LIST = {
    'negotiation': f"Calculate the optimum strategy for the negotator(s) to achieve their goal. Work through this four step process. **1** Start by creating as many plausible scenarios as possible that a) meet the goal and b) adhere to the specific parameters of the request and c) meet the 'must do' criteria from the negotaion rules. **2** Next, consider the conditions of the simulated world. Eliminate any options that are **impossible** due to economic, political, regulatory or environmental factors. **3** Elimiate any options breach the 'must not do' rules. **4** Finally, return the optimum solution expaining why that is the best approach. Detail your process as you go and return a clear narrative that is undersatdnable. The negotation rules are {negotiations_rules}",
    'kidnapping': "Crisis response heuristic for hostage and kidnapping situations",
    'geopolitics': "Analysis heuristic for international relations and political dynamics",
}

def check_shortcode(message: str) -> Optional[str]:
    """
    Check if message contains a valid heuristic shortcode.
    Returns the heuristic name if found, None otherwise.
    """
    if not message:
        return None

    words = message.lower().split()
    for word in words:
        if word.startswith('/'):
            # Remove the '/' and check if it's a valid heuristic
            potential_heuristic = word[1:]
            if potential_heuristic in HEURISTIC_LIST:
                logger.debug(f"Found valid shortcode: {potential_heuristic}")
                return potential_heuristic

    logger.debug("No valid shortcode found")
    return None

def match_heuristic_with_llm(message: str) -> Tuple[str, str]:
    """
    Use Claude to match message content with appropriate heuristic.
    Returns tuple of (heuristic_name, settings).
    """
    logger.debug("Attempting to match message with heuristic using Claude")

    system_prompt = """
    Analyze the following scenario and determine which heuristic best matches its content.
    For geopolitical analysis involving international relations, trade, or political dynamics, use the 'geopolitics' heuristic.
    For negotiation scenarios involving diplomatic discussions or conflict resolution, use the 'negotiation' heuristic.
    For crisis scenarios involving immediate threats or hostage situations, use the 'kidnapping' heuristic.

    Respond in JSON format only:
    {
        "heuristic": "geopolitics|negotiation|kidnapping|none",
        "confidence": <float between 0 and 1>,
        "reasoning": "<brief explanation>"
    }
    """

    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": message
            }],
            system=system_prompt
        )

        try:
            result = json.loads(response.content[0].text)
            heuristic = result.get('heuristic', 'none')
            confidence = result.get('confidence', 0.0)

            logger.debug(f"LLM matched heuristic: {heuristic} with confidence: {confidence}")

            if heuristic != 'none' and confidence > 0.7:
                return heuristic, HEURISTIC_LIST[heuristic]
            return 'none', 'No matching heuristic found'

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return 'none', 'Error parsing response'

    except Exception as e:
        logger.error(f"Error in LLM matching: {e}")
        return 'none', 'Error in processing'

def process_scenario(message: str) -> Dict:
    """
    Complete workflow for processing a scenario:
    1. Route to appropriate heuristic
    2. Parse scenario details
    3. Return formatted scenario for confirmation

    Returns a dictionary containing:
    - heuristic: the matched heuristic
    - parsed_scenario: structured scenario details
    - display_format: human-readable format for confirmation
    - original_prompt: the original user input for editing
    """
    logger.info("Processing new scenario request")

    # Step 1: Route to appropriate heuristic
    shortcode_match = check_shortcode(message)
    if shortcode_match:
        heuristic = shortcode_match
        heuristic_desc = HEURISTIC_LIST[shortcode_match]
    else:
        heuristic, heuristic_desc = match_heuristic_with_llm(message)
        if heuristic == 'none':
            raise ValueError("Could not match scenario to any available heuristic")

    # Step 2: Parse scenario details
    try:
        parsed_scenario = scenario_parser.parse_scenario(message)
        # Add the matched heuristic to the scenario parameters
        parsed_scenario['parameters'] = parsed_scenario.get('parameters', {})
        parsed_scenario['parameters']['heuristic'] = heuristic

        # Step 3: Format for display
        display_format = scenario_parser.format_for_display(parsed_scenario)

        return {
            'heuristic': heuristic,
            'heuristic_description': heuristic_desc,
            'parsed_scenario': parsed_scenario,
            'display_format': display_format,
            'original_prompt': message  # Include original prompt for editing
        }
    except Exception as e:
        logger.error(f"Error processing scenario: {e}")
        raise

def initial_routing(message: str) -> str:
    """
    Main routing function that checks for shortcodes first,
    then falls back to LLM matching if no shortcode is found.
    """
    logger.debug(f"Processing message for routing: {message}")

    shortcode_match = check_shortcode(message)
    if shortcode_match:
        logger.info(f"Routing via shortcode to heuristic: {shortcode_match}")
        return HEURISTIC_LIST[shortcode_match]

    logger.debug("No shortcode found, attempting LLM matching")
    heuristic, settings = match_heuristic_with_llm(message)

    if heuristic == 'none':
        logger.info("No matching heuristic found")
        return "No specific heuristic matched - using default processing"

    logger.info(f"Routing via LLM match to heuristic: {heuristic}")
    return settings