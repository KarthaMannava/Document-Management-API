import logging

class Logger:
    """
    Singleton Logger class for creating and managing a logging instance.
    """
    _instance = None

    def __new__(cls):
        """
        Override the __new__ method to enforce the Singleton pattern.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize_logger()
        return cls._instance

    def initialize_logger(self):
        """
        Initialize the logger with desired configuration.
        """
        self.logger = logging.getLogger("my_app")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        file_handler = logging.FileHandler("logger/app.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
