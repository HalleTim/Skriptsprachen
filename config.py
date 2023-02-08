import board

RATE=44100
chunk=2048
frames_per_buffer = int(44100 / 60)
effect="freqToRGB"
rpiPin=board.D18
ledCount=10
brightness=1
