import config
import neopixel

class ledStrip:
    global pin
    global ledCount
    global brightness
    global LEDs
    global ledTVState

    def __init__(self) -> None:
        self.pin=config.rpiPin
        self.ledCount=config.ledCount
        self.brightness=config.brightness
        self.LEDs=neopixel.NeoPixel(self.pin,self.ledCount,brightness=self.brightness)
        self.ledTVState=False
    
    #Berechnete Farben auf 3 LEDs des Streifens darstellen
    def movingColor(self, rgb):
        for i in range(self.ledCount-1,-1,-3):
            #bisherige Farben um 3 LEDs verschieben
            if i > 5: 
                self.LEDs[i]=self.LEDs[i-3]
                self.LEDs[i-1]=self.LEDs[i-4]
                self.LEDs[i-2]=self.LEDs[i-5]
            #neue Farbe auf 3 LEDs darstellen
            else:
                self.LEDs[i]=rgb
                self.LEDs[i-1]=rgb
                self.LEDs[i-2]=rgb

        #neue LED-Farben anzeigen
        self.LEDs.write()

    #LED-Streifen in einer Farbe leuchten lassen
    def fillColor(self,rgb):
        self.LEDs.fill(rgb)
        self.ledTVState=True