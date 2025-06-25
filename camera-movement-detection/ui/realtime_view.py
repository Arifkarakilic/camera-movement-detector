import streamlit as st
from streamlit_webrtc import webrtc_streamer
from logic.realtime_detector import OpticalFlowDetector

def run_realtime_view():
    sensitivity = st.slider(" Ortalama Flow Büyüklüğü", 0.1, 5.0, 0.4, 0.1)
    variance_limit = st.slider(" Maksimum Varyans", 0.1, 3.0, 2.1, 0.1)
    OpticalFlowDetector.set_params(sensitivity, variance_limit)

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