###################################################################
#Datei Wave2RGB wurde aus dem Repository Psynesthesia übernommen. # 
#Link: https://github.com/off-by-some/Psynesthesia                #
###################################################################

def Adjust_and_Scale(Color, Factor, Highest=100):
        """Gamma adjustment.
        Arguments:
        * Color:  Value of R, G, or B, on a scale from 0 to 1, inclusive,
          with 0 being lowest intensity and 1 being highest.  Floating
          point value.
        * Factor:  Factor obtained to have intensity fall off at limits 
          of human vision.  Floating point value.
        * Highest:  Maximum intensity of output, scaled value.  The 
          lowest intensity is 0.  Scalar integer.
        Returns an adjusted and scaled value of R, G, or B, on a scale 
        from 0 to Highest, inclusive, as an integer, with 0 as the lowest 
        and Highest as highest intensity.
        Since this is a helper function I keep its existence hidden.
        See http://www.efg2.com/Lab/ScienceAndEngineering/Spectra.htm and
        http://www.physics.sfasu.edu/astro/color/spectra.html for details.
        """
        Gamma = 0.80

        if Color == 0.0:
            result = 0
        else:
            result = int( round(pow(Color * Factor, Gamma) * round(Highest)) )
            if result < 0:        result = 0
            if result > Highest:  result = Highest

        return result


def wavelen2rgb(Wavelength, MaxIntensity=100):
    if (Wavelength >= 380.0) and (Wavelength < 440.0):
        Red   = -(Wavelength - 440.) / (440. - 380.)
        Green = 0.0
        Blue  = 1.0

    elif (Wavelength >= 440.0) and (Wavelength < 490.0):
        Red   = 0.0
        Green = (Wavelength - 440.) / (490. - 440.)
        Blue  = 1.0

    elif (Wavelength >= 490.0) and (Wavelength < 510.0):
        Red   = 0.0
        Green = 1.0
        Blue  = -(Wavelength - 510.) / (510. - 490.)

    elif (Wavelength >= 510.0) and (Wavelength < 580.0):
        Red   = (Wavelength - 510.) / (580. - 510.)
        Green = 1.0
        Blue  = 0.0

    elif (Wavelength >= 580.0) and (Wavelength < 645.0):
        Red   = 1.0
        Green = -(Wavelength - 645.) / (645. - 580.)
        Blue  = 0.0

    elif (Wavelength >= 645.0) and (Wavelength <= 780.0):
        Red   = 1.0
        Green = 0.0
        Blue  = 0.0

    else:
        Red   = 0.0
        Green = 0.0
        Blue  = 0.0


    #- Let the intensity fall off near the vision limits:

    if (Wavelength >= 380.0) and (Wavelength < 420.0):
        Factor = 0.3 + 0.7*(Wavelength - 380.) / (420. - 380.)
    elif (Wavelength >= 420.0) and (Wavelength < 701.0):
        Factor = 1.0
    elif (Wavelength >= 701.0) and (Wavelength <= 780.0):
        Factor = 0.3 + 0.7*(780. - Wavelength) / (780. - 700.)
    else:
        Factor = 0.0


    #- Adjust and scale RGB values to 0 to MaxIntensity integer range:

    R = Adjust_and_Scale(Red,   Factor, MaxIntensity)
    G = Adjust_and_Scale(Green, Factor, MaxIntensity)
    B = Adjust_and_Scale(Blue,  Factor, MaxIntensity)


    #- Return 3-element list value:

    return [R, G, B]