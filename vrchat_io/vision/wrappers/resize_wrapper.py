"""This file contains the frame wrapper class for resizing read frames."""

import cv2
import numpy as np

from ...abc.video_capture import FrameWrapper, VideoCapture


class ResizeWrapper(FrameWrapper):
    """Resizing read frames to specified size.

    Attributes:
        size (tuple[int, int]): (width, height), the size of the frame.
    """

    def __init__(self, video_capture: VideoCapture, size: tuple[int, int]) -> None:
        """Initialize the resize wrapper.

        Args:
            video_capture (VideoCapture): The video capture to be wrapped.
            size (tuple[int, int]): (width, height), the size of the frame.
        """
        super().__init__(video_capture)
        self.size = size

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process the frame read from the video capture.

        Args:
            frame (np.ndarray): The frame read from the video capture.

        Returns:
            np.ndarray: The processed frame.
        """
        return cv2.resize(frame, self.size)
