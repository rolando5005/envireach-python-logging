import os

from src.logging import Logger

def test_logger():
    logger = Logger()
    logger.info("This is an info message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    assert True

def test_logger_debug():
    logger = Logger(debug=True)
    logger.info("This is an info message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    assert True

def test_logger_file():
    file_name = "/logs.log"
    
    if os.path.exists(os.path.dirname(__file__) + file_name):
        os.remove(os.path.dirname(__file__) + file_name)
    assert not os.path.exists(os.path.dirname(__file__) + file_name)
    
    logger = Logger(folder=os.path.dirname(__file__))
    logger.info("This is an info message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    with open(os.path.dirname(__file__) + file_name, "r") as file:
        log = file.read()
    assert "This is an info message" in log
    assert "This is a debug message" in log
    assert "This is a warning message" in log
    assert "This is an error message" in log
    assert "This is a critical message" in log
    
    assert True