from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

PAGE_DELAY = 2 # default 3
IDEA_DELAY = 1 # default 2
DEVELOPMENT_TESTING = True # default True only parses 1 page not all
HEADLESS_MODE = False # default False

