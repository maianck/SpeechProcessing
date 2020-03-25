import sounddevice as sd
import soundfile as sf
import time 

def recording(filename, duration, sr, channels):
    print('recording')
    myrecording = sd.rec(int(duration * sr), samplerate=sr, channels=channels)
    sd.wait()
    sf.write(filename, myrecording, sr)
    print('done recording')

recording('sync_record.wav', 10, 16000, 1)