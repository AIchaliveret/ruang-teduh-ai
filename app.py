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

# ===== CSS SEJAJAR GEMINI STYLE =====
st.markdown("""
<style>
[data-testid="column"] {
    align-self: flex-start !important;
}
.big-title { font-size:28px; font-weight:800; margin-bottom:0; }
.sub { color: #6b7280; margin-bottom:12px; }
.card { padding:16px; border-radius:16px; background:#f8fafc; border:1px solid #e5e7eb; margin-bottom:12px; }
.right-panel {
    background:#ffffff;
    border:1px solid #e5e7eb;
    border-radius:16px;
    padding:16px;
    position: sticky;
    top: 20px;
    height: calc(100vh - 40px);
    display: flex;
    flex-direction: column;
}
.chat-scroll {
    flex: 1;
    overflow-y: auto;
    margin-bottom:12px;
    padding-right:4px;
}
.chat-bubble-user { background:#dbeafe; padding:10px 12px; border-radius:12px 12px 2px 12px; margin:8px 0; font-size:14px; }
.chat-bubble-ai { background:#f3f4f6; padding:10px 12px; border-radius:12px 12px 12px 2px; margin:8px 0; border:1px solid #e5e7eb; font-size:14px; }
</style>
""", unsafe_allow_html=True)

# HEADER FULL WIDTH
st.markdown('<div class="big-title">🏠 RUANG TEDUH AI - TAVO MALKHUTKHA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Two Journeys, One QR | Wellbeing Library - Kerja max 60km dari rumah</div>', unsafe_allow_html=True)
st.progress(st.session_state.room / 3, text=f"Ruang {st.session_state.room} dari 3")
st.markdown("")

# 2 KOLOM SEJAJAR
col_main, col_ai = st.columns([2.6, 1], gap="large")

with col_main:
    if st.session_state.room == 1:
        st.header("Ruang 1: Pintu Masuk Perpustakaan")
        st.write("Member masuk via QR -> Pilih jalur lo")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("👨‍💼 Employee", use_container_width=True, key="emp"):
                st.session_state.tipe_member = "Employee"
        with c2:
            if st.button("🚀 Entrepreneur", use_container_width=True, key="ent"):
                st.session_state.tipe_member = "Entrepreneur"
        if st.session_state.tipe_member:
            st.success(f"Jalur terpilih: {st.session_state.tipe_member} - Rate {'200rb' if st.session_state.tipe_member=='Employee' else '300rb'}/bulan")
        st.session_state.nama_member = st.text_input("Nama Lengkap", value=st.session_state.nama_member, placeholder="Tulis nama lo...")
        st.markdown("### 🔊 Suara Teduh Hari Ini")
        st.markdown("**Kolose 3:23 & Amsal 16:3** - Apapun yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
        st.caption("Visual + teks cukup - audio jadi penuntun")
        if st.button("➡️ Masuk Ruang 2", type="primary", use_container_width=True):
            if not st.session_state.nama_member:
                st.warning("Isi nama dulu bro")
            elif not st.session_state.tipe_member:
                st.warning("Pilih Employee / Entrepreneur dulu")
            else:
                st.session_state.room = 2
                st.rerun()
    elif st.session_state.room == 2:
        st.header(f"Ruang 2: Perjalanan {st.session_state.tipe_member}")
        st.write(f"Halo {st.session_state.nama_member}, ini jalur {st.session_state.tipe_member} lo")
        if st.session_state.tipe_member == "Employee":
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("👨‍💼 Employee - Chef, Staff, Barista, IT Staff")
            umr = st.number_input("UMR Domisili Lo (Rp)", value=4900000, step=100000)
            st.write(f"Estimasi 5% wellbeing: Rp {umr*0.05:,.0f}")
            st.markdown("**Biaya Langganan FIXED: Rp 200.000 / bulan**")
            st.markdown("Fasilitas: 3 Kolom + SOP + KPI + Mood Tracker")
            st.markdown('</div>', unsafe_allow_html=True)
            biaya = 200000
        else:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🚀 Entrepreneur - Boss Kios / Ruko / Rukan")
            omzet = st.number_input("Omzet Bulanan (Rp)", value=20000000, step=1000000)
            st.write(f"Profit 20%: Rp {omzet*0.2:,.0f}")
            st.markdown("**Biaya Langganan FIXED: Rp 300.000 / bulan**")
            st.markdown("Fasilitas: 3 Kolom + ERP + OEE + Vendor + 12 Folder GDrive")
            st.markdown('</div>', unsafe_allow_html=True)
            biaya = 300000
        tab1, tab2, tab3 = st.tabs(["Kolom 1: Fondasi", "Kolom 2: Perjalanan", "Kolom 3: Puncak"])
        with tab1:
            st.write("**Fondasi Teduh - Mindset & Niat**")
            st.image("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600", caption="Fondasi")
            st.write("Dokumen: Kolom1_Fondasi.pdf dari GDrive")
        with tab2:
            st.write("**Perjalanan Kerja - Ikhtiar & Skill**")
            st.image("https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=600", caption="Perjalanan")
            st.write("Dokumen: Kolom2_Perjalanan.pdf dari GDrive")
        with tab3:
            st.write("**Puncak Teduh - Tawakal & Makna**")
            st.image("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600", caption="Puncak")
            st.write("Dokumen: Kolom3_Puncak.pdf dari GDrive")
        st.markdown(f"### 💳 Keterikatan: Rp {biaya:,} / bulan")
        setuju = st.checkbox(f"Gua setuju langganan {st.session_state.tipe_member} Rp {biaya:,}/bulan setiap bulan")
        b1, b2 = st.columns(2)
        with b1:
            if st.button("⬅️ Kembali Ruang 1", use_container_width=True):
                st.session_state.room = 1
                st.rerun()
        with b2:
            if st.button("➡️ Masuk Ruang 3", type="primary", use_container_width=True):
                if not setuju:
                    st.warning("Centang dulu bro")
                else:
                    st.session_state.room = 3
                    st.rerun()
    else:
        st.header("Ruang 3: Corporation Access & Jaminan")
        st.balloons()
        st.success(f"Selamat {st.session_state.nama_member}! Member {st.session_state.tipe_member}")
        biaya = 200000 if st.session_state.tipe_member == "Employee" else 300000
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💰 Hitungan Bisnis - Hackathon Ready")
        st.write(f"- 100 member x Rp {biaya:,} = Rp {100*biaya:,}/bulan")
        st.write(f"- 1000 member x Rp {biaya:,} = Rp {1000*biaya:,}/bulan")
        st.write("**Mix 500+500 = Rp 250jt/bulan recurring!**")
        st.markdown('</div>', unsafe_allow_html=True)
        st.write("📂 12 Folder GDrive: SOP | ERP | OEE | KPI | Vendor | Mood | Docs | Audio | Member | Finance | Legal | Report")
        if st.button("🔄 Ulangi dari Ruang 1", use_container_width=True):
            st.session_state.room = 1
            st.rerun()

with col_ai:
    st.markdown('<div class="right-panel">', unsafe_allow_html=True)
    st.markdown("### 🤖 Meta AI - Tanya Teduh")
    st.caption(f"Sejajar | Ruang {st.session_state.room} | {st.session_state.tipe_member or 'Belum pilih jalur'}")
    st.divider()
    st.markdown('<div class="chat-scroll">', unsafe_allow_html=True)
    if not st.session_state.chat_history:
        st.markdown(f'<div class="chat-bubble-ai">🧘 Halo bro! Gua di kanan sini standby. Lu lagi di Ruang {st.session_state.room} - tanya apa aja, gua arahin langsung.</div>', unsafe_allow_html=True)
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user">🧑‍💼 {chat["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-ai">🧘 {chat["text"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    tanya = st.text_input("Tanya", placeholder="Gua stress commute 2 jam...", key="tanya_kanan_sejajar", label_visibility="collapsed")
    col_kirim, col_hapus = st.columns([3,1])
    with col_kirim:
        if st.button("Kirim 💬", use_container_width=True, type="primary"):
            if tanya:
                st.session_state.chat_history.append({"role":"user", "text": tanya})
                if st.session_state.room == 1:
                    prefix = "Lu di Ruang 1 - Pintu Masuk. "
                elif st.session_state.room == 2:
                    prefix = f"Lu di Ruang 2 jalur {st.session_state.tipe_member}. "
                else:
                    prefix = "Lu di Ruang 3 Corporation. "
                rate = "200rb" if st.session_state.tipe_member=="Employee" else "300rb" if st.session_state.tipe_member=="Entrepreneur" else "200rb/300rb"
                jawaban = f"{prefix}Soal '{tanya}' -> ingat 3 Kolom: Fondasi (niat ibadah Kolose 3:23), Perjalanan (kerja max 60km), Puncak (tawakal). Rate lo {rate}/bulan. Cek kiri ya."
                st.session_state.chat_history.append({"role":"ai", "text": jawaban})
                st.rerun()
    with col_hapus:
        if st.button("🗑️", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    st.divider()
    st.markdown("**Quick Arahan:**")
    if st.button("🧘 Cara nggak burnout?", use_container_width=True, key="q1"):
        st.session_state.chat_history.append({"role":"user", "text":"Cara nggak burnout?"})
        st.session_state.chat_history.append({"role":"ai", "text":"Ruang 2 - 3 langkah: 1) Fondasi: niat ibadah, 2) Perjalanan: kerja max 60km, 3) Puncak: tawakal. Lihat tab Kolom 1-3 di kiri."})
        st.rerun()
    if st.button("💰 Hitung langganan?", use_container_width=True, key="q2"):
        st.session_state.chat_history.append({"role":"user", "text":"Hitung langganan?"})
        st.session_state.chat_history.append({"role":"ai", "text":"Employee 200rb/bulan, Entrepreneur 300rb/bulan. 1000 member mix = 250jt/bulan recurring. Keterikatan setiap bulan!"})
        st.rerun()
    if st.button(f"📍 Gua di Ruang {st.session_state.room}, next apa?", use_container_width=True, key="q3"):
        if st.session_state.room == 1:
            txt = "Di Ruang 1: pilih Employee/Entrepreneur + isi nama + klik Masuk Ruang 2 di kiri bawah."
        elif st.session_state.room == 2:
            txt = "Di Ruang 2: cek 3 tab Kolom, centang setuju langganan, klik Masuk Ruang 3."
        else:
            txt = "Di Ruang 3: lo udah resmi! Cek hitungan bisnis & 12 Folder GDrive."
        st.session_state.chat_history.append({"role":"user", "text":f"Gua di Ruang {st.session_state.room}, next apa?"})
        st.session_state.chat_history.append({"role":"ai", "text": txt})
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.caption("v2.3 SEJAJAR - 2026-09-02 - Layout Kanan Kiri Rata Atas Persis Kayak Gemini - Fixed Rate 200rb/300rb")
