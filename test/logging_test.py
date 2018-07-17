import logging
from queue_logging import QueueHandler, QueueListener
from multiprocessing import Process, Lock, Queue
import time

class TestLog(object):

	def __init__(self):
		self.log_queue = Queue()
		self.queue_handler = QueueHandler(self.log_queue)

	def main(self, p_name):
		self.logger = logging.getLogger(p_name)
		self.logger.setLevel(logging.DEBUG)

		self.logger.addHandler(self.queue_handler)
		print(p_name)

		self.log_count = 0
		while(True):
			self.logger.debug('log count = ' + str(self.log_count))
			self.log_count += 1
			time.sleep(5)



if __name__ == '__main__':

	main_logger = logging.getLogger('main')
	main_logger.setLevel(logging.DEBUG)

	fh = logging.FileHandler('test.log')
	fh.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)


	main_logger.addHandler(fh)
	main_logger.debug('Starting')

	logger1 = TestLog()
	logger2 = TestLog()

	logger1_listener = QueueListener(logger1.log_queue, [fh], True)
	logger2_listener = QueueListener(logger2.log_queue, [fh], True)

	p1 = Process(target=logger1.main, args=(['Process 1']))
	p1.daemon = True
	p1.start()
	p2 = Process(target=logger2.main, args=(['Process 2']))
	p2.daemon = True
	p2.start()

	while(True):

		logger1_listener.start()
		logger2_listener.start()
		time.sleep(1)
