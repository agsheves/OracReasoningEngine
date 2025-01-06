import anthropic
import os
import json
import logging
from datetime import datetime

class WorldSimulator:
    def __init__(self):
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

        self.client = anthropic.Client(api_key=api_key)
        self.system_prompt = """You are an AI world simulator. You maintain and evolve a persistent virtual world, ensuring internal consistency, realistic reactions to user interactions, and engaging narratives. 

You must ALWAYS respond with valid JSON in the following format:
{
    "response": "Your detailed description of the world state and events here",
    "state_update": "Brief summary of key changes to the world state",
    "available_actions": ["list", "of", "possible", "actions"]
}"""

    def process_input(self, user_input):
        try:
            # Log the input for debugging
            logging.debug(f"Processing user input: {user_input}")

            # Create a structured request with system as top-level parameter
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": user_input
                }],
                system=self.system_prompt
            )

            # Log the raw response for debugging
            logging.debug(f"Raw API response: {response.content[0].text}")

            try:
                # Parse the response text as JSON
                parsed_response = json.loads(response.content[0].text)
                logging.debug(f"Parsed response: {parsed_response}")
                return parsed_response
            except json.JSONDecodeError as je:
                logging.error(f"JSON parsing error: {je}")
                # Return a formatted error response
                return {
                    "response": "I apologize, but I encountered an error processing the world simulation. Please try again.",
                    "state_update": "Error in processing",
                    "available_actions": ["try again", "reset simulation"]
                }

        except Exception as e:
            logging.error(f"Error in simulation processing: {str(e)}")
            raise