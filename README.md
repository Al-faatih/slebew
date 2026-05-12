# 📊 Dicoding Collection Dashboard

Dashboard ini dibuat menggunakan **Streamlit** untuk menganalisis data e-commerce dan menjawab beberapa pertanyaan bisnis utama, yaitu:

- 💳 Metode pembayaran yang paling sering digunakan  
- 🏪 Seller dengan kontribusi penjualan tertinggi  

Dashboard juga dilengkapi dengan **fitur filter interaktif** sehingga pengguna dapat mengeksplorasi data secara dinamis.

---

## ⚙️ Setup Environment

### 🐍 Menggunakan Anaconda

conda create --name main-ds python=3.9  
conda activate main-ds  
pip install -r requirements.txt  

---

### 💻 Menggunakan Shell / Terminal (Alternatif)

mkdir proyek_analisis_data  
cd proyek_analisis_data  

pipenv install  
pipenv shell  

pip install -r requirements.txt  

---

## ▶️ Menjalankan Dashboard

streamlit run dashboard.py  

Setelah dijalankan, buka browser di:  
http://localhost:8501  

---

## 📁 Struktur Folder

proyek_analisis_data/  
│  
├── dashboard.py  
├── requirements.txt  
│  
└── data/  
  ├── orders_dataset.csv  
  ├── order_items_dataset.csv  
  ├── products_dataset.csv  
  └── order_payments_dataset.csv  

---

## 📌 Fitur Dashboard

- 📅 Filter waktu interaktif  
- 💳 Analisis metode pembayaran  
- 🏪 Analisis top seller  
- 📊 Visualisasi data sederhana & informatif  
- 💡 Insight bisnis otomatis  

---

## 🚀 Insight yang Dihasilkan

- Metode pembayaran tertentu mendominasi transaksi  
- Sebagian kecil seller menyumbang mayoritas penjualan  
- Terdapat ketimpangan kontribusi antar seller dalam ekosistem penjualan  

---

## 🛠️ Teknologi yang Digunakan

- Python  
- Streamlit  
- Pandas  
- Matplotlib / Seaborn  

---

## 📬 Catatan

Pastikan semua file dataset berada di dalam folder `data/` agar dashboard dapat berjalan dengan baik.
