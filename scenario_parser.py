import json
import logging
from typing import Dict, Optional
import os
import anthropic

logger = logging.getLogger(__name__)
api_key = os.environ.get('ANTHROPIC_API_KEY')
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

client = anthropic.Client(api_key=api_key)

class ScenarioParser:
    def __init__(self):
        self.required_fields = ['goal', 'constraints', 'conditions']

    def parse_scenario(self, user_input: str) -> Dict:
        """
        Parse user input into a structured scenario format.
        Returns a dictionary containing the parsed scenario elements.
        """
        try:
            # Format the prompt to extract structured information
            system_prompt = """
            Parse the given scenario into a structured format. Extract:
            1. Main goal/objective
            2. Time constraints or deadlines
            3. Specific conditions or rules
            4. Key parameters or variables

            For geopolitical scenarios, consider:
            - International relations
            - Economic factors
            - Strategic implications
            - Current global context

            Respond in JSON format with these fields:
            {
                "goal": "clear statement of the main objective",
                "constraints": ["list of time or resource constraints"],
                "conditions": ["list of specific rules or conditions"],
                "parameters": {
                    "key": "value",
                    "entities": ["list of involved entities"],
                    "timeline": "relevant timeframe"
                }
            }
            If you cannot identify any of these elements, respond with "none specified" for that field to ensure there is a coplete JSON payload returned.
            """

            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": user_input
                }],
                system=system_prompt)

            # Parse the structured response
            try:
                parsed_json = json.loads(response.content[0].text)
                logger.debug(f"Parsed scenario: {parsed_json}")

                # Validate required fields
                for field in self.required_fields:
                    if field not in parsed_json:
                        raise ValueError(f"Missing required field: {field}")

                return parsed_json

            except json.JSONDecodeError as je:
                logger.error(f"Failed to parse scenario JSON: {je}")
                raise ValueError("Failed to parse scenario into structured format")

        except Exception as e:
            logger.error(f"Error in scenario parsing: {e}")
            raise ValueError(f"Failed to process scenario: {str(e)}")

    def format_for_display(self, parsed_scenario: Dict) -> str:
        """
        Convert the parsed scenario into a human-readable format for user confirmation.
        """
        try:
            output = [
                "=== Scenario Summary ===\n",
                f"Goal: {parsed_scenario['goal']}\n",
                "\nConstraints:",
                *[f"- {constraint}" for constraint in parsed_scenario['constraints']],
                "\nConditions:",
                *[f"- {condition}" for condition in parsed_scenario['conditions']],
            ]

            if 'parameters' in parsed_scenario:
                output.extend([
                    "\nAdditional Parameters:",
                    *[f"- {key}: {value}" for key, value in parsed_scenario['parameters'].items()]
                ])

            return "\n".join(output)

        except Exception as e:
            logger.error(f"Error formatting scenario: {e}")
            raise ValueError("Failed to format scenario for display")