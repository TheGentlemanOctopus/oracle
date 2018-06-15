from multiprocessing import Process, Queue, Lock
from Queue import Empty

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

    def start(self):
        """
            Starts itself in a new process
            Returns: the new process
        """
        p = Process(target=self.main)
        p.start()
        return p

    def get_in_queue(self):
        """
            No wait by default
            Saves having to do an empty check and safer
        """
        return get_nowait(self.in_queue)

    def get_out_queue(self):
        """
            Saves having to do an empty check and safer
        """
        return get_nowait(self.out_queue)


def get_nowait(queue):
    """
        A helper to get something from a queue
        I think this is nicer than catching an exception from get_nowait()
        TODO: should this be in utils or something?
    """

    try:
        return queue.get_nowait()

    except Empty as e:
        return None