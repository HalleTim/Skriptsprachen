import config
import neopixel
import numpy as np

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
        self.leds[0][0]=rgb[0]
        self.leds[1][0]=rgb[1]
        self.leds[2][0]=rgb[2]

        #neue LED-Farben anzeigen

        for i in range(self.ledCount):
            self.strip[i]=(self.leds[i][0],self.leds[i][1],self.leds[i][2])
        self.strip.write()

    #LED-Streifen in einer Farbe leuchten lassen
    def fillColor(self,rgb):
        self.LEDs.fill(rgb)
        self.ledTVState=True