import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment


fs = 44100  # Sample rate
duration =2

myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
write('output.wav', fs, myrecording)  # Save as WAV file
sound=AudioSegment.from_wav('output.wav')
sound.export('output.mp3',format='mp3')
