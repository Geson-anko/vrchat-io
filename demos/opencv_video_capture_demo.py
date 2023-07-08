"""This demo show how to use OpenCVVideoCapture object."""
from time import perf_counter

import cv2

from vrchat_io.vision import OpenCVVideoCapture

cam = OpenCVVideoCapture(camera=cv2.VideoCapture(0), width=640, height=480, fps=30, bgr2rgb=False)

try:
    while True:
        start_time = perf_counter()
        frame = cam.read()

        cv2.imshow("OpenCV VideoCapture Demo", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        print(f"\rframe shape: {frame.shape}, fps: {1/(perf_counter() - start_time): .3f}", end="")

except KeyboardInterrupt:
    pass

cv2.destroyAllWindows()
