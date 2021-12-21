import logging

class DiscordLogs():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('logs/debug.log')
    fh.setLevel(logging.INFO)

    ch = logging.FileHandler('logs/error.log')
    ch.setLevel(logging.WARNING)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
