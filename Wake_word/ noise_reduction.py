from pydub import AudioSegment
from pydub.playback import play

# Load the audio file
input_audio_file = "recorded_audio_1.wav"
audio = AudioSegment.from_file(input_audio_file, format="wav")

# Reduce noise (adjust the dB parameter as needed)
reduced_audio = audio - 20

# Save the output
output_audio_file = "output_audio_file.wav"
reduced_audio.export(output_audio_file, format="wav")

