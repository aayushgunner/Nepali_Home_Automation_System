import numpy as np
import soundfile as sf
import librosa
import librosa.display
import matplotlib as plt

# Load the audio file
audio_file = '0.wav'
signal, sr = librosa.load(audio_file, sr=None)

# Estimate noise profile
noise_sample = signal[:44100]  # Assuming the noise is present in the first 1 second
noise_profile = np.mean(np.abs(noise_sample))

# Set a threshold for noise reduction
alpha = 1.5

# Apply noise reduction
processed_signal = signal - alpha * noise_profile
processed_signal = np.clip(processed_signal, -1.0, 1.0)  # Clip the values to the valid range

# Save the processed audio
sf.write('processed_audio.wav', processed_signal, sr)
