from pydub import AudioSegment
from pydub.silence import split_on_silence
import pytorch
def extract_speech_with_noise_reduction(input_file, output_file, silence_thresh=-40, noise_reduction_strength=1000):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Split the audio on silence
    segments = split_on_silence(audio, silence_thresh=silence_thresh)

    # Find the first non-silent segment
    for i, segment in enumerate(segments):
        if segment.dBFS > silence_thresh:
            break
    else:
        i = len(segments)  # If no non-silent segment is found, use all segments

    # Concatenate the segments where speech is present, starting from the first non-silent segment
    output_audio = AudioSegment.silent()
    for segment in segments[i:]:
        output_audio += segment

    # Apply a low-pass filter for noise reduction
    output_audio = output_audio.low_pass_filter(noise_reduction_strength)

    # Export the result to a new file
    output_audio.export(output_file, format="wav")

if __name__ == "__main__":
    input_file = "recorded_audio.wav"
    output_file = "output_speech_with_noise_reduction.wav"

    print("Extracting speech and applying noise reduction...")
    extract_speech_with_noise_reduction(input_file, output_file)
    print(f"Speech extracted with noise reduction and saved to {output_file}")
