from openai import OpenAI
from sounddevice import rec, wait, play
from scipy.io.wavfile import write


OpenAI.api_key = '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'
client = OpenAI(api_key= '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')


fs = 44100                                                          #sample rate
seconds = 3                                                         #seconds of data read
filename = "command.wav"
class_names = ["Wake Word NOT Detected", "Wake Word Detected"]

print("Say Now: ")                                              #prompts listener
myrecording = rec(int(seconds * fs), samplerate=fs, channels=2)
wait()
write(filename, fs, myrecording)


audio_file= open("command.wav", "rb")
transcription = client.audio.translations.create(
  model="whisper-1", 
  file=audio_file
)
print(transcription.text)