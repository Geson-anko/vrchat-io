import numpy as np
import pytest

from vrchat_io.abc.video_capture import VideoCapture


class VideoCaptureImpl(VideoCapture):
    def __init__(self) -> None:
        self.frame = np.zeros((480, 640, 3), dtype=np.uint8)

    def read(self) -> np.ndarray:
        return self.frame


class TestVideoCapture:
    def test_instantiation(self):
        video_capture = VideoCaptureImpl()
        video_capture.read()

    def test_error_of_abstract_class_instantiation(self):
        with pytest.raises(TypeError):
            VideoCapture()
