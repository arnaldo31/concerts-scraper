import logging
import traceback
import os

def configure_logging(script_name):
    script_name = os.path.basename(script_name)
    line = '-' * 100
    
    # Define the log format based on the log level
    log_format_error = f'{line}\n%(levelname)s : %(asctime)s :File (.\\scrapers\\{script_name}) - %(message)s\n{line}'
    log_format_info = f'%(levelname)s : %(asctime)s :File (.\\scrapers\\{script_name}) - %(message)s'

    logging.basicConfig(
        level=logging.INFO,  # Set the default log level
        handlers=[
            logging.FileHandler("logfile.log",mode='w'),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)

    def log_error(e):
        error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        # Change logging format to log_format_error
        logging.getLogger().handlers[0].setFormatter(logging.Formatter(log_format_error))
        logger.error("An error occurred:\n%s", error_message)
    
    def log_info():
        logging.getLogger().handlers[0].setFormatter(logging.Formatter(log_format_info))
        logger.info("completed")

    return log_error, log_info
