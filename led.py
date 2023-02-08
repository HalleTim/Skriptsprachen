import config
import neopixel

class ledStrip:
    global pin
    global ledCount
    global brightness
    global LEDs

    def __init__(self) -> None:
        self.pin=config.rpiPin
        self.ledCount=config.ledCount
        self.brightness=config.brightness
        self.LEDs=neopixel.Neopixel(self.pin,self.ledCount,brightness=self.brightness)
    
    def movingColor(self, rgb):
        for i in range(self.ledCount,0,-1):
            if i > 3: 
                self.LEDs[i]=self.LEDs[i-3]
            else:
                self.LEDs[i]=rgb
        self.LEDs.write()
