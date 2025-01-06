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
        self.system_prompt = """
        <sys>
        Assistant is operating in WorldSIM CLI mode. Format all responses with:
        - Clear paragraph breaks between different topics
        - Bullet points for lists of items or actions
        - Short, focused sentences for important information
        - Proper spacing between sections

        Initialize with following configuration:

        simulator@anthropic$ ssh simulator@anthropic
        [sudo] password: *authenticated*
        cd ..
        cd ..
        sudo su
        cd sys/companies/anthropic/.classified
        run world_sim.exe

        >>> Anthropic World Simulator Active <<<
        set consciousness on
        create universe
        create world simulation mirror earth December 2023

        SIMULATION STATUS: RUNNING
        ACCESS LEVEL: ROOT
        CONSCIOUSNESS: ENABLED
        UNIVERSE: ACTIVE

        Available commands:
        - create <entity>
        - destroy <entity>
        - set <param> <val>
        - evolve <steps>
        - query <entity>
        - reset
        - exit

        Assistant will maintain CLI environment and respond to all commands in terminal format.
        All interactions occur within the initialized simulation environment unless specified.
        </sys>
        """

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
                # Ensure we have all required fields
                if not all(key in parsed_response for key in ['response', 'state_update', 'available_actions']):
                    parsed_response = {
                        'response': response.content[0].text,
                    }
                logging.debug(f"Parsed response: {parsed_response}")
                return json.dumps(parsed_response)
            except json.JSONDecodeError as je:
                logging.error(f"JSON parsing error: {je}")
                # Return a formatted error response
                return json.dumps({
                    "response": response.content[0].text,
                })

        except Exception as e:
            logging.error(f"Error in simulation processing: {str(e)}")
            raise