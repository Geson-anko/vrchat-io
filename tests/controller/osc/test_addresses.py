from vrchat_io.controller.osc import addresses
from vrchat_io.controller.osc.addresses import Axes, Buttons


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
