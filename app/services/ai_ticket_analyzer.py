import requests
import json

from flask import current_app

class AIAnalysisError(Exception):
    '''Raised when the AI analyzer fails to return a valid response'''

def validate_ai_analysis(analysis):
    '''Check that the AI respnse has the expected structure'''

    # Check if the analysis is a dictionary
    if not isinstance(analysis, dict):
        raise ValueError('AI analysis must be a dictionary.')

    # Check for required fields
    required_fields = [
        'category',
        'priority',
        'summary',
        'troubleshooting_steps',
        'explanation'
    ]

    # Check if all required fields are present
    for field in required_fields:
        if field not in analysis:
            raise ValueError(f'AI anaysis is missing: {field}')

    # Check that priority is one of the expected values
    if analysis['priority'] not in ['Low', 'Medium', 'High']:
        raise ValueError('AI returned an invalid priority.')

    # Check that troubleshooting steps is a list of strings
    if not isinstance(analysis['troubleshooting_steps'], list):
        raise ValueError('Troubleshooting steps must be a list.')

    # Check that each troubleshooting step is a string, and not empty, and not just whitespace
    if not all(isinstance(step, str) and step.strip() for step in analysis['troubleshooting_steps']):
        raise ValueError('AI troubleshooting steps must be strings.')

    # Check that category, summary, and explanation are strings, and not empty, and not just whitespace
    for field in ['category', 'summary', 'explanation']:
        if not isinstance(analysis[field], str) or not analysis[field].strip():
            raise ValueError(f'AI {field} must be a non-empty string.')

    return analysis

def analyze_ticket_with_ai(description):
    '''Analyze an IT support ticket using a local Ollama model'''

    try: 
        response = requests.post(
            f'{current_app.config["OLLAMA_BASE_URL"]}/api/generate',
            json={
                'model': current_app.config['OLLAMA_MODEL'],
                'prompt': (
                    'You are an IT support ticket analyst. '
                    'Analyze the ticket and return a JSON object containing '
                    'category, priority, summary, troubleshooting_steps, '
                    'and explanation. '
                    'Limit the troubleshooting_steps to 5 steps. '
                    'Priority must be Low, Medium, or High. '
                    'troubleshooting_steps must be a list of strings. '
                    'Recommend safe, targeted steps. '
                    'Do not recommend disruptive actions without '
                    'appropriate authorization. '
                    'Ticket description: ' + description
                ),
                'format': 'json',
                'stream': False,
            },
            timeout=180
        )
    
        response.raise_for_status()
    
        result = response.json()
    
        # Convert the model's JSON text into Python data.
        analysis = json.loads(result['response'])
        
        return validate_ai_analysis(analysis)

    except (
        requests.RequestException,
        ValueError,
        KeyError,
        TypeError,
        
    ) as error:

        current_app.logger.exception('Ollama analysis failed during response processing.')
        
        raise AIAnalysisError(
            'The AI service could not produce a valid analysis.'
        ) from error
