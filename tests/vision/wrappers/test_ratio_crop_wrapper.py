import numpy as np
import pytest
from pytest_mock import MockerFixture

from vrchat_io.abc.video_capture import VideoCapture
from vrchat_io.vision.wrappers import ratio_crop_wrapper
from vrchat_io.vision.wrappers.ratio_crop_wrapper import (
    AnchorMode,
    RatioCropWrapper,
    center_crop,
)

from ...abc.test_video_capture import VideoCaptureImpl


@pytest.fixture
def random_image():
    return np.random.randint(0, 256, 480 * 640 * 3, dtype=np.uint8).reshape((480, 640, 3))


def test_anchor_mode():
    assert AnchorMode.CENTER == "center"


class TestRatioCropWrapper:
    @pytest.mark.parametrize(
        ["ratio", "anchor"],
        [
            (1.0, AnchorMode.CENTER),
        ],
    )
    def test_init(self, ratio, anchor):
        video_capture = VideoCaptureImpl()
        wrapper = RatioCropWrapper(video_capture, 1.0, anchor=anchor)
        assert wrapper._video_capture is video_capture
        assert wrapper.ratio == ratio
        assert wrapper.anchor == anchor

    @pytest.mark.parametrize(
        ["ratio", "anchor"],
        [
            (1.0, AnchorMode.CENTER),
            (2.0, "not implemented"),
        ],
    )
    def test_process_frame(self, mocker: MockerFixture, ratio, anchor):
        video_capture = VideoCaptureImpl()
        wrapper = RatioCropWrapper(video_capture, 1.0, anchor=anchor)

        match anchor:
            case AnchorMode.CENTER:
                mock = mocker.patch.object(ratio_crop_wrapper, "center_crop")
                wrapper.read()
                mock.assert_called_once_with(video_capture.frame, ratio)
            case _:
                with pytest.raises(NotImplementedError):
                    wrapper.read()


@pytest.mark.parametrize(
    "ratio",
    [
        1.0,
        2.0,
        0.5,
    ],
)
def test_center_crop(random_image: np.ndarray, ratio: float):
    cropped = center_crop(random_image, ratio)
    height, width = cropped.shape[:2]
    assert width / height == pytest.approx(ratio)

    match ratio:
        case 1.0:
            assert cropped.shape == (480, 480, 3)
            np.testing.assert_equal(cropped, random_image[:, 80:-80])
        case 2.0:
            assert cropped.shape == (320, 640, 3)
            np.testing.assert_equal(cropped, random_image[80:-80, :])
        case 0.5:
            assert cropped.shape == (480, 240, 3)
            np.testing.assert_equal(cropped, random_image[:, 200:-200])
