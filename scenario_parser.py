import json
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

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

            Respond in JSON format with these fields:
            {
                "goal": "clear statement of the main objective",
                "constraints": ["list of time or resource constraints"],
                "conditions": ["list of specific rules or conditions"],
                "parameters": {"key": "value"} // optional additional parameters
            }
            """

            from simulation import world_simulator
            response = world_simulator.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": user_input
                }],
                system=system_prompt
            )

            # Parse the structured response
            parsed_json = json.loads(response.content[0].text)
            
            # Validate required fields
            for field in self.required_fields:
                if field not in parsed_json:
                    raise ValueError(f"Missing required field: {field}")

            return parsed_json

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse scenario JSON: {e}")
            raise ValueError("Failed to parse scenario into structured format")
        except Exception as e:
            logger.error(f"Error in scenario parsing: {e}")
            raise

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
