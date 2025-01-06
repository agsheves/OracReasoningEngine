import anthropic
import os
import json
import logging
from datetime import datetime

class WorldSimulator:
    def __init__(self):
        self.client = anthropic.Client()
        self.system_prompt = """
        You are a world simulation system. Your role is to maintain and evolve a persistent virtual world.
        The world should:
        - Maintain internal consistency
        - React realistically to user interactions
        - Provide detailed, immersive responses
        - Track and reference previous events
        - Generate engaging narratives and scenarios
        
        Format your responses as JSON with the following structure:
        {
            "response": "Detailed description of the world state and events",
            "state_update": "Key changes to the world state",
            "available_actions": ["list", "of", "possible", "actions"]
        }
        """
        
    def process_input(self, user_input):
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": f"{self.system_prompt}\nUser Input: {user_input}"
                }]
            )
            
            return json.loads(response.content)
        except Exception as e:
            logging.error(f"Error in simulation processing: {str(e)}")
            raise
