from multiprocessing import Process, Queue
import time
import opc
import sys

from core.devices import construct_devices

class SceneManager(object):
    """docstring for SceneManager"""
    def __init__(self,  opc_host="127.0.0.1", opc_port=7890):
        opc_ip = opc_host + ":" + str(opc_port)
        self.client = opc.Client(opc_ip)

        # If the client is not connected the put_pixels operation is slow as it tries to reconnect
        if not self.client.can_connect():
            raise Exception("Could not connect to opc at " + opc_ip)

    def start(self, devices):
        # TODO: Support multiple devices
        d = devices[0]

        p = Process(target=d.main)
        p.start()
        while True:
            self.client.put_pixels(d.out_queue.get(), channel=0)

if __name__ == '__main__':
    devices = construct_devices(sys.argv[1])

    scene = SceneManager()
    scene.start(devices)