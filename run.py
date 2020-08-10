import logging
import sys
import os

# Add the src directory to our python path
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))


from natohuismanager import main, PgDatabase    
from config import Config

config = Config("config/production.json")

logging.basicConfig(
    level=logging.getLevelName(config['LOGLEVEL']),
    # Not printing the time here, since Heroku already adds the time to the logs.
    format="%(levelname)s: %(message)s", 
    datefmt="%H:%M:%S",
)

db = PgDatabase(config)
main(config, db)