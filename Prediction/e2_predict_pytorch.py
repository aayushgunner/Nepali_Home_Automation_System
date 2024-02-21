import sounddevice as sd
from scipy.io.wavfile import write
import librosa
import numpy as np
import torch
import torch.nn as nn
from sys import exit 
import subprocess
from os import remove

fs = 44100                                                          # Sample rate
seconds = 3                                                         # Seconds of data read
filename = "prediction.wav"
class_names = ["Wake Word NOT Detected", "Wake Word Detected"]      # Two classes to identify

# Define your PyTorch model class
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # Define your model architecture here
        self.fc1 = nn.Linear(40, 256)
        self.fc2 = nn.Linear(256, 256)
        self.fc3 = nn.Linear(256, 2)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return torch.softmax(x, dim=1)

# Instantiate your model
model = torch.load("D:/Voice/Project/Nepali_Home_Automation_System/Wake_word/saved_model/WWD.pth")

# Set model to evaluation mode
model.eval()

print("Prediction Started: ")
i = 0
while True:
    print("Say Now: ")                                              
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(filename, fs, myrecording)

    audio, sample_rate = librosa.load(filename)                     
    mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40) 
    mfcc_processed = np.mean(mfcc.T, axis=0)                        
    mfcc_tensor = torch.tensor(mfcc_processed, dtype=torch.float32)  

    # Instantiate your model inside the loop
    # model = torch.load("saved_model/WWD.pth")
    # model.eval()

    # Perform prediction
    with torch.no_grad():
        output = model(mfcc_tensor.unsqueeze(0))  
        _, predicted_class = torch.max(output, 1)
        confidence = torch.softmax(output, dim=1)[0][1].item()
        
    if confidence > 0.72:
        print(f"Wake Word Detected for ({i})")
        print("Confidence:", confidence)
        remove("prediction.wav")
        subprocess.call(['python', 'D:/Voice/Project/Nepali_Home_Automation_System/Speech_processing/f_whisper_ai.py'])
        exit()
        
    else:
        print(f"Wake Word NOT Detected")
        print("Confidence:", 1 - confidence)
        remove("prediction.wav")
