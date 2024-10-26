"""This file contains AudioCapture class using Sounddevice module."""

from logging import getLogger
from typing import Literal

import numpy as np
import numpy.typing as npt
import sounddevice as sd

from ..abc.audio_capture import AudioCapture

logger = getLogger(__name__)


class SounddeviceAudioCapture(AudioCapture):
    """This class implements audio capture functionality using the Sounddevice
    library.

    Attributes:
        _stream (sd.InputStream): The Sounddevice input stream object.
        _frame_size (int): Number of frames to read in each capture.

    How to use:
        >>> audio_capture = SounddeviceAudioCapture(
        ...     samplerate=44100,
        ...     device=None,  # Uses default input device
        ...     frame_size=1024,
        ...     channels=1,
        ...     latency="high"
        ... )
        >>> audio_frames = audio_capture.read()
    """

    def __init__(
        self,
        samplerate: float | None = None,
        device: str | int | None = None,
        frame_size: int = 1024,
        channels: int = 1,
        latency: Literal["high", "low"] | float | None = None,
    ) -> None:
        """Initializes an instance of SounddeviceAudioCapture.

        Args:
            samplerate (float | None, optional): The desired sample rate in Hz. If None, uses default.
            device (str | int | None, optional): The audio input device to use. Can be device name,
                index, or None for default device.
            frame_size (int, optional): Number of frames to read in each capture. Defaults to 1024.
            channels (int, optional): Number of audio channels to capture. Defaults to 1 (mono).
            latency (Literal["high", "low"] | float | None, optional): Stream latency in seconds or
                preset ("high"/"low"). None uses default.
        """
        super().__init__()
        self._stream = sd.InputStream(
            samplerate=samplerate,
            device=device,
            latency=latency,
            channels=channels,
            dtype=np.float32,
        )
        self._frame_size = frame_size
        self._stream.start()

    def read(self) -> npt.NDArray[np.float32]:
        """Reads audio frames from the input stream.

        Returns:
            npt.NDArray[np.float32]: Array of captured audio frames with shape
                (frame_size, channels) and values normalized between -1.0 and 1.0.

        Note:
            If buffer overflow occurs during capture, a warning message will be logged.
        """
        frames, overflow = self._stream.read(self._frame_size)
        if overflow:
            logger.warning("Audio buffer overflow detected - some samples may have been dropped")
        return frames.astype(np.float32)

    def __del__(self) -> None:
        """Cleanup method to properly close the audio stream when the object is
        destroyed."""
        self._stream.stop()
        self._stream.close()
