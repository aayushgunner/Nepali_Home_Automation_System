import sounddevice as sd
from scipy.io.wavfile import write
import librosa
import numpy as np
from keras.models import load_model
from subprocess import call
from sys import exit
from os import remove
from soundfile import read


fs = 44100                                                          #sample rate
seconds = 3                                                         #seconds of data read
filename = "prediction.wav"
class_names = ["Wake Word NOT Detected", "Wake Word Detected"]      #two classes to identify

model = load_model("D:/Voice/Project/Nepali_Home_Automation_System/Wake_word/saved_model/WWD.h5")                            #load model

print("Prediction Started: ")
i = 0
while True:
    print("Say Now: ")                                              #prompts listener
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(filename, fs, myrecording)

    audio, sample_rate = librosa.load(filename)                     #numpy array from audio sample
    mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40) #mfcc value of input
    mfcc_processed = np.mean(mfcc.T, axis=0)                        #processed mfcc

    prediction = model.predict(np.expand_dims(mfcc_processed, axis=0))
    if prediction[:, 1] > 0.99:
        print(f"Wake Word Detected for ({i})")
        print("Confidence:", prediction[:, 1])
        i += 1
        remove("prediction.wav")
        #call(['python', 'D:/Voice/Project/Nepali_Home_Automation_System/Speech_processing/f_whisper_ai.py'])
        #exit()
        data, fs = read('D:/Voice/Project/Nepali_Home_Automation_System/Wake_word/Affirmation/affirm.mp3')
        sd.play(data, fs)
        sd.wait()


    else:
        print(f"Wake Word NOT Detected")
        print("Confidence:", prediction[:, 0])
        remove("prediction.wav")



