import board

RATE=44100
chunk=2048
frames_per_buffer = int(44100 / 60)
effect="AudioDB2Amplitude"
rpiPin=board.D18
ledCount=90
brightness=1
tvColor=(0,240,0)