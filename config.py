from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

DEVELOPMENT_TESTING = False # default True only parses 1 page not all
HEADLESS_MODE = True # default False

