import pytest

from vrchat_io.vision.wrappers.resize_wrapper import ResizeWrapper

from ...abc.test_video_capture import VideoCaptureImpl


class TestResizeWrapper:
    @pytest.fixture
    def wrapper(self):
        return ResizeWrapper(VideoCaptureImpl(), (120, 160))

    def test_init(self, wrapper: ResizeWrapper):
        assert wrapper.size == (120, 160)

    def test_process_frame(self, wrapper: ResizeWrapper):
        frame = wrapper.read()
        assert frame.shape == (160, 120, 3)
