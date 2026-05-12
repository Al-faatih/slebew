# 📊 Dicoding Collection Dashboard

Dashboard ini dibuat menggunakan **Streamlit** untuk menganalisis data e-commerce dan menghasilkan insight bisnis dari dataset penjualan.

---

## 🎯 Tujuan Analisis

Dashboard ini bertujuan untuk menjawab beberapa pertanyaan bisnis utama:

- 💳 Metode pembayaran yang paling sering digunakan  
- 🏪 Seller dengan kontribusi penjualan tertinggi  
- 📊 Pola distribusi penjualan antar seller  

---

## ✨ Fitur Dashboard

- 📅 Filter data interaktif berdasarkan waktu  
- 💳 Analisis metode pembayaran  
- 🏪 Analisis top seller berdasarkan penjualan  
- 📊 Visualisasi data menggunakan grafik  
- 💡 Insight otomatis dari hasil analisis  

---

## 🛠️ Teknologi yang Digunakan

- Python 3.9  
- Streamlit  
- Pandas  
- Matplotlib  
- Seaborn  

---

## ⚙️ Setup Environment

### 🐍 Menggunakan Anaconda

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

## ▶️ Menjalankan Dashboard
cd submission
streamlit run dashboard/dashboard.py
