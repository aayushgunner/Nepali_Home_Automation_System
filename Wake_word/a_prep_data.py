import sounddevice as sd                                                            #record sound and make numpy array
from scipy.io.wavfile import write                                                  #take array and save as wav audio file

def record_audio_and_save(save_path, n_times= 50):                                  #wakeword recording function
    input("To record wakeword, press Enter ")
    for i in range(n_times):
        j = i + 151;
        fs = 44100                                                                  #sample rate
        seconds = 3                                                                 #seconds of recording
        myrecording = sd.rec(int(seconds*fs), samplerate = fs, channels = 2)
        sd.wait()
        write(save_path + str(j) + "wake.wav", fs, myrecording)                         #save recording
        #input(f"Press to record next or to stop, press ctrl c ({i+1}/{n_times})")
        print("Next....\n")
    pass

def record_background_save(save_path, n_times=50):                                 #background audio
    input("To start background recording press Enter ")
    for i in range(n_times):
        j = i+151;
        fs = 44100                                                                  #sample rate
        seconds = 3                                                                 #seconds of recording
        myrecording = sd.rec(int(seconds*fs), samplerate = fs, channels = 2)
        sd.wait()
        write(save_path + str(j) + ".wav", fs, myrecording)                         #save recording
        print("Next")
    pass

def command_and_save(save_path, n_times=1):                                        #command recording function
    input("To record command, press Enter ")
    for i in range(n_times):
        fs = 44100                                                                  #sample rate
        seconds = 3                                                                 #seconds of recording
        myrecording = sd.rec(int(seconds*fs), samplerate = fs, channels = 2)
        sd.wait()
        write("signal.wav", fs, myrecording)                         #save recording
        #input(f"Press to record next or to stop, press ctrl c ({i+1}/{n_times})")
        print("Next....\n")
    pass

print("Recording wake word: \n")
record_audio_and_save("D:\Voice\Project\Audio_data/")

# print("Recording background noise\n")
# record_background_save("D:\Voice\Project\Background_data/")

# print("Recording commands\n")
# command_and_save("D:\Voice\Project/")                                       #for making selective asr