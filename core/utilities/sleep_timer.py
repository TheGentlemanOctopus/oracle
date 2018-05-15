"""
    A timer that sleeps for the remainder of its time
    Useful for efficiently keeping to a framerate
"""

import time

class SleepTimer:
    def __init__(self, t):
        """
            t is how long the timer should be for
        """
        self.t = t
        self.start_time = 0

    def start(self):
        """
            start the timer
        """
        self.start_time = time.time()

    def sleep(self):
        """
            sleeps for the remainder of the timer
        """
        elapsed = time.time() - self.start_time
        sleep_time = self.t - elapsed
        if sleep_time < 0: 
            sleep_time = 0

        time.sleep(sleep_time)