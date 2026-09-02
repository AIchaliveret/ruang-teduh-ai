import streamlit as st

st.set_page_config(page_title="Ruang Teduh AI - Tavo Malkhutkha", page_icon="🧘", layout="wide")

# Init session
if 'room' not in st.session_state:
    st.session_state.room = 1
if 'tipe_member' not in st.session_state:
    st.session_state.tipe_member = None
if 'nama_member' not in st.session_state:
    st.session_state.nama_member = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Style
st.markdown("""
<style>
.big-title { font-size:28px; font-weight:800; }
.sub { color: #6b7280; }
.card { padding:16px; border-radius:16px; background:#f8fafc; border:1px solid #e5e7eb; margin-bottom:12px; }
.right-panel { background:#ffffff; border-left:2px solid #e5e7eb; padding:16px; border-radius:12px; height:80vh; overflow-y:auto; position:sticky; top:20px; }
.chat-bubble-user { background:#dbeafe; padding:10px; border-radius:12px; margin:6px 0; }
.chat-bubble-ai { background:#f3f4f6; padding:10px; border-radius:12px; margin:6px 0; border:1px solid #e5e7eb; }
</style>
""", unsafe_allow_html=True)

# ===== LAYOUT UTAMA: KIRI KONTEN, KANAN AI (kayak Gemini) =====
col_main, col_ai = st.columns([2.2, 1])

with col_main:
    st.markdown('<div class="big-title">🏠 RUANG TEDUH AI - TAVO MALKHUTKHA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub">Two Journeys, One QR | Wellbeing Library - Kerja max 60km dari rumah</div>', unsafe_allow_html=True)
    st.markdown("---")
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
        
        if st.session_state.tipe_member == "Employee":
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("👨‍💼 Employee - Chef, Staff, Barista, IT Staff")
            umr = st.number_input("UMR Domisili Lo (Rp)", value=4900000, step=100000)
            st.write(f"Estimasi 5% wellbeing: Rp {umr*0.05:,.0f}")
            st.markdown("**Biaya Langganan FIXED: Rp 200.000 / bulan**")
            st.markdown('</div>', unsafe_allow_html=True)
            biaya = 200000
        else:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🚀 Entrepreneur - Boss Kios / Ruko / Rukan")
            omzet = st.number_input("Omzet Bulanan (Rp)", value=20000000, step=1000000)
            st.write(f"Profit 20%: Rp {omzet*0.2:,.0f}")
            st.markdown("**Biaya Langganan FIXED: Rp 300.000 / bulan**")
            st.markdown('</div>', unsafe_allow_html=True)
            biaya = 300000

        tab1, tab2, tab3 = st.tabs(["Kolom 1: Fondasi", "Kolom 2: Perjalanan", "Kolom 3: Puncak"])
        with tab1:
            st.write("**Fondasi Teduh - Mindset & Niat**")
            st.image("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600", caption="Fondasi Teduh")
            st.write("Isi dari GDrive: Dokumen Kolom1_Fondasi.pdf")
            st.button("🔊 Putar Audio Kolom 1")
        with tab2:
            st.write("**Perjalanan Kerja - Ikhtiar & Skill**")
            st.image("https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=600", caption="Perjalanan Kerja")
            st.write("Isi dari GDrive: Dokumen Kolom2_Perjalanan.pdf")
            st.button("🔊 Putar Audio Kolom 2")
        with tab3:
            st.write("**Puncak Teduh - Tawakal & Makna**")
            st.image("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600", caption="Puncak Teduh")
            st.write("Isi dari GDrive: Dokumen Kolom3_Puncak.pdf")
            st.button("🔊 Putar Audio Kolom 3")

        st.markdown(f"### 💳 Keterikatan: Rp {biaya:,} / bulan (setiap bulan)")
        setuju = st.checkbox(f"Gua setuju langganan {st.session_state.tipe_member} Rp {biaya:,}/bulan setiap bulan")

        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("⬅️ Kembali Ruang 1", use_container_width=True):
                st.session_state.room = 1
                st.rerun()
        with col_next:
            if st.button("➡️ Masuk Ruang 3", type="primary", use_container_width=True):
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
        st.write(f"- 100 member x Rp {biaya:,} = Rp {100*biaya:,} / bulan")
        st.write(f"- 1000 member x Rp {biaya:,} = Rp {1000*biaya:,} / bulan")
        st.write("**Mix 500+500 = Rp 250jt / bulan recurring!**")
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("🔄 Ulangi dari Ruang 1", use_container_width=True):
            st.session_state.room = 1
            st.rerun()

# ===== PANEL KANAN - META AI KAYAK GEMINI =====
with col_ai:
    st.markdown('<div class="right-panel">', unsafe_allow_html=True)
    st.markdown("### 🤖 Meta AI - Tanya Teduh")
    st.caption("Kayak Gemini di kanan - standby jawab")
    
    st.markdown("---")
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user">🧑‍💼 {chat["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-ai">🧘 {chat["text"]}</div>', unsafe_allow_html=True)

    st.markdown("---")
    tanya = st.text_input("Tanya apa yang bikin belum teduh?", placeholder="Gua stress commute...", key="tanya_kanan", label_visibility="collapsed")
    col_kirim, col_hapus = st.columns([2,1])
    with col_kirim:
        if st.button("Kirim 💬", use_container_width=True):
            if tanya:
                st.session_state.chat_history.append({"role":"user", "text": tanya})
                # Jawaban simpel - nanti bisa connect ke LLM API
                jawaban = f"Teduhin dulu bro: '{tanya}' - ingat kerja max 60km dari rumah. Coba denger audio Kolom 1 lagi, tarik napas. Lo jalur {st.session_state.tipe_member or '...'} rate { '200rb' if st.session_state.tipe_member=='Employee' else '300rb' if st.session_state.tipe_member=='Entrepreneur' else '...'} /bulan udah aman."
                st.session_state.chat_history.append({"role":"ai", "text": jawaban})
                st.rerun()
    with col_hapus:
        if st.button("Hapus", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("#### 📚 Quick Prompt")
    if st.button("🧘 Cara biar nggak burnout?", use_container_width=True):
        st.session_state.chat_history.append({"role":"user", "text":"Cara biar nggak burnout?"})
        st.session_state.chat_history.append({"role":"ai", "text":"3 langkah Ruang Teduh: 1) Fondasi - niat kerja ibadah (Kolose 3:23), 2) Perjalanan - kerja max 60km, 3) Puncak - tawakal. Denger audio Kolom 2 ya."})
        st.rerun()
    if st.button("💰 Hitung langganan?", use_container_width=True):
        st.session_state.chat_history.append({"role":"user", "text":"Hitung langganan?"})
        st.session_state.chat_history.append({"role":"ai", "text":"Employee 200rb/bulan, Entrepreneur 300rb/bulan. 1000 member mix = 250jt/bulan recurring. Keterikatan setiap bulan!"})
        st.rerun()

    st.markdown("---")
    st.caption("12 Folder GDrive | SOP ERP OEE KPI")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("v2.3 - 2026-09-02 - Layout Kanan Meta AI kayak Gemini - v2.2 Fixed Rate 200rb/300rb - Hackathon Assembling Ready")
