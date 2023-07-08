"""This file contains VideoCapture class using OpenCV."""
import logging

import cv2
import numpy as np

from ..abc.video_capture import VideoCapture as AbstractVideoCapture

logger = logging.getLogger(__name__)


class OpenCVVideoCapture(AbstractVideoCapture):
    """This class is the video capture class using OpenCV.

    Attributes:
        camera (cv2.VideoCapture): OpenCV VideoCapture.
        bgr2rgb (bool): Whether convert BGR to RGB.
        num_trials_on_read_failure (int): Number of trials on read failure.
        expected_width (int): Expected width of captured frame.
        expected_height (int): Expected height of captured frame.
        expected_fps (float): Expected FPS of capture.

    How to use:
        >>> cam = OpenCVVideoCapture(
        ... camera = cv2.VideoCapture(2), # Device index depends on your pc.
        ... width = 1920,
        ... height = 1080,
        ... fps = 30,
        ... )
        >>> frame = cam.read()
    """

    def __init__(
        self,
        camera: cv2.VideoCapture,
        width: int = 640,
        height: int = 480,
        fps: float = 30,
        bgr2rgb: bool = True,
        num_trials_on_read_failure: int = 10,
    ) -> None:
        """Initializes an instance of OpenCVVideoCapture.

        Args:
            camera (cv2.VideoCapture): The OpenCV VideoCapture object to use.
            width (int, optional): The desired width of the video frames.
            height (int, optional): The desired height of the video frames.
            fps (float, optional): The desired frames per second (fps) of the video.
            bgr2rgb (bool, optional): If True, converts video frames from BGR to RGB.
            num_trials_on_read_failure (int, optional): Number of trials on read failure.
        """

        self.camera = camera
        self.bgr2rgb = bgr2rgb
        self.num_trials_on_read_failure = num_trials_on_read_failure

        self.expected_width = width
        self.expected_height = height
        self.expected_fps = fps

        self.configure_camera()

    def configure_camera(self) -> None:
        """Configures the camera settings with the desired properties."""
        if not self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.expected_width):
            logger.warning(f"Failed to set width to {self.expected_width}.")
        if not self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.expected_height):
            logger.warning(f"Failed to set height to {self.expected_height}.")
        if not self.camera.set(cv2.CAP_PROP_FPS, self.expected_fps):
            logger.warning(f"Failed to set fps to {self.expected_fps}.")

    @property
    def width(self) -> int:
        """Get the current width of the video frames from the camera.

        Returns:
            int: The current width of the video frames.
        """
        return int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self) -> int:
        """Get the current height of the video frames from the camera.

        Returns:
            int: The current height of the video frames.
        """
        return int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def fps(self) -> float:
        """Get the current frames per second (fps) from the camera.

        Returns:
            float: The current frames per second (fps) of the video.
        """
        return float(self.camera.get(cv2.CAP_PROP_FPS))

    def read(self) -> np.ndarray:
        """Reads a frame from the video capture.

        Returns:
            np.ndarray: The frame read from the video capture with shape (height, width, 3).

        Raises:
            RuntimeError: If the frame cannot be read after num_trials_on_read_failure attempts.
        """

        for i in range(self.num_trials_on_read_failure):
            ret, frame = self.camera.read()
            if ret:
                if self.bgr2rgb:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return frame
            else:
                logger.debug(f"Failed to read capture frame, retrying ({i+1}/{self.num_trials_on_read_failure})...")

        raise RuntimeError("Failed to read capture frame.")
