import logging

logging.basicConfig(filename='app.log', level=logging.INFO)

def log_message(msg):
    logging.info(msg)