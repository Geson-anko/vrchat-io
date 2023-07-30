"""This file contains abstract controller class and its base wrapper class."""
from abc import ABC, abstractmethod
from typing import Any


class Controller(ABC):
    """Abstract Controller Class.

    This class is the abstract class for controlling, sending commands
    to the VRChat. If you want to add a new controller type, you should
    inherit this class and implement the :meth:`command` method.
    """

    @abstractmethod
    def command(self, *args: Any, **kwds: Any) -> None:
        """Send a command to the VRChat."""
        pass


class ControllerWrapper(Controller):
    """The Base Wrapper Class for Controller.

    You can access base controller object by ``self._controller``.
    """

    def __init__(self, controller: Controller, *args: Any, **kwds: Any) -> None:
        """Initialize the controller wrapper.

        Args:
            controller (Controller): The controller to be wrapped.
        """
        self._controller = controller
