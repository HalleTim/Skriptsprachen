import pyaudio
import numpy as np
import config

#Klasse zur Aufnahme der Audiodaten
class Recorder:

    global stream
    global errorCounter

    def __init__(self) -> None:
        p = pyaudio.PyAudio()
        self.stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=config.frames_per_buffer)
        self.errorCounter=0

#Aufnahme eines Audio frames
    def recordAudio(self):
        try:
            y = np.fromstring(self.stream.read(config.frames_per_buffer, exception_on_overflow=False), dtype=np.int16)
            y = y.astype(np.float32)
            
        except:
            print("Undefined Error ocurred!")
            self.recordAudio(self)
            self.errorCounter+=1
            
            if self.errorCounter>300:
                print("Max errors ocurred while recording")
                exit()
        return y
    
    def stop(self):
        self.stream.close()