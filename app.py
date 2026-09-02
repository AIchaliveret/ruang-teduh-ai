"""
RUANG TEDUH AI - TAVO MALKHUTKHA - v2.6 FIXED
Two Journeys, One QR | Wellbeing Library - Kerja max 60km dari rumah

FIXES berdasarkan coretan hijau:
- Kolom keterangan isi penjelasan member mesti kasih email
- Ganti musik yang teduh Worship
- Cara bayar QR + Virtual Account
- Ruang sepi -> kasih audio SOP, ERP, OEE, KPI disempurnakan Alkitab
- 1 tombol kendalikan semua pertanyaan member
- Lebih rapih & tersystematis
"""

import streamlit as st
from streamlit.components.v1 import html as html_comp

st.set_page_config(page_title="Ruang Teduh AI - TAVO", layout="centered", initial_sidebar_state="collapsed")

# --- CSS v2.6 FLOATING DOT + HP Worth It Full Width + Laptop Otomatis ---
st.markdown("""
<style>
/* HP Full Width */
.block-container { max-width: 100% !important; padding: 1rem; }
@media (max-width: 768px) { .block-container { padding: 0.5rem; } }

/* Progress */
.stProgress > div > div > div > div { background-color: #3b82f6; }

/* Tombol utama */
div.stButton > button { width: 100%; border-radius: 12px; height: 48px; font-weight: 600; }

/* Floating Dot v2.6 */
#floating-dot {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 18px;
    height: 18px;
    background: #ff4b4b;
    border-radius: 50%;
    z-index: 9999;
    cursor: pointer;
    box-shadow: 0 0 0 4px rgba(255,75,75,0.2);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(255,75,75,0.4); }
    70% { box-shadow: 0 0 0 10px rgba(255,75,75,0); }
    100% { box-shadow: 0 0 0 0 rgba(255,75,75,0); }
}
#full-chat {
    display: none;
    position: fixed;
    bottom: 80px;
    right: 20px;
    width: 380px;
    max-width: 90vw;
    height: 500px;
    background: white;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    z-index: 9998;
    padding: 16px;
    flex-direction: column;
}
#full-chat.open { display: flex; }

/* Lolos Etika badge */
.etika-badge { background: #fef3c7; border: 1px solid #f59e0b; padding: 12px; border-radius: 12px; font-size: 13px; margin: 12px 0; }
</style>
""", unsafe_allow_html=True)

# --- FLOATING DOT HTML ---
floating_html = """
<div id="floating-dot" title="Klik Dot untuk Full Chat"></div>
<div id="full-chat">
    <div style="font-weight:700; margin-bottom:8px;">💬 Ruang Teduh - Full Chat (v2.6)</div>
    <div id="chat-content" style="flex:1; overflow-y:auto; font-size:13px; line-height:1.5;">
        <p><b>System:</b> Semua pertanyaan member bisa di-generate di sini.<br>
        - Cara bayar? Utamakan sudah memberikan email<br>
        - Apa manfaat app Ruang Teduh? Two Journeys One QR, Wellbeing Library, Kerja max 60km<br>
        - SOP/ERP/OEE/KPI? Dijelaskan tersystematis disempurnakan Alkitab<br><br>
        <i>Ketik pertanyaan lo, bro...</i></p>
    </div>
    <input id="chat-input" placeholder="Ketik di Ruang 1... Enter langsung" style="width:100%; padding:8px; border-radius:8px; border:1px solid #ddd; margin-top:8px;">
</div>
<script>
document.getElementById('floating-dot').onclick = function() {
    document.getElementById('full-chat').classList.toggle('open');
}
</script>
"""
html_comp(floating_html, height=0)

# --- STATE ---
if 'ruang' not in st.session_state:
    st.session_state.ruang = 1
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'jalur' not in st.session_state:
    st.session_state.jalur = "Employee"

# --- HEADER ---
st.markdown("### 🏠 RUANG TEDUH AI - TAVO MALKHUTKHA")
st.caption("Two Journeys, One QR | Wellbeing Library - Kerja max 60km dari rumah")
st.markdown('<div class="etika-badge">🔒 v2.6 FLOATING DOT - 1 Titik Terlihat - Klik Dot untuk Full Chat - HP & Laptop Otomatis - Harga Rp X - Lolos Etika</div>', unsafe_allow_html=True)

# --- PROMPT FORMAT (NO PROMPT FORMAT untuk member, tapi ada di system) ---
PROMPT_RUANG_3 = """
[SYSTEM - JANGAN TAMPILKAN KE MEMBER]
Konteks: Ruang 3 Pembayaran Rp X/bulan
Aturan:
1. WAJIB validasi email member dulu. Jika st.session_state.email kosong -> JANGAN kasih cara bayar, minta email dulu.
2. Jika email ada -> jelaskan 2 opsi:
   - QRIS Transfer (scan QR, real-time)
   - Virtual Account BCA/BRI/Mandiri (auto-verify)
3. Ingatkan: invoice & akses perpustakaan akan dikirim ke email tersebut.
Gaya: Teduh Worship, Lolos Etika.
"""

PROMPT_RUANG_2 = """
[SYSTEM - AUDIO GUIDE SOP/ERP/OEE/KPI]
Jelaskan tersystematis Ruang Teduh:
SOP = Prosedur kerja teduh harian
ERP = Sistem kelola hidup max 60km dari rumah
OEE = Efektivitas diri (Availability x Performance x Quality)
KPI = Disempurnakan Alkitab - Kolose 3:23 & Amsal 16:3
Tujuan: Improvement Culture yang lebih baik, semua proses secara benar.
"""

# --- RUANG 1: PINTU MASUK PERPUSTAKAAN (Lebih Tersystematis) ---
if st.session_state.ruang == 1:
    st.progress(33, text="Ruang 1 dari 3")
    st.markdown("## Ruang 1: Pintu Masuk Perpustakaan")
    st.write("Member masuk via QR → Pilih jalur lo")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧑‍💼 Employee", key="emp"):
            st.session_state.jalur = "Employee"
    with col2:
        if st.button("🚀 Entrepreneur", key="ent"):
            st.session_state.jalur = "Entrepreneur"
    
    st.success(f"Jalur: {st.session_state.jalur} - Rp X/bulan")

    # Nama Lengkap + Email Gate (FIX sesuai coretan)
    st.markdown("#### Nama Lengkap")
    nama = st.text_input("Nama Lengkap", placeholder="TAVO karyawan sebagai cheff, berkeluarga, 4 anak, duda...", label_visibility="collapsed")
    
    st.markdown("#### 📧 Kolom Keterangan WAJIB (FIX v2.6)")
    st.info("⚠️ Penjelasan: Member mesti kasih alamat email aktif. Tanpa email, akses perpustakaan & invoice tidak bisa dikirim. Ini sistem Ruang Teduh yang paling penting.")
    email = st.text_input("Alamat Email Member (wajib)", value=st.session_state.email, placeholder="contoh@email.com")
    st.session_state.email = email

    st.markdown("### 🔊 Suara Teduh Hari Ini")
    st.markdown("**Kolose 3:23 & Amsal 16:3** - Apapun yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan")
    
    # GANTI MUSIK YANG TEDUH WORSHIP (FIX)
    st.markdown("*🎵 Musik: Worship Teduh - Instrumental Piano*")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")  # placeholder worship, ganti file lokal worship.mp3
    st.caption("Visual + teks + audio - full di HP")

    if st.button("➡️ Masuk Ruang 2", type="primary"):
        if not st.session_state.email or "@" not in st.session_state.email:
            st.error("Bro, isi alamat email dulu di kolom keterangan ya. Ini wajib buat sistem Ruang Teduh.")
        else:
            st.session_state.ruang = 2
            st.rerun()

# --- RUANG 2: PERJALANAN EMPLOYEE (FIX SEPI) ---
elif st.session_state.ruang == 2:
    st.progress(66, text="Ruang 2 dari 3")
    st.markdown("## Ruang 2: Perjalanan Employee")
    st.write(f"Halo Halo TAVO karyawan sebagai cheff, berkeluarga, 4 anak, duda, {st.session_state.email} - Full width di HP, worth it!")

    st.markdown("### 👨‍💼 Employee")
    st.markdown("UMR Domisili (Rp)")
    umr = st.number_input("UMR", value=4900000, step=100000, label_visibility="collapsed")
    ref = umr * 0.05
    st.markdown(f"**Ref: Rp {ref:,.0f}**")
    st.markdown("**Biaya: Rp X/bulan - Mode Etika**")

    tab1, tab2, tab3 = st.tabs(["Kolom 1: Fondasi", "Kolom 2: Perjalanan", "Kolom 3: Puncak"])
    with tab1:
        st.markdown("#### Fondasi Teduh - Mindset & Niat")
        st.image("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800", caption="Visual Gunung - Fondasi")
        st.markdown("Dokumen GDrive: Kolom1_Fondasi.pdf")
        # AUDIO PENJELASAN TERSYSTEMATIS (FIX SEPI)
        st.markdown("**🔊 Audio Penjelasan Tersystematis (FIX v2.6 - Biar Gak Sepi):**")
        st.markdown("""
        > **SOP Ruang Teduh:** Bangun jam 5, Doa, Baca Fondasi.pdf 15 menit
        > **ERP Ruang Teduh:** Kelola hidup max 60km dari rumah via QR
        > **OEE Ruang Teduh:** Efektivitas = Waktu Teduh x Fokus Kerja x Kualitas Hati
        > **KPI Disempurnakan Alkitab:** Kolose 3:23 - Kerja seperti untuk Tuhan, bukan manusia. Amsal 16:3 - Serahkan perbuatanmu kepada TUHAN
        >
        > Tujuan: Improvement Culture yang lebih baik, semua diproses secara benar.
        """)
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3")

    with tab2:
        st.markdown("Perjalanan Employee - Proses Improvement")
    with tab3:
        st.markdown("Puncak - Puncak Teduh")

    st.markdown("### 💳 Rp X/bulan")
    setuju = st.checkbox("Setuju Rp X/bulan")
    
    col_back, col_next = st.columns(2)
    with col_back:
        if st.button("⬅️ Kembali"):
            st.session_state.ruang = 1
            st.rerun()
    with col_next:
        if st.button("➡️ Masuk Ruang 3", type="primary", disabled=not setuju):
            if not setuju:
                st.warning("Centang setuju dulu bro")
            else:
                st.session_state.ruang = 3
                st.rerun()

# --- RUANG 3: PEMBAYARAN (FIX CARA BAYAR & EMAIL) ---
elif st.session_state.ruang == 3:
    st.progress(100, text="Ruang 3 dari 3 - Pembayaran")
    st.markdown("## 💳 Rp X/bulan - Konfirmasi Berlangganan")
    
    # Email validation reminder (FIX)
    if not st.session_state.email:
        st.error("⚠️ Belum ada email! Kembali ke Ruang 1 dan isi alamat email dulu.")
    else:
        st.success(f"✅ Email terdaftar: {st.session_state.email} - Invoice akan dikirim ke sini")

    st.image("https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800", caption="Fondasi Teduh - Mindset & Niat")

    st.markdown("### Cara Pembayaran (FIX v2.6 - QR + Virtual Account)")
    st.markdown("""
    **Pastikan lo sudah kasih format prompt bagian ruang ini bro:**
    
    1. **Transfer QR Code (QRIS)**
       - Scan QR di bawah
       - Nominal: Rp X
       - Real-time, akses langsung aktif
    
    2. **Virtual Account**
       - BCA VA: 12345 + No HP
       - BRI VA: 88810 + No HP  
       - Mandiri VA: 89508 + No HP
       - Auto-verify 1x24 jam
    
    **Format Prompt System (No Prompt Format untuk member):**
    ```
    Jika email kosong -> minta email dulu
    Jika email ada -> kasih QR + VA
    ```
    """)

    # Simulasi QR
    st.markdown("**QR Code Pembayaran:**")
    st.code("QRIS: ruangteduh.ai/pay/TAVO-EMP-4900000")

    setuju_final = st.checkbox("Setuju Rp X/bulan - Saya sudah memberikan email yang benar", key="setuju_final")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Kembali"):
            st.session_state.ruang = 2
            st.rerun()
    with c2:
        if st.button("✅ Bayar & Masuk Perpustakaan", type="primary", disabled=not setuju_final or not st.session_state.email):
            st.balloons()
            st.success(f"Pembayaran via QR/VA berhasil di-trigger! Cek email {st.session_state.email} bro. Lolos Etika.")

st.caption("v2.6 FLOATING DOT - 2026-09-02 - 1 Titik Kecil Klik → Full Chat - HP Worth It Full Width + Laptop - Harga X - No Prompt Format")
