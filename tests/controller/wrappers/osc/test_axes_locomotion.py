import pytest
from pytest_mock import MockerFixture

from vrchat_io.controller.wrappers.osc.axes_locomotion_wrapper import (
    RESET_VALUES,
    Axes,
    AxesLocomotionWrapper,
)
from vrchat_io.controller.wrappers.osc.multi_input_wrapper import MultiInputWrapper


def test_RESET_VALUES():
    assert RESET_VALUES == [0.0, 0.0, 0.0]


class TestAxesLocomotionWrapper:
    @pytest.fixture
    def mock_controller(self, mocker: MockerFixture) -> MultiInputWrapper:
        mock_controller = mocker.Mock(spec=MultiInputWrapper)
        return mock_controller

    @pytest.fixture
    def wrapper(self, mock_controller: MultiInputWrapper) -> AxesLocomotionWrapper:
        return AxesLocomotionWrapper(mock_controller)

    def test_init(self, wrapper: AxesLocomotionWrapper, mock_controller: MultiInputWrapper) -> None:
        assert wrapper._controller == mock_controller

    @pytest.mark.parametrize(
        ["vertical", "horizontal", "look_horizontal", "expected"],
        [
            [None, None, None, {}],
            [0.0, None, None, {Axes.Vertical: 0.0}],
            [None, 0.0, None, {Axes.Horizontal: 0.0}],
            [None, None, 0.0, {Axes.LookHorizontal: 0.0}],
            [0.0, 0.0, None, {Axes.Vertical: 0.0, Axes.Horizontal: 0.0}],
            [0.0, None, 0.0, {Axes.Vertical: 0.0, Axes.LookHorizontal: 0.0}],
            [None, 0.0, 0.0, {Axes.Horizontal: 0.0, Axes.LookHorizontal: 0.0}],
            [0.0, 0.0, 0.0, {Axes.Vertical: 0.0, Axes.Horizontal: 0.0, Axes.LookHorizontal: 0.0}],
        ],
    )
    def test_command(
        self,
        wrapper: AxesLocomotionWrapper,
        mock_controller: MultiInputWrapper,
        vertical: float,
        horizontal: float,
        look_horizontal: float,
        expected: dict[str, float],
    ) -> None:
        wrapper.command(vertical, horizontal, look_horizontal)
        mock_controller.command.assert_called_with(expected)
