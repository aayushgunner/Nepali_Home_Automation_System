import shutil
import os

# Set the path to the original .wav file
original_wav_path = "lol.wav"

# Create a directory to store the copies
output_directory = "loldata"
os.makedirs(output_directory, exist_ok=True)

# Specify the number of copies
num_copies = 100

# Copy the .wav file multiple times
for i in range(1, num_copies + 1):
    copy_path = os.path.join(output_directory, f"lol_{i}.wav")
    shutil.copy2(original_wav_path, copy_path)
    print(f"Copy {i} created at {copy_path}")