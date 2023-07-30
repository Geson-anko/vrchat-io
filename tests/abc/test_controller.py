import pytest

from vrchat_io.abc.controller import Controller


class ControllerImpl(Controller):
    def command(self, *args, **kwds) -> None:
        return None


class TestController:
    def test_instantiation(self):
        ControllerImpl()

    def test_error_of_abstract_class_instantiation(self):
        with pytest.raises(TypeError):
            Controller()
