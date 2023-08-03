"""this file contains a wrapper class for sending multiple commands at once."""

from typing import Any

from ....abc.controller import ControllerWrapper
from ...osc.input_controller import RESET_VALUES, InputController


class MultiInputWrapper(ControllerWrapper):
    """Sending multiple commands at once.

    How to use:
    ```python
    controller = MultiInputWrapper(InputController(client))
    controller.command({
        address1: value1,
        address2: value2,
        ...
    })
    ```
    """

    _controller: InputController

    def __init__(self, controller: InputController) -> None:
        """Initialize MultiInputWrapper with InputController.

        Args:
            controller (InputController): OSC InputController or its subclass.
        """
        super().__init__(controller)

    def command(self, actions: dict[str, Any]) -> None:
        """Send multiple commands to VRChat.

        Args:
            actions (dict[str, Any]): Multiple action dictionary. `{address: value}`.

        NOTE: If resetting all actions, use `vrchat_io.controller.osc.RESET_VALUES`.
        """

        for address, value in actions.items():
            self._controller.command(address, value)
