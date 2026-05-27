import cv2
import numpy as np
from config import FRAME_CENTER_X, FRAME_CENTER_Y


class VisionSystem:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.detector = cv2.QRCodeDetector()

    def get_frame(self):
        ret, frame = self.cap.read()

        if not ret:
            return None

        return frame

    def detect_qr(self, frame):
        data, points, _ = self.detector.detectAndDecode(frame)

        if points is None:
            return None

        points = points[0]

        center_x = int(np.mean(points[:, 0]))
        center_y = int(np.mean(points[:, 1]))

        error_x = center_x - FRAME_CENTER_X
        error_y = center_y - FRAME_CENTER_Y

        return {
            "data": data,
            "center_x": center_x,
            "center_y": center_y,
            "error_x": error_x,
            "error_y": error_y,
            "points": points
        }

    def release(self):
        self.cap.release()
