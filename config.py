import board

RATE=44100
chunk=2048
frames_per_buffer = int(44100 / 60)
effect="freqToRGB"
rpiPin=board.D18
ledCount=150
brightness=1
tvColor=(0,240,0)