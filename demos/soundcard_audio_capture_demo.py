"""This demo shows how to use SoundcardAudioCapture class."""
from pathlib import Path

import numpy as np
import soundcard as sc
import soundfile as sf

from vrchat_io.audio import SoundcardAudioCapture

# List available microphones
mics = sc.all_microphones(include_loopback=True)
print("--- Available Microphones ---")
for mic in mics:
    print(f"Name: {mic.name}")
    print(f"ID: {mic.id}")
    print("-------------------------------")

# Use default microphone
DEVICE_NAME = sc.default_microphone().name  # specify your microphone.
print(f"Using default microphone: {DEVICE_NAME}")
print()

# Initialize audio capture
capture = SoundcardAudioCapture(device_id=DEVICE_NAME, samplerate=44100, frame_size=4410, channels=1)  # 0.1 sec

# Record audio
frames = []
for i in range(10):  # 1 sec
    frames.append(capture.read())
    print("Frame count:", i + 1)
wave_data = np.concatenate(frames)

print("--- Wave data information ---")
print("Wave shape:", wave_data.shape)
print("Wave dtype:", wave_data.dtype)
print("Wave abs max:", np.abs(wave_data).max())
print("Wave abs min:", np.abs(wave_data).min())


# Save to file
FILE = Path(__file__).parent / "soundcard_audio_capture_demo.wav"
sf.write(FILE, wave_data, samplerate=44100)
