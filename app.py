import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import RobustScaler
import numpy as np
from streamlit_lottie import st_lottie
import json

# Memuat model dan scaler
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

# Memuat animasi Lottie
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Sidebar Navigasi Manual
st.sidebar.markdown("<h2 class='sidebar-header'>Navigasi</h2>", unsafe_allow_html=True)

# Menentukan halaman
pages = {
    "🏠 Beranda": "home",
    "ℹ️ Tentang": "about",
    "📊 Konten": "content"
}

# Mengingat halaman yang dipilih menggunakan session state
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "home"

# Tombol untuk memilih halaman tanpa menggunakan perulangan
home_button = st.sidebar.button("🏠 Beranda", key="home")
about_button = st.sidebar.button("ℹ️ Tentang", key="about")
content_button = st.sidebar.button("📊 Konten", key="content")

# Menangani navigasi tanpa perulangan
if home_button:
    st.session_state.selected_page = "home"
elif about_button:
    st.session_state.selected_page = "about"
elif content_button:
    st.session_state.selected_page = "content"

# Menampilkan halaman berdasarkan pemilihan
page = st.session_state.selected_page

# ---------------------- HOME ----------------------
if page == "home":
    st.markdown(
        """
        <div style="text-align:center">
            <h1 style="font-size: 60px;">🚧 SIDARA</h1>
            <h3>Sistem Deteksi Risiko Urbanisasi Daerah</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.image("urbanisasi.png", use_container_width=True)

    st.markdown("""
    <div style='text-align: justify; font-size: 18px;'>
        <p>
            <strong>SIDARA</strong> adalah sistem deteksi risiko urbanisasi daerah berbasis <em>data mining</em> 
            yang dirancang untuk mengidentifikasi tingkat risiko urbanisasi pada kabupaten/kota di Indonesia. 
            Sistem ini mempertimbangkan berbagai indikator sosial ekonomi untuk mendukung 
            <strong>perencanaan pembangunan yang berkelanjutan</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

# about
elif page == "about":
    st.title("📊 Tentang Fitur-Fitur yang Digunakan")
    st.markdown("Berikut adalah fitur-fitur yang digunakan dalam sistem **klasifikasi risiko urbanisasi**:")

    # Dua kolom untuk membagi fitur
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        🧾 **NCPR (National Cost Poverty Rate)**  
        Persentase penduduk yang hidup di bawah garis kemiskinan.

        🍚 **Pengeluaran Pangan (%)**  
        Persentase pengeluaran rumah tangga untuk konsumsi pangan.

        ⚡ **Tanpa Listrik (%)**  
        Persentase penduduk yang tidak memiliki akses listrik.

        🚰 **Tanpa Air Bersih (%)**  
        Persentase penduduk yang tidak memiliki akses ke air bersih.

        🎓 **Lama Sekolah Perempuan (tahun)**  
        Rata-rata lama sekolah untuk perempuan di daerah tersebut.
        """)

    with col2:
        st.markdown("""
        🏥 **Rasio Tenaga Kesehatan**  
        Perbandingan jumlah tenaga kesehatan terhadap jumlah penduduk.

        ❤️ **Angka Harapan Hidup (tahun)**  
        Rata-rata usia yang diharapkan pada saat kelahiran.

        📉 **Stunting (%)**  
        Persentase anak-anak yang mengalami stunting.

        🥦 **IKP (Indeks Ketahanan Pangan)**  
        Ukuran tingkat ketahanan pangan daerah.

        👥 **Jumlah Penduduk (jiwa)**  
        Total jumlah penduduk di daerah tersebut.
        """)

    st.markdown("---")
    st.success("Fitur-fitur di atas digunakan sebagai indikator dalam sistem klasifikasi untuk menilai potensi risiko urbanisasi suatu wilayah.")




elif page == "content":
    st.title("🧮 Prediksi Risiko Urbanisasi")
    st.markdown("Masukkan data pada form di bawah ini untuk mengetahui klasifikasi risiko.")

    with st.form("input_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            feature1 = st.number_input('NCPR', min_value=0.0)
            feature2 = st.number_input('Pengeluaran Pangan (%)', min_value=0.0)
            feature3 = st.number_input('Tanpa Listrik (%)', min_value=0.0)
            feature4 = st.number_input('Tanpa Air Bersih (%)', min_value=0.0)
            feature5 = st.number_input('Lama Sekolah Perempuan (tahun)', min_value=0.0)

        with col2:
            feature6 = st.number_input('Rasio Tenaga Kesehatan', min_value=0.0)
            feature7 = st.number_input('Angka Harapan Hidup (tahun)', min_value=0.0)
            feature8 = st.number_input('Stunting (%)', min_value=0.0)
            feature9 = st.number_input('IKP', min_value=0.0)
            feature10 = st.number_input('Jumlah Penduduk (jiwa)', format="%d", step=1, min_value=1)

        submit_button = st.form_submit_button("🔍 Prediksi")

    if submit_button:
        # Konversi input menjadi float untuk fitur 1-9 dan int untuk fitur ke-10
        input_data = pd.DataFrame([[
            float(feature1), float(feature2), float(feature3),
            float(feature4), float(feature5), float(feature6),
            float(feature7), float(feature8), float(feature9),
            int(feature10)
        ]])

        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)

        st.markdown("### 💡 Hasil Prediksi:")
        if prediction[0] == 1:
            st.error('⚠️ Risiko Urbanisasi: **Tinggi**')
        else:
            st.success('✅ Risiko Urbanisasi: **Rendah**')


