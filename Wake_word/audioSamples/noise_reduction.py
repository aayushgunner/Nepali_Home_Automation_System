import pywt
from scipy.io import wavfile
import numpy as np
def denoise_audio(input_file , output_file):
    
    # Load the audio file
    rate, data = wavfile.read(input_file)
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
    wavfile.write(output_file, rate, denoised_signal.astype(np.int16))

for i in range (1,51):
    input_file = f"recorded_audio_{i}.wav"
    output_file = f"denoised_audio_{i}.wav"
    denoise_audio(input_file , output_file)
# Save the denoised audio

