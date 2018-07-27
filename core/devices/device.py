from multiprocessing import Process, Queue, Lock
from Queue import Empty
from core.utilities import logging_handler_setup

class Device(object):
    layout_type = "Layout"

    def __init__(self):
        # Output queue
        self.out_queue = Queue()

        # Input Queue
        self.in_queue = Queue()

        # Mutex for the queues
        self.queue_mutex = Lock()

        # Default to the class name, overwrite this for a unique human-readable reference
        self.name = self.__class__.__name__

    def main(self):
        """
            This should be called to start the process
        """
        raise NotImplementedException("Need to define main for %s"%self.__class__.__name__)

    def run_main(self, *args):
        # TODO: Make this accept a device name
        self.logger = logging_handler_setup(self.name)
        self.logger.info("Starting Process")
        self.main(*args)

    def start(self, *args):
        """
            Starts itself in a new process, all *args are passed to device main
            Returns the new process
        """
        p = Process(target=self.run_main, args=args)
        p.daemon = True
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
        Queue.get_nowait() throws an exception if nothing is in the queue
        And python docs say you shouldn't assume Queue.empty() is reliable
        I think this is nicer than catching an exception
        TODO: should this be in utils or something?
    """

    try:
        return queue.get_nowait()

    except Empty as e:
        return None
