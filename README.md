# Template Pemrograman Python dengan FastAPI, SQLModel, dan Uvicorn

## 📌 Deskripsi Umum

Repository ini berisi **template pemrograman backend berbasis Python** yang dirancang untuk memudahkan pengembangan aplikasi web modern menggunakan **FastAPI** sebagai framework utama. Template ini dibuat dengan struktur yang rapi, modular, dan mudah dipahami, sehingga cocok digunakan sebagai:

* Kerangka awal (starter template) proyek backend
* Bahan pembelajaran FastAPI dan SQLModel
* Dasar pengembangan REST API skala kecil hingga menengah
* Fondasi aplikasi produksi yang dapat dikembangkan lebih lanjut

Template ini mengintegrasikan beberapa teknologi inti, yaitu **FastAPI**, **SQLModel**, dan **Uvicorn**, yang masing-masing memiliki peran penting dalam arsitektur aplikasi.

---

## 🧩 Teknologi yang Digunakan

### 1️⃣ FastAPI

FastAPI adalah framework web modern untuk Python yang berfokus pada:

* **Performa tinggi** (setara Node.js dan Go)
* **Kemudahan penulisan kode**
* **Validasi data otomatis** menggunakan type hints Python
* **Dokumentasi API otomatis** (Swagger UI & ReDoc)

Dalam template ini, FastAPI digunakan sebagai:

* Framework utama untuk membangun REST API
* Pengatur routing (endpoint API)
* Validasi request dan response
* Manajemen dependency injection

FastAPI sangat cocok untuk pengembangan API yang bersih, cepat, dan terstruktur.

---

### 2️⃣ SQLModel

SQLModel adalah library Python yang menggabungkan keunggulan:

* **SQLAlchemy** (ORM untuk database SQL)
* **Pydantic** (validasi dan serialisasi data)

Peran SQLModel dalam template ini:

* Menjadi **penghubung antara database SQL dan Python**
* Mendefinisikan model database menggunakan class Python
* Mengelola skema tabel database
* Menyederhanakan operasi CRUD (Create, Read, Update, Delete)

Dengan SQLModel, satu model dapat digunakan sekaligus sebagai:

* Model database
* Model request API
* Model response API

Hal ini membuat kode lebih ringkas, konsisten, dan mudah dipelihara.

---

### 3️⃣ Uvicorn

Uvicorn adalah server **ASGI (Asynchronous Server Gateway Interface)** yang digunakan untuk menjalankan aplikasi FastAPI.

Fungsi Uvicorn dalam template ini:

* Menjalankan aplikasi FastAPI secara lokal maupun production
* Mendukung asynchronous programming
* Memberikan performa tinggi dan startup cepat

Pada template ini, Uvicorn **dijalankan langsung melalui kode Python**, bukan melalui command line, dengan konfigurasi sebagai berikut:

```python
uvicorn.run(
    "main:app",
    host="127.0.0.1",
    port=5000,
    reload=True
)
```

Penjelasan konfigurasi:

* `main:app` → menunjuk file `main.py` dan instance FastAPI bernama `app`
* `host="127.0.0.1"` → server berjalan di localhost
* `port=5000` → aplikasi diakses melalui port 5000
* `reload=True` → server otomatis restart saat terjadi perubahan kode (mode development)

Pendekatan ini memudahkan developer untuk menjalankan aplikasi langsung dari file Python.

Uvicorn adalah server **ASGI (Asynchronous Server Gateway Interface)** yang digunakan untuk menjalankan aplikasi FastAPI.

Fungsi Uvicorn dalam template ini:

* Menjalankan aplikasi FastAPI secara lokal maupun production
* Mendukung asynchronous programming
* Memberikan performa tinggi dan startup cepat

Uvicorn biasanya dijalankan dengan perintah:

```bash
uvicorn main:app --reload
```

Opsi `--reload` digunakan saat development agar server otomatis restart ketika terjadi perubahan kode.

Tapi untuk template ini hanya menggunakan

```bash
python3 main.py     # Linux / macOS
python main.py      # Windows
```
---

## 📁 Tujuan Pembuatan Template

Template ini dibuat dengan tujuan utama:

* ✅ Menyediakan **struktur dasar proyek FastAPI** yang siap pakai
* ✅ Mempermudah pemula memahami alur kerja FastAPI + SQLModel
* ✅ Menghemat waktu setup awal proyek backend
* ✅ Menjadi fondasi yang fleksibel untuk dikembangkan lebih lanjut

Dengan menggunakan template ini, developer dapat langsung fokus pada logika bisnis aplikasi tanpa harus mengatur ulang konfigurasi dasar dari awal.

---

## 🚀 Fitur Utama Template

Template ini juga **sudah dilengkapi fitur autentikasi dasar**, sehingga dapat langsung digunakan sebagai fondasi aplikasi yang membutuhkan sistem login.

Fitur autentikasi yang tersedia meliputi:

* 🔐 **Signup (Registrasi Pengguna)**
  Pengguna dapat membuat akun baru dengan data yang divalidasi secara otomatis oleh FastAPI dan SQLModel.

* 🔑 **Login (Autentikasi Pengguna)**
  Sistem login telah diimplementasikan untuk memverifikasi kredensial pengguna.

* 🪪 **JWT (JSON Web Token)**
  Autentikasi menggunakan **JWT** untuk menjaga keamanan sesi pengguna. Token digunakan sebagai akses ke endpoint yang dilindungi.

* 🔒 **Keamanan Password**
  Password pengguna **tidak disimpan dalam bentuk teks asli**, melainkan sudah melalui proses hashing sebelum disimpan ke database.

Dengan adanya fitur ini, template dapat langsung dikembangkan menjadi aplikasi yang memiliki sistem autentikasi lengkap.

---

## 🚀 Fitur Utama Template

Template ini telah dilengkapi dengan berbagai fitur dasar backend yang umum digunakan dalam aplikasi modern, antara lain:

* Struktur folder yang rapi dan mudah dikembangkan
* Integrasi FastAPI, SQLModel, dan Uvicorn
* Dukungan REST API
* Validasi data otomatis menggunakan type hints Python
* Dokumentasi API otomatis (Swagger UI & ReDoc)
* Mudah diintegrasikan dengan berbagai database SQL (SQLite, PostgreSQL, MySQL, dll)

### 🔐 Fitur Autentikasi (Login & Signup)

Template ini **sudah memiliki implementasi fitur autentikasi pengguna**, sehingga dapat langsung digunakan atau dikembangkan lebih lanjut. Fitur autentikasi yang tersedia meliputi:

* **Signup (Registrasi Pengguna)**

  * Pendaftaran akun pengguna baru
  * Validasi data input (username/email unik)
  * Password disimpan dalam bentuk **hash** (bukan plain text)

* **Login (Autentikasi Pengguna)**

  * Verifikasi kredensial pengguna
  * Penerbitan token autentikasi setelah login berhasil

* **JWT (JSON Web Token)**

  * Menggunakan **JWT sebagai metode autentikasi**
  * Token digunakan untuk mengamankan endpoint tertentu
  * Mendukung skema *Bearer Token*
  * Cocok untuk REST API dan frontend terpisah (SPA / Mobile App)

Dengan sistem ini, endpoint dapat dibatasi hanya untuk pengguna yang telah login, sehingga keamanan aplikasi lebih terjaga.

---

## 🛠️ Cara Menjalankan Aplikasi

### 1. Clone Repository

```bash
git clone <url-repository>
cd <nama-folder>
```

### 2. Buat dan Aktifkan Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

### 3. Install Dependency

```bash
pip install -r requirements.txt
```

### 4. Jalankan Server

```bash
uvicorn main:app --reload
```
Bisa juga menggunakan
```bash
python3 main.py     # Linux / macOS
python main.py      # Windows
```

Aplikasi dapat diakses melalui:

* **API:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📝 Logging & Penanganan Error

Template ini juga telah dilengkapi dengan **mekanisme logging error** untuk membantu proses debugging dan monitoring aplikasi.

### 📄 File Log

* **Nama folder log:** `logs.log`
* **Nama file log:** `app_errors.log`
* File ini digunakan untuk mencatat berbagai error yang terjadi selama aplikasi berjalan.

### ⚠️ Jenis Error yang Dicatat

Beberapa jenis error yang secara khusus ditangani dan dicatat ke dalam file log antara lain:

* **HTTPException**
  Digunakan untuk mencatat error yang berasal dari request client, seperti:

  * Status code 400 (Bad Request)
  * Status code 401 (Unauthorized)
  * Status code 403 (Forbidden)
  * Status code 404 (Not Found)

* **Exception (Error Umum)**
  Digunakan untuk mencatat error tak terduga yang terjadi di sisi server, seperti:

  * Kesalahan logika program
  * Error database
  * Kesalahan konfigurasi

### 🎯 Tujuan Logging

Penerapan logging ini bertujuan untuk:

* Mempermudah developer melacak sumber masalah
* Menyediakan riwayat error tanpa harus melihat console secara langsung
* Membantu proses debugging pada tahap development maupun production
* Meningkatkan keandalan dan maintainability aplikasi

Dengan adanya file `app_errors.log`, developer dapat dengan cepat mengetahui **kapan error terjadi**, **jenis error**, serta **pesan error yang dihasilkan**, tanpa mengganggu alur penggunaan aplikasi.

---

## 📚 Catatan Tambahan

Template ini bersifat **open untuk dikembangkan**, seperti:

* Penambahan autentikasi (JWT, OAuth2)
* Integrasi database production
* Penambahan role & permission
* Implementasi clean architecture
* Deployment ke server atau cloud

---

## 📄 Lisensi

Template ini bebas digunakan untuk keperluan pembelajaran maupun pengembangan proyek pribadi dan komersial.

---

✨ Semoga template ini dapat membantu mempercepat proses pengembangan backend Python Anda dan menjadi fondasi yang kuat untuk proyek FastAPI selanjutnya.
