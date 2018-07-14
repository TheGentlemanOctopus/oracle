import logging
from multiprocessing import Process
import time

class TestLog(object):

	def main(self, p_name, log_handler):
		self.logger = logging.getLogger(p_name)
		self.logger.setLevel(logging.DEBUG)
		self.logger.addHandler(log_handler)
		print(p_name)
		print(log_handler)

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
	p1 = Process(target=logger1.main, args=('Process 1', fh))
	p1.daemon = True
	p1.start()
	p2 = Process(target=logger2.main, args=('Process 2', fh))
	p2.daemon = True
	p2.start()
	while(True):
		time.sleep(1)
