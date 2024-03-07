import time
import threading
import tkinter as tk
from tkinter import ttk, font

# Ref: https://github.com/rdbende/Sun-Valley-ttk-theme
# Install: pip install sv-ttk
import sv_ttk

from wifi_communicator import WiFiCommunicator, OutMessage

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

client = OpenAI(api_key= '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')
fs = 44100                                                          #sample rate
seconds = 3                                                         #seconds of data read
filename = "prediction.wav"
door_close = door_open = batti_off = batti_off = "None"


class GUI(tk.Tk):
    '''
    '''

    ON_BUTTON_STR = 'Start Listener'
    OFF_BUTTON_STR = 'OFF'
    ON_COLOR = 'red'
    OFF_COLOR = 'Green'
    ON_lights = "OFF"

    def __init__(self, communicator: WiFiCommunicator, *, title: str = 'Test GUI', min_size: 'tuple[int, int]' = (300, 100)) -> None:
        '''
        '''
        super().__init__()

        # The wifi communicator object
        self._communicator = communicator


        # Initialize the application
        self.__set_style_and_configure_font(dark=True)
        self.__initialise_window(title, min_size)
        self.__create_widgets()

        # Bind the click on (X) button event to the __on_closing_cb
        self.protocol("WM_DELETE_WINDOW", self.__on_closing_cb)

        
        # Keep alive the GUI and do whatever periodic update to the screen
        self.after(1, self.__update)

    def __set_style_and_configure_font(self, dark: bool = True):
        '''
        sets the app style and font size
        '''
        sv_ttk.set_theme("dark" if dark else 'light')
        font.nametofont('TkDefaultFont').configure(size=9)
        ttk.Style().configure('.', font=(None, 10))

    def __initialise_window(self, title, min_size):
        self.title(title)
        self.minsize(*min_size)
        
    def __create_widgets(self):
        '''
        Create all graphical elements
        '''
        self.__create_led_button()       
        

    def __create_led_button(self):
        self._btn_state_txt = tk.StringVar(value=self.ON_BUTTON_STR)
        self._on_off_btn = tk.Button(self, textvariable=self._btn_state_txt, bg=self.ON_COLOR, command=self.__on_led_btn_click_cb)
        self._on_off_btn.place(relx=0.3, rely=0.2, relwidth=0.4)




    # -------------------- #
    #  On events callbacks #
    # -------------------- #

    def __on_closing_cb(self):
        '''
        Callback to the click on (X) event
        '''
        self._end_signal = True
        self._communicator.destroy()
        self.destroy()


    def __on_led_btn_click_cb(self, *args):
        '''
        '''
        self._btn_state_txt.set("Listening") 
        data, fs = read('../Wake_word/Affirmation/affirm.mp3')
        play(data, fs)

        wait()
        self._btn_state_txt.set("Thank you")
              
        self.__wake_word()
        self.__asm()
        
        led_on = self.ON_lights
        # Update the button text
        #self._btn_state_txt.set(self.ON_BUTTON_STR if led_on else self.OFF_BUTTON_STR)
        self._on_off_btn['bg'] = self.ON_COLOR if led_on else self.OFF_COLOR

        # This should be in accordance to what the other end is expecting
        # (there must be a defined protocol for what each command means)
        msg = OutMessage(data='f' if led_on else 'n')
        self._communicator.send_message(msg)

    def __wake_word(self):
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
                break

            else:
                #print(f"Wake Word NOT Detected")
                #print("Confidence:", prediction[:, 0])
                remove("prediction.wav")

    def __asm(self): 
        door_close = door_open = batti_off = batti_off = "None"
        fs = 44100                                                          #sample rate
        seconds = 3                                                         #seconds of data read
        filename = "command.wav"

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
            lights_off = True
            self.ON_lights = 0

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
            self.ON_lights = 0
        elif (batti_on):
            print("Lights On")
            self.ON_lights = 1

        if (door_close):
            print("Door Closed")
        elif (door_open):
            print("Door Opened")    
        

        return



    # ------------------------------- #
    #  Update the screen periodically #
    # ------------------------------- #

    def __update(self):
        '''
        This is called each 1ms to update the GUI elements and do periodic actions
        '''
        return
    
    