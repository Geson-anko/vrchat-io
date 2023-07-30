import pytest

from vrchat_io.abc.controller import Controller, ControllerWrapper


class ControllerImpl(Controller):
    def command(self, *args, **kwds) -> None:
        return None


class TestController:
    def test_instantiation(self):
        ControllerImpl()

    def test_error_of_abstract_class_instantiation(self):
        with pytest.raises(TypeError):
            Controller()


class ControllerWrapperImpl(ControllerWrapper):
    def command(self, *args, **kwds) -> None:
        return None


class TestControllerWrapper:
    def test_instantiation(self):
        controller = ControllerImpl()
        wrapper = ControllerWrapperImpl(controller)
        assert wrapper._controller is controller

    def test_subclass(self):
        assert issubclass(ControllerWrapper, Controller)
