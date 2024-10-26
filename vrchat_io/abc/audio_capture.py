"""This file contains the abstract audio capture class and its variants."""

from abc import ABC, abstractmethod

import numpy as np
import numpy.typing as npt


class AudioCapture(ABC):
    """Abstract Audio Capture Class.

    This class is the abstract class for capturing audio. If you want to add a
    new audio capture method, you should inherit this class and implement the
    :meth:`read` method.
    """

    @abstractmethod
    def read(self) -> npt.NDArray[np.float32]:
        """Reads frames from audio source.

        Returns:
            NDArray[np.float32]: The freame read from audio source.
                Expected shape is `(frame_count, channels)`.
        """


class ApplicationAudioCapture(AudioCapture):
    """Abstract Application Audio Capture class.

    Capturing the audio from specific application.
    """

    @abstractmethod
    def __init__(self, target_application: str) -> None:
        """Constructs ApplicationAudioCapture.

        Args:
            target_application (str): Please specify target application name.
        """
        super().__init__()
