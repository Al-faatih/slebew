# 📊 Dicoding Collection Dashboard

Dashboard ini dibuat menggunakan Streamlit untuk menganalisis data e-commerce dan menjawab beberapa pertanyaan bisnis, yaitu:

💳 Metode pembayaran yang paling sering digunakan
🏪 Seller dengan kontribusi penjualan tertinggi

Dashboard juga dilengkapi fitur filter interaktif agar pengguna dapat mengeksplorasi data secara dinamis.

## ⚙️ Setup Environment
## 🐍 Menggunakan Anaconda
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
💻 Menggunakan Shell / Terminal (Alternatif)
mkdir proyek_analisis_data
cd proyek_analisis_data

pipenv install
pipenv shell

pip install -r requirements.txt
▶️ Menjalankan Dashboard
streamlit run dashboard.py
📁 Struktur Folder
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
## 📌 Fitur Dashboard
📅 Filter waktu interaktif
💳 Analisis metode pembayaran
🏪 Analisis top seller
📊 Visualisasi data sederhana & informatif
💡 Insight bisnis otomatis
🚀 Insight yang Dihasilkan
Metode pembayaran tertentu mendominasi transaksi
Sebagian kecil seller menyumbang mayoritas penjualan (Pareto Principle)
Terdapat ketimpangan kontribusi antar seller dalam ekosistem penjualan
