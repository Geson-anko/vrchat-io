import threading

import pytest
from pytest_mock import MockerFixture

from vrchat_io.abc.controller import Controller
from vrchat_io.controller.osc.input_controller import (
    RESET_VALUES,
    Axes,
    Buttons,
    InputController,
    logger,
)


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
        logger_mocker = mocker.patch.object(logger, "exception")

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


def test_Axes():
    assert Axes.Vertical == "/input/Vertical"
    assert Axes.Horizontal == "/input/Horizontal"
    assert Axes.LookHorizontal == "/input/LookHorizontal"
    assert Axes.UseAxisRight == "/input/UseAxisRight"
    assert Axes.GrabAxisRight == "/input/GrabAxisRight"
    assert Axes.MoveHoldFB == "/input/MoveHoldFB"
    assert Axes.SpinHoldCwCcw == "/input/SpinHoldCwCcw"
    assert Axes.SpinHoldUD == "/input/SpinHoldUD"
    assert Axes.SpinHoldLR == "/input/SpinHoldLR"


def test_Buttons():
    assert Buttons.MoveForward == "/input/MoveForward"
    assert Buttons.MoveBackward == "/input/MoveBackward"
    assert Buttons.MoveLeft == "/input/MoveLeft"
    assert Buttons.MoveRight == "/input/MoveRight"
    assert Buttons.LookLeft == "/input/LookLeft"
    assert Buttons.LookRight == "/input/LookRight"
    assert Buttons.Jump == "/input/Jump"
    assert Buttons.Run == "/input/Run"
    assert Buttons.ComfortLeft == "/input/ComfortLeft"
    assert Buttons.ComfortRight == "/input/ComfortRight"
    assert Buttons.DropRight == "/input/DropRight"
    assert Buttons.UseRight == "/input/UseRight"
    assert Buttons.GrabRight == "/input/GrabRight"
    assert Buttons.DropLeft == "/input/DropLeft"
    assert Buttons.UseLeft == "/input/UseLeft"
    assert Buttons.GrabLeft == "/input/GrabLeft"
    assert Buttons.PanicButton == "/input/PanicButton"
    assert Buttons.QuickMenuToggleLeft == "/input/QuickMenuToggleLeft"
    assert Buttons.QuickMenuToggleRight == "/input/QuickMenuToggleRight"
    assert Buttons.Voice == "/input/Voice"


def test_RESET_VALUES():
    assert RESET_VALUES[Axes.Vertical] == 0.0
    assert RESET_VALUES[Axes.Horizontal] == 0.0
    assert RESET_VALUES[Axes.LookHorizontal] == 0.0
    assert RESET_VALUES[Axes.UseAxisRight] == 0.0
    assert RESET_VALUES[Axes.GrabAxisRight] == 0.0
    assert RESET_VALUES[Axes.MoveHoldFB] == 0.0
    assert RESET_VALUES[Axes.SpinHoldCwCcw] == 0.0
    assert RESET_VALUES[Axes.SpinHoldUD] == 0.0
    assert RESET_VALUES[Axes.SpinHoldLR] == 0.0
    assert RESET_VALUES[Buttons.MoveForward] == 0
    assert RESET_VALUES[Buttons.MoveBackward] == 0
    assert RESET_VALUES[Buttons.MoveLeft] == 0
    assert RESET_VALUES[Buttons.MoveRight] == 0
    assert RESET_VALUES[Buttons.LookLeft] == 0
    assert RESET_VALUES[Buttons.LookRight] == 0
    assert RESET_VALUES[Buttons.Jump] == 0
    assert RESET_VALUES[Buttons.Run] == 0
    assert RESET_VALUES[Buttons.ComfortLeft] == 0
    assert RESET_VALUES[Buttons.ComfortRight] == 0
    assert RESET_VALUES[Buttons.DropRight] == 0
    assert RESET_VALUES[Buttons.UseRight] == 0
    assert RESET_VALUES[Buttons.GrabRight] == 0
    assert RESET_VALUES[Buttons.DropLeft] == 0
    assert RESET_VALUES[Buttons.UseLeft] == 0
    assert RESET_VALUES[Buttons.GrabLeft] == 0
    assert RESET_VALUES[Buttons.PanicButton] == 0
    assert RESET_VALUES[Buttons.QuickMenuToggleLeft] == 0
    assert RESET_VALUES[Buttons.QuickMenuToggleRight] == 0
    assert RESET_VALUES[Buttons.Voice] == 0
