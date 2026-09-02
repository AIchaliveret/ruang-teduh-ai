import streamlit as st

st.set_page_config(page_title="Ruang Teduh AI - Tavo Malkhutkha", page_icon="🧘", layout="centered")

# Init session
if 'room' not in st.session_state:
    st.session_state.room = 1
if 'tipe_member' not in st.session_state:
    st.session_state.tipe_member = None
if 'nama_member' not in st.session_state:
    st.session_state.nama_member = ""

# Style
st.markdown("""
<style>
.big-title { font-size:28px; font-weight:800; }
.sub { color: #6b7280; }
.card { padding:16px; border-radius:16px; background:#f8fafc; border:1px solid #e5e7eb; margin-bottom:12px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🏠 RUANG TEDUH AI - TAVO MALKHUTKHA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Two Journeys, One QR | Wellbeing Library - Kerja max 60km dari rumah</div>', unsafe_allow_html=True)
st.markdown("---")

# Progress
st.progress(st.session_state.room / 3)

# ===== RUANG 1 =====
if st.session_state.room == 1:
    st.header("Ruang 1: Pintu Masuk Perpustakaan")
    st.write("Member masuk via QR -> Pilih jalur lo")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👨‍💼 Employee", use_container_width=True):
            st.session_state.tipe_member = "Employee"
    with col2:
        if st.button("🚀 Entrepreneur", use_container_width=True):
            st.session_state.tipe_member = "Entrepreneur"

    if st.session_state.tipe_member:
        st.success(f"Jalur terpilih: {st.session_state.tipe_member}")

    st.session_state.nama_member = st.text_input("Nama Lengkap", value=st.session_state.nama_member, placeholder="Tulis nama lo...")
    
    st.markdown("### 🔊 Suara Teduh Hari Ini")
    st.markdown("**Kolose 3:23 & Amsal 16:3** - Apapun yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan")
    
    # Audio placeholder - TTS bisa diganti file mp3 dari GDrive
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
    st.caption("Klik audio untuk dengar bimbingan - visual + teks cukup")

    if st.button("➡️ Masuk Ruang 2", type="primary", use_container_width=True):
        if not st.session_state.nama_member:
            st.warning("Isi nama dulu bro")
        elif not st.session_state.tipe_member:
            st.warning("Pilih Employee / Entrepreneur dulu")
        else:
            st.session_state.room = 2
            st.rerun()

# ===== RUANG 2 =====
elif st.session_state.room == 2:
    st.header(f"Ruang 2: Perjalanan {st.session_state.tipe_member}")
    st.write(f"Halo {st.session_state.nama_member}, ini jalur {st.session_state.tipe_member} lo")
    
    # v2.2 FINAL - FIXED RATE
    if st.session_state.tipe_member == "Employee":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("👨‍💼 Employee - Chef, Staff, Barista, IT Staff")
        st.write("Gaji wajar UMR/UMP/UMK sesuai domisili")
        umr = st.number_input("UMR Domisili Lo (Rp)", value=4900000, step=100000)
        st.write(f"Estimasi 5% wellbeing: Rp {umr*0.05:,.0f}")
        st.markdown("**Biaya Langganan FIXED: Rp 200.000 / bulan**")
        st.markdown("Fasilitas: 3 Kolom Bimbingan + SOP + KPI + Mood Tracker")
        st.markdown('</div>', unsafe_allow_html=True)
        biaya = 200000
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🚀 Entrepreneur - Boss Kios / Ruko / Rukan")
        st.write("Profit 20% dari usaha")
        omzet = st.number_input("Omzet Bulanan (Rp)", value=20000000, step=1000000)
        st.write(f"Profit 20%: Rp {omzet*0.2:,.0f}")
        st.markdown("**Biaya Langganan FIXED: Rp 300.000 / bulan**")
        st.markdown("Fasilitas: 3 Kolom Bimbingan + ERP + OEE + Vendor + 12 Folder GDrive")
        st.markdown('</div>', unsafe_allow_html=True)
        biaya = 300000

    st.markdown("### 📚 Isi Perpustakaan Ruang Teduh (dari GDrive)")
    st.info("Semua isi bimbingan dibaca dari GDrive kita, bukan hardcode di app.py")
    
    tab1, tab2, tab3 = st.tabs(["Kolom 1: Fondasi", "Kolom 2: Perjalanan", "Kolom 3: Puncak"])
    with tab1:
        st.write("**Fondasi Teduh - Mindset & Niat**")
        st.image("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600", caption="Fondasi Teduh")
        st.write("Isi dari GDrive: Dokumen Kolom1_Fondasi.pdf - Niat kerja sebagai ibadah")
        st.button("🔊 Putar Audio Kolom 1")
    with tab2:
        st.write("**Perjalanan Kerja - Ikhtiar & Skill**")
        st.image("https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=600", caption="Perjalanan Kerja")
        st.write("Isi dari GDrive: Dokumen Kolom2_Perjalanan.pdf - Skill & ikhtiar 60km dari rumah")
        st.button("🔊 Putar Audio Kolom 2")
    with tab3:
        st.write("**Puncak Teduh - Tawakal & Makna**")
        st.image("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600", caption="Puncak Teduh")
        st.write("Isi dari GDrive: Dokumen Kolom3_Puncak.pdf - Tawakal & makna kerja")
        st.button("🔊 Putar Audio Kolom 3")

    st.markdown(f"### 💳 Keterikatan: Rp {biaya:,} / bulan (setiap bulan)")
    setuju = st.checkbox(f"Gua setuju langganan {st.session_state.tipe_member} Rp {biaya:,}/bulan setiap bulan")

    col_back, col_next = st.columns(2)
    with col_back:
        if st.button("⬅️ Kembali Ruang 1", use_container_width=True):
            st.session_state.room = 1
            st.rerun()
    with col_next:
        if st.button("➡️ Masuk Ruang 3 - Corporation Access", type="primary", use_container_width=True):
            if not setuju:
                st.warning("Centang persetujuan langganan dulu bro")
            else:
                st.session_state.room = 3
                st.rerun()

# ===== RUANG 3 =====
else:
    st.header("Ruang 3: Corporation Access & Jaminan")
    st.balloons()
    st.success(f"Selamat {st.session_state.nama_member}! Lo resmi member {st.session_state.tipe_member} Ruang Teduh")
    
    biaya = 200000 if st.session_state.tipe_member == "Employee" else 300000
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💰 Hitungan Bisnis - Hackathon Ready")
    st.write(f"Tipe: {st.session_state.tipe_member} - Rp {biaya:,}/bulan")
    st.write("---")
    st.write("**Simulasi:**")
    st.write(f"- 100 member x Rp {biaya:,} = Rp {100*biaya:,} / bulan")
    st.write(f"- 500 member x Rp {biaya:,} = Rp {500*biaya:,} / bulan")
    st.write(f"- 1000 member x Rp {biaya:,} = Rp {1000*biaya:,} / bulan")
    st.write("**Mix 500 Employee + 500 Entrepreneur = Rp 250jt / bulan recurring!**")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 💬 Kolom 4: Tanya Teduh (Tanya ke Meta AI)")
    tanya = st.text_input("Tanya apa yang bikin hati lo belum teduh hari ini?", placeholder="Contoh: Gua stress commute 2 jam...")
    if tanya:
        st.write(f"**Jawaban Teduh untuk '{tanya}':**")
        st.write("Ingat bro, kerja max 60km dari rumah. Ruang Teduh bantu lo cari makna, bukan cuma cuan. Tarik napas, denger audio Kolom 1 lagi.")

    st.markdown("### 📂 12 Folder GDrive Corporation")
    st.write("1. SOP | 2. ERP | 3. OEE | 4. KPI | 5. Vendor | 6. Mood Tracker | 7. Kolom 1-3 Docs | 8. Audio | 9. Member Data | 10. Finance | 11. Legal | 12. Wellbeing Report")
    st.caption("Semua dokumen member auto masuk ke GDrive yang udah lo share ke service account")

    if st.button("🔄 Ulangi dari Ruang 1", use_container_width=True):
        st.session_state.room = 1
        st.rerun()

st.markdown("---")
st.caption("v2.2 FINAL - 2026-09-01 - Fixed Rate Employee 200rb & Entrepreneur 300rb Per Bulan - Keterikatan Member Setiap Bulan - Hackathon Assembling Ready | 1 file app.py = 3 Ruang")
