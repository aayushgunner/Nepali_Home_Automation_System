import pyaudio
import numpy as np
import wave

json_path = "check.json"
def record_audio(file_path_template, duration=3, channels=2, sample_rate=44100, chunk_size=1024):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    print("Say the command")

    frames = []
    for i in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("Command input complete!")

    stream.stop_stream()
    stream.close()
    current_file_path = file_path_template
    print(f"Saving recording  to", current_file_path)
    with wave.open(current_file_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

    p.terminate()

    audio_data = b''.join(frames)
    audio_np = np.frombuffer(audio_data, dtype=np.int16)
    return audio_np, sample_rate



if __name__ == "__main__":
    file_path_template = "wehaveto.wav"
    audio_data, sample_rate = record_audio(file_path_template)

