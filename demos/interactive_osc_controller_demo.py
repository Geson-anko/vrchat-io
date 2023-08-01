"""Interactive OSC controller demo.

How to control:
    - Move vertical: 'w' is forward, 's' is backward.
    - Move horizontal: 'a' is left, 'd' is right.
    - Look horizontal: 'o' is turn left, 'p' is turn right.

NOTE: Linux User
    You need to run this script as root user.
    Because keyboard module requires root user to access keyboard device.
    So run the following command in this directory.
    ```sh
    PYTHON_PATH=$(which python3) && sudo $PYTHON_PATH interactive_osc_controller_demo.py
    ```
"""
# -- Settings ---

vertical_speed = 1.0
horizontal_speed = 1.0
look_horizontal_speed = 1.0

# ---------------


import time

import keyboard  # Specified dependency for this demo.
from pythonosc.udp_client import SimpleUDPClient

from vrchat_io.controller.osc import InputController
from vrchat_io.controller.wrappers.osc import (
    AXES_LOCOMOTION_RESET_VALUES,
    AxesLocomotionWrapper,
    MultiInputWrapper,
)

# Controller setup.
controller = InputController(
    SimpleUDPClient("127.0.0.1", 9000),
)
controller = MultiInputWrapper(controller)
controller = AxesLocomotionWrapper(controller)

# Reset all axes.
controller.command(*AXES_LOCOMOTION_RESET_VALUES)

# Main loop.
try:
    while True:
        if keyboard.is_pressed("w"):
            vertical = vertical_speed
        elif keyboard.is_pressed("s"):
            vertical = -vertical_speed
        else:
            vertical = 0.0

        if keyboard.is_pressed("a"):
            horizontal = -horizontal_speed
        elif keyboard.is_pressed("d"):
            horizontal = horizontal_speed
        else:
            horizontal = 0.0

        if keyboard.is_pressed("o"):
            look = -look_horizontal_speed
        elif keyboard.is_pressed("p"):
            look = look_horizontal_speed
        else:
            look = 0.0

        controller.command(vertical, horizontal, look)
        print(f"\rvertical: {vertical}, horizontal: {horizontal}, look: {look}", end="")
        time.sleep(0.01)
except KeyboardInterrupt:
    pass
finally:
    # Reset all axes.
    controller.command(*AXES_LOCOMOTION_RESET_VALUES)
