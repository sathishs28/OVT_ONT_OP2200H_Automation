import os
import logging
from datetime import datetime

# log_path = "./Logs/"

relative_log_path = "./Logs/"
log_path = os.path.abspath(relative_log_path)


class LogGen:
    @staticmethod
    def loggen(log_directory=log_path):
        # Create the log directory if it doesn't exist
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        # Get the current date and time for the log filename
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = os.path.join(log_directory, f"Automation_Log_{current_datetime}.log")

        # Create a logger and configure it
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # Create a formatter for the log messages
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Create a file handler to write logs to the file
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)
        return logger
