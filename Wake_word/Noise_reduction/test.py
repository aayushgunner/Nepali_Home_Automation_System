import pywt
from scipy.io import wavfile
import numpy as np
import os

def denoise_audio(input_file, output_file, wavelet='db4', level=5, mode='symmetric'):
    try:
        # Load the audio file
        rate, data = wavfile.read(input_file)

        # Perform Wavelet Transform
        coeffs = pywt.wavedec(data, wavelet, level=level, mode=mode)

        # Set the threshold for denoising
        threshold = np.median(np.abs(coeffs[-1])) / 0.6745

        # Apply soft thresholding
        coeffs = [pywt.threshold(c, threshold, mode='soft') for c in coeffs]

        # Reconstruct the denoised signal
        denoised_signal = pywt.waverec(coeffs, wavelet, mode=mode)

        # Save the denoised audio
        wavfile.write(output_file, rate, denoised_signal.astype(np.int16))
        print(f"Denoised audio saved to '{output_file}' successfully.")
    except Exception as e:
        print(f"An error occurred while processing '{input_file}':", e)

def denoise_audio_files(input_dir, output_dir, wavelet='db4', level=5, mode='symmetric'):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each audio file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".wav"):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)
            denoise_audio(input_file, output_file, wavelet, level, mode)

# Example usage:
input_directory = "Audio_data"
output_directory = "Filtered"
denoise_audio_files(input_directory, output_directory)
