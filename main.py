import numpy as np
import config
import microInput
from math import *
from wave2RGB import *
import threading
import time
import queue

global thefreq

def freqToRGB(input):
    #Frequenz mit größten Anteil finden
    which = input[1:].argmax() + 1
    #umwandeln des Index in Frequenz
    thefreq = which*config.RATE/config.chunk

    #anpassen der festgestellten Wertes für schönere Farben :=)
    while thefreq < 350 and thefreq > 15:
            thefreq = thefreq*2
            #print ("the new freq is "+str(thefreq) )
    while thefreq > 700:
        thefreq = thefreq/2
        #print ("the new freq is"+str(thefreq))
    
    #Berechnung zur Umwandlung der Frequenz in sichtbare Farbe
    c = 3*10**8
    THz = thefreq*2**40
    pre = float(c)/float(THz)
    nm = int(pre*10**(-floor(log10(pre)))*100)	
    rgb = wavelen2rgb(nm, MaxIntensity=255)

    return rgb

def recordAudio():
    recorder=microInput.Recorder()
    
    while(True):
        Rinput=recorder.recordAudio()
        Rinput=abs(np.fft.rfft(Rinput))**2
        globals()[config.effect](Rinput)

        if(not q.empty()):
            status=q.get()
            recorder.stop()
            print("Beende")
            q.task_done()
            break

def main():
    recordThread= threading.Thread(target=recordAudio)

    while(True):
        test="y"
        if(test=="y" and not recordThread.is_alive()):
            recordThread.start()
        elif(test=="n"):
            q.put(True)
        else:
            time.sleep(5)
            q.put(True)
            q.join()
            recordThread= threading.Thread(target=recordAudio)
        #Aufruf des in der config gespeicherten Effekts

q=queue.Queue()
main()
        

    