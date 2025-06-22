# 🎥 Camera Movement Detection

This project is developed to detect **camera motion** in video or image sequences from a static camera.  
The goal is to determine only the **physical changes of the camera** (e.g., pan, tilt, shift, shake), independently of object movements in the scene.

---

##  Project Summary

- **Motivation:** In video surveillance systems, detecting **camera movement** (e.g., tampering) is often more critical than detecting object motion.
- **Solution:** Global motion was calculated using `ORB feature matching`, `Optical Flow`, and `Affine` methods between consecutive frames.
- **Detection:** Translation values derived from the transformations are used to decide if there is "significant movement."

---

##  Technologies Used

- Python
- OpenCV (ORB, Homography, Optical Flow, Affine)
- Streamlit (Web UI)
- Hugging Face `syCen/CameraBench` dataset
- SMTP
- Docker

---

##  Algorithm Descriptions

### 🔹 ORB + Homography

- **Purpose:** Detect global camera movement by identifying and matching keypoints between consecutive frames.
- **Method:**
  1. Use ORB (Oriented FAST and Rotated BRIEF) to extract prominent keypoints.
  2. Match keypoints between frames.
  3. Analyze the homography matrix to determine if the motion is from the camera or objects.

- **Advantage:** Focuses more on camera movement than object motion.
- **Limitation:** May produce false positives on local motion like hand waving.

### 🔹 Optical Flow

- **Purpose:** Track per-pixel motion to estimate direction and intensity of movement.
- **Method:**
  1. Compute optical flow between two frames using Farneback method.
  2. Calculate mean flow magnitude and variance.
  3. High mean + low variance = likely camera movement.

- **Advantage:** Filters out local object motion like hand/arm using variance.
- **Limitation:** May miss very small camera shakes.

### 🔹 Affine + Good Features

- **Purpose:** Model the global scene transformation (translation, rotation, scaling) to estimate camera movement.
- **Method:**
  1. Detect strong corners using Harris or Shi-Tomasi.
  2. Track these corners across frames.
  3. Analyze the affine transformation matrix.

- **Advantage:** Sensitive to overall scene geometry.
- **Limitation:** Unstable if too few corners are detected.

---

## 🚀 Setup Steps

### 1. Installation

```bash
git clone https://github.com/Arifkarakilic/camera-movement-detector.git
cd camera-movement-detector
python -m venv .venv
source .venv/bin/activate  # For Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2.  Real-Time Email Alerts (SMTP Setup)

⚠️ "Real-Time Camera" feature works **only in local environments**. Streamlit Cloud does not support this.

Create a `.env` file in the root directory and add:

```ini
SMTP_USER=youremail@gmail.com
SMTP_PASSWORD=your_app_password
RECEIVER_EMAIL=targetmail@gmail.com
```

When motion is detected via live camera, an alert email will be sent.  
SMTP is handled in the background using `threading` so streaming is not interrupted.

### 3. Launch the App

```bash
streamlit run camera-movement-detection/app.py
```

### 4. How to Use

-  Select from available frame folders
-  Upload `.mp4` or `.gif` files
-  Tune detection sensitivity using sliders
-  Visually inspect detected motion frames
-  Trigger alert emails during real-time detection

---

## 📦 Project Structure

```bash
camera-movement-detector/
├── README.md
└── camera-movement-detection/
    ├── app.py
    ├── camera_loader.py
    ├── detectors/
    │   ├── movement_detector.py
    │   ├── movement_detector_affine.py
    │   └── movement_detector_optical.py
    ├── frames/
    ├── send_mail.py
    ├── requirements.txt
    ├── .env
    ├── Dockerfile
    └── .streamlit/
        └── config.toml
```

---

##  Sample Output

```text
Detected camera motion frames: [13, 14, 15, 30]
```

Each frame is displayed as an image.

---

## 🐳 Run with Docker

You can run this project in an isolated environment using Docker.

### 1. With Dockerfile

```bash
docker build -t camera-app .
docker run -p 8501:8501 --env-file .env camera-app
```

> Make sure `.env` is added to `.dockerignore`.

---

## 🌐 Live App

### 🔗 [Try the Live Demo](https://camera-movement-detector.streamlit.app/)

### 🔗 [GitHub Repo](https://github.com/Arifkarakilic/camera-movement-detector)

---

##  AI Assistance

Some parts of this project were assisted and optimized with AI (OpenAI / ChatGPT).

---

##  References

- https://huggingface.co/datasets/syCen/CameraBench  
- https://docs.opencv.org  
- https://streamlit.io  
