import pyaudio
import wave
import threading
import os

is_recording = False
frames = []
stream = None
p = None

def record_thread():
    global is_recording, frames, stream, p
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []
    
    while is_recording:
        try:
            data = stream.read(CHUNK)
            frames.append(data)
        except Exception as e:
            print(f"Error recording: {e}")
            break
        
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open("audio_record.wav", "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()

def start_recording():
    global is_recording
    if not is_recording:
        is_recording = True
        t = threading.Thread(target=record_thread)
        t.start()

def stop_recording():
    global is_recording
    is_recording = False

