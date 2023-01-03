import numpy as np
import config
import microInput
from math import *
from wave2RGB import *

global thefreq

def freqToRGB(input):
    #Frequenz mit größten Anteil finden
    which = input[1:].argmax() + 1
    #umwandeln des Index in Frequenz
    thefreq = which*config.RATE/config.chunk
    print(which)

    #anpassen der festgestellten Wertes für schönere Farben :=)
    while thefreq < 350 and thefreq > 15:
            thefreq = thefreq*2
            print ("the new freq is "+str(thefreq) )
    while thefreq > 700:
        thefreq = thefreq/2
        print ("the new freq is"+str(thefreq))
    
    #Berechnung zur Umwandlung der Frequenz in sichtbare Farbe
    c = 3*10**8
    THz = thefreq*2**40
    pre = float(c)/float(THz)
    nm = int(pre*10**(-floor(log10(pre)))*100)	
    rgb = wavelen2rgb(nm, MaxIntensity=255)

    return rgb


def __main___():
    recorder=microInput.Recorder()

    while(True):
        input=recorder.recordAudio()

        input=abs(np.fft.rfft(input))**2

        #Aufruf des in der config gespeicherten Effekts
        locals()[config.effect](input)

    