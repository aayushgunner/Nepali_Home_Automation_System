import pywt
from scipy.io import wavfile
import numpy as np
import os

# Specify the path to your audio file
audio_dir = "Audio_data/"
i = 0
save_path = "Filtered/"

for files in os.listdir(audio_dir):
    print(files)
    i = i+1
    # Load the audio file
    rate, data = wavfile.read("Audio_data/" + files)
    # Perform Wavelet Transform
    # Perform Wavelet Transform
    level = 0 # Adjust the level of decomposition
    coeffs = pywt.wavedec(data, 'db4', level=level, mode='symmetric')

    # Set the threshold for denoising
    threshold = np.median(np.abs(coeffs[-1])) / 0.6745

    # Apply soft thresholding
    coeffs = [pywt.threshold(c, threshold, mode='soft') for c in coeffs]

    # Reconstruct the denoised signal
    denoised_signal = pywt.waverec(coeffs, 'db4', mode='symmetric')

    # Save the Denoised Audio to a New File
    output_file = save_path + str(i) + ".wav"

    wavfile.write(output_file, rate, denoised_signal.astype(np.int16))
    # Save the denoised audio
    wavfile.write(output_file, rate, denoised_signal.astype(np.int16))