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
        self.strip=neopixel.Adafruit_NeoPixel(self.pin,self.ledCount,brightness=self.brightness)
        self.leds=np.tile(0,(3,self.ledCount))
        self.ledTVState=False
    
    #Berechnete Farben auf 3 LEDs des Streifens darstellen
    def movingColor(self, rgb):
        self.leds=np.roll(self.leds,3,axis=1)
        #neue LED-Farben anzeigen
        self.strip.write()

    #LED-Streifen in einer Farbe leuchten lassen
    def fillColor(self,rgb):
        self.LEDs.fill(rgb)
        self.ledTVState=True