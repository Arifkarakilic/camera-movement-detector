import os
import cv2
import numpy as np
import tempfile
import time
import threading
import streamlit as st
from PIL import Image
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

from detectors.movement_detector import detect_camera_movement
from detectors.movement_detector_affine import detect_camera_movement_affine
from detectors.movement_detector_optical import detect_camera_movement_optical
from send_mail import send_alert_email

st.set_page_config(layout="wide")
st.title(" Camera Movement Detection By Arif Karakılıç")

mode = st.radio(" Mod Seç", [" Video / Frame Analizi", " Gerçek Zamanlı Takip"])

#  GERÇEK ZAMANLI MOD
if mode == " Gerçek Zamanlı Takip":
    sensitivity = st.slider(" Ortalama Flow Büyüklüğü", 0.1, 5.0, 0.4, 0.1)
    variance_limit = st.slider(" Maksimum Varyans", 0.1, 3.0, 2.1, 0.1)

    class OpticalFlowDetector(VideoTransformerBase):
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

                if mean_shift > sensitivity and variance < variance_limit:
                    cv2.putText(img, "Camera Movement Detected!", (30, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
                    if(current_time - self.last_sent_time > 60):
                        print("Hareket algılandı, e-posta gönderiliyor.......")
                        alert = threading.Thread(target=send_alert_email)
                        alert.start()
                        self.last_sent_time = current_time
                        alert.join()

            self.prev_gray = gray
            return img



    st.header(" Anlık Kamera Hareketi Takibi")
    st.markdown(
        "Kameranız açıkken cihaz sabit değilse bu ekranda **'Camera Movement Detected!'** uyarısı görünecektir. "
        "Sağ üstteki eşik değeri ile hassasiyeti ayarlayabilirsiniz."
    )
    with st.expander("ℹ️ Parametre Açıklamaları"):
        st.markdown("""
        ** Ortalama Flow Büyüklüğü**  
        - Piksel başına düşen ortalama hareket miktarıdır.  
        - Kamera oynarsa tüm sahnede belirgin artış olur.

        ** Varyans Limiti**  
        - Hareketin sahneye yayılma derecesi.  
        - Kamera oynarsa varyans düşer (her yer oynar).  
        - Obje oynarsa varyans artar (tek bölgede değişim olur).

        **  *Önerilen Ayarlar:**
        | Durum                  | Mean Flow | Varyans Limit |
        |------------------------|-----------|----------------|
        | Dengeli & güvenilir   | `1.2`     | `0.8`          |
        | Daha hassas           | `0.4`     | `2.1`          |
        | Daha seçici (kamera)  | `1.5`     | `0.5`          |
        """)
    webrtc_streamer(key="realtime", video_processor_factory=OpticalFlowDetector)

#  VİDEO / FRAME ANALİZİ MODU
else:
    method = st.radio(" Algoritma Seç", [
        "ORB (Homografi)",
        "Optical Flow",
        "Affine (GoodFeatures + RANSAC)"
    ])

    if method == "ORB (Homografi)":
        threshold = st.slider(" Translationsal Shift Eşiği (px)", 1, 100, 50, 1)
        min_matches = st.slider("🔹 Minimum Eşleşme Sayısı", 5, 100, 10, 1)
        st.info("Eşik değer kameranın kaymasını, eşleşme sayısı benzerlik güvenini ifade eder.\n\n"
                "Returns:\n"
                "    List[int]: Kamera hareketi algılanan kare indexleri"
                )
    elif method == "Optical Flow":
        threshold = st.slider(" Ortalama Flow Büyüklüğü (px)", 0.1, 5.0, 1.2, 0.1)
        variance_limit = st.slider(" Varyans Limiti", 0.1, 3.0, 0.8, 0.1)
        st.info(
                "Optical flow ile sadece kamera hareketini algılar.\n"
                "Nesne hareketlerini varyans analizi ile filtreler.\n\n"
                "Args:\n"
                "    frame_dir (str): Frame dizini\n"
                "    threshold (float): Ortalama hareket eşiği\n"
                "    variance_limit (float): Hareket yayılımı varyans sınırı\n\n"
                "Returns:\n"
                "    List[int]: Kamera hareketi algılanan kare indexleri"
                )

    else:
        threshold = st.slider(" Affine Model Kayma Eşiği (px)", 0.5, 10.0, 2.0, 0.5)
        min_features = st.slider("🔹 Minimum Feature Sayısı", 10, 500, 100, 10)
        st.info(
                "Affine model ile kamera hareketini tespit eder.\n"
                "Sahnede hareket eden objeleri filtreler.\n\n"
                "Args:\n"
                "    frame_dir (str): Kare klasörü\n"
                "    threshold (float): Ortalama transform vektör şiddeti\n"
                "    min_features (int): Minimum izlenecek nokta sayısı\n\n"
                "Returns:\n"
                "    List[int]: Kamera hareketi algılanan frame indexleri"
            )


    uploaded_file = st.file_uploader(" Video veya GIF Yükle (.mp4 / .gif)", type=["mp4", "gif"])
    frame_root = "frames"
    os.makedirs(frame_root, exist_ok=True)
    available_dirs = [os.path.join(frame_root, d) for d in os.listdir(frame_root) if d.startswith("frames_video_")]
    selected_dir = st.radio(" Hazır Frame Klasörü Seç", available_dirs, index=0 if available_dirs else None)

    def extract_frames(video_path, output_dir, progress_placeholder):
        os.makedirs(output_dir, exist_ok=True)
        cap = cv2.VideoCapture(video_path)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        i = 0
        progress = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imwrite(os.path.join(output_dir, f"frame_{i:03d}.jpg"), frame)
            i += 1
            new_progress = int((i / total) * 100)
            if new_progress > progress:
                progress = new_progress
                progress_placeholder.progress(min(progress, 100))
        cap.release()
        return i

    def run_detection(frame_dir):
        if method == "ORB (Homografi)":
            return detect_camera_movement(frame_dir, threshold, min_matches)
        elif method == "Optical Flow":
            return detect_camera_movement_optical(frame_dir, threshold, variance_limit)
        else:
            return detect_camera_movement_affine(frame_dir, threshold, min_features)

    temp_dir = None
    if uploaded_file is not None:
        with st.spinner("🎞 Video karelere ayrılıyor..."):
            temp_dir = tempfile.mkdtemp()
            video_path = os.path.join(temp_dir, uploaded_file.name)
            with open(video_path, "wb") as f:
                f.write(uploaded_file.read())

            frame_dir = os.path.join(temp_dir, "frames")
            if 'video_processed' not in st.session_state or not os.path.exists(frame_dir):
                progress_placeholder = st.empty()
                total = extract_frames(video_path, frame_dir, progress_placeholder)
                progress_placeholder.empty()
                st.session_state.video_processed = True
            else:
                total = len([f for f in os.listdir(frame_dir) if f.endswith('.jpg')])
            st.success(f"Toplam {total} kare çıkarıldı.")

            if st.button("📊 Yüklenen Videoyu Analiz Et"):
                with st.spinner("Analiz ediliyor..."):
                    movement_frames = run_detection(frame_dir)
                st.success(f"{len(movement_frames)} hareketli kare tespit edildi.")
                for idx in movement_frames:
                    img_path = os.path.join(frame_dir, f"frame_{idx:03d}.jpg")
                    if os.path.exists(img_path):
                        st.image(Image.open(img_path), caption=f"Kare {idx}", use_column_width=True)

    if selected_dir and st.button("📊 Seçili Klasörü Analiz Et"):
        with st.spinner("Analiz ediliyor..."):
            movement_frames = run_detection(selected_dir)
        st.success(f"{len(movement_frames)} hareketli kare bulundu.")
        for idx in movement_frames:
            img_path = os.path.join(selected_dir, f"frame_{idx:03d}.jpg")
            if os.path.exists(img_path):
                st.image(Image.open(img_path), caption=f"Kare {idx}", use_column_width=True)
