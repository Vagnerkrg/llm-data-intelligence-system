import logging

from src.logging.log_config import LOG_FILE



class Logger:


    @staticmethod
    def get_logger(
        name: str
    ) -> logging.Logger:


        logger = logging.getLogger(
            name
        )


        if logger.handlers:

            return logger



        logger.setLevel(
            logging.INFO
        )


        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )



        file_handler = logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        )


        file_handler.setLevel(
            logging.INFO
        )


        file_handler.setFormatter(
            formatter
        )



        logger.addHandler(
            file_handler
        )


        return logger