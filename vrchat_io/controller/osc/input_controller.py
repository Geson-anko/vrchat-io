"""This file contains a tool for sending OSC messages to VRChat.

See official docs: 
https://docs.vrchat.com/docs/osc-overview 
https://docs.vrchat.com/docs/osc-as-input-controller
"""
import logging
import threading
import time
from typing import Any

from pythonosc.udp_client import SimpleUDPClient

from ...abc.controller import Controller

logger = logging.getLogger(__name__)


class InputController(Controller):
    """OSC as Input Controller.

    All addresses (commands) are listed below.
    """

    def __init__(self, client: SimpleUDPClient) -> None:
        """Initialize InputController with UDPClient. (dependency injection.)

        Args:
            client (SimpleUDPClient): UDPClient of python-osc.
        """
        self.client = client

    def command(self, address: str, value: Any) -> None:
        """Send command to VRChat.

        Args:
            address (str): Address of command.
            value (Any): Sending value(s).
        """
        self.client.send_message(address, value)

    def command_and_reset(self, address: str, value: Any, reset_value: Any, duration: float) -> None:
        """Send command to VRChat and reset value after duration.

        Args:
            address (str): Address of command.
            value (Any): Sending value(s).
            reset_value (Any): Reset value(s).
            duration (float): Duration of sending value.
        """
        self.command(address, value)
        time.sleep(duration)
        self.command(address, reset_value)

    def _command_and_reset_with_error_catch(self, *args, **kwargs) -> Any:
        """Wrapper of `command_and_reset` method for catching errors."""
        try:
            return self.command_and_reset(*args, **kwargs)
        except Exception as e:
            logger.exception(e)

    def command_and_reset_background(self, *args, **kwargs) -> threading.Thread:
        """Background version of `command_and_reset` method. Arguments are same
        as `command_and_reset` method.

        Returns:
            threading.Thread: Thread of `command_and_reset` method.
        """
        task = threading.Thread(
            target=self._command_and_reset_with_error_catch,
            args=args,
            kwargs=kwargs,
        )
        task.start()
        return task


class Axes:
    Vertical = "/input/Vertical"
    Horizontal = "/input/Horizontal"
    LookHorizontal = "/input/LookHorizontal"
    UseAxisRight = "/input/UseAxisRight"
    GrabAxisRight = "/input/GrabAxisRight"
    MoveHoldFB = "/input/MoveHoldFB"
    SpinHoldCwCcw = "/input/SpinHoldCwCcw"
    SpinHoldUD = "/input/SpinHoldUD"
    SpinHoldLR = "/input/SpinHoldLR"


class Buttons:
    MoveForward = "/input/MoveForward"
    MoveBackward = "/input/MoveBackward"
    MoveLeft = "/input/MoveLeft"
    MoveRight = "/input/MoveRight"
    LookLeft = "/input/LookLeft"
    LookRight = "/input/LookRight"
    Jump = "/input/Jump"
    Run = "/input/Run"
    ComfortLeft = "/input/ComfortLeft"
    ComfortRight = "/input/ComfortRight"
    DropRight = "/input/DropRight"
    UseRight = "/input/UseRight"
    GrabRight = "/input/GrabRight"
    DropLeft = "/input/DropLeft"
    UseLeft = "/input/UseLeft"
    GrabLeft = "/input/GrabLeft"
    PanicButton = "/input/PanicButton"
    QuickMenuToggleLeft = "/input/QuickMenuToggleLeft"
    QuickMenuToggleRight = "/input/QuickMenuToggleRight"
    Voice = "/input/Voice"
