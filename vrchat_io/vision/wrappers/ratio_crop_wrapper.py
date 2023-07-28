"""This file contains the frame wrapper class for cropping read frames by
aspect ratio."""

from enum import Enum
from typing import Literal

import numpy as np

from ...abc.video_capture import FrameWrapper, VideoCapture


class AnchorMode(str, Enum):
    CENTER = "center"
    # 2023-07-26: Not implemented yet.
    # TOP_LEFT = 'top_left'
    # TOP_RIGHT = 'top_right'
    # BOTTOM_LEFT = 'bottom_left'
    # BOTTOM_RIGHT = 'bottom_right'


_anchor_t = Literal[AnchorMode.CENTER]


class RatioCropWrapper(FrameWrapper):
    """Cropping read frames to specified aspect ratio.

    Attributes:
        anchor (str): The anchor of the crop.
        ratio (float): The aspect ratio of the crop, width / height.
    """

    def __init__(self, video_capture: VideoCapture, ratio: float, anchor: _anchor_t = AnchorMode.CENTER) -> None:
        """Initialize the ratio crop wrapper.

        Args:
            video_capture (VideoCapture): The video capture to be wrapped.
            ratio (float): The aspect ratio of the crop, width / height.
            anchor (str): The anchor mode of the crop. `center` is the only supported mode for now.
        """
        super().__init__(video_capture)
        self.anchor = anchor
        self.ratio = ratio

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process the frame read from the video capture.

        Args:
            frame (np.ndarray): The frame read from the video capture.

        Returns:
            np.ndarray: The processed frame.
        """
        match self.anchor:
            case AnchorMode.CENTER:
                frame = center_crop(frame, self.ratio)
            case _:
                raise NotImplementedError(f"Anchor mode {self.anchor} is not implemented yet.")
        return frame


def center_crop(frame: np.ndarray, ratio: float):
    """Crop a frame at the center by aspect ratio.

    Args:
        frame (np.ndarray): The frame to be cropped. (height, width, channels)
        ratio (float): The aspect ratio of the crop, width / height.
    """
    height, width = frame.shape[:2]

    if width / height > ratio:
        new_width = int(height * ratio)
        frame = frame[:, (width - new_width) // 2 : (width + new_width) // 2]
    else:
        new_height = int(width / ratio)
        frame = frame[(height - new_height) // 2 : (height + new_height) // 2, :]
    return frame
