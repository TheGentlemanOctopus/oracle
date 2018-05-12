import time

class Device(object):
    """Generic Device"""
    def __init__(self):
        pass

    def main(self):
        while True:
            print(time.time())
            time.sleep(1.0/30)
            

if __name__ == '__main__':
    device = Device()
    device.main()
        