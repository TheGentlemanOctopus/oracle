from math import floor, log10

def round_to_exponent(x):
    return 10**int(floor(log10(abs(x)))) if x != 0 else 0

def logging_handler_setup(process_name):
	return

