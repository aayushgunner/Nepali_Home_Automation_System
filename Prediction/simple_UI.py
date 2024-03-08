import tkinter as tk
from sounddevice import rec, wait, play
from scipy.io.wavfile import write
from librosa import load, feature
from numpy import mean, expand_dims
from keras.models import load_model
from subprocess import call
from os import remove
from soundfile import read
from openai import OpenAI
import threading


door_close = door_open = batti_on = batti_off = "None"
client = OpenAI(api_key= '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')
fs = 44100                                                          #sample rate
seconds = 3                                                         #seconds of data read
filename = "prediction.wav"

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Wake Word Detection")

        self.label = tk.Label(self, text="Click the button to start detecting the wake word.")
        self.label.pack(padx=20, pady=20)
        
        self.button_first = tk.Button(self, text="Start Detection", command=self.start_detection)
        self.button_first.pack(padx=5, pady=5)

        self.button_second = tk.Button(self, text="Direct Command", command=self.end_detection)
        self.button_second.pack(padx=5, pady=5)
        
        self.button_third = tk.Button(self, text="Turn on lights", command=self.change_state)
        self.button_third.pack(padx=5, pady=5)

        self.label.config(text="Click the button to start detecting the wake word.")

        

        self.geometry("300x300")
        self.after(1, self.update())

    def start_detection(self):
        data, fs = read('../Wake_word/Affirmation/affirm.mp3')
        play(data, fs)
        wait()
        self.label.config(text="Listening...")

        # Call your function to detect the wake word
        wake_word()
        self.label.config(text="Wake word detected. Listening for command...")
        threading.Thread(target=asm).start()
        return
        

    def end_detection(self):        
        threading.Thread(target=asm).start()
        self.label.config(text = "Listening for command...")
        return
    
    def change_state(self):
        self.label.config(text = "Lights on")
        self.button_third.setvar("Turn off")
        return
        
    
    def update(self):
        return 

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
            return
            #break;

        else:
            #print(f"Wake Word NOT Detected")
            #print("Confidence:", prediction[:, 0])
            remove("prediction.wav")


def asm(): 
    global door_close, door_open, batti_on, batti_off 
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
    lower = transcription.text
    transcription = lower.lower()
   
    
    substrings_lights = ["batti", "vati", "bati", "batii", "bhatti", "bhati"]
    lights_on = ["bala", "vala", "valor", "wala", "on", "baala", "bhala"]
    lights_off = ["nibhau", "nibau", "banda", "wanda", "off", "vanda", "bhanda", "nibha"]

    substrings_doors = ["dhoka", "doka", "dhukha", "dhuka", "duka", "coca", "dukkha", "dhooka", "duca"]
    door_open = ["khola", "kola", "koala", "cola", "open", "kholo", "khula", "khunna"]
    door_close = ["lagau", "laga", "laaga", "lagaa", "close", "laghau"]


    if ("night" in transcription):
        print("\nGood Night")
        door_close = True
        batti_off = True

    if any(substring in transcription for substring in substrings_lights):
        if any(further in transcription for further in lights_on):
            batti_on = True
            batti_off = False
        elif any(further in transcription for further in lights_off):
            batti_off = True
            batti_on = False
        

    if(any(substring in transcription for substring in substrings_doors)):
        if any(newer in transcription for newer in door_open):
            door_open = True
            door_close = False
        elif any(newer in transcription for newer in door_close):
            door_close = True
            door_open = False
            
    if (batti_off):
        print("Lights Off")
    elif (batti_on):
        print("Lights On")

    if (door_close):
        print("Door Closed")
    elif (door_open):
        print("Door Opened")    
    

    return

if __name__ == "__main__":
    app = GUI()
    app.mainloop()
