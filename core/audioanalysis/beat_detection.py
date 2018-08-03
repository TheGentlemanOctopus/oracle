import numpy as np
import time

class BeatDetect():
    ''' Beat detection class.
    @param wait is minimum seconds between beats. anything inbetween is ignored.
    @param threshold is the minimum positive step change between samples
    @history is the length of the list containing past beats for comparison. This 
    is only currently used if you are the plot the beats along side the fft.

    All arguments set in setup json file as "beats_args":{}
    '''

    def __init__(self, wait=0.2, threshold=2, history=30):
        self.lastbeat = time.time()
        self.wait = wait
        self.threshold = threshold
        self.history_length = history
        self.history = np.array([])

    def detect(self, window):
        ''' detect compares current value against the mean value 
        of the history list. If greater than mean by a step of threshold
        then a beat is acknowledged. A beat cannot then be acknowledged 
        until a period 'wait' has passed '''

        self.decrement_history()

        ave = sum(window[:-1])/(len(window)-1)
        dif = time.time()-self.lastbeat

        if ((window[-1] - ave) > self.threshold) and (dif > self.wait):
            self.lastbeat = time.time()
            self.history = np.append(self.history, self.history_length-1)
            # self.history.append(self.history_length-1)
            return 1
        else:
            return 0

    def decrement_history(self):
        ''' decrement beat_history '''
        self.history-=1   
        self.history = np.array([ x for x in self.history if (x > 0)])
        


if __name__ == '__main__':
    
    import matplotlib.pyplot as plt
    from audiostream import Audio
    from fft import Fft

    history_length = 30
    bin_history = [[] for x in xrange(7)]    
    beat_detectors = [BeatDetect(wait=0.3, threshold=2, history=history_length) for x in xrange(7)]

    datasize = 2048
    frate = 44100

    mode = 'mic'

    if mode == 'wav':
        audio = Audio(source={'input':'wav','path':'resources/DaftPunk.wav','datasize':datasize},
                output=True)

    if mode == 'mic':
        audio = Audio(source={'input':'mic','datasize':datasize, 'rate':frate},
                output=False)

    fft = Fft(datasize=datasize,frate=frate)
    
    data = audio.sample_and_send()
    fft.configure_fft(data)
    fft.getDominantF()
    fft.splitLevels()     
    fft.normalize_bin_values()

    # bin_history.append(fft.stats['bin_values_normalized'][chan])

    # print len(bin_history)

    while (len(bin_history[0]) < history_length):
        data = audio.sample_and_send()
        fft.configure_fft(data)
        fft.getDominantF()
        fft.splitLevels()     
        fft.normalize_bin_values()
        for x in xrange(7):
            bin_history[x].append(fft.stats['bin_values_normalized'][x])

    xAxis = [x for x in xrange(history_length)]

    plt.xlim((0, history_length))
    plt.ylim((-0.1, 40.1))

    animated_plots = []

    labels = ['63 Hz', '160 Hz', '400 Hz', '1 KHz', '2.5 KHz', '6.25 KHz', '16 Khz']

    for x in xrange(7):
        animated_plots.append(plt.plot(xAxis,bin_history[x], '-', label=labels[x], marker='o', markersize=12, markevery=[])[0])

    plt.legend(loc='upper left')

    # beat_detect.lastbeat = time.time()

    while True:
        data = audio.sample_and_send()
        fft.run_fft(data)
        fft.getDominantF()
        fft.splitLevels()     
        # fft.set_freq_bins_max()
        fft.normalize_bin_values()

        for x in xrange(7):
            bin_history[x].pop(0)
            bin_history[x].append(fft.stats['bin_values_normalized'][x])
            beat_detectors[x].detect((bin_history[x][:]))

        
        for x in xrange(7):
            animated_plots[x].set_ydata(bin_history[x])

            animated_plots[x].set_markevery(beat_detectors[x].history)
                        
        plt.draw()
        plt.pause(0.00001)

    exit()

