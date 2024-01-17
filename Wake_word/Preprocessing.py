import os
import librosa
import librosa.display
import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd 

all_data = []

data_path_dict = {
    0 : ["Background_data/" + file_path for file_path in os.listdir("Background_data/")],       #for each file in directory, identify 0 case
    1 : ["Audio_data/" + file_path for file_path in os.listdir("Audio_data/")]                  #for each file in directory, identify 1 case
}

for class_label, list_of_files in data_path_dict.items():
    for single_file in list_of_files:
        data, sample_rate = librosa.load(single_file)                                           #input audio file, returns numpy arra, sample rate
        mfccs = librosa.feature.mfcc(y=data, sr = sample_rate, n_mfcc=40)                       #calculate mfcc val
        mfcc_processed = np.mean(mfccs.T, axis=0)                                               #process mfcc by axis reduction
        all_data.append([mfcc_processed, class_label])                                          #append to list
    print(f"Info: Successful preprocess {class_label}")


df = pd.DataFrame(all_data, columns = ["feature", "class_label"])                               
df.to_pickle("Final_audio_data_csv/audio_data.csv")                                             #forms a csv file