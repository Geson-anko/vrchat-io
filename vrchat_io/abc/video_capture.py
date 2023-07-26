"""This file contains the abstract video capture class and its wrapper
class."""

from abc import ABC, abstractmethod
from typing import Any

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


class VideoCaptureWrapper(VideoCapture):
    """The Base Wrapper Class for VideoCapture.

    You can access base video capture object by ``self._video_capture``.
    """

    def __init__(self, video_capture: VideoCapture, *args: Any, **kwds: Any) -> None:
        """Initialize the video capture wrapper.

        Args:
            video_capture (VideoCapture): The video capture to be wrapped.
        """
        self._video_capture = video_capture


class FrameWrapper(VideoCaptureWrapper):
    """Wrapper class for video capture.

    This class wraps the return value of :meth:`read` method of the
    video capture class. Please implement the :meth:`process_frame`
    method to process the frame.
    """

    @abstractmethod
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process the frame read from the video capture.

        Args:
            frame (np.ndarray): The frame read from the video capture.

        Returns:
            np.ndarray: The processed frame.
        """
        pass

    def read(self) -> np.ndarray:
        """Read a frame from the video capture.

        Returns:
            np.ndarray: The processed frame read from the video capture.
        """
        return self.process_frame(self._video_capture.read())
