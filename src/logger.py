import logging 
import os 
from datetime import datetime

LOG_DIRECTORY = "logs"

os.makedirs(LOG_DIRECTORY, exist_ok=True)

log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
log_filepath = os.path.join(LOG_DIRECTORY, log_filename)

logging.basicConfig(
    level=logging.INFO
    ,format="[%(asctime)s] %(levelname)s %(name)s: %(message)s"
    ,handlers = [
        logging.FileHandler(log_filepath)
        ,logging.StreamHandler()
    ],
)

logger = logging.getLogger("mlproject")
