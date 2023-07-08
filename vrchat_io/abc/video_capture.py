"""This file contains the abstract video capture class."""

from abc import ABC, abstractmethod

import numpy as np


class VideoCapture(ABC):
    """Abstract Video Capture Class.

    This class is the abstract class for capturing video. If you want to add a
    new video capture method, you should inherit this class and implement the
    :meth:`read` method.
    """

    @abstractmethod
    def read(self) -> np.ndarray:
        """Read a frame from the video capture.

        Returns:
            np.ndarray: The frame read from the video capture.
        """
        pass
