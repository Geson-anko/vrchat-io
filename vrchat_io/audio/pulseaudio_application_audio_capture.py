import shutil
import subprocess
import time

import numpy as np
import numpy.typing as npt

from ..abc.audio_capture import ApplicationAudioCapture


class PulseAudioApplicationAudioCapture(ApplicationAudioCapture):
    """"""

    def __init__(
        self,
        target_application: str,
        frame_size: int = 1024,
        sample_rate: float = 44100,
        channels: int = 2,
    ) -> None:
        """"""
        assert shutil.which("parecord") is not None, "PulseAudio record command `parecord` is not available"
        super().__init__(target_application)
        self.frame_size = frame_size
        self.sample_rate = sample_rate
        self.channels = channels
        self.process: subprocess.Popen | None = None
        self._buffer = bytearray()

    def read(self) -> npt.NDArray[np.float32]:
        """"""
        if self.process is None:
            self.open()
        while len(self._buffer) < self.bytes_to_read:
            self._buffer += self.process.stdout.read(self.bytes_to_read)
            time.sleep(self.frame_size / self.sample_rate * 0.1)
        frames = np.frombuffer(self._buffer[: self.bytes_to_read], dtype=np.float32).reshape(
            self.frame_size, self.channels
        )
        self._buffer = self._buffer[self.bytes_to_read :]
        return frames

    @property
    def bytes_to_read(self) -> int:
        return self.frame_size * self.channels * 4  # float32 = 4 bytes

    def open(self) -> None:
        """"""
        # fmt: off
        cmd = [
            "parecord",
            "--channels", str(self.channels),
            "--rate", str(self.sample_rate),
            "--format", "float32le",
            "-n", self.target_application,
            "--raw",  # Output raw audio data
            "--latency-msec=50",  # Low latency
            # Output to stdout
        ]
        # fmt: on
        self.process = subprocess.Popen(
            args=cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def close(self) -> None:
        """"""
        if self.process is not None:
            self.process.terminate()
            self.process.wait()
            self.process = None

    def __del__(self) -> None:
        """"""
        self.close()
