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
        self.leds[0]=np.put(self.leds[0],[0,1,2],[rgb[0],rgb[0],rgb[0]])
        self.leds[1]=np.put(self.leds[1],[0,1,2],[rgb[1],rgb[1],rgb[1]])
        self.leds[2]=np.put(self.leds[2],[0,1,2],[rgb[2],rgb[2],rgb[2]])
        #neue LED-Farben anzeigen

        for i in range(self.ledCount):
            self.strip[i]=(self.leds[0][i],self.leds[1][i],self.leds[2][i])
        self.strip.write()

    #LED-Streifen in einer Farbe leuchten lassen
    def fillColor(self,rgb):
        self.LEDs.fill(rgb)
        self.ledTVState=True