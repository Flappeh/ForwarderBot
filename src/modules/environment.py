from dotenv import load_dotenv
import os

load_dotenv(override=True)

TOKEN = os.getenv("TOKEN") 
BOT_USERNAME  = os.getenv("BOT_USERNAME") 
TIMEOUT_LIMIT = int(os.getenv("TIMEOUT_LIMIT"))

def get_all_env():
    data = [f"{i}: {j}" for i,j in os.environ.items()]
    return "\n".join(data)
