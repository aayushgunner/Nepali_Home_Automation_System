from sounddevice import rec, wait, play
from scipy.io.wavfile import write
from librosa import load, feature
from numpy import mean, expand_dims
from keras.models import load_model
from subprocess import call
from sys import exit
from os import remove
from soundfile import read
from openai import OpenAI

client = OpenAI(api_key= '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')
fs = 44100                                                          #sample rate
seconds = 3                                                         #seconds of data read
filename = "prediction.wav"

def wake_word():
    class_names = ["Wake Word NOT Detected", "Wake Word Detected"]      #two classes to identify

    model = load_model("../Wake_word/saved_model/WWD.h5")                            #load model

    print("Wake word listener ")
    while True:
        print("Scanning...")                                              #prompts listener
        myrecording = rec(int(seconds * fs), samplerate=fs, channels=2)
        wait()
        write(filename, fs, myrecording)

        audio, sample_rate = load(filename)                     #numpy array from audio sample
        mfcc = feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40) #mfcc value of input
        mfcc_processed = mean(mfcc.T, axis=0)                        #processed mfcc

        prediction = model.predict(expand_dims(mfcc_processed, axis=0))
        if (prediction[:, 1] > 0.98 or prediction[:, 0] < 0.03) :
            print(f"Wake Word Detected")
            print("Confidence:", prediction[:, 1])        
            remove("prediction.wav")
            #data, fs = read('../Wake_word/Affirmation/affirm.mp3')
            #play(data, fs)
            #wait()
            #call(['python', 'e2_translator.py'])
            asm()
            break;

        else:
            #print(f"Wake Word NOT Detected")
            #print("Confidence:", prediction[:, 0])
            remove("prediction.wav")


def asm(): 

    fs = 44100                                                          #sample rate
    seconds = 3                                                         #seconds of data read
    filename = "command.wav"
    class_names = ["Wake Word NOT Detected", "Wake Word Detected"]

    data, fs = read('../Wake_word/Affirmation/affirm_2.mp3')
    play(data, fs)
    wait()                                              #prompts listener
    print("\n \nProvide Command")
    myrecording = rec(int(seconds * fs), samplerate=fs, channels=2)
    wait()
    write(filename, fs, myrecording)


    audio_file= open("command.wav", "rb")
    transcription = client.audio.translations.create(
      model="whisper-1", 
      file=audio_file
    )
    print(transcription.text)


if __name__ == "__main__":
    wake_word()