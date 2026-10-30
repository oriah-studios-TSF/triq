import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    ''' Base configuration for the triq application '''

    # Set the secret key from the environment variable
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Controls whether the Flask application should be in debug mode
    DEBUG = True

    # Select which ticket analyzer to use
    AI_PROVIDER = os.getenv('AI_PROVIDER')

    # Ollama configuration
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL','qwen3:1.7b')
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

    

