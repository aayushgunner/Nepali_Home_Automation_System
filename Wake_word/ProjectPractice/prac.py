import os
import librosa
import math
import json
import matplotlib.pyplot as plt
FILE_TO_PROCESS = "wehaveto.wav"
json_path = "atti.json"
SAMPLE_RATE = 22050
DURATION = 3
# SAMPLES_PER_TRACK = SAMPLE_RATE * DURATION


def save_mfcc(file_path, json_path, n_mfcc=13, n_fft=2048, hop_length=512, num_segments=3):
    data = {
        "mfcc": [],
    }

    signal, sr = librosa.load(file_path, sr=SAMPLE_RATE)
    
    segment_duration = DURATION / num_segments
    num_samples_per_segment = int (segment_duration * sr)
    expected_num_mfcc_vectors_per_segment = math.ceil(num_samples_per_segment / hop_length)

    for s in range(num_segments):
        start_sample = num_samples_per_segment * s
        finish_sample = start_sample + num_samples_per_segment

        mfcc = librosa.feature.mfcc(y=signal[start_sample:finish_sample], sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)
        mfcc = mfcc.T

        # Ensure that the length of mfcc matches the expected_num_mfcc_vectors_per_segment
        if len(mfcc) == expected_num_mfcc_vectors_per_segment:
            data["mfcc"].append(mfcc.tolist())
            plt.figure(figsize=(10, 6))
            librosa.display.specshow(mfcc.T, sr=sr, hop_length=hop_length, x_axis='time')
            plt.colorbar(format='%+2.0f dB')
            plt.title('MFCC', fontsize=20)  # Increase title font size
            plt.xlabel('Time', fontsize=16)  # Increase x-axis label font size
            plt.ylabel('MFCC Coefficients', fontsize=16)
            plt.show()


    with open(json_path, "w") as fp:
        json.dump(data, fp, indent=4)
if __name__ == "__main__":
    current_directory = os.getcwd()
    file_to_process_path = os.path.join(current_directory, FILE_TO_PROCESS)
    save_mfcc(file_to_process_path, json_path)
