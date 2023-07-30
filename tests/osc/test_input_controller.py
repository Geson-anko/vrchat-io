import threading

import pytest
from pytest_mock import MockerFixture

from vrchat_io.abc.controller import Controller
from vrchat_io.osc.input_controller import InputController


class TestInputController:
    @pytest.fixture
    def controller(self, osc_client):
        return InputController(osc_client)

    def test_inheritance(self):
        assert issubclass(InputController, Controller)

    def test_init(self, osc_client, controller: InputController):
        assert controller.client == osc_client

    def test_command(self, osc_client, controller: InputController):
        address = "/test/address"
        value = "value"

        controller.command(address, value)

        osc_client.send_message.assert_called_once_with(address, value)

    def test_command_and_reset(self, osc_client, controller: InputController, mocker: MockerFixture):
        address = "/test/address"
        value = "test_value"
        reset_value = "reset_value"
        duration = 1

        sleep_mocker = mocker.patch("time.sleep")
        controller.command_and_reset(address, value, reset_value, duration)

        assert osc_client.send_message.call_args_list[0].args == (
            address,
            value,
        )
        sleep_mocker.assert_called_once_with(duration)
        assert osc_client.send_message.call_args_list[1].args == (
            address,
            reset_value,
        )

    # Sanity check of `_command_and_reset_with_error_catch`
    def test__command_and_reset(self, controller: InputController, mocker: MockerFixture):
        args = ("/test/address", "test_value", "reset_value", 1.0)

        command_and_reset_mocker = mocker.patch.object(controller, "command_and_reset")
        controller._command_and_reset_with_error_catch(*args)

        command_and_reset_mocker.assert_called_once_with(*args)

    # Check if `_command_and_reset_with_error_catch` catches error
    def test__command_and_reset_with_error(self, controller: InputController, mocker: MockerFixture):
        args = ("/test/address", "test_value", "reset_value", 1.0)

        command_and_reset_mocker = mocker.patch.object(controller, "command_and_reset")
        command_and_reset_mocker.side_effect = Exception("test error")
        logger_mocker = mocker.patch("vrchat_io.osc.input_controller.logger.exception")

        controller._command_and_reset_with_error_catch(*args)

        command_and_reset_mocker.assert_called_once_with(*args)
        logger_mocker.assert_called_once()

    def test_command_and_reset_background(self, controller: InputController, mocker: MockerFixture):
        args = ("address", "value", "reset_value", 1.0)
        mock = mocker.patch.object(controller, "_command_and_reset_with_error_catch")
        thread = controller.command_and_reset_background(*args)
        assert isinstance(thread, threading.Thread)
        thread.join()
        mock.assert_called_once_with(*args)
