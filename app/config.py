import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    ''' Base configuration for the triq application '''

    # Set the secret key from the environment variable
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Set the database URI from the environment variable
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Disable modification tracking for SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Controls whether the Flask application should be in debug mode
    DEBUG = True

    # Select which ticket analyzer to use
    AI_PROVIDER = os.getenv('AI_PROVIDER')

    

