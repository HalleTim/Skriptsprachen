import pyaudio
import numpy as np
from scipy import signal

# Audio-Parameter
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Erstellen von Pyaudio-Stream
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                frames_per_buffer=CHUNK)

# Hann-Fensterfunktion
window = signal.hann(CHUNK)

while True:
    # Lesen von Audio-Samples vom Stream
    data = stream.read(CHUNK)
    # Konvertieren von binären Daten in ein numpy-Array
    data = np.frombuffer(data, dtype=np.float32)
    # Anwenden der Hann-Fensterfunktion auf das Signal
    data = data * window
    # Anwenden der diskreten Fourier-Transformation (DFT)
    fft = np.fft.fft(data)
    # Berechnen der Leistung des Signals für jedes Frequenzband
    power = np.abs(fft)**2
    # Berechnen des dB-Werts für jedes Frequenzband
    db = 10 * np.log10(power)
    # Ausgabe des durchschnittlichen dB-Werts für das gesamte Spektrum
    print("dB-Wert:", np.max(db)+100)