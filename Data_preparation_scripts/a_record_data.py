from sounddevice import wait, rec                                                            #record sound and make numpy array
from scipy.io.wavfile import write                                                  #take array and save as wav audio file

def record_audio_and_save(save_path, n_times= 50):                                  #wakeword recording function
    input("To record wakeword, press Enter ")
    for i in range(n_times):
        fs = 44100                                                                  #sample rate
        seconds = 3                                                                 #seconds of recording
        myrecording = rec(int(seconds*fs), samplerate = fs, channels = 2)
        wait()
        write(save_path + str(i) + ".wav", fs, myrecording)                         #save recording
        #input(f"Press to record next or to stop, press ctrl c ({i+1}/{n_times})")
        print("Next....\n")
    pass

def record_background_save(save_path, n_times=50):                                 #background audio
    input("To start background recording press Enter ")
    for i in range(n_times):
        fs = 44100                                                                  #sample rate
        seconds = 3                                                                 #seconds of recording
        myrecording = rec(int(seconds*fs), samplerate = fs, channels = 2)
        wait()
        write(save_path + str(i) + "latest.wav", fs, myrecording)                         #save recording
        print("Next")
    pass


def word_record(save_path, n_times=1):                                            #background audio
    input("To start recording press Enter ")
    for i in range(n_times):
        fs = 44100                                                                  #sample rate
        seconds = 3                                                                 #seconds of recording
        myrecording = rec(int(seconds*fs), samplerate = fs, channels = 2)
        wait()
        write(save_path + str(i) + ".wav", fs, myrecording)                         #save recording
        print("Next")
    pass


# print("Recording wake word: \n")
# record_audio_and_save("D:\Voice\Project\Audio_data/")

print("Recording background noise\n")
record_background_save("D:\Voice\Project\Background_data/")

# print("Recording word\n")
# word_record(r"D:\Voice\Project\Nepali_Home_Automation_System\Data_preparation_scripts/")