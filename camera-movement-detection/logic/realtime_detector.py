import cv2
import time
import numpy as np
import threading
from streamlit_webrtc import VideoTransformerBase
from utils.send_mail import send_alert_email
from utils.log_utils import log_event
from utils.notify import notify_camera_movement, notify_email_sent

class OpticalFlowDetector(VideoTransformerBase):
    sensitivity = 1.0
    variance_limit = 1.0

    @classmethod
    def set_params(cls, sens, var):
        cls.sensitivity = sens
        cls.variance_limit = var

    def __init__(self):
        self.prev_gray = None
        self.last_sent_time = time.time() - 61

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        current_time = time.time()

        if self.prev_gray is not None:
            flow = cv2.calcOpticalFlowFarneback(
                self.prev_gray, gray, None,
                0.5, 3, 15, 3, 5, 1.2, 0
            )
            dx = flow[..., 0]
            dy = flow[..., 1]
            magnitude = np.sqrt(dx**2 + dy**2)

            mean_shift = np.mean(magnitude)
            variance = np.var(magnitude)

            if mean_shift > self.sensitivity and variance < self.variance_limit:
                notify_camera_movement()
                cv2.putText(img, "Camera Movement Detected!", (30, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                if current_time - self.last_sent_time > 60:
                    log_event("Hareket algılandı, e-posta gönderiliyor...")
                    threading.Thread(target=send_alert_email).start()
                    self.last_sent_time = current_time

        self.prev_gray = gray
        return img