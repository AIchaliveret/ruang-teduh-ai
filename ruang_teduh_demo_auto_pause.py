# ============================================================
# RUANG TEDUH AI - DEMO STREAMLIT
# AUTO ACTIVE + PAUSE - V1-V2-V3
# Cara jalan: streamlit run ruang_teduh_demo_auto_pause.py
# ============================================================
import streamlit as st
import time
import random
from datetime import datetime

st.set_page_config(page_title="Ruang Teduh AI - Auto Active + Pause", layout="wide")

# --- SESSION STATE = INGATAN SISTEM ---
# Ini yang bikin PAUSE bisa nyimpen data terakhir
if "mode" not in st.session_state:
    st.session_state.mode = "STANDBY"
if "last_suhu" not in st.session_state:
    st.session_state.last_suhu = 25.0
if "last_lembab" not in st.session_state:
    st.session_state.last_lembab = 60.0
if "last_warna" not in st.session_state:
    st.session_state.last_warna = "Belum Scan"
if "last_tangan" not in st.session_state:
    st.session_state.last_tangan = "Siaga"
if "log" not in st.session_state:
    st.session_state.log = []

def tambah_log(pesan):
    jam = datetime.now().strftime("%H:%M:%S")
    st.session_state.log.insert(0, f"[{jam}] {pesan}")
    st.session_state.log = st.session_state.log[:20]

# --- HEADER ---
st.title("Ruang Teduh AI - Auto Active + Pause Control")
st.caption("V1 Fondasi | V2 Modular | V3 NASA Space Guardian | SaaS SCM for Bio Healthy Space")

# --- STATUS BESAR ---
if st.session_state.mode == "AUTO":
    st.success("● AUTO AKTIF - Sensor jalan sendiri tiap 2 detik")
elif st.session_state.mode == "PAUSE":
    st.warning("⏸ PAUSED - Semua dibekukan di tempat, data terakhir disimpan")
else:
    st.info("○ STANDBY - Belum jalan, pencet START AUTO")

# --- TOMBOL KONTROL ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("▶ START AUTO", use_container_width=True):
        st.session_state.mode = "AUTO"
        tambah_log("AUTO AKTIF - Sensor Infrared mulai scan")
        st.rerun()
with col2:
    if st.button("⏸ PAUSE", use_container_width=True):
        st.session_state.mode = "PAUSE"
        tambah_log(f"PAUSED - Data disimpan: Suhu {st.session_state.last_suhu}C, Warna {st.session_state.last_warna}, Tangan {st.session_state.last_tangan}")
        st.rerun()
with col3:
    if st.button("▶ RESUME / LANJUTKAN", use_container_width=True):
        st.session_state.mode = "AUTO"
        tambah_log("RESUME - Lanjut dari data terakhir, bukan dari nol")
        st.rerun()
with col4:
    if st.button("■ STOP / RESET", use_container_width=True):
        st.session_state.mode = "STANDBY"
        st.session_state.last_warna = "Belum Scan"
        st.session_state.last_tangan = "Siaga"
        tambah_log("STOP - Balik ke STANDBY")
        st.rerun()

st.divider()

# --- PANEL SENSOR LIVE ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Suhu", f"{st.session_state.last_suhu:.1f} °C")
c2.metric("Kelembaban", f"{st.session_state.last_lembab:.1f} %")
c3.metric("Warna Infrared", st.session_state.last_warna)
c4.metric("Tiang Tangan", st.session_state.last_tangan)

# Warna artinya apa?
if st.session_state.last_warna == "Hijau":
    st.success("Hijau = Sehat - Barang Aman, Tangan Siaga")
elif st.session_state.last_warna == "Kuning":
    st.warning("Kuning = Waspada - Pantau, Tangan Geser Sedikit")
elif st.session_state.last_warna == "Coklat":
    st.error("Coklat = Bahaya / Busuk - Tangan Bergerak ke Karantina")

st.divider()

# --- LOG AKTIVITAS ---
st.subheader("Log Aktivitas")
for item in st.session_state.log:
    st.text(item)
if not st.session_state.log:
    st.text("Belum ada aktivitas. Pencet START AUTO.")

# --- LOGIKA AUTO / PAUSE - INI INTINYA ---
# Kalau mode == AUTO: baca sensor, putuskan warna, gerakkan tangan
# Kalau mode == PAUSE: JANGAN baca, JANGAN gerak, simpan data terakhir
# Kalau mode == RESUME: mode jadi AUTO lagi, lanjut dari data terakhir
if st.session_state.mode == "AUTO":
    # 1. BACA SENSOR (simulasi)
    st.session_state.last_suhu = round(random.uniform(24.0, 27.5), 1)
    st.session_state.last_lembab = round(random.uniform(55.0, 68.0), 1)
    st.session_state.last_warna = random.choice(["Hijau", "Hijau", "Kuning", "Coklat"])

    # 2. PUTUSKAN WARNA -> 3. GERAKKAN TANGAN
    if st.session_state.last_warna == "Hijau":
        st.session_state.last_tangan = "Siaga - Barang Aman"
    elif st.session_state.last_warna == "Kuning":
        st.session_state.last_tangan = "Waspada - Pantau"
    else:
        st.session_state.last_tangan = "Bergerak ke Karantina"

    tambah_log(f"Scan - Suhu {st.session_state.last_suhu}C, Warna {st.session_state.last_warna}, Tangan {st.session_state.last_tangan}")
    time.sleep(2)
    st.rerun()

# Kalau PAUSE, kode di atas TIDAK jalan.
# Jadi angka tidak berubah, tangan tidak gerak, data terakhir tetap aman.
