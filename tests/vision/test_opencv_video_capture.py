import cv2
import numpy as np
import pytest
from pytest_mock import MockerFixture

from vrchat_io.vision.opencv_video_capture import OpenCVVideoCapture


class TestOpenCVVideoCapture:
    @pytest.fixture
    def mock_camera(self, mocker: MockerFixture):
        return mocker.MagicMock(spec=cv2.VideoCapture)

    def test_init(self, mock_camera):
        cam = OpenCVVideoCapture(mock_camera)
        assert cam.camera == mock_camera
        assert cam.expected_width == 640
        assert cam.expected_height == 480
        assert cam.expected_fps == 30
        assert cam.bgr2rgb is True
        assert cam.num_trials_on_read_failure == 10

    def test_configure_camera(self, mock_camera, mocker: MockerFixture):
        cam = OpenCVVideoCapture(mock_camera)
        cam.configure_camera()

        assert mocker.call(cv2.CAP_PROP_FRAME_WIDTH, cam.expected_width) in mock_camera.set.mock_calls
        assert mocker.call(cv2.CAP_PROP_FRAME_HEIGHT, cam.expected_height) in mock_camera.set.mock_calls
        assert mocker.call(cv2.CAP_PROP_FPS, cam.expected_fps) in mock_camera.set.mock_calls

    @pytest.mark.parametrize("width, height, fps", [(640, 480, 30), (1280, 720, 60)])
    def test_properties(self, mock_camera, width, height, fps):
        def mock_get(*args, **kwds):
            match args[0]:
                case cv2.CAP_PROP_FRAME_WIDTH:
                    return width
                case cv2.CAP_PROP_FRAME_HEIGHT:
                    return height
                case cv2.CAP_PROP_FPS:
                    return fps
                case _:
                    raise ValueError(f"Unexpected property: {args[0]}")

        mock_camera.get.side_effect = mock_get
        cam = OpenCVVideoCapture(mock_camera, width, height, fps)
        assert cam.width == width
        assert cam.height == height
        assert cam.fps == fps

    def test_read(self, mock_camera):
        frame = (np.random.rand(480, 640, 3) * 255).astype(np.uint8)
        mock_camera.read.return_value = (True, frame)
        cam = OpenCVVideoCapture(mock_camera, bgr2rgb=False)

        np.testing.assert_array_equal(cam.read(), frame)

    def test_read_failure(self, mock_camera):
        mock_camera.read.return_value = (False, None)
        cam = OpenCVVideoCapture(mock_camera)
        with pytest.raises(RuntimeError):
            cam.read()
