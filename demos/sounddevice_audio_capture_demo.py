"""This demo shows how to use SounddeviceAudioCapture class."""
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf

from vrchat_io.audio import SounddeviceAudioCapture

devices = sd.query_devices()
print("--- devices ---")
print(devices)
print()
print("selecting device:", devices[sd.default.device[0]]["name"])
print("---------------")

capture = SounddeviceAudioCapture(
    samplerate=16000, device=devices[sd.default.device[0]]["name"], frame_size=1600, channels=1
)  # 0.1 sec


frames = []
for i in range(10):  # 1 sec
    frames.append(capture.read())
    print("Frame count:", i + 1)
wave_data = np.concatenate(frames)


FILE = Path(__file__).parent / "sounddevice_audio_capture_demo.wav"
sf.write(FILE, wave_data, samplerate=16000)
