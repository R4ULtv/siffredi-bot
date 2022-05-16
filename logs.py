import logging

class DiscordLogs():
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)

    ch = logging.FileHandler('logs/error.log')
    ch.setLevel(logging.WARNING)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)
