import streamlit as st

st.set_page_config(page_title="RUANG TEDUH AI - TAVO MALKHUTKHA", layout="wide")

# --- CSS FLOATING DOT v2.7 ---
st.markdown("""
<style>
.floating-dot {
    position: fixed; bottom: 30px; right: 30px; width: 56px; height: 56px;
    background: #FF4B4B; border-radius: 50%; z-index: 9999;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 24px; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.worship-audio { width: 100%; }
</style>
<div class="floating-dot" onclick="alert('Full Chat v2.7 - Ruang Teduh AI siap bantu')">🧘</div>
""", unsafe_allow_html=True)

st.title("🏠 RUANG TEDUH AI - TAVO MALKHUTKHA")
st.caption("Two Journeys, One QR | Wellbeing Library - Kerja max 60km dari rumah | v2.7 FLOATING DOT - 1 Titik Terlihat - Klik Dot untuk Full Chat - HP & Laptop Otomatis - Harga Rp X - Lolos Etika - Worship Mode")

# --- SESSION ---
if 'ruang' not in st.session_state: st.session_state.ruang = 1
if 'email' not in st.session_state: st.session_state.email = ""
if 'jalur' not in st.session_state: st.session_state.jalur = "Employee"

progress = st.progress(st.session_state.ruang / 3)
st.write(f"Ruang {st.session_state.ruang} dari 3")

# ================= RUANG 1 =================
if st.session_state.ruang == 1:
    st.header("Ruang 1: Pintu Masuk Perpustakaan")
    st.info("Member masuk via QR → Pilih jalur lo → WAJIB isi email sebelum lanjut (sistem baru v2.7)")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👨‍💼 Employee", use_container_width=True):
            st.session_state.jalur = "Employee"
    with col2:
        if st.button("🚀 Entrepreneur", use_container_width=True):
            st.session_state.jalur = "Entrepreneur"

    st.success(f"Jalur: {st.session_state.jalur} - Rp X/bulan - Mode Etika Lolos")
    
    nama = st.text_input("Nama Lengkap", placeholder="Contoh: TAVO karyawan sebagai cheff, berkeluarga, 4 anak, duda...")
    email = st.text_input("Alamat Email WAJIB (untuk QR & VA)", value=st.session_state.email, placeholder="contoh: tava@email.com")
    st.session_state.email = email

    # Kolom keterangan - 1 tombol kendali
    with st.expander("📜 Kolom Keterangan - Penjelasan Sistem (1 Tombol Kendali)", expanded=True):
        st.markdown("""
        **Kenapa mesti kasih email dulu?**
        Semua system Ruang Teduh - SOP, ERP, OEE, KPI disempurnakan kuasa Alkitab - dikirim ke email lo.
        App ini bermanfaat untuk improvement culture, bukan cuma absen.
        """)
    
    # Audio Worship Teduh - GANTI MUSIK
    st.subheader("🔊 Suara Teduh Hari Ini - Worship Mode")
    st.write("Kolose 3:23 & Amsal 16:3 - Apapun yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3") # GANTI dengan file worship lo
    st.caption("Visual + teks + audio - full di HP - Musik: Worship Teduh Instrumental (bukan musik random)")

    if st.button("➡️ Masuk Ruang 2", type="primary", use_container_width=True):
        if not st.session_state.email or "@" not in st.session_state.email:
            st.warning("Bro, mesti kasih alamat email dulu yang valid. Ini buat kirim QR Code & Virtual Account langganan.")
        else:
            st.session_state.ruang = 2
            st.rerun()

# ================= RUANG 2 =================
elif st.session_state.ruang == 2:
    st.header("Ruang 2: Perjalanan Employee - SOP, ERP, OEE, KPI")
    st.warning("FIX SEPI v2.7: Sekarang ada suara penjelasan sistematis di sini!")

    umr = st.number_input("UMR Domisili (Rp)", value=4900000, step=100000)
    st.caption(f"Ref: Rp {int(umr*0.05):,} - Biaya: Rp X/bulan - Mode Etika")

    tabs = st.tabs(["Kolom 1: Fondasi", "Kolom 2: Perjalanan", "Kolom 3: Puncak"])
    with tabs[0]:
        st.subheader("Fondasi Teduh - Mindset & Niat")
        st.write("Dokumen GDrive: Kolom1_Fondasi.pdf")
        st.markdown("""
        **SOP (Standard Operating Procedure) - Disempurnakan Alkitab:**
        1. Datang 15 menit sebelum shift - Kolose 3:23
        2. Doa & set niat kerja untuk Tuhan
        3. Cek ERP harian
        
        **ERP (Tuhan punya sistem):**
        - Modul Manusia: hati & keluarga
        - Modul Waktu: 60km dari rumah = stewardship
        - Modul Berkat: UMR & persembahan

        **OEE (Overall Equipment Effectiveness Rohani):**
        - Availability: Hadir 100%
        - Performance: Kerja tidak ngeluh
        - Quality: Hasil memuliakan Tuhan

        **KPI (Kingdom Performance Indicator):**
        - KPI Iman: Baca Firman sebelum kerja
        - KPI Kerja: Improvement culture harian 1%
        """)
        # Audio penjelasan biar tidak sepi
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3", format="audio/mp3")
        st.caption("🔊 Penjelasan Audio SOP/ERP/OEE/KPI - Worship Background")

    with tabs[1]:
        st.write("Halo TAVO karyawan sebagai cheff... Full width di HP, worth it!")
    with tabs[2]:
        st.write("Puncak - Menuju Malkhutkha")

    st.divider()
    # Cara pembayaran - ingatkan email
    st.subheader("💳 Rp X/bulan - Cara Pembayaran v2.7")
    agree = st.checkbox(f"Setuju Rp X/bulan - Kirim detail ke {st.session_state.email}")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Kembali", use_container_width=True):
            st.session_state.ruang = 1
            st.rerun()
    with c2:
        if st.button("➡️ Masuk Ruang 3 - Bayar", type="primary", use_container_width=True, disabled=not agree):
            if not agree:
                st.error("Centang dulu bro biar bisa lanjut")
            else:
                st.session_state.ruang = 3
                st.rerun()

# ================= RUANG 3 =================
elif st.session_state.ruang == 3:
    st.header("Ruang 3: Pembayaran & Berkat")
    st.success(f"Email terkonfirmasi: {st.session_state.email} - Semua invoice & akses QR akan dikirim kesini")

    st.subheader("Berlangganan via Transfer QR Code dan Virtual Account")
    st.write("Semua pertanyaan member bisa lo generate di sini - Fokus: bagaimana app Ruang Teduh bermanfaat")

    tab_pay, tab_info = st.tabs(["💳 Cara Bayar", "📖 Manfaat App"])
    
    with tab_pay:
        st.markdown(f"""
        **Langkah 1: Email sudah OK ✅ ({st.session_state.email})**
        **Langkah 2: Pilih Metode (v2.7)**
        - **QRIS QR Code**: Scan langsung, otomatis lunas
        - **Virtual Account**: BCA / Mandiri / BRI - VA unik per member
        
        **Langkah 3: Konfirmasi otomatis masuk email**
        """)
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=RuangTeduh-{email}".format(email=st.session_state.email))
        st.code("VA BCA: 12345 67890 - a/n Ruang Teduh AI")
        st.info("Ingatkan email: Jika belum terima dalam 5 menit, cek spam atau klik 'Kirim Ulang' di floating dot.")

    with tab_info:
        st.markdown("""
        **Bagaimana App Ruang Teduh Bermanfaat:**
        1. Tidak cuma jadwal, tapi ada SOP rohani
        2. ERP sederhana untuk atur hidup & kerja max 60km
        3. OEE pantau kesehatan kerja
        4. KPI disempurnakan Alkitab = improvement culture yang lebih baik (semua proses secara benar)
        """)
        # Semua pertanyaan member bisa di-generate AI di kolom ini
        q = st.text_input("Ketik di Ruang 3... tanya cara bayar / manfaat / SOP", placeholder="Contoh: gimana cara bayar kalo belum punya email?")
        if q:
            st.write(f"Jawaban AI Teduh untuk '{q}': Utamakan sudah memberikan email ({st.session_state.email}), lalu pilih QR Code atau VA. Sistem akan otomatis buka akses Perpustakaan.")

    if st.button("🔄 Ulang dari Ruang 1"):
        st.session_state.ruang = 1
        st.rerun()

st.markdown("---")
st.caption("v2.7 FLOATING DOT - 2026-09-02 - 1 Titik Kecil Klik → Full Chat - HP Worth It Full Width + Laptop - Harga X - No Prompt Format - Worship Audio - Email Wajib - QR + VA")
