import os
import librosa
import math
import json

FILE_TO_PROCESS = "sounddevice_dhoka.wav"
json_path = "atti.json"
SAMPLE_RATE = 22050
DURATION = 3
# SAMPLES_PER_TRACK = SAMPLE_RATE * DURATION

def save_mfcc(file_path, json_path, n_mfcc=13, n_fft=2048, hop_length=512):
    data = {
        "mfcc": [],
       
    }

    signal, sr = librosa.load(file_path, sr=SAMPLE_RATE)

    mfcc = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)
    mfcc = mfcc.T

    data["mfcc"].append(mfcc.tolist())
    with open(json_path, "w") as fp:
        json.dump(data, fp, indent=4)

if __name__ == "__main__":
    current_directory = os.getcwd()
    file_to_process_path = os.path.join(current_directory, FILE_TO_PROCESS)
    save_mfcc(file_to_process_path, json_path)
