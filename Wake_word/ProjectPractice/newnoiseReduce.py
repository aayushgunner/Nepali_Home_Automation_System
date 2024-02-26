import pyaudio
import numpy as np
import scipy.signal
import wave

CHUNK = 1024*2

WIDTH = 2
DTYPE = np.int16
MAX_INT = 32768.0

CHANNELS = 1
RATE = 11025*1

# Open the input .wav file for reading
input_wav = wave.open('sounddevice.wav', 'rb')

# Create a new .wav file for writing the processed audio
output_wav = wave.open('output.wav', 'wb')
output_wav.setnchannels(CHANNELS)
output_wav.setsampwidth(WIDTH)
output_wav.setframerate(RATE)

p = pyaudio.PyAudio()

# Read frames from the input .wav file
audio_data = input_wav.readframes(CHUNK)

print("* processing")

while audio_data:
    # Convert binary data to NumPy array
    normalized_data = np.frombuffer(audio_data, dtype=DTYPE) / MAX_INT
    freq_data = np.fft.fft(normalized_data)

    # Processing steps similar to microphone input
    
    # Write processed audio to the output .wav file
    output_wav.writeframes(normalized_data.tobytes())

    # Read next frames from the input .wav file
    audio_data = input_wav.readframes(CHUNK)

print("* done processing")

# Close the input and output .wav files
input_wav.close()
output_wav.close()

p.terminate()
