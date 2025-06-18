import os
import time
import numpy as np
from PIL import Image
import glob


class BaseCamera:
    def __init__(self):
        self.frame = None

    def run_threaded(self):
        return np.zeros((120, 160, 3), dtype=np.uint8)  # should be: return self.frame


class PiCamera(BaseCamera):
    def __init__(self, resolution=(120, 160), framerate=20):
        from picamera.array import PiRGBArray
        from picamera import PiCamera

        # Note: PiCamera expects (width, height), so we flip
        self.camera = PiCamera()
        self.camera.resolution = (resolution[1], resolution[0])
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        self.stream = self.camera.capture_continuous(
            self.rawCapture,
            format="rgb",
            use_video_port=True
        )

        self.frame = None
        self.on = True

        print('[INFO] PiCamera initialized, warming up...')
        time.sleep(2)

    def run(self):
        # Grabs one frame and returns it
        f = next(self.stream)
        frame = f.array
        self.rawCapture.truncate(0)
        return frame

    def update(self):
        # Continuously updates the latest frame
        for f in self.stream:
            self.frame = f.array
            self.rawCapture.truncate(0)

            if not self.on:
                break

    def shutdown(self):
        print('[INFO] Shutting down PiCamera...')
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()
        self.on = False
        time.sleep(0.5)
