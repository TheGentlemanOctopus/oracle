import matplotlib.pyplot as plt
import sys
import numpy as np
import csv
import argparse

from pylab import meshgrid

"""
    Plot a CSV generated by an FftDevice
"""

def plot_csv(filepath):
    # Parse CSV
    raw_data = []
    with open(filepath, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csv_reader:
            data = [float(x) for x in row]
            if data:
                raw_data.append(data)

    raw_data = np.array(raw_data).astype(float)

    # Split up columns
    t = raw_data[:, 0]
    bands = raw_data[:, 1:]

    # Waterfall plot
    X, Y = meshgrid(t, np.arange(len(bands.T)+1)+0.5)

    plt.pcolor(X, Y, bands.T)

    plt.xlabel('Time (s)')
    plt.ylabel('Band #')

    cbar = plt.colorbar()
    cbar.set_label('Intensity')

    plt.legend()
    plt.title(filepath)
    plt.show()

def main(args):
    parser = argparse.ArgumentParser("Plot a CSV of fft data")
    parser.add_argument("filepath", help="filepath to csv")

    parser_args = parser.parse_args(args)
    plot_csv(parser_args.filepath)


if __name__=='__main__':
    main(sys.argv[1:])