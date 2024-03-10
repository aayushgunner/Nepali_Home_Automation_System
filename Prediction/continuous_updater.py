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
from wifi_communicator import WiFiCommunicator, OutMessage

dhoka_close = dhoka_open = batti_on = batti_off = night = "None"
client = OpenAI(api_key= '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')
fs = 44100                                                          #sample rate
seconds = 3                                                         #seconds of data read
filename = "prediction.wav"
i = 0

def wake_word(communicator: WiFiCommunicator ):
    global i
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
            msg = OutMessage(data='f' if batti_off else 'n')
            communicator.send_message(msg)
            msg = OutMessage(data = 'c' if dhoka_close else 'o')
            communicator.send_message(msg)     
            if (night == 1):
                exit()   
            
            wake_word(communicator=communicator)

        else:
            #print(f"Wake Word NOT Detected")
            #print("Confidence:", prediction[:, 0])
            remove("prediction.wav")


def asm(): 
    global dhoka_close, dhoka_open, batti_on, batti_off, night
    night = 0
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
    print(transcription)
    
    substrings_lights = ["batti", "vati", "bati", "batii", "bhatti", "bhati", "but", "light", "lights", "batthi", "बति", "bath", 'बत्ति', 'batii' ]
    lights_on = ["bala", "vala", "valor", "wala", "on", "baala", "bhala", "bahla", "turn on", "balla", "बादः"]
    lights_off = ["nibhau", "nibau", "banda", "wanda", "off", "vanda", "bhanda", "nibha", "turn off", "mebow", "nibbhau", 'निबाव', 'mibaaw']

    substrings_doors = ["dhoka", "doka", "dhukha", "dhuka", "duka", "coca", "dukkha", "dhooka", "duca", "dhūkā", "dooka", "दुखा", "धुका", "lid", "dhūkha"]
    door_open = ["khola", "kola", "koala", "cola", "open", "kholo", "khula", "khunna", "khūlā", "khūlā", "kula", "khoola", "kholau", "khoolau"]
    door_close = ["lagau", "laga","loga", "laaga", "lagaa", "close", "laghau", "बन्द" , "ladau", "banda", "bundhu", "bunda", "baanda", "band", "logo", "logau", "bandha", "bondoo", "bondo", "bondho", "bonda"]


    if ("night" in transcription):
        print("\nGood Night")
        night = 1
        dhoka_open = False
        dhoka_close = True
        batti_off = True
        batti_on = False

    if any(substring in transcription for substring in substrings_lights):
        if any(further in transcription for further in lights_on):
            batti_on = True
            batti_off = False
        elif any(further in transcription for further in lights_off):
            batti_off = True
            batti_on = False
        

    if(any(substring in transcription for substring in substrings_doors)):
        if any(newer in transcription for newer in door_open):
            dhoka_open = True
            dhoka_close = False
        elif any(newer in transcription for newer in door_close):
            dhoka_close = True
            dhoka_open = False
            
    if (batti_off):
        print("Lights Off")
    elif (batti_on):
        print("Lights On")

    if (dhoka_close):
        print("Door Closed")
    elif (dhoka_open):
        print("Door Opened")    

    return


if __name__ == "__main__":
    communicator = WiFiCommunicator(max_buffer_sz=128)
    msg = OutMessage(data='f')
    communicator.send_message(msg)
    msg = OutMessage(data = 'c')
    communicator.send_message(msg)  
    wake_word(communicator)