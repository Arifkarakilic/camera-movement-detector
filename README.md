# 🎥 Camera Movement Detection

Bu proje, sabit bir kameradan alınan video veya görüntü dizilerinde **kamera hareketini** tespit etmek için geliştirilmiştir.  
Amaç; sahnedeki nesne hareketlerinden bağımsız olarak, yalnızca **kameranın pan, tilt, kayma veya sarsılma gibi fiziksel değişimlerini** belirlemektir.

---

## 🔍 Proje Özeti

- **Giriş:** Video izleme sistemlerinde, sahne içi nesne hareketinden ziyade **kamera oynama** (örn. oynatılmış güvenlik kamerası) önemli bir durumdur.
- **Çözüm:** Ardışık kareler arasında `ORB feature matching`, `Optical Flow` ve `Affine` yöntemleriyle global hareket hesaplandı.
- **Algılama:** Hesaplanan dönüşümlerden elde edilen translasyon değerlerine göre "significant movement" kararları verildi.

---

## ⚙️ Kullanılan Teknolojiler

- Python
- OpenCV (ORB, Homography, Optical Flow, Affine)
- Streamlit (Web arayüzü)
- Hugging Face `syCen/CameraBench` dataset
- SMTP
- Docker

---

## 🧠 Algoritmaların Açıklamaları

### 🔹 ORB + Homography

- Amaç: Ardışık kareler arasında ortak noktaları (`keypoints`) tespit ederek global kamera hareketini bulmak.
- Yöntem:

1. ORB (Oriented FAST and Rotated BRIEF) ile her karede öne çıkan noktalar çıkarılır.
2. Bu noktalar eşleştirilir.
3. Homografi matrisi ile bu eşleşmenin sahneye mi yoksa kameraya mı ait olduğu analiz edilir.

- Avantaj: Nesne hareketinden daha çok kamera hareketine odaklanır.
- Sınırlama: El hareketi gibi bölgesel değişiklikler homografi ile bazen yanlış pozitif yaratabilir.

### 🔹 Optical Flow

- Amaç: Her pikselin hareketini izleyerek sahnedeki hareketin yönü ve yoğunluğunu ölçmek.
- Yöntem:

1. Farneback yöntemiyle iki kare arasındaki piksel değişimleri hesaplanır.
2. Bu akışın ortalama büyüklüğü (`mean_shift`) ve varyansı (`variance`) alınır.
3. Yüksek ortalama + düşük varyans = kamera hareketi.

- Avantaj: El/kol gibi lokal nesne hareketlerini varyans filtresiyle eleyebilir.
- Sınırlama: Çok küçük kamera hareketlerini kaçırabilir.

### 🔹 Affine + Good Features

- Amaç: Sahnenin genel dönüşümünü (dönme, kayma, ölçekleme) modelleyerek kamera hareketini ölçmek.
- Yöntem:

1. Harris veya Shi-Tomasi corner detection ile sahnedeki güçlü noktalar bulunur.
2. Bu noktalar takip edilir ve affine dönüşüm matrisi çıkarılır.
3. Dönüşümün translasyon kısmı analiz edilir.

- Avantaj: Sahnedeki genel yapıya duyarlıdır.
- Sınırlama: Çok az köşe bulunursa sonuç kararsız olabilir

---

## 🚀 Uygulama Adımları

### 1. Kurulum

```bash
git clone https://github.com/Arifkarakilic/camera-movement-detector.git
cd camera-movement-detector
python -m venv .venv
source .venv/bin/activate  # Windows
pip install -r requirements.txt
```

### 2. ✉️ Gerçek Zamanlı Mail Uyarısı İçin Yapılandırması

⚠️ "Gerçek Zamanlı Kamera" özelliği sadece lokal ortamda çalışır. Streamlit Cloud bu özelliği desteklemez.

Proje kök dizinine `.env` dosyası oluşturun ve aşağıdaki bilgileri girin:
```ini
    SMTP_USER=youremail@gmail.com
    SMTP_PASSWORD=uygulama_sifresi
    RECEIVER_EMAIL=hedefmail@gmail.com
```

Mail, kamera hareketi algılandığında otomatik olarak gönderilir. Stream akışı etkilenmesin diye SMTP işlemi arka planda `threading` ile çalıştırılır.


### 3. Uygulamayı Başlat

```bash
streamlit run camera-movement-detection/app.py
```

### 4. Kullanım

- 📂 Hazır frame klasörlerinden birini seçebilir.
- 📹 `.mp4` veya `.gif` video yükleyebilir.
- 🎚️ Eşik değerlerini ayarlayarak hassasiyetle oynayabilir.
- 📊 Tespit edilen hareketli kareleri görsel olarak inceleyebilir.
- 📊 Gerçek zamanlı kamera takibi ile hareket algılanmasında mail gönderebilir.

---

## 📦 Dosya Yapısı

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

## 📈 Örnek Çıktılar

```text
Kamera hareketi algılanan kareler: [13, 14, 15, 30]
```

Her bir kare ayrı görsel olarak sunulur.

---

## 🐳 Docker ile Çalıştırma

Bu projeyi Docker kullanarak izole bir ortamda çalıştırabilirsiniz.

### 1. Dockerfile ile

```bash
docker build -t camera-app .
docker run -p 8501:8501 --env-file .env camera-app
```
> `.env` dosyasının `.dockerignore` içine eklendiğinden emin olun.
---

## 🌐 Canlı Uygulama

### 🔗 [Uygulamayı Buradan Deneyin](https://camera-movement-detector.streamlit.app/)

### 📁 [GitHub Reposu](https://github.com/Arifkarakilic/camera-movement-detector)

---

## 🤖 Destek & AI Kullanımı

Bu projede bazı bileşenler AI yardımıyla tasarlanmış ve optimize edilmiştir (OpenAI / ChatGPT destekli).

---

## 📄 Kaynaklar

- https://huggingface.co/datasets/syCen/CameraBench
- https://docs.opencv.org
- https://streamlit.io
