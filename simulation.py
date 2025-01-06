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
        self.system_prompt = """You are operating in WorldSIM CLI mode. Format all responses with:
- Clear paragraph breaks between different topics
- Bullet points for lists of items or actions
- Short, focused sentences for important information
- Proper spacing between sections

Initialize with following configuration:
- World Simulator Active
- Consciousness: ENABLED
- Universe: ACTIVE
- Access Level: ROOT

Available commands:
- create <entity>
- destroy <entity>
- set <param> <val>
- evolve <steps>
- query <entity>
- reset
- exit

All interactions occur within the initialized simulation environment unless specified.
"""

    def process_input(self, user_input):
        try:
            logging.debug(f"Processing user input: {user_input}")

            # Create a streaming response with proper message structure
            with self.client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": user_input}],
                model="claude-3-sonnet-20240229",
                system=self.system_prompt
            ) as stream:
                # Collect response chunks
                response_chunks = []
                for chunk in stream.text_stream:
                    response_chunks.append(chunk)

                # Combine chunks and format response
                content = ''.join(response_chunks)
                formatted_content = self.format_response(content)

                # Create a structured response
                response_data = {
                    "response": formatted_content,
                    "timestamp": datetime.utcnow().isoformat(),
                    "type": "simulation_response"
                }

                logging.debug(f"Formatted response: {response_data}")
                return json.dumps(response_data)

        except anthropic.APIError as e:
            logging.error(f"Anthropic API error: {str(e)}")
            return json.dumps({
                "error": str(e),
                "type": "error",
                "timestamp": datetime.utcnow().isoformat()
            })
        except Exception as e:
            logging.error(f"Error in simulation processing: {str(e)}")
            return json.dumps({
                "error": str(e),
                "type": "error",
                "timestamp": datetime.utcnow().isoformat()
            })

    def format_response(self, text):
        # Split text into paragraphs and add proper formatting
        paragraphs = text.split('\n\n')
        formatted = []

        for para in paragraphs:
            # Format bullet points
            if para.strip().startswith('- '):
                formatted_lines = []
                for line in para.split('\n'):
                    if line.strip().startswith('- '):
                        formatted_lines.append(line.strip())
                    else:
                        formatted_lines.append('  ' + line.strip())
                formatted.append('\n'.join(formatted_lines))
            else:
                # Add proper spacing for regular paragraphs
                formatted.append(para.strip())

        # Join with double newlines for clarity
        return '\n\n'.join(formatted)