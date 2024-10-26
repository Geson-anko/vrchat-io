import numpy as np
import numpy.typing as npt
import pytest

from vrchat_io.abc.audio_capture import AudioCapture


class AudioCaptureImpl(AudioCapture):
    def __init__(self) -> None:
        self.frames = np.zeros((2048, 2), dtype=np.float32)

    def read(self) -> npt.NDArray[np.float32]:
        return self.frames


class TestAudioCapture:
    def test_instantiation(self):
        cap = AudioCaptureImpl()
        cap.read()

    def test_error_of_abstract_class_instantiation(self):
        with pytest.raises(TypeError):
            AudioCapture()
