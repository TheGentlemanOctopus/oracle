import argparse
import sys

import core.opc as opc

def configure(host, port, channel, brightness):

    # Connect to opc client
    opc_ip = host + ":" + str(port)
    client = opc.Client(opc_ip)

    if not client.can_connect():
        raise Exception("Could not connect to opc at " + opc_ip)

    num_pixels = 0
    num_pixels_on = 0

    while True:
        num_pixels_off = num_pixels - num_pixels_on
        pixels = [[brightness, brightness, brightness]]*num_pixels_on + [[0,0,0]]*num_pixels_off

        print "Updating"
        print "num_pixels", num_pixels
        print "num_pixels_on", num_pixels_on
        print "channel", channel
        client.put_pixels(pixels)

        print "="*20


        print "commands: "
        print "\tw: Increase Pixel Count"
        print "\ts: Decrease Pixel Count"
        print "\te: Increase Num Pixels On"
        print "\td: Decrease Num Pixel On"
        print "\tr: Channel Up"
        print "\tf: Channel Down"
        print "\t#: Type a number to set total pixel count and number of pixels on"
        print "\tq: exit"
        k = raw_input('Enter command:')

        if k=="w":
            num_pixels += 1
        
        elif k=="s":
            num_pixels -= 1

        elif k=="e":
            num_pixels_on = (num_pixels_on+1)%(num_pixels+1)

        elif k=="d":
            num_pixels_on = (num_pixels_on-1)%(num_pixels+1)

        elif k=="r":
            channel += 1

        elif k=="f":
            channel -= 1

        elif k=="q":
            return

        else:
            try:
                num = int(k)
                num_pixels = num
                num_pixels_on = num

            except:
                print "Unknown command"


def main(args):
    parser = argparse.ArgumentParser("Configure Me")
    parser.add_argument("--host", default="127.0.0.1", help="opc host")
    parser.add_argument("--port", type=int, default=7890, help="opc port")
    parser.add_argument("--channel", type=int, default=0, help="channel")
    parser.add_argument("--brightness", type=int, default=200, help="brightness")

    parser_args = parser.parse_args(args)

    configure(**vars(parser_args))


if __name__ == "__main__":
    sys.argv[1:]