import logging
import os
from datetime import datetime

def get_logger(directory, run_name):
    """Logger for results
    """
    name_id = datetime.now().strftime('%Y%m%d%H%M%S')
    run_id = run_name + "_" + name_id + ".log"
    path = os.path.join(directory, run_id)
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(message)s")
    
    if len(logger.handlers) == 0:
        file_handler = logging.FileHandler(path, "w")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)

    return logger