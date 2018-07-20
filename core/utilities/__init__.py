from math import floor, log10
import logging
import logging.handlers

def round_to_exponent(x):
    return 10**int(floor(log10(abs(x)))) if x != 0 else 0

def logging_handler_setup(process_name):
		logger = logging.getLogger(process_name)
		logger.setLevel(logging.DEBUG)

		sock_handler = logging.handlers.SocketHandler('localhost',
							logging.handlers.DEFAULT_TCP_LOGGING_PORT)

		logger.addHandler(sock_handler)
		return logger

