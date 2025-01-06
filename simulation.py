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
        - Every response should start with a clear summary of the action taken
        - Use markdown formatting for better readability
        - Use bullet points and numbered lists where appropriate
        - Add line breaks between different topics or sections
        - If describing multiple items or steps, use numbered lists
        - For important information, use bold text with **asterisks**
        - Use code blocks for technical content or commands
        - Keep paragraphs short and focused (3-4 sentences max)

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

        SIMULATION STATUS: **RUNNING**
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
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": user_input
                }],
                system=self.system_prompt
            )

            # Log the raw response for debugging
            logging.debug(f"Raw API response: {response.content[0].text}")

            try:
                # Try to format the response content nicely
                content = response.content[0].text

                # Add separators between sections if they're not present
                content = content.replace("\n\n", "\n---\n")

                # Parse as JSON if possible for structured output
                try:
                    parsed_response = {
                        'response': content,
                        'state_update': response.content[0].text.split('State Update:')[-1].split('\n')[0].strip() if 'State Update:' in response.content[0].text else None,
                        'available_actions': [action.strip() for action in response.content[0].text.split('Available actions:')[-1].split('\n')[0].split(',')] if 'Available actions:' in response.content[0].text else []
                    }
                    return json.dumps(parsed_response)
                except:
                    # If not JSON, return formatted text
                    return json.dumps({
                        'response': content,
                    })

            except json.JSONDecodeError as je:
                logging.error(f"JSON parsing error: {je}")
                # Return a formatted error response
                return json.dumps({
                    "response": response.content[0].text,
                })

        except Exception as e:
            logging.error(f"Error in simulation processing: {str(e)}")
            raise