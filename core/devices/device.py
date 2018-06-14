from multiprocessing import Queue, Lock

class Device(object):
    def __init__(self):
        # Output queue
        self.out_queue = Queue()

        # Input Queue
        self.in_queue = Queue()

        # Mutex for the queues
        self.queue_mutex = Lock()

    def main(self):
        """
            This should be called to start the process
        """
        raise NotImplementedException("Need to define main for %s"%self.__class__.__name__)


def get_nowait(queue):
    """
        A helper to get something from a queue
        I think this is nicer than catching an exception from get_nowait()
        TODO: should this be in utils or something?
    """

    try:
        return queue.get_nowait()

    except Exception:
        return None