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
```

### 2. Uygulamayı Başlat
```bash
streamlit run app.py
```

### 3. Kullanım

* 📂 Hazır frame klasörlerinden birini seçebilir

* 📹 .mp4 veya .gif video yükleyebilir

* 🎚️ Eşik değerini (threshold) ayarlayarak hassasiyetle oynayabilir

* 📊 Tespit edilen hareketli kareleri görsel olarak inceleyebilir

---

## 📦 Dosya Yapısı

```bash
camera-movement-detector/
├── app.py                    # Streamlit arayüzü
├── camera_loader.py          # CameraBench dataset’inden veri indirici
├── movement_detector.py      # Kamera hareketini tespit eden algoritma
├── requirements.txt
├── README.md
├── frames_video_*/           # Örnek frame dizinleri
```
---

## 📈 Örnek Çıktılar

---

## 🌐 Canlı Uygulama

### 🔗 [Uygulamayı Buradan Deneyin](https://github.com/Arifkarakilic/camera-movement-detector).

### 📁 GitHub Reposu

---

## 🤖 Destek & AI Kullanımı

Bu projede bazı bileşenler AI yardımıyla tasarlanmış ve optimize edilmiştir (OpenAI / ChatGPT destekli).

---

## 📄 Kaynaklar

* https://huggingface.co/datasets/syCen/CameraBench
* https://docs.opencv.org
* https://streamlit.io 

---