import logging, logging.handlers
from datetime import datetime

import config


def listener_log_configurer():
    root = logging.getLogger()
    h = logging.StreamHandler()
    f = logging.Formatter(
        "%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s"
    )
    h.setFormatter(f)
    root.addHandler(h)
    now = datetime.now()
    logfilehandler = logging.handlers.TimedRotatingFileHandler(
        f"{config.LOGGER_FNAME}{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}.txt",
        when="midnight",
        backupCount=180,
    )
    logfilehandler.setFormatter(f)
    root.addHandler(logfilehandler)


def worker_log_configurer(queue):
    h = logging.handlers.QueueHandler(queue)
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.INFO)


class BlankLogger:
    def __init__(self):
        pass

    def info(self, message):
        print(message)

    def warning(self, message):
        print(message)

    def __str__(self):
        return "Blank logging class to allow for testing without logging thread"
