import anthropic
import os
import json
import logging
from datetime import datetime

class WorldSimulator:

    def __init__(self):
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable is not set")

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

    def process_input(self, user_input, is_followup=False, scenario_context=None):
        try:
            logging.debug(f"Processing input: {user_input}, is_followup: {is_followup}")

            if is_followup and scenario_context:
                # For follow-up questions, include the original scenario context
                prompt = f"""Based on the following scenario context:
                {json.dumps(scenario_context, indent=2)}

                Please address this follow-up question while maintaining consistency with the scenario above:
                {user_input}

                Important:
                1. Use the scenario parameters and constraints from above
                2. Consider all previously established facts and conditions
                3. Provide a focused response to the specific follow-up question
                4. Maintain consistency with the world-state and previous responses"""
            else:
                # For initial scenarios, use the input directly
                prompt = user_input

            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                system=self.system_prompt)

            try:
                content = response.content[0].text
                content = content.replace("\n\n", "\n---\n")

                return json.dumps({
                    'response': content,
                    'state_update': response.content[0].text.split(
                        'State Update:')[-1].split('\n')[0].strip() if
                    'State Update:' in response.content[0].text else None,
                    'available_actions': [
                        action.strip()
                        for action in response.content[0].text.split(
                            'Available actions:')[-1].split('\n')[0].split(',')
                    ] if 'Available actions:' in response.content[0].text else []
                })

            except json.JSONDecodeError as je:
                logging.error(f"JSON parsing error: {je}")
                return json.dumps({
                    "response": response.content[0].text,
                })

        except Exception as e:
            logging.error(f"Error in simulation processing: {str(e)}")
            raise