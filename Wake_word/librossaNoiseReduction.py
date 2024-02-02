import librosa
import numpy as np
from sklearn.decomposition import NMF
import soundfile as sf

# Load the audio signal
audio_file = "background_noise_1.wav"
y, sr = librosa.load(audio_file, sr=None)

# Compute the spectrogram
D = np.abs(librosa.stft(y))

# Perform Non-negative Matrix Factorization (NMF)
n_components = 2  # Number of sound sources to separate
model = NMF(n_components=n_components, init='random', random_state=0)
W = model.fit_transform(D)
H = model.components_

# Reconstruct the source signals
source_signals = np.dot(W, H)

# Save the separated source signals
for i in range(n_components):
    source_file = f'source_{i+1}.wav'
    print(f"Shape of source signal {i+1}: {source_signals[:, i].shape}")  # Debugging
    sf.write(source_file, librosa.istft(source_signals[:, i]), sr)
