"""This demo shows how to use OSC as input controller.

Script is,
1. Connect to VRChat.
2. Move forward for 1 second.
3. Move backward for 1 second in background.
4. Move right for 1 second.
5. Jump and turn left for 1 second.
6. Run forward for 3 second.
"""

import time

from pythonosc.udp_client import SimpleUDPClient

from vrchat_io.controller.osc import Axes, Buttons, InputController

# Connect to VRChat.
controller = InputController(
    SimpleUDPClient("127.0.0.1", 9000),
)

print("Move forward for 1 second.")
controller.command_and_reset(Axes.Vertical, 0.5, 0.0, 1.0)

print("Move backward for 1 second in background.")
controller.command_and_reset_background(Axes.Vertical, -1.0, 0.0, 1.0)

print("Move right for 1 second.")
controller.command_and_reset(Buttons.MoveRight, 1, 0, 1.0)

print("Jump and turn left for 1 second.")
controller.command(Buttons.Jump, 1)  # NOTE: You need to release the button.
time.sleep(1.0)
controller.command_and_reset(Axes.LookHorizontal, -1.0, 0.0, 1.0)
controller.command(Buttons.Jump, 0)  # Releasing.

print("Run forward for 1 second.")
controller.command(Buttons.Run, 1)
controller.command_and_reset(Buttons.MoveForward, 1, 0, 3.0)
controller.command(Buttons.Run, 0)  # Releasing.
