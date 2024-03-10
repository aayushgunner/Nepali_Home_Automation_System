from audiomentations import Compose, AddGaussianNoise, PitchShift, HighPassFilter, ClippingDistortion, LowPassFilter
from librosa import load
from soundfile import write
from os import listdir 


def augmenter(path, dest):
    i = 1000
    for files in listdir(path):
        if "latest" in files:
            augment = Compose([
                AddGaussianNoise(min_amplitude = 0.001, max_amplitude = 0.0011, p = 0.5),
                PitchShift(min_semitones=-3, max_semitones=4, p = 0.6),
                ClippingDistortion(min_percentile_threshold=2, max_percentile_threshold=7, p=0.5),
                HighPassFilter(min_cutoff_freq=600, max_cutoff_freq=3400, p=0.8)
           ])
            signal, sample_rate = load(path + files)
            augmented_signal = augment(signal, sample_rate)
            write(dest + str(i) + "_newaug.wav", augmented_signal, sample_rate)
            i = i + 1



file_path = "..\..\Background_data/"
dest = "..\..\Background_data/"
augmenter(file_path, dest)
