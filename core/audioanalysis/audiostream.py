import pyaudio # from http://people.csail.mit.edu/hubert/pyaudio/
import numpy as np
import wave
import struct
import math
import os
import platform
import time

class Audio():

    def __init__(self, source=None, output=False):
        '''
        source is a dictionary e.g. 
            {'input':'mic','device':0,'datasize':2048} or 
            {'input':'wav','path':'resources/DaftPunk.wav','datasize':2048} 
        
        Notes on pyaudio & sampling:
            Notes on parameters - http://support.ircam.fr/docs/AudioSculpt/3.0/co/Window%20Size.html
            - "RATE" is the "sampling rate", i.e. the number of frames per second
                ... Nyquist theorem dictates that freqMax is half sample rate.
            - "CHUNK" is the (arbitrarily chosen) number of frames the (potentially very long) signals are split into in this example
            - Lowest detectable frequency:
                
                The duration of the window must be five time longer than the period of the signal, that is :
                T(Window) = 5* T(Signal).

                For instance, the window size for a 440 Hz signal should be  :
                    5*(1/440)  : 0.025 seconds

                F0 = 5*(44100/1024) = 215 Hz.
        '''

        p = pyaudio.PyAudio()

        ''' process input source '''
        print "Setting up input audio"
        if isinstance(source, dict):
            if 'input' in source:

                ''' WAVE '''
                if source['input'] == 'wav':
                    if 'path' in source:
                        self.stream = wave.open(source['path'], 'rb')
                        self.frate = self.stream.getframerate()
                        print self.stream.getparams()
                    else:
                        raise Exception('Audio error: no wav path provided')
               
                    ''' MIC '''
                elif source['input'] == 'mic':
                    # chunk = 1024
                    print 'datasize', source['datasize'], type(source['datasize'])
                    self.stream = p.open(
                                    rate=source['rate'], 
                                    channels=1, 
                                    input=True, 
                                    output=True, 
                                    format=pyaudio.paInt16, 
                                    frames_per_buffer=source['datasize'])
                    output = False
                
                else:
                    raise Exception('Audio error: source dictionary provide with an unknown input key')
                if 'datasize' in source:
                    self.datasize = source['datasize']
            else:
                raise Exception('Audio error: source dictionary provide without an input key')
            

        ''' process output stream '''
        if output:
            print "Setting up output audio"
            print self.stream.getsampwidth(), self.stream.getnchannels(), self.stream.getframerate()
            self.streamop = p.open(format=p.get_format_from_width(self.stream.getsampwidth()),
                                   channels=self.stream.getnchannels(),
                                   rate=self.frate,
                                   output=True)

        self.output = output
        self.source = source
        

    def close_stream(self):
        self.stream.close()

    def sample_and_send(self):
        data = self.get_audio()
        if self.output:
            self.send_audio(data)
        return data


    def get_audio(self):
        if self.source['input'] == 'mic':
            data = self.stream.read(self.datasize, exception_on_overflow = False)
        elif self.source['input'] == 'wav':
            data = self.stream.readframes(self.datasize)

        return data


    def send_audio(self, data):
        self.streamop.write(data)

    '''
    Scans for audio input devices 
    '''
    def list_devices(self):
        # List all audio input devices
        p = pyaudio.PyAudio()
        i = 0
        n = p.get_device_count()
        while i < n:
            dev = p.get_device_info_by_index(i)
            if dev['maxInputChannels'] > 0:
                print str(i)+'. '+dev['name']
            i += 1


if __name__ == '__main__':

    audio = Audio(source={'input':'wav','path':'resources/DaftPunk.wav','datasize':2048},
                  output=True)

    while True:
        audio.sample_and_send()

    exit()