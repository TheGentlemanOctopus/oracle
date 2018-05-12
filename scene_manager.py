from multiprocessing import Process
import device
import time

class SceneManager(object):
    """docstring for SceneManager"""
    def __init__(self):
        pass

    def start(self):
        d = device.Device()
        p = Process(target=d.main)
        p.start()
        time.sleep(10)

if __name__ == '__main__':
    scene = SceneManager()
    scene.start()