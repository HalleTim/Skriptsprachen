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
        self.LEDs=neopixel.NeoPixel(self.pin,self.ledCount,brightness=self.brightness)
    
    def movingColor(self, rgb):
        for i in range(self.ledCount-1,-1,-3):
            if i > 5: 
                self.LEDs[i]=self.LEDs[i-3]
                self.LEDs[i-1]=self.LEDs[i-4]
                self.LEDs[i-2]=self.LEDs[i-5]
            else:
                self.LEDs[i]=rgb
                self.LEDs[i-1]=rgb
                self.LEDs[i-2]=rgb

        self.LEDs.write()
