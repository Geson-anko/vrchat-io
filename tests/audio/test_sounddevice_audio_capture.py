from unittest.mock import Mock

import numpy as np
import pytest
import sounddevice as sd
from pytest_mock import MockerFixture

from vrchat_io.audio.sounddevice_audio_capture import SounddeviceAudioCapture


class TestSounddeviceAudioCapture:
    @pytest.fixture
    def mock_stream(self):
        """Creates a mock InputStream object."""
        stream = Mock(spec=sd.InputStream)
        return stream

    @pytest.fixture
    def mock_sounddevice(self, mocker: MockerFixture, mock_stream):
        """Mocks the sounddevice module and returns the mocked InputStream."""
        mock_sd = mocker.patch("vrchat_io.audio.sounddevice_audio_capture.sd")
        mock_sd.InputStream.return_value = mock_stream
        return mock_sd

    @pytest.mark.parametrize(
        "params",
        [
            # samplerate, device, frame_size, channels, latency
            (None, None, 1024, 1, None),
            (44100, "test_device", 2048, 2, "low"),
            (48000, 1, 512, 4, "high"),
        ],
    )
    def test_init(self, mock_sounddevice, mock_stream, params):
        """Tests the initialization of SounddeviceAudioCapture with various
        parameters."""
        samplerate, device, frame_size, channels, latency = params

        capture = SounddeviceAudioCapture(
            samplerate=samplerate,
            device=device,
            frame_size=frame_size,
            channels=channels,
            latency=latency,
        )

        mock_sounddevice.InputStream.assert_called_once_with(
            samplerate=samplerate,
            device=device,
            latency=latency,
            channels=channels,
            dtype=np.float32,
        )
        mock_stream.start.assert_called_once()

    @pytest.mark.parametrize("overflow", [True, False])
    def test_read(self, mock_sounddevice, mock_stream, overflow):
        """Tests the read method with and without overflow."""
        test_frames = np.random.rand(1024, 1).astype(np.float32)
        mock_stream.read.return_value = (test_frames, overflow)

        capture = SounddeviceAudioCapture(frame_size=1024)
        result = capture.read()

        mock_stream.read.assert_called_once_with(1024)
        np.testing.assert_array_equal(result, test_frames)

    def test_cleanup(self, mock_sounddevice, mock_stream):
        """Tests the cleanup process when the object is destroyed."""
        capture = SounddeviceAudioCapture()
        capture.__del__()

        mock_stream.stop.assert_called_once()
        mock_stream.close.assert_called_once()

    @pytest.mark.parametrize("frame_size", [512, 1024, 2048])
    def test_different_frame_sizes(self, mock_sounddevice, mock_stream, frame_size):
        """Tests that different frame sizes are handled correctly."""
        test_frames = np.random.rand(frame_size, 1).astype(np.float32)
        mock_stream.read.return_value = (test_frames, False)

        capture = SounddeviceAudioCapture(frame_size=frame_size)
        result = capture.read()

        mock_stream.read.assert_called_once_with(frame_size)
        assert result.shape[0] == frame_size
        assert result.dtype == np.float32

    @pytest.mark.parametrize("channels", [1, 2, 4])
    def test_different_channel_counts(self, mock_sounddevice, mock_stream, channels):
        """Tests that different channel counts are handled correctly."""
        capture = SounddeviceAudioCapture(channels=channels)

        mock_sounddevice.InputStream.assert_called_once_with(
            samplerate=None,
            device=None,
            latency=None,
            channels=channels,
            dtype=np.float32,
        )

        test_frames = np.random.rand(1024, channels).astype(np.float32)
        mock_stream.read.return_value = (test_frames, False)

        result = capture.read()
        assert result.shape[1] == channels
