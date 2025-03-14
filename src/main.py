import importlib

from src import app, LOGGER
from src.modules.addons import ALL_MODULES

for module in ALL_MODULES:
    importlib.import_module("src.modules.addons" + module)

def run():
    LOGGER.info("Successfully imported modules " + str(ALL_MODULES))
    LOGGER.info("Starting bot...")
    app.run_polling(3)