import numpy as np
import pytest
from pytest_mock import MockerFixture

from vrchat_io.abc.video_capture import VideoCapture, VideoCaptureWrapper


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


class VideoCaptureWrapperImpl(VideoCaptureWrapper):
    def after_read(self, frame: np.ndarray) -> np.ndarray:
        return frame


class TestVideoCaptureWrapper:
    def test_instantiation(self):
        VideoCaptureWrapperImpl(VideoCaptureImpl())

    def test_call_after_read(self, mocker: MockerFixture):
        video_capture_wrapper = VideoCaptureWrapperImpl(VideoCaptureImpl())

        meth = mocker.spy(video_capture_wrapper, "after_read")
        frame = video_capture_wrapper.read()
        meth.assert_called_once_with(frame)

    def test_error_of_abstract_class_instantiation(self):
        video_capture = VideoCaptureImpl()
        with pytest.raises(TypeError):
            VideoCaptureWrapper(video_capture)
