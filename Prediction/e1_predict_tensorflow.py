from sounddevice import rec, wait, play
from scipy.io.wavfile import write
from librosa import load, feature
from numpy import mean, expand_dims
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
    myrecording = rec(int(seconds * fs), samplerate=fs, channels=2)
    wait()
    write(filename, fs, myrecording)

    audio, sample_rate = load(filename)                     #numpy array from audio sample
    mfcc = feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40) #mfcc value of input
    mfcc_processed = mean(mfcc.T, axis=0)                        #processed mfcc

    prediction = model.predict(expand_dims(mfcc_processed, axis=0))
    if (prediction[:, 1] > 0.98 or prediction[:, 0] < 0.03) :
        print(f"Wake Word Detected for ({i})")
        print("Confidence:", prediction[:, 1])
        i += 1        
        remove("prediction.wav")
        data, fs = read('../Wake_word/Affirmation/affirm.mp3')
        play(data, fs)
        wait()

    else:
        print(f"Wake Word NOT Detected")
        print("Confidence:", prediction[:, 0])
        remove("prediction.wav")



