📖 BUKU 1 RUANG 3 LEMBAR - RUANG TEDUH - LEMBAR 3 HIJAU
Konsep Three Way Function - 1x Tulis Tembus 3x Otomatis (NCR System)
Flowchart Tersystematis - SEMPURNA
[QR GATE] 
   |
[FORM ORG LENGKAP: Nama, Tempat & Tgl Lahir, Pengalaman, Pendidikan, Zona, Email, HP]
   |
[VALIDASI ROLE - EMPLOYEE vs ENTREPRENEUR]
   |---carbon copy (garis putus-putus)---> LEMBAR 1 PUTIH - ASLI
   |---carbon copy-----------------------> LEMBAR 2 MERAH - TEMBUSAN 1
   |---carbon copy-----------------------> LEMBAR 3 HIJAU - TEMBUSAN 2
LEMBAR 1 PUTIH - ASLI | RUANG TEDUH - Pintu Depan
File: app.py + requirements.txt
Flow: [QR GATE] -> [FORM ORG LENGKAP] -> [VALIDASI]

Form Registrasi Sesuai Struktur Organisasi Perusahaan (Terbaru):
Nama Lengkap *
Tempat Lahir * + Tanggal Lahir *
Alamat Email * + Nomor Telepon/WA *
Zona Rumah Tinggal * (Jakarta Pusat/Utara/Barat/Timur/Selatan/Bogor/Depok/Tangerang/Bekasi)
Pendidikan Terakhir * (SMA/SMK - S3) + Jurusan
Tahun Pengalaman (0-20th slider) + Deskripsi Pengalaman lengkap
Kategori Utama:
EMPLOYEE Rp30k = Staff s/d Supervisor (Pelaksana)
ENTREPRENEUR Rp50k = Manager s/d Business Owner (Pimpinan Bisnis Utama)
LEMBAR 2 MERAH - TEMBUSAN 1 | RUANG INTERAKSI
File: core.py (otak) + nasehat_mingguan.txt
Ruang PALING BESAR - 4 Pilar:

PILAR 1: PILIH & PROFIL ORG LENGKAP - Menampilkan nama, TTL, pendidikan, zona, pengalaman, jabatan, wewenang
PILAR 2: AUDIO TEDUH (TTS Speaker) - nasehat_mingguan.txt bisa dibacakan dengan suara (gTTS + Web Speech API) - Sesuai saran: bunyi speaker
PILAR 3: CHAT TEDUH - Chat antar member sesuai zona & jabatan
PILAR 4: MANAGE IKATAN - Ikatan Score naik +10 tiap melamar, +5 tiap posting
BURSA KERJA TEDUH - Sesuai Jenjang Org (Fitur Utama):
Employee (Staff, Senior Staff, Supervisor) = Pencari Kesempatan - Bisa melamar semua loker, data lengkap (nama, TTL, pengalaman, pendidikan, zona, email, HP) terkirim otomatis ke entrepreneur
Entrepreneur (Manager, GM, Director, Business Owner) = Pemberi Kesempatan - Bisa posting loker untuk Staff-Supervisor, approve lamaran
Saling terkoneksi karena satu struktur organisasi perusahaan, sudah terdaftar di aplikasi Ruang Teduh
Filter by Zona & Level Jabatan
LEMBAR 3 HIJAU - TEMBUSAN 2 | BOARDING / STORAGE
File: README.md + 5 Rak System
Flow: [QRIS VA] -> [INVOICE] -> [FULL ACCESS] -> [STORAGE]

5 RAK SYSTEM (Gudang Aturan Tersystematis):
RAK 1: SOP - Kebersihan

Checklist harian, wajib Employee Staff-Supervisor, dicek Pimpinan
RAK 2: ERP - Jam 9

Check-in 09:00 WIB wajib semua jenjang, Supervisor & Manager monitoring
RAK 3: OEE - 95%

Overall Equipment Effectiveness versi manusia: Availability 100%, Performance 95%, Quality 95% - Target diri 95% hadir utuh
RAK 4: KPI - Performance

Employee KPI: Jumlah apply loker, kehadiran, SOP
Entrepreneur KPI: Jumlah posting loker, approve lamaran, retensi employee
RAK 5: ALKITAB - Fondasi

Fondasi Ruang Teduh: Teduh, Terikat, Tumbuh. Bukan sekadar co-working, tapi co-growing. Fondasi semua jabatan dari Staff sampai Business Owner.
TARIF & WEWENANG SESUAI STRUKTUR ORG:
Role	Jabatan	Tarif	Wewenang
EMPLOYEE	Staff, Senior Staff, Supervisor	Rp30.000	Melamar loker, akses SOP/ERP, chat, audio teduh
ENTREPRENEUR	Manager, GM, Director, Business Owner	Rp50.000	Posting loker, approve lamaran, Full 5 Rak, QRIS VA, Invoice, KPI/OEE
FILE LENGKAP - Siap Assembly Hackathon:
app.py - LEMBAR PUTIH + MERAH + HIJAU (Streamlit, fix bug st.button inside form)
core.py - Otak, logic org, bursa kerja, TTS
nasehat_mingguan.txt - 6 nasehat, bisa TTS speaker
requirements.txt - Dependencies (streamlit, gTTS, qrcode, pydub, dotenv)
inquirement.txt - Alias untuk requirements.txt (typo yang lu pakai, tetap support)
README.md - Dokumentasi LEMBAR HIJAU + 5 Rak + Flowchart
Cara Jalan:
bash
pip install -r requirements.txt
streamlit run app.py
Deployment Streamlit Cloud:
Main file: app.py
Python 3.11+
Sudah fix: tidak ada st.button() di dalam st.form(), hanya st.form_submit_button()
Floating Dot Orange pojok kanan bawah navigasi ke semua lembar - Three Way Carbon Copy garis putus-putus - Flowchart Sempurna - Tersystematis!

