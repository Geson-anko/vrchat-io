"""This file contains AudioCapture class using Soundcard module."""

from logging import getLogger

import numpy as np
import numpy.typing as npt
import soundcard as sc

from ..abc.audio_capture import AudioCapture

logger = getLogger(__name__)


class SoundcardAudioCapture(AudioCapture):
    """This class implements audio capture functionality using the Soundcard
    library.

    Attributes:
        _mic: The Soundcard microphone object.
        _stream: The Soundcard recording stream.
        _frame_size (int): Number of frames to read in each capture.
        _blocksize (int): Size of each audio block for the recorder.
        _samplerate (float): The sampling rate in Hz.
        _channels (int): Number of audio channels.

    How to use:
        >>> audio_capture = SoundcardAudioCapture(
        ...     samplerate=44100,
        ...     device_id=None,  # Uses default input device
        ...     frame_size=1024,
        ...     blocksize=1024,  # Optional, defaults to frame_size
        ...     channels=1
        ... )
        >>> audio_frames = audio_capture.read()
    """

    def __init__(
        self,
        samplerate: float = 44100,
        device_id: str | None = None,
        frame_size: int = 1024,
        blocksize: int | None = None,
        channels: int = 1,
    ) -> None:
        """Initializes an instance of SoundcardAudioCapture.

        Args:
            samplerate (float, optional): The desired sample rate in Hz. Defaults to 44100.
            device_id (str | None, optional): The audio input device id to use. Can be device name
                or None for default device.
            frame_size (int, optional): Number of frames to read in each capture. Defaults to 1024.
            blocksize (int | None, optional): Size of each audio block for the recorder. Defaults to None.
            channels (int, optional): Number of audio channels to capture. Defaults to 1 (mono).

        Raises:
            IndexError: If specified device is not found.
        """
        super().__init__()

        # Get the microphone device
        if device_id is None:
            self._mic = sc.default_microphone()
        else:
            self._mic = sc.get_microphone(device_id, include_loopback=True)
        self._frame_size = frame_size
        self._blocksize = blocksize

        self._samplerate = samplerate
        self._channels = channels

        # Open the recording stream
        self._stream = self._mic.recorder(samplerate=samplerate, channels=channels, blocksize=blocksize)
        self._stream.__enter__()

    def read(self) -> npt.NDArray[np.float32]:
        """Reads audio frames from the input stream.

        Returns:
            npt.NDArray[np.float32]: Array of captured audio frames with shape
                (frame_size, channels) and values normalized between -1.0 and 1.0.
        """
        frames = self._stream.record(numframes=self._frame_size)
        return frames.astype(np.float32)

    def __del__(self) -> None:
        """Cleanup method to properly close the audio stream when the object is
        destroyed."""
        if hasattr(self, "_stream"):
            self._stream.__exit__(None, None, None)
