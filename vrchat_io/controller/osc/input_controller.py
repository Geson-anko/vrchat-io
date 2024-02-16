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

    def __init__(self, client: SimpleUDPClient | tuple[str, int]) -> None:
        """Initialize InputController with UDPClient. (dependency injection.)

        Args:
            client (SimpleUDPClient | tuple[str, int]): UDPClient of python-osc or UDP address to connect.
        """
        if not isinstance(client, SimpleUDPClient):
            client = SimpleUDPClient(client[0], client[1])
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


RESET_VALUES = {
    Axes.Vertical: 0.0,
    Axes.Horizontal: 0.0,
    Axes.LookHorizontal: 0.0,
    Axes.UseAxisRight: 0.0,
    Axes.GrabAxisRight: 0.0,
    Axes.MoveHoldFB: 0.0,
    Axes.SpinHoldCwCcw: 0.0,
    Axes.SpinHoldUD: 0.0,
    Axes.SpinHoldLR: 0.0,
    Buttons.MoveForward: 0,
    Buttons.MoveBackward: 0,
    Buttons.MoveLeft: 0,
    Buttons.MoveRight: 0,
    Buttons.LookLeft: 0,
    Buttons.LookRight: 0,
    Buttons.Jump: 0,
    Buttons.Run: 0,
    Buttons.ComfortLeft: 0,
    Buttons.ComfortRight: 0,
    Buttons.DropRight: 0,
    Buttons.UseRight: 0,
    Buttons.GrabRight: 0,
    Buttons.DropLeft: 0,
    Buttons.UseLeft: 0,
    Buttons.GrabLeft: 0,
    Buttons.PanicButton: 0,
    Buttons.QuickMenuToggleLeft: 0,
    Buttons.QuickMenuToggleRight: 0,
    Buttons.Voice: 0,
}
