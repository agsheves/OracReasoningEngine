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

# Define available heuristics with descriptions
HEURISTIC_LIST = {
    'negotiation': "Simulation heuristic for negotiation scenarios and diplomatic interactions",
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

    # Construct the prompt for Claude
    heuristic_options = "\n".join([f"- {key}: {value}" for key, value in HEURISTIC_LIST.items()])

    system_prompt = f"""
    Analyze the following message and determine which heuristic best matches its content.
    Available heuristics:
    {heuristic_options}

    Respond in JSON format only:
    {{
        "heuristic": "<heuristic_name>",
        "confidence": <float between 0 and 1>,
        "reasoning": "<brief explanation>"
    }}

    If no heuristic matches well, use "none" as the heuristic name.
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
            'display_format': display_format
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

    # First check for shortcode
    shortcode_match = check_shortcode(message)
    if shortcode_match:
        logger.info(f"Routing via shortcode to heuristic: {shortcode_match}")
        return HEURISTIC_LIST[shortcode_match]

    # If no shortcode, use LLM matching
    logger.debug("No shortcode found, attempting LLM matching")
    heuristic, settings = match_heuristic_with_llm(message)

    if heuristic == 'none':
        logger.info("No matching heuristic found")
        return "No specific heuristic matched - using default processing"

    logger.info(f"Routing via LLM match to heuristic: {heuristic}")
    return settings