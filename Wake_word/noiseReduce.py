# from scipy.io import wavfile
# import noisereduce as nr
# # load data
# rate, data = wavfile.read("background_noise_1.wav")
# # perform noise reduction
# print(rate, data)
# reduced_noise = nr.reduce_noise(y=data, sr=rate)
# wavfile.write("mywav_reduced_noise.wav", rate, reduced_noise)


# from scipy.io import wavfile
# import noisereduce as nr
# import numpy as np

# # Specify the path to your audio file
# audio_file = "background_noise_1.wav"

# # Load the audio file
# rate, data = wavfile.read(audio_file)

# orig_shape = data.shape
# data = np.reshape(data, (2, -1))

# # perform noise reduction
# # optimized for speech
# reduced_noise = nr.reduce_noise(
#     y=data,
#     sr=rate,
#     stationary=True
# )
# # Specify the output file name
# output_file = "output_reduced_noise.wav"

# # Normalize the audio data to the range [-32768, 32767]
# max_val = np.max(reduced_noise)
# min_val = np.min(reduced_noise)
# reduced_noise_normalized = (reduced_noise - min_val) / (max_val - min_val) * 32767

# # Convert the data type to 16-bit signed integer (numpy.int16)
# reduced_noise_normalized = reduced_noise_normalized.astype(np.int16)

# # Write the normalized audio data to the WAV file
# wavfile.write(output_file, rate, reduced_noise_normalized)

# # Save the noise-reduced audio
# # wavfile.write(output_file, rate, reduced_noise)
from scipy.io import wavfile
import noisereduce as nr
# load data
rate, data = wavfile.read("background_noise_1.wav")
# select section of data that is noise
noisy_part = data[10000:15000]
# perform noise reduction
reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, verbose=True)

output_file = "output_reduced_noise.wav"
wavfile.write(output_file, rate, reduced_noise)