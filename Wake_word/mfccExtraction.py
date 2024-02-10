
import os
import librosa
import numpy as np
import json

# Function to extract MFCC features from audio files in a folder
def extract_mfcc_from_folder(folder_path, n_fft=2048, hop_length=512, n_mfcc=13):
    mfcc_list = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.wav'):
            audio_path = os.path.join(folder_path, filename)
            signal, sr = librosa.load(audio_path)
            mfccs = librosa.feature.mfcc(y=signal, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mfcc=n_mfcc)
            mfcc_list.append(mfccs.T.tolist())  # Convert NumPy array to list and append to list
    return mfcc_list

# Define paths to the folders containing audio files
folder_paths = [
    "/home/aayushgunner/aayush/coding/Nepali_Home_Automation_System/Wake_word/audioSamples/NoiseReduced"
]

# Dictionary to store MFCC features for each folder
mfcc_data = {"mapping": [], "mfcc": []}

# Extract MFCC features for each folder and store in the same dictionary
for folder_path in folder_paths:
    folder_name = os.path.basename(folder_path)
    mfcc_list = extract_mfcc_from_folder(folder_path)
    mfcc_data["mapping"].append(folder_name)
    mfcc_data["mfcc"].append(mfcc_list)

# Save the combined MFCC data to a JSON file
combined_json_file = "/home/aayushgunner/aayush/coding/Nepali_Home_Automation_System/Wake_word/combined_mfcc.json"
with open(combined_json_file, 'w') as f:
    json.dump(mfcc_data, f)

print("Combined MFCC features saved to:", combined_json_file)
