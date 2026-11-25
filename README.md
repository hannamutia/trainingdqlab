# Machine Learning Predictive Portal

Aplikasi Streamlit untuk klasifikasi spesies bunga Iris dan penilaian risiko penyakit jantung menggunakan model machine learning.

## Menjalankan aplikasi

Pastikan Python sudah terpasang, lalu buka terminal di folder `project` dan jalankan:

```bash
python -m venv .venv
```

Aktifkan virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Instal dependensi dan jalankan aplikasi:

```bash
python -m pip install streamlit pandas plotly scikit-learn
streamlit run main15hma.py
```

Jika PowerShell memblokir aktivasi virtual environment, jalankan perintah instalasi dan Streamlit menggunakan `.venv\Scripts\python.exe` sebagai pengganti `python`.

## Modul aplikasi

- **Heart Disease Assessment**: prediksi menggunakan input manual atau file CSV.
- **Iris Species Classification**: klasifikasi bunga menggunakan input manual atau file CSV.

Untuk prediksi satu data, isi parameter pada sidebar. Untuk prediksi beberapa data sekaligus, pilih **Upload CSV** dan unggah CSV dengan nama kolom yang sesuai.

### Kolom CSV

Untuk modul penyakit jantung, CSV harus memiliki kolom berikut:

```text
cp,thalach,slope,oldpeak,exang,ca,thal,sex,age
```

Untuk modul Iris, CSV harus memiliki kolom berikut:

```text
SepalLengthCm,SepalWidthCm,PetalLengthCm,PetalWidthCm
```

## File pendukung

File berikut harus tetap tersedia di folder yang sama dengan `main15hma.py`:

- `generate_heart_disease.pkl` dan `model_iris.pkl`: model prediksi.
- `heart-disease.jpg` dan `iris.JPG`: gambar pendukung aplikasi.

Jangan menghapus atau memindahkan file tersebut tanpa memperbarui aplikasi. File model pickle hanya boleh dimuat jika berasal dari sumber tepercaya.

## Deploy ke Streamlit Community Cloud

1. Push isi folder `project` ke repository GitHub.
2. Buat atau pilih aplikasi di Streamlit Community Cloud dan hubungkan repository tersebut.
3. Pilih branch yang akan di-deploy.
4. Isi **Main file path** dengan `main15hma.py`.
5. Pastikan kedua file model dan gambar pendukung ikut tersedia di repository.

Jangan unggah dataset atau informasi pasien yang sensitif ke repository publik. Untuk repository publik, pertimbangkan apakah file model dan aset lain memang boleh dibagikan.
