"""This demo shows how to use SoundcardAudioCapture class."""
from pathlib import Path

import numpy as np
import pulsectl
import soundfile as sf

from vrchat_io.audio import PulseAudioApplicationAudioCapture

with pulsectl.Pulse("pulseaudio_application_audio_capture_demo") as pulse:
    print("--- Available Target Applications ---")
    client_names = []
    for client in pulse.client_list():
        print(client.name)
        client_names.append(client.name)
    print("-------------------------------------")
    print()

TARGET_APPLICATION = "Steam" if "Steam" in client_names else client_names[0]
print("Selecting:", TARGET_APPLICATION)

capture = PulseAudioApplicationAudioCapture(TARGET_APPLICATION, sample_rate=44100, frame_size=4410)  # 0.1 sec

frames = []
for i in range(10):
    frame = capture.read()
    print(f"Frame: {i+1}, Shape: {frame.shape}")
    frames.append(frame)

wave_data = np.concatenate(frames)
print()
print("Wave data shape:", wave_data.shape)
print(f"Max: {abs(wave_data).max()}")


FILE = Path(__file__).parent / "pulseaudio_application_audio_capture_demo.wav"
sf.write(FILE, wave_data, samplerate=44100)
