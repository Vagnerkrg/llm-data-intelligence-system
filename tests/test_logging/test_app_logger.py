from src.logging.app_logger import AppLogger



def test_app_logger_standard_message():

    logger = AppLogger(
        "test"
    )

    logger.info(
        "simple message"
    )



def test_app_logger_structured_message():

    logger = AppLogger(
        "test"
    )

    logger.info(

        "question_received",

        {
            "route": "rag"
        }

    )