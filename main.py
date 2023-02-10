import numpy as np
import config
import microInput
from math import *
from wave2RGB import *
import threading
import time
import queue
from soco import SoCo
from soco.discovery import by_name
from TVStateEnum import TVState
import led

global thefreq
playState=TVState.music
q=queue.Queue()
global recordThread

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

#Aufnahme des Audios
def recordAudio():
    recorder=microInput.Recorder()
    ledStrip1=led.ledStrip()

    while(True):
        Rinput=recorder.recordAudio()
        Rinput=abs(np.fft.rfft(Rinput))**2
        color=globals()[config.effect](Rinput)
#        print(color)
        ledStrip1.movingColor(color)


        if(not q.empty()):
            status=q.get()
            recorder.stop()
            print("Beende")
            q.task_done()
            break




def updateCurrentState(SonosAnlage):
    currentTrack=SonosAnlage.get_current_track_info()['title']
    state=SonosAnlage.get_current_transport_info()['current_transport_state']

    if(state=="PLAYING" and not currentTrack==""):
        return TVState.music
    elif (state=="PLAYING"):
        return TVState.TV
    else:
        return TVState.pause
    

def endThread():
    q.put(True)
    q.join()
    globals()['recordThread']= threading.Thread(target=recordAudio)

def main():
    globals()['recordThread']= threading.Thread(target=recordAudio)
    SonosAnlage = by_name("Wohnzimmer")
    threadState=False
    
    while(True):
        threadState=globals()['recordThread'].is_alive()
        playState=updateCurrentState(SonosAnlage)

        if(playState==TVState.music and not threadState):
            globals()['recordThread'].start()
        elif(playState==TVState.TV):
            if threadState:
                endThread()
            ledStrip1=led.ledStrip()
            ledStrip1.fillColor(config.tvColor)
        elif(threadState and playState==TVState.pause):
            endThread()      
        else:
            time.sleep(5)


main()
        

    
