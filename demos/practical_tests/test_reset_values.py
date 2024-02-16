import time

from vrchat_io.controller.osc.input_controller import RESET_VALUES, InputController

# Connect to VRChat.
controller = InputController(
    ("127.0.0.1", 9000),
)

for addr, val in RESET_VALUES.items():
    print(f"Setting {addr} to 1.0.")
    controller.command(addr, 1)
    time.sleep(0.2)

for addr, val in RESET_VALUES.items():
    print(f"Resetting {addr} to {val}")
    controller.command(addr, val)
    time.sleep(0.2)
