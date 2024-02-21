#chimes after wake word recognized

import sounddevice as sd 
from scipy.io.wavfile import write

fs = 44100                                                          #sample rate
seconds = 3                                                         #seconds of data read
filename = "sample.wav"

for i in range (10):
    print("New")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write("Affirmation/hajur_" + str(i+1) + ".wav", fs, myrecording)