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

    #LED-Streifen in einer Farbe leuchten lassen
    def fillColor(self,rgb):
        self.LEDs.fill(rgb)
        self.ledTVState=True

    def Impulse(self,db):
        color=(0,0,200)

        if(db>130):
            db=130
        
        percent = db/130

        SumLedsToShine=np.array(int(self.ledCount*percent))

        leftLedsToShine=np.arange(self.ledCount//2-SumLedsToShine//2,SumLedsToShine//2)
        self.leds=np.put(self.leds,leftLedsToShine,[color]*len(leftLedsToShine))
        
        print(self.leds)
        rightLedsToShine=np.arange(self.ledCount//2+SumLedsToShine//2,SumLedsToShine)
        self.leds=np.put(self.leds,rightLedsToShine,[color]*len(rightLedsToShine))

        self.strip.show()

        self.strip.fill((0,0,0))

        

