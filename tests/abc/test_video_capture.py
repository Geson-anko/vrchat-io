import numpy as np
import pytest
from pytest_mock import MockerFixture

from vrchat_io.abc.video_capture import FrameWrapper, VideoCapture, VideoCaptureWrapper


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
    def read(self) -> np.ndarray:
        return self._video_capture.read()


class TestVideoCaptureWrapper:
    def test_instantiation(self):
        cap = VideoCaptureImpl()
        wrapper = VideoCaptureWrapperImpl(cap)
        assert wrapper._video_capture is cap

    def test_subclass(self):
        assert issubclass(VideoCaptureWrapper, VideoCapture)


class FrameWrapperImpl(FrameWrapper):
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        return frame


class TestFrameWrapper:
    def test_instantiation(self):
        FrameWrapperImpl(VideoCaptureImpl())

    def test_call_process_frame(self, mocker: MockerFixture):
        video_capture_wrapper = FrameWrapperImpl(VideoCaptureImpl())

        meth = mocker.spy(video_capture_wrapper, "process_frame")
        frame = video_capture_wrapper.read()
        meth.assert_called_once_with(frame)

    def test_error_of_abstract_class_instantiation(self):
        video_capture = VideoCaptureImpl()
        with pytest.raises(TypeError):
            FrameWrapper(video_capture)
