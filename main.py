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
global ledStrip1


#################################################################
#Funktion freqToRGB aus dem Repository Psynesthesia übernommen. #
#Link: https://github.com/off-by-some/Psynesthesia              #
#################################################################
def freqToRGB(input):

    #Frequenz mit größten Anteil finden
    which = input[1:].argmax() + 1

    #umwandeln des Index in Frequenz
    thefreq = which*config.RATE/config.chunk

    #anpassen ermittelten Frequenz
    while thefreq < 350 and thefreq > 15:
        thefreq = thefreq*2
    while thefreq > 700:
        thefreq = thefreq/2
    
    #Berechnung zur Umwandlung der Frequenz in sichtbare Farbe
    c = 3*10**8
    THz = thefreq*2**40
    pre = float(c)/float(THz)
    nm = int(pre*10**(-floor(log10(pre)))*100)	
    rgb = wavelen2rgb(nm, MaxIntensity=255)

    #Abbilden der Farbe auf LED-Streifen
    globals()['ledStrip1'].movingColor(rgb)

def AudioDB2Amplitude(input):
   
    # Berechnen des Mitellwerts der dB-Werte für jedes Frequenzband
    db = np.mean(10 * np.log10(input))

    globals()['ledStrip1'].Impulse(db)



#Aufnahme des Audioss
def recordAudio():
    recorder=microInput.Recorder()


    while(True):
        #audio Aufnehmen
        Rinput=recorder.recordAudio()
        #fourier Transformation durchführen
        Rinput=abs(np.fft.rfft(Rinput))**2 
        globals()[config.effect](Rinput)

        #Handler zum Benden des Musik Threads
        if(not q.empty()):
            status=q.get()
            recorder.stop()
            print("Beende")
            q.task_done()
            break



#Abfrage der Sonos Anlage
def updateCurrentState(SonosAnlage):
    currentTrack=SonosAnlage.get_current_track_info()['title']
    state=SonosAnlage.get_current_transport_info()['current_transport_state']

    if(state=="PLAYING" and not currentTrack==""):
        return TVState.music
    elif (state=="PLAYING"):
        return TVState.TV
    else:
        return TVState.pause
    

#Musik Thread beenden
def endThread():
    q.put(True)
    q.join()
    globals()['recordThread']= threading.Thread(target=recordAudio)
    

def main():
    globals()['recordThread']= threading.Thread(target=recordAudio)
    globals()['ledStrip1']=led.ledStrip()
    SonosAnlage = by_name("Wohnzimmer")
    threadState=False
    
    #Schleife bis Programm beendet
    while(True):

        #Erstellung des Musik Threads und Abfrage der Sonos Anlage
        threadState=globals()['recordThread'].is_alive()
        playState=updateCurrentState(SonosAnlage)

        #Musikmodus starten
        if(playState==TVState.music and not threadState):
            globals()['ledStrip1'].ledTVState=False
            globals()['recordThread'].start()

        #TV Modus starten
        elif(playState==TVState.TV and globals()['ledStrip1'].ledTVState==False):
            #Musik Modus beenden
            if threadState:
                endThread()
            globals()['ledStrip1'].fillColor(config.tvColor)
            globals()['ledStrip1'].ledTVState=True
        
        #Musik Modus beenden und LED-Streifen ausschalten
        elif(threadState and playState==TVState.pause):
            globals()['ledStrip1'].fillColor((0,0,0))
            endThread() 

        #Main Thread pausieren     
        else:
            time.sleep(5)


main()
        

    
