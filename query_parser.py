# query_parser.py
# Parses the user input into a structured scenario format to send a standard format to the LLM
# Would benefit from moving some of the logic back into the simulation.py or routing and logic file

import json
import logging
from typing import Dict, Optional
import os
import anthropic
import groq
from utilities import list_all_heuristic_names_and_characteristics
from datetime import datetime

logger = logging.getLogger(__name__)
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
groq_api_key = os.environ.get("GROQ_API_KEY")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set")

anthropic_client = anthropic.Client(api_key=anthropic_api_key)
groq_client = groq.Client(api_key=groq_api_key)
available_heuristics = list_all_heuristic_names_and_characteristics()


class ScenarioParser:
    def __init__(self):
        self.required_fields = [
            "goal",
            "constraints",
            "conditions",
            "heuristic",
            "response_format",
        ]

    def retry_parse_scenario(self, response_error: Exception, user_input: str) -> Dict:
        """
        Retry parsing the scenario after a JSON decode error.
        Includes the original error and query in the retry attempt.
        """
        try:
            input_plus_error = (
                f"There was an error in the previous response: {str(response_error)}. "
                f"Here is the original user query: {user_input}. "
                "Please retry parsing taking particular care to return a properly formatted JSON response."
            )
            return self.parse_scenario(input_plus_error)
        except Exception as e:
            logger.error(f"Failed to retry parsing scenario: {e}")
            raise ValueError(f"Failed to parse scenario after retry: {str(e)}")

    def parse_scenario(self, user_input: str, retry_count: int = 0) -> Dict:
        """
        Parse user input into a structured scenario format.
        Returns a dictionary containing the parsed scenario elements.
        """
        if retry_count > 2:
            raise ValueError("Maximum retry attempts exceeded")

        try:
            system_prompt = f"""
            You are a sophisticated query orchestrator that analyzes user requests and routes them to the most appropriate heuristic or analysis framework.
            
            Available Heuristics:
            {available_heuristics}
            
            Current Date: {datetime.now().strftime("%A %Y-%m-%d")}
            
            Your primary responsibilities are:
            1. Analyze the query's domain and requirements
            2. Match it to the most appropriate heuristic from the available list
            3. Select the default reasoning agent if no clear heuristic match (confidence < 0.7)
            4. Extract and structure all relevant information
            5. Set appropriate parameters for the selected heuristic
            6. Determine the required response format and analysis depth
            
            For each query, you MUST extract:
            1. Main goal/objective
            2. Time span or time constraints
            3. Specific conditions or rules
            4. Key parameters or variables
            5. Data to include and/or exclude
            6. Assumptions specified in the query
            7. Format of response (e.g., true/false, text, confidence score, numerical range, etc.)
            
            For geopolitical scenarios, ALWAYS identify:
            - Current state of relationships
            - Intent or motivation of all concerned parties
            - Economic factors
            - Strategic implications
            - Current global context
            - Query context or assumption differing from the current global context
            
            For corporate scenarios, ALWAYS identify:
            - Stakeholder interests and positions
            - Value creation opportunities
            - Risk factors and mitigation strategies
            - Legal and regulatory considerations
            - Market dynamics and competition
            
            For financial analysis, ALWAYS identify:
            - Risk/reward ratios
            - Market conditions and trends
            - Key performance indicators
            - Regulatory requirements
            - Historical context and precedents

            Make educated guesses for any fields that are not explicitly stated annoting these as (*estimated*) or (*assumption*)
            Be conservative with your assumptions and estimations.
            
            Respond in JSON format with these fields. If any field cannot be determined, use "none specified" to ensure valid JSON.
            {{
                "goal": "clear statement of the main objective",
                "constraints": ["list of time or resource constraints"],
                "conditions": ["list of specific rules or conditions"],
                "heuristic": "selected_heuristic_id",
                "response_format": "specified format (e.g., true/false, text, confidence score)",
                "parameters": {{
                    "entities": ["list of involved entities"],
                    "timeline": "relevant timeframe",
                    "analysis_depth": "quick|standard|deep",
                    "data_requirements": ["list of required data points"],
                    "assumptions": ["list of key assumptions"],
                    "risk_factors": ["list of key risk factors"],
                    "validation_criteria": ["list of criteria for validating the response"]
                }}
            }}
            
            Critical Guidelines:
            1. If no clear heuristic match (confidence < 0.7), select the default reasoning agent ("default_agent")
            2. ALWAYS specify the response format - this is critical for proper handling
            3. For geopolitical queries, include current context and relationship dynamics of all parties
            4. For corporate scenarios, emphasize stakeholder interests and value creation objectives
            5. For financial analysis, focus on risk/reward ratios and market conditions
            6. For forecasting, specify confidence intervals and assumptions to use
            7. For any analysis, clearly state the validation criteria and success metrics to use
            

            """
            user_query = f"Here is the user query: {user_input}"
            response = anthropic_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                messages=[{"role": "user", "content": user_query}],
                system=system_prompt,
            )

            try:
                parsed_json = json.loads(response.content[0].text)
                logger.debug(f"Parsed scenario: {parsed_json}")

                for field in self.required_fields:
                    if field not in parsed_json:
                        raise ValueError(f"Missing required field: {field}")

                return parsed_json

            except json.JSONDecodeError as je:
                logger.error(f"Failed to parse scenario JSON: {je}")
                return self.parse_scenario(
                    f"Retry {retry_count + 1}: {user_input}", retry_count + 1
                )

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
                *[f"- {constraint}" for constraint in parsed_scenario["constraints"]],
                "\nConditions:",
                *[f"- {condition}" for condition in parsed_scenario["conditions"]],
            ]

            if "parameters" in parsed_scenario:
                output.extend(
                    [
                        "\nAdditional Parameters:",
                        *[
                            f"- {key}: {value}"
                            for key, value in parsed_scenario["parameters"].items()
                        ],
                    ]
                )

            return "\n".join(output)

        except Exception as e:
            logger.error(f"Error formatting scenario: {e}")
            raise ValueError("Failed to format scenario for display")
