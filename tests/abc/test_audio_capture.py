import numpy as np
import numpy.typing as npt
import pytest

from vrchat_io.abc.audio_capture import ApplicationAudioCapture, AudioCapture


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


class ApplicationAudioCaptureImpl(ApplicationAudioCapture):
    def __init__(self, target_application: str) -> None:
        super().__init__(target_application)
        self.frames = np.zeros((2048, 2), dtype=np.float32)

    def read(self) -> npt.NDArray[np.float32]:
        return self.frames


class TestApplicationAudioCapture:
    def test_instantiation(self):
        cap = ApplicationAudioCaptureImpl("some app")
        assert cap.target_application == "some app"
        cap.read()

    def test_error_of_abstract_class_instantiation(self):
        class NoInit(ApplicationAudioCapture):
            def read(self) -> npt.NDArray[np.float32]:
                return np.zeros((2048, 2), dtype=np.float32)

        with pytest.raises(TypeError):
            NoInit()
