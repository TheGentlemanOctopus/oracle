from multiprocessing import Process, Queue
import device
import time
import opc

from lonely import Lonely
from cube_strip import CubeStrip

class SceneManager(object):
    """docstring for SceneManager"""
    def __init__(self,  opc_host="127.0.0.1", opc_port=7890):
        opc_ip = opc_host + ":" + str(opc_port)
        self.client = opc.Client(opc_ip)

        # If the client is not connected the put_pixels operation is slow as it tries to reconnect
        if not self.client.can_connect():
            raise Exception("Could not connect to opc at " + opc_ip)

    def start(self):
        start = [0,0,0]
        direction = [1,0,0]
        spacing = 0.2
        num_pixels = 10
        d = CubeStrip(start, direction, spacing, num_pixels)

        p = Process(target=d.main)
        p.start()
        while True:
            self.client.put_pixels(d.out_queue.get(), channel=0)


if __name__ == '__main__':
    scene = SceneManager()
    scene.start()