from audiomentations import Compose, AddGaussianNoise, PitchShift, HighPassFilter, ClippingDistortion, LowPassFilter
import librosa
import soundfile as sf
from os import listdir 


def augmenter(path, dest):
    i = 0
    for files in listdir(path):
        
        augment = Compose([
            AddGaussianNoise(min_amplitude = 0.001, max_amplitude = 0.0011, p = 0.3),
            PitchShift(min_semitones=-2, max_semitones=4, p = 0.6),
            #ClippingDistortion(min_percentile_threshold=2, max_percentile_threshold=9, p=0.2),
            HighPassFilter(min_cutoff_freq=600, max_cutoff_freq=3400, p=0.8)
        ])
        signal, sample_rate = librosa.load(path + files)
        augmented_signal = augment(signal, sample_rate)
        sf.write(dest + str(i) + "aug.wav", augmented_signal, sample_rate)
        i = i + 1



file_path = "D:\Voice\Project\Background_data/"
dest = "D:\Voice\Project\Background_data/"
augmenter(file_path, dest)
