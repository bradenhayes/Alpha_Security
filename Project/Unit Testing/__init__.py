import RPi.GPIO as GPIO
import time
from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import which
import simpleaudio as sa
import soundfile as sf
import simpleaudio as sa
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
import os
import glob
pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)
frequency = 440  # Our played note will be 440 Hz
fs = 44100  # 44100 samples per second
seconds = 3  # Note duration of 3 seconds
duration=1



def testusbmic():


    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    write('test.mp3', fs, myrecording)

    for file in os.listdir("/home/pi/Desktop/Sysc3010/Project/AudioFiles/"):
        if "test.mp3" in file:
            return 1


    os.remove("/home/pi/Desktop/Sysc3010/Project/AudioFiles/Audio_files/test.mp3")



def playaudio():
        # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
    t = np.linspace(0, seconds, seconds * fs, False)

# Generate a 440 Hz sine wave
    note = np.sin(frequency * t * 2 * np.pi)

# Ensure that highest value is in 16-bit range
    audio = note * (2**15 - 1) / np.max(np.abs(note))
# Convert to 16-bit data
    audio = audio.astype(np.int16)

# Start playback
    play_obj = sa.play_buffer(audio, 1, 2, fs)

# Wait for playback to finish before exiting
    play_obj.wait_done()
    
def callback(pin):
        if GPIO.input(pin):
                return 1
        else:
                return 1

GPIO.add_event_detect(pin, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(pin, callback)  # assign function to GPIO PIN, Run function on change

if __name__ == '__main__':
    while True:
        time.sleep(1)
        playaudio()
        testusbmic()
        
