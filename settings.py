# settings.py
from dotenv import load_dotenv
import os
load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
# API_KEY = os.getenv("TELEGRAM_API_KEY")
API_KEY=os.environ.get('TELEGRAM_API_KEY')
# DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
print(API_KEY)