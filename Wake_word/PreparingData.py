import sounddevice as sd                                                            #record sound and make numpy array
from scipy.io.wavfile import write                                                  #take array and save as wav audio file

def record_audio_and_save(save_path, n_times=100):                                  #wakeword recording function
    input("To record wakeword, press Enter ")
    for i in range(n_times):
        fs = 44100                                                                  #sample rate
        seconds = 3                                                                 #seconds of recording
        myrecording = sd.rec(int(seconds*fs), samplerate = fs, channels = 2)
        sd.wait()
        write(save_path + str(i) + ".wav", fs, myrecording)                         #save recording
        #input(f"Press to record next or to stop, press ctrl c ({i+1}/{n_times})")
    pass

def record_background_save(save_path, n_times=100):                                 #background audio
    input("To start background recording press Enter ")
    for i in range(n_times):
        fs = 44100                                                                  #sample rate
        seconds = 3                                                                 #seconds of recording
        myrecording = sd.rec(int(seconds*fs), samplerate = fs, channels = 2)
        sd.wait()
        write(save_path + str(i) + ".wav", fs, myrecording)                         #save recording
    pass


#print("Recording wake word: \n")
#record_audio_and_save("Audio_data/")

print("Recording background noise\n")
record_background_save("Background_data/")
