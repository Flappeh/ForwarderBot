__version__ = "0.0.1"

from telegram.ext import Application, Defaults
from src.modules.environment import TOKEN
import pytz
from src.modules.utils.logger import get_logger


LOGGER = get_logger(name=__name__)

builder = Application.builder()
builder.token(TOKEN)
builder.defaults(Defaults(tzinfo=pytz.timezone('Asia/Jakarta')))
app = builder.build()


LOGGER.info("INITIALIZING Telegram Pi Wallet Bot")

