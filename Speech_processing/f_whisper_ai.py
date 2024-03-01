from sounddevice import play, wait, rec
from soundfile import read
from scipy.io.wavfile import write
#import subprocess 
from sys import exit
from whisper import load_model 
import time


data, fs = read('D:/Voice/Project/Nepali_Home_Automation_System/Wake_word/Affirmation/affirm.mp3')
play(data, fs)
wait()

print("Recording starts in 3...")
time.sleep(0.5)
print("Recording starts in 2...")
time.sleep(0.5)
print("Recording starts in 1...")
time.sleep(0.5)

fs = 44100                                                          #sample rate
seconds = 3                                                         #seconds of data read
filename = "sample.wav"

myrecording = rec(int(seconds * fs), samplerate=fs, channels=2)
wait()
write(filename, fs, myrecording)

model = load_model("small")
result = model.transcribe(audio="sample.wav", task = 'translate', language = "nepali")
print(result['text'])

