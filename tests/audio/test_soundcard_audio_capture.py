from unittest.mock import MagicMock, Mock

import numpy as np
import pytest
from pytest_mock import MockerFixture

from vrchat_io.audio.soundcard_audio_capture import SoundcardAudioCapture


class TestSoundcardAudioCapture:
    @pytest.fixture
    def mock_microphone(self):
        """Creates a mock Microphone object."""
        mic = Mock()
        recorder = MagicMock()
        mic.recorder.return_value = recorder
        return mic

    @pytest.fixture
    def mock_soundcard(self, mocker: MockerFixture, mock_microphone):
        """Mocks the soundcard module and returns the mock setup."""
        mock_sc = mocker.patch("vrchat_io.audio.soundcard_audio_capture.sc")
        mock_sc.default_microphone.return_value = mock_microphone
        mock_sc.get_microphone.return_value = mock_microphone
        return mock_sc, mock_microphone

    def test_init_default_device(self, mock_soundcard):
        """Tests initialization with default device."""
        mock_sc, mock_mic = mock_soundcard

        capture = SoundcardAudioCapture(samplerate=44100, frame_size=1024, blocksize=512, channels=1)

        mock_sc.default_microphone.assert_called_once()
        mock_mic.recorder.assert_called_once_with(samplerate=44100, channels=1, blocksize=512)

    def test_init_specific_device(self, mock_soundcard):
        """Tests initialization with specific device."""
        mock_sc, mock_mic = mock_soundcard
        mock_mic.name = "test_device"

        capture = SoundcardAudioCapture(device_id="test_device", samplerate=44100, frame_size=1024, channels=1)

        mock_sc.get_microphone.assert_called_once_with("test_device", include_loopback=True)
        mock_mic.recorder.assert_called_once()
