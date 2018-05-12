from multiprocessing import Process, Queue
from lonely import Lonely
import device
import time


class SceneManager(object):
    """docstring for SceneManager"""
    def __init__(self):
        pass

    def start(self):
        d = Lonely()
        p = Process(target=d.main)
        p.start()
        while True:
            print(d.out_queue.get())


if __name__ == '__main__':
    scene = SceneManager()
    scene.start()