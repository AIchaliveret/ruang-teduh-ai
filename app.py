# app.py - Ruang Teduh AI
# Kerja Dekat Rumah + Wellbeing

import streamlit as st
from core.mapping import cari_loker_dekat

st.set_page_config(page_title="Ruang Teduh AI", page_icon="🏠")

st.title("🏠 Ruang Teduh AI")
st.subheader("Tavo Malkhutkha: Two Journeys, One QR")
st.write("Wellbeing AI for Future of Work - Kerja max 60km dari rumah")

# Data dummy loker
semua_loker = [
    {"judul": "Admin Online Shop", "lokasi": "DKI Jakarta"},
    {"judul": "Barista", "lokasi": "Jakarta Selatan"},
    {"judul": "Staff IT", "lokasi": "Jakarta Pusat"},
    {"judul": "Guru Les", "lokasi": "DKI Jakarta"},
    {"judul": "Content Creator", "lokasi": "Jakarta Barat"},
    {"judul": "Driver", "lokasi": "Jakarta Timur"},
]
 
domisili = st.selectbox("Pilih Domisili Lo:", ["DKI Jakarta", "Jakarta Selatan", "Jakarta Barat", "Jakarta Timur", "Jakarta Utara", "Jakarta Pusat"])

if st.button("Cari Loker Dekat Rumah"):
    hasil = cari_loker_dekat(domisili, semua_loker)
    st.success(f"Ketemu {len(hasil)} loker dekat {domisili} (max 60km)")
    for loker in hasil:
        st.write(f"✅ {loker['judul']} - {loker['lokasi']} ({loker['jarak']})")

    st.divider()
    st.write("🧘 **Ruang Doa / Wellbeing Check:**")
    st.info("Sudah minum air? Tarik napas 3x dulu sebelum apply. Kerja dekat itu untuk teduh, bukan stress.")
