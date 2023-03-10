import config
import neopixel
import numpy as np
import time

class ledStrip:
    global pin
    global ledCount
    global brightness
    global strip
    global ledTVState
    global leds

    def __init__(self) -> None:
        self.pin=config.rpiPin
        self.ledCount=config.ledCount
        self.brightness=config.brightness
        self.strip=neopixel.NeoPixel(self.pin,self.ledCount,brightness=self.brightness)
        self.leds=np.tile(0,(3,self.ledCount))
        self.ledTVState=False
    
    #Berechnete Farben auf 3 LEDs des Streifens darstellen
    def movingColor(self, rgb):
        self.leds=np.roll(self.leds,3,axis=1)
        r=self.leds[0]
        g=self.leds[1]
        b=self.leds[2]

        np.put_along_axis(r,np.array([0,1,2]),rgb[0], axis=0)
        np.put_along_axis(g,np.array([0,1,2]),rgb[1], axis=0)
        np.put_along_axis(b,np.array([0,1,2]),rgb[2], axis=0)

        self.leds=np.stack((r,g,b))
        
        #neue LED-Farben anzeigen
        for i in range(self.ledCount):
            self.strip[i]=(self.leds[0][i],self.leds[1][i],self.leds[2][i])
        self.strip.show()

    #LED-Streifen in einer Farbe leuchten lassen und TV Modus setzen
    def fillColor(self,rgb):
        self.strip.fill(rgb)
        self.ledTVState=True

    def Impulse(self,db):
        #Farbe für Impuls
        color=(0,0,200)

        #Maxiumum festlegen
        if(db>100):
            db=100
        
        #Prozentualen Anteil berechnen
        percent = (db-30)/100

        #Anzahl der zu leuchtenden LEDs
        SumLedsToShine=np.array(int(self.ledCount*percent))

        #Linke und rechte Hälfte auf RGB Liste abbilden
        leftLedsToShine=np.arange(self.ledCount//2-SumLedsToShine//2 ,self.ledCount//2)
        rightLedsToShine=np.arange(self.ledCount//2,self.ledCount//2+SumLedsToShine//2)

        r=self.leds[0]
        g=self.leds[1]
        b=self.leds[2]

        #linke Hälfte schreiben
        np.put_along_axis(r,leftLedsToShine,color[0], axis=0)
        np.put_along_axis(g,leftLedsToShine,color[1], axis=0)
        np.put_along_axis(b,leftLedsToShine,color[2], axis=0)

        #rechte Hälfte schreiben
        np.put_along_axis(r,rightLedsToShine,color[0], axis=0)
        np.put_along_axis(g,rightLedsToShine,color[1], axis=0)
        np.put_along_axis(b,rightLedsToShine,color[2], axis=0)
        
        self.leds=np.stack((r,g,b))

        #RGB-Farbwerte in Liste schreiben
        zeitanfang= time.time()
        for i in range(self.ledCount):
            self.strip[i]=(self.leds[0][i],self.leds[1][i],self.leds[2][i])
        
        zeitende=time.time()
        print("Zeit zum schreiben der RGB Werte in Liste:" + str(zeitende-zeitanfang))

        #LED-Streifen aktualisieren
        zeitanfang= time.time()
        self.strip.show()
        zeitende=time.time()
        print("Zeit zum aktualisieren des LED-Streifens:" + str(zeitende-zeitanfang))

        b=np.clip(b,0,0)
        self.leds=np.stack((r,g,b))
        self.strip.fill((0,0,0))

        

