from dotenv import load_dotenv
from src.modules.utils.logger import get_logger
import json
import os

load_dotenv(override=True)


LOGGER = get_logger(__name__)

TOKEN = os.getenv("TOKEN") 
BOT_USERNAME  = os.getenv("BOT_USERNAME") 
TIMEOUT_LIMIT = int(os.getenv("TIMEOUT_LIMIT"))
REMOVE_TAG = bool(os.getenv("REMOVE_TAG"))

# load json file
config_name = "chat_list.json"
CONFIG = {}
if not os.path.isfile(config_name):
    LOGGER.error("No chat_list.json config file found! Exiting...")
    exit(1)
with open(config_name, "r") as data:
    CONFIG = json.load(data)


def get_all_env():
    data = [f"{i}: {j}" for i,j in os.environ.items()]
    return "\n".join(data)