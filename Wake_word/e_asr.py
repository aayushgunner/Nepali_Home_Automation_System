import sounddevice as sd
from soundfile import read
from scipy.io.wavfile import write
#import subprocess 
from sys import exit
import whisper 
import time


data, fs = read('Affirmation/affirm.mp3')
sd.play(data, fs)
sd.wait()

print("Recording starts in 3...")
time.sleep(0.5)
print("Recording starts in 2...")
time.sleep(0.5)
print("Recording starts in 1...")
time.sleep(0.5)

fs = 44100                                                          #sample rate
seconds = 5                                                         #seconds of data read
filename = "sample.wav"

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()
write(filename, fs, myrecording)

model = whisper.load_model("small")
result = model.transcribe(audio="sample.wav", task = 'translate', language = "nepali")
print(result['text'])

