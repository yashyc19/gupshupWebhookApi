import logging
# import sys
import os
import atexit

class LogGen:
    _instance = None

    @staticmethod
    def loggen(log_file_name="Automation.log"):
        if LogGen._instance is None:
            LogGen(log_file_name)
        return LogGen._instance

    def __init__(self, log_file_name):
        if LogGen._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            LogGen._instance = self
            # Create a logs folder if it does not exist
            os.makedirs(os.path.join(os.getcwd(), 'logs'), exist_ok=True)
            self.log_file_path = os.path.join(os.getcwd(), 'logs', log_file_name)
            self.logger = logging.getLogger(log_file_name)
            self.logger.setLevel(logging.INFO)

            # Create a file handler
            handler = logging.FileHandler(self.log_file_path)
            handler.setLevel(logging.INFO)

            # Create a logging format
            formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
            handler.setFormatter(formatter)

            # Add the handlers to the logger
            self.logger.addHandler(handler)

            # Register a function to close the logger when the application exits
            atexit.register(self.close)

    def close(self):
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)
        logging.shutdown()

    def log_request(self, request):
        """
        Log details about an incoming request.
        """
        self.info(f"Request received: {request.method} {request.url}")
        # Log headers and body with caution
        self.info(f"Headers: {request.headers}")
        # Be cautious with logging request body
        # self.info(f"Body: {request.get_data(as_text=True)}")

    def log_response(self, response):
        """
        Log details about an outgoing response.
        """
        self.info(f"Response sent: {response.status_code}")
        # Log headers and body with caution
        self.info(f"Headers: {response.headers}")
        # Be cautious with logging response body
        # self.info(f"Body: {response.get_data(as_text=True)}")

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)