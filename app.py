"""
RUANG TEDUH AI - v2.6 FIXED FOR GITHUB - PASTI MUNCUL FLOATING DOT
Main file harus: app.py ATAU aplikasi.py (pilih satu, jangan dua)
Letakkan file ini sebagai aplikasi.py di repo lo Alchaliveret/ruang-teduh-ai
"""

import streamlit as st

st.set_page_config(page_title="Ruang Teduh AI - TAVO", layout="centered", initial_sidebar_state="collapsed")

# --- CSS FIX v2.6 - FLOATING DOT PAKAI TOMBOL ASLI (ANTI GAGAL DI STREAMLIT CLOUD) ---
st.markdown("""
<style>
.block-container { max-width: 100% !important; padding-top: 1rem; }

/* Jadikan tombol terakhir jadi Floating Dot Merah */
div[data-testid="stButton"]:last-of-type > button {
    position: fixed !important;
    bottom: 22px !important;
    right: 22px !important;
    width: 20px !important;
    height: 20px !important;
    min-height: 20px !important;
    border-radius: 50% !important;
    background: #ff3b30 !important;
    border: 3px solid white !important;
    box-shadow: 0 0 0 4px rgba(255,59,48,0.2), 0 4px 12px rgba(0,0,0,0.3) !important;
    z-index: 999999 !important;
    padding: 0 !important;
    animation: pulse-dot 2s infinite;
}
div[data-testid="stButton"]:last-of-type > button p { display: none; }

@keyframes pulse-dot {
    0% { box-shadow: 0 0 0 0 rgba(255,59,48,0.5), 0 4px 12px rgba(0,0,0,0.3); }
    70% { box-shadow: 0 0 0 12px rgba(255,59,48,0), 0 4px 12px rgba(0,0,0,0.3); }
    100% { box-shadow: 0 0 0 0 rgba(255,59,48,0), 0 4px 12px rgba(0,0,0,0.3); }
}

/* Panel Full Chat */
.full-chat-panel {
    position: fixed;
    bottom: 70px;
    right: 20px;
    width: 380px;
    max-width: 90vw;
    max-height: 60vh;
    background: white;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.25);
    z-index: 999998;
    padding: 16px;
    overflow-y: auto;
    border: 1px solid #eee;
}
.etika-badge { background: #fef3c7; border: 1px solid #f59e0b; padding: 10px 12px; border-radius: 12px; font-size: 12px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

if 'ruang' not in st.session_state: st.session_state.ruang = 1
if 'email' not in st.session_state: st.session_state.email = ""
if 'jalur' not in st.session_state: st.session_state.jalur = "Employee"
if 'show_chat' not in st.session_state: st.session_state.show_chat = False
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- HEADER ---
st.markdown("### 🏠 RUANG TEDUH AI - TAVO MALKHUTKHA")
st.caption("Two Journeys, One QR | Wellbeing Library - Kerja max 60km dari rumah")
st.markdown('<div class="etika-badge">🔒 v2.6 FLOATING DOT - 1 Titik Terlihat - Klik Dot untuk Full Chat - HP & Laptop Otomatis - Harga Rp X - Lolos Etika</div>', unsafe_allow_html=True)

# --- RUANG 1 ---
if st.session_state.ruang == 1:
    st.progress(33, text="Ruang 1 dari 3")
    st.markdown("## Ruang 1: Pintu Masuk Perpustakaan")
    st.write("Member masuk via QR → Pilih jalur lo")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🧑‍💼 Employee", use_container_width=True): st.session_state.jalur = "Employee"
    with c2:
        if st.button("🚀 Entrepreneur", use_container_width=True): st.session_state.jalur = "Entrepreneur"
    st.success(f"Jalur: {st.session_state.jalur} - Rp X/bulan")

    st.markdown("#### Nama Lengkap")
    nama = st.text_input("Nama Lengkap", placeholder="TAVO karyawan sebagai cheff, berkeluarga, 4 anak, duda...", label_visibility="collapsed")
    
    st.markdown("#### 📧 Kolom Keterangan WAJIB")
    st.info("⚠️ FIX v2.6: Member mesti kasih alamat email aktif. Tanpa email, invoice & akses perpustakaan tidak bisa dikirim. Kolom ini lo yang kendalikan 1 tombol.")
    email = st.text_input("Alamat Email Member (wajib)", value=st.session_state.email, placeholder="contoh@email.com")
    st.session_state.email = email

    st.markdown("### 🔊 Suara Teduh Hari Ini")
    st.markdown("**Kolose 3:23 & Amsal 16:3** - Apapun yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan")
    st.markdown("*🎵 FIX: Ganti musik yang teduh Worship*")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    st.caption("Visual + teks + audio - full di HP")

    if st.button("➡️ Masuk Ruang 2", type="primary", use_container_width=True):
        if "@" not in st.session_state.email:
            st.error("Bro, isi alamat email dulu di kolom keterangan ya. Wajib!")
        else:
            st.session_state.ruang = 2
            st.rerun()

# --- RUANG 2 ---
elif st.session_state.ruang == 2:
    st.progress(66, text="Ruang 2 dari 3")
    st.markdown("## Ruang 2: Perjalanan Employee")
    st.write(f"Halo Halo TAVO {st.session_state.email} - Full width di HP, worth it!")

    st.markdown("### 👨‍💼 Employee")
    umr = st.number_input("UMR Domisili (Rp)", value=4900000, step=100000)
    ref = umr * 0.05
    st.markdown(f"**Ref: Rp {ref:,.0f} | Biaya: Rp X/bulan - Mode Etika**")

    tab1, tab2, tab3 = st.tabs(["Kolom 1: Fondasi", "Kolom 2: Perjalanan", "Kolom 3: Puncak"])
    with tab1:
        st.markdown("#### Fondasi Teduh - Mindset & Niat")
        st.image("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800")
        st.markdown("Dokumen GDrive: Kolom1_Fondasi.pdf")
        st.markdown("**🔊 FIX SEPI - Audio Tersystematis Ruang Teduh (SOP, ERP, OEE, KPI):**")
        st.markdown("""
        > **SOP:** Bangun Doa 05:00, Baca Fondasi 15 menit
        > **ERP:** Sistem kelola hidup max 60km dari rumah via QR
        > **OEE:** Efektivitas = Waktu Teduh x Fokus x Kualitas Hati
        > **KPI Disempurnakan Alkitab:** Kolose 3:23 - Kerja untuk Tuhan. Amsal 16:3 - Serahkan perbuatanmu kepada TUHAN
        > **Tujuan:** Improvement Culture yang lebih baik, semua diproses secara benar.
        """)
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3")
    with tab2:
        st.write("Perjalanan Employee - Proses menuju improvement")
    with tab3:
        st.write("Puncak Teduh")

    setuju = st.checkbox("Setuju Rp X/bulan")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Kembali", use_container_width=True):
            st.session_state.ruang = 1
            st.rerun()
    with col2:
        if st.button("➡️ Masuk Ruang 3", type="primary", use_container_width=True, disabled=not setuju):
            st.session_state.ruang = 3
            st.rerun()

# --- RUANG 3 ---
elif st.session_state.ruang == 3:
    st.progress(100, text="Ruang 3 dari 3 - Pembayaran")
    st.markdown("## 💳 Rp X/bulan - Konfirmasi")
    if "@" not in st.session_state.email:
        st.error("Email belum ada! Balik ke Ruang 1 dulu bro.")
    else:
        st.success(f"✅ Email: {st.session_state.email} - Invoice akan dikirim ke sini")

    st.markdown("### Cara Pembayaran (FIX v2.6)")
    st.markdown("""
    **Format prompt bagian ruang ini (sudah di dalam system):**
    1. **Transfer QR Code (QRIS)** - Scan, real-time, akses langsung aktif
    2. **Virtual Account** - BCA 12345 + No HP, BRI 88810 + No HP, Mandiri 89508 + No HP
    """)
    st.code("QRIS: ruangteduh.ai/pay/TAVO-EMP")
    
    setuju_final = st.checkbox("Setuju Rp X/bulan - Email sudah benar", key="final")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Kembali", use_container_width=True):
            st.session_state.ruang = 2
            st.rerun()
    with c2:
        if st.button("✅ Bayar & Masuk Perpustakaan", type="primary", use_container_width=True, disabled=not setuju_final):
            st.balloons()
            st.success(f"Berlangganan via QR/VA berhasil! Cek email {st.session_state.email}")

# --- PANEL FULL CHAT (KOLOM FLOATING META AI) ---
if st.session_state.show_chat:
    st.markdown('<div class="full-chat-panel">', unsafe_allow_html=True)
    st.markdown("**💬 Full Chat - Ruang Teduh (v2.6)**")
    st.caption("Semua pertanyaan member bisa lo generate di sini. Utamakan sudah memberikan email.")
    for msg in st.session_state.chat_history:
        st.markdown(f"**{msg['role']}:** {msg['text']}")
    
    q = st.text_input("Ketik di Ruang 1... Enter langsung", key="chat_q", placeholder="Contoh: cara bayar? manfaat app?")
    if q:
        st.session_state.chat_history.append({"role": "Member", "text": q})
        # Logic simple
        if "bayar" in q.lower():
            ans = f"Bro, cara bayar via QR Code & Virtual Account. Tapi email lo {st.session_state.email} sudah terdaftar belum? Kalau belum, isi dulu di kolom keterangan."
        elif "manfaat" in q.lower() or "app" in q.lower():
            ans = "Manfaat Ruang Teduh: Two Journeys One QR, Wellbeing Library, Kerja max 60km dari rumah, SOP/ERP/OEE/KPI disempurnakan Alkitab untuk improvement culture."
        elif "sop" in q.lower() or "erp" in q.lower():
            ans = "SOP=Prosedur Teduh, ERP=Sistem kelola hidup, OEE=Efektivitas diri, KPI=Kolose 3:23 & Amsal 16:3 - semua proses secara benar untuk improvement culture."
        else:
            ans = f"Siap, pertanyaan '{q}' sudah di-generate sistem Ruang Teduh. Email {st.session_state.email} akan dipakai untuk kirim jawaban lengkap + audio worship 6:12."
        st.session_state.chat_history.append({"role": "AI Teduh", "text": ans})
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- FLOATING DOT BUTTON (HARUS PALING AKHIR BIAR JADI :last-of-type) ---
# Ini yang bikin dot merah muncul, klik untuk toggle Full Chat
if st.button("dot", key="floating_dot_toggle"):
    st.session_state.show_chat = not st.session_state.show_chat
    st.rerun()

st.caption("v2.6 FLOATING DOT - 2026-09-02 - 1 Titik Kecil Klik → Full Chat - HP Worth It Full Width + Laptop - Harga X - No Prompt Format")
