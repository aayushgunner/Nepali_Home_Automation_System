import pyaudio
import wave

def record_audio(file_path_template, duration=3, channels=2, sample_rate=44100, chunk_size=1024, num_recordings=30):
    p = pyaudio.PyAudio()

    for recording_num in range(1, num_recordings + 1):
        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

        print(f"Recording {recording_num}...")

        frames = []
        for i in range(0, int(sample_rate / chunk_size * duration)):
            data = stream.read(chunk_size)
            frames.append(data)

        print(f"Recording {recording_num} complete!")

        stream.stop_stream()
        stream.close()

        current_file_path = file_path_template.format(recording_num)
        print(f"Saving recording {recording_num} to", current_file_path)
        with wave.open(current_file_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

    p.terminate()

if __name__ == "__main__":
    file_path_template = "background_noise_{}.wav"
    record_audio(file_path_template, num_recordings=5)

