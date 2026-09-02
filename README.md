# 🧘 Ruang Teduh AI - TAVO MALKHUTKHA
### V28.1 AUDIO FIX + V2.7 Wellbeing Library - Kerja max 60km dari rumah
**Mode:** HP Worth It Full Width + Laptop + Floating Dot
**Developer:** aichaliveret | **Status:** Hening Total - No Music Stress

> IDENTITAS: Wellbeing Library yang membantu Employee mencapai improvement culture melalui SOP/ERP/OEE/KPI yang disempurnakan Alkitab.

### 🚨 CRITICAL FIX V28.1
Masalah: Musik stress masih muncul walau USE_MUSIC=False
Penyebab: Flag doang gak cukup di Streamlit Cloud, file lama masih ke-cache
Solusi:
1. Hapus: musik_teduh.mp3, backsound.mp3
2. Rename: ruang1.mp3 -> ruang1_V28.1_NO_MUSIC.mp3
3. Reboot app + Clear cache

### 🎛️ ATURAN UTAMA TERSYSTEMATIS
1. SOP Kolose 3:23 - Datang, Doa, Kerja untuk Tuhan - Senin: cek kebersihan
2. ERP Hati - Manusia, Material 60km, Money UMR Rp 4,900,000 - Selasa: update stok jam 9
3. OEE Rohani - Availability 100%, Performance 1%, Quality - Rabu: OEE mesin 1 95%
4. KPI Amsal 16:3 - Serahkan perbuatanmu kepada Tuhan
5. Kolom Keterangan = Floating Dot 1 tombol kendali

### 🗺️ FLOORPLAN 3 RUANG
[QR GATE] -> [RUANG 1: PINTU MASUK - WAJIB EMAIL] -> [RUANG 2: PERJALANAN EMPLOYEE - SOP/ERP/OEE/KPI] -> [RUANG 3: BAYAR - QRIS & VA BCA/Mandiri/BRI]
[FLOATING DOT Pojok Kanan Bawah - Kolom Lo + Meta AI]

### 🔊 AUDIO V28.1
Mode: Worship Teduh Slow Piano + Nature (bukan musik stress)
Fix: Speaker PASTI bunyi asal di-KLIK, autoplay=False

### 📁 FILE CORE
- app.py - Main app V28.1
- core.py - Otak SOP/ERP/OEE/KPI
- nasehat_mingguan.txt - Senin SOP, Selasa ERP jam 9, Rabu OEE 95%
- requirements.txt - streamlit==1.39.0

### 🚀 Deploy
Push -> share.streamlit.io -> Manage app -> Reboot -> Clear cache
