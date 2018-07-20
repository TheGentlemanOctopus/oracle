import logging
from queue_logging import QueueHandler, QueueListener
from multiprocessing import Process, Lock, Queue
import time
from utilities.logging_server import LogRecordSocketReceiver

class TestLog(object):
	def __init__(self, process_name):
		self.logger = logging.getLogger(process_name)
		self.logger.setLevel(logging.DEBUG)

		self.sock_handler = logging.handlers.SocketHandler('localhost',
							logging.handlers.DEFAULT_TCP_LOGGING_PORT)

		self.logger.addHandler(self.sock_handler)


	def main(self):
		self.log_count = 0
		while(True):
			self.logger.debug('log count = ' + str(self.log_count))
			self.log_count += 1
			time.sleep(5)



if __name__ == '__main__':
	logger1 = TestLog("Process1")
	logger2 = TestLog("Process2")

	p1 = Process(target=logger1.main)
	p1.daemon = True
	p1.start()
	p2 = Process(target=logger2.main)
	p2.daemon = True
	p2.start()

	while(True):

		time.sleep(1)
