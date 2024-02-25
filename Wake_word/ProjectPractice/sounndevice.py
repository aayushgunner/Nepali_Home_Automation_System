import sounddevice as sd
import soundfile as sf

def record_audio(file_path, duration=3, samplerate=44100, channels=2):
    print("Recording...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
    sd.wait()
    print("Finished recording.")
    sf.write(file_path, audio_data, samplerate)

if __name__ == "__main__":
    file_path = "sounddevice.wav"
    record_audio(file_path, duration=3)
    print(f"Audio recorded and saved to {file_path}")

