
# 2025
ATPTech Core Talent Repo

# Camera Movement Detection Challenge

This project is a starter kit for detecting significant camera movement from a sequence of images using computer vision techniques.

## 📸 Challenge Overview

Build an algorithm that detects *significant movement* of a camera (e.g., shake, tilt, pan) by analyzing consecutive image frames.

**Your tasks:**
- Implement movement detection logic in `movement_detector.py`
- Create a simple web app interface in `app.py` for uploading images/videos and viewing results
- Deploy your solution (e.g., Streamlit Cloud or Hugging Face Spaces)
- Submit your app URL and GitHub repo

---

## 🚀 Getting Started

1. Clone this repo
2. Install dependencies:  
    pip install -r requirements.txt
3. Add or use sample frames in `test_images/`
4. Run locally:  

---

## 📝 Deliverables

- Publicly deployed app URL
- Updated GitHub repo (this one or your fork)
- Complete README with approach and instructions

---

## 📂 Files

- `movement_detector.py`: Put your main detection logic here
- `app.py`: Streamlit web app
- `requirements.txt`: Dependencies
- `test_images/`: Place sample image frames for testing

---

## 💡 Hints

- Check out OpenCV functions like `cv2.absdiff`, `cv2.goodFeaturesToTrack`, `cv2.findHomography`
- For extra credit: Visualize detected movement on output frames

---

Good luck!
# 🎥 Camera Movement Detection

Bu proje, sabit bir kameradan alınan video veya görüntü dizilerinde **kamera hareketini** tespit etmek için geliştirilmiştir.  
Amaç; sahnedeki nesne hareketlerinden bağımsız olarak, yalnızca **kameranın pan, tilt, kayma veya sarsılma gibi fiziksel değişimlerini** belirlemektir.

---

## 🔍 Proje Özeti

- **Giriş:** Video izleme sistemlerinde, sahne içi nesne hareketinden ziyade **kamera oynama** (örn. oynatılmış güvenlik kamerası) önemli bir durumdur.
- **Çözüm:** Ardışık kareler arasında `ORB feature matching` kullanarak global hareket (Homography) hesaplandı.
- **Algılama:** Hesaplanan homografi dönüşümündeki kayma (`dx`, `dy`) değerlerinin büyüklüğüne göre "significant movement" kararları verildi.

---

## ⚙️ Kullanılan Teknolojiler

- Python
- OpenCV (ORB, Homography)
- Streamlit (Web arayüzü)
- Hugging Face `syCen/CameraBench` dataset

---

## 🚀 Uygulama Adımları

### 1. Kurulum

```bash
git clone https://github.com/kullanici-adi/camera-movement-detector.git
cd camera-movement-detector
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
