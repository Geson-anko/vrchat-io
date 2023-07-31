"""This file contains a wrapper class for sending locomotion commands of Axes
to VRChat."""
from typing import Optional

from ....abc.controller import ControllerWrapper
from ...osc.input_controller import Axes
from .multi_input_wrapper import MultiInputWrapper

AXES_LOCOMOTION_RESET_VALUES = [0.0, 0.0, 0.0]  # vertical, horizontal, look_horizontal


class AxesLocomotionWrapper(MultiInputWrapper):
    """Send only locomotion commands of Axes to VRChat.

    This wrapper can wrap MultiInputWrapper or its subclass only.
    because sending multiple commands at once.
    """

    _controller: MultiInputWrapper

    def __init__(self, controller: MultiInputWrapper) -> None:
        """Initialize AxesLocomotionWrapper with MultiInputWrapper.

        Args:
            controller (MultiInputWrapper): MultiInputWrapper or its subclass.
        """
        super().__init__(controller)

    def command(
        self,
        vertical: Optional[float] = None,
        horizontal: Optional[float] = None,
        look_horizontal: Optional[float] = None,
    ) -> None:
        """Send locomotion commands of Axes to VRChat. Default arguments are
        `None`, so sending only the items to be manipulated.

        NOTE: If you want to reset, use `command(*AXES_LOCOMOTION_RESET_VALUES)`.

        Args:
            vertical (Optional[float]): move forward or backward.
            horizontal (Optional[float]): move left or right.
            look_horizontal (Optional[float]): turn left or right.
        """
        actions = {}
        if vertical is not None:
            actions[Axes.Vertical] = vertical
        if horizontal is not None:
            actions[Axes.Horizontal] = horizontal
        if look_horizontal is not None:
            actions[Axes.LookHorizontal] = look_horizontal

        self._controller.command(actions)
