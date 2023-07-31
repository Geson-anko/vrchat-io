from unittest.mock import call

import pytest
from pytest_mock import MockerFixture

from vrchat_io.controller.osc import InputController
from vrchat_io.controller.wrappers.osc.multi_input_wrapper import MultiInputWrapper


class TestMultiInputWrapper:
    @pytest.fixture
    def controller(self, mocker: MockerFixture) -> InputController:
        return mocker.Mock(InputController)

    @pytest.fixture
    def wrapped(self, mocker: MockerFixture, controller: InputController) -> MultiInputWrapper:
        return MultiInputWrapper(controller)

    def test_init(self, controller: InputController, wrapped: MultiInputWrapper):

        assert wrapped._controller is controller

    def test_command(self, mocker: MockerFixture, controller: InputController, wrapped: MultiInputWrapper):
        actions = {
            "address1": 1.0,
            "address2": 2,
        }

        cmd_meth = mocker.spy(controller, "command")
        wrapped.command(actions)

        args_list = cmd_meth.call_args_list
        for idx, (addr, val) in enumerate(actions.items()):
            assert args_list[idx] == call(addr, val)
