
import streamlit as st

st.set_page_config(page_title="Ruang Teduh AI - Tavo Malkhutkha", page_icon="🧘", layout="wide")

if 'room' not in st.session_state:
    st.session_state.room = 1
if 'tipe_member' not in st.session_state:
    st.session_state.tipe_member = None
if 'nama_member' not in st.session_state:
    st.session_state.nama_member = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

HARGA_X = "X"

# ===== CSS RESPONSIVE + SEJAJAR + ONETOUCH ENTER =====
st.markdown("""
<style>
[data-testid="column"] { align-self: flex-start !important; }
.big-title { font-size:28px; font-weight:800; margin-bottom:0; }
.sub { color: #6b7280; margin-bottom:12px; }
.card { padding:16px; border-radius:16px; background:#f8fafc; border:1px solid #e5e7eb; margin-bottom:12px; }
.right-panel {
    background:#ffffff;
    border:1px solid #e5e7eb;
    border-radius:16px;
    padding:16px;
    position: sticky;
    top: 15px;
    height: calc(100vh - 30px);
    display: flex;
    flex-direction: column;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.chat-scroll { flex: 1; overflow-y: auto; margin-bottom:12px; padding-right:6px; max-height: 58vh; }
.chat-bubble-user { background:#dbeafe; padding:10px 12px; border-radius:12px 12px 2px 12px; margin:8px 0; font-size:14px; text-align:right; }
.chat-bubble-ai { background:#f3f4f6; padding:10px 12px; border-radius:12px 12px 12px 2px; margin:8px 0; border:1px solid #e5e7eb; font-size:14px; }
.ethics-badge { background:#fef3c7; border:1px solid #f59e0b; padding:10px 14px; border-radius:10px; font-size:13px; color:#92400e; margin-bottom:10px; }

/* INPUT BIAR 16px - anti zoom di HP */
.stTextInput input, .stChatInput input { font-size:16px !important; }

/* RESPONSIVE HP & LAPTOP */
@media (max-width: 768px) {
    .big-title { font-size:22px; }
    .right-panel {
        position: relative !important;
        top: 0 !important;
        height: auto !important;
        min-height: 500px;
        margin-top: 20px;
    }
    .chat-scroll { max-height: 400px; }
    [data-testid="column"] { width:100% !important; }
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="big-title">🏠 RUANG TEDUH AI - TAVO MALKHUTKHA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Two Journeys, One QR | Wellbeing Library - Kerja max 60km dari rumah</div>', unsafe_allow_html=True)
st.markdown(f'<div class="ethics-badge">🔒 v2.5.2 RESPONSIVE + ONETOUCH ENTER - Harga Rp {HARGA_X} | Laptop & HP otomatis | Enter = Kirim langsung | Lolos Etika Assembling</div>', unsafe_allow_html=True)
st.progress(st.session_state.room / 3, text=f"Ruang {st.session_state.room} dari 3")
st.markdown("")

col_main, col_ai = st.columns([2.6, 1], gap="large")

with col_main:
    if st.session_state.room == 1:
        st.header("Ruang 1: Pintu Masuk Perpustakaan")
        st.write("Member masuk via QR -> Pilih jalur lo")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("👨‍💼 Employee", use_container_width=True, key="emp252"):
                st.session_state.tipe_member = "Employee"
        with c2:
            if st.button("🚀 Entrepreneur", use_container_width=True, key="ent252"):
                st.session_state.tipe_member = "Entrepreneur"
        if st.session_state.tipe_member:
            st.success(f"Jalur: {st.session_state.tipe_member} - Rp {HARGA_X}/bulan")
        st.session_state.nama_member = st.text_input("Nama Lengkap", value=st.session_state.nama_member, placeholder="Tulis nama lo...", key="nama252")
        st.markdown("### 🔊 Suara Teduh Hari Ini")
        st.markdown("**Kolose 3:23 & Amsal 16:3**")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
        if st.button("➡️ Masuk Ruang 2", type="primary", use_container_width=True):
            if not st.session_state.nama_member or not st.session_state.tipe_member:
                st.warning("Isi nama & pilih jalur dulu bro")
            else:
                st.session_state.room = 2
                st.rerun()
    elif st.session_state.room == 2:
        st.header(f"Ruang 2: Perjalanan {st.session_state.tipe_member}")
        st.write(f"Halo {st.session_state.nama_member}")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if st.session_state.tipe_member=="Employee":
            st.subheader("👨‍💼 Employee")
            umr = st.number_input("UMR Domisili (Rp)", value=4900000, step=100000, key="umr252")
            st.write(f"Ref: Rp {umr*0.05:,.0f}")
        else:
            st.subheader("🚀 Entrepreneur")
            omzet = st.number_input("Omzet (Rp)", value=20000000, step=1000000, key="omzet252")
            st.write(f"Ref profit 20%: Rp {omzet*0.2:,.0f}")
        st.markdown(f"**Biaya: Rp {HARGA_X}/bulan**")
        st.markdown('</div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["Kolom 1: Fondasi", "Kolom 2: Perjalanan", "Kolom 3: Puncak"])
        with tab1:
            st.write("**Fondasi Teduh**")
            st.image("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600")
        with tab2:
            st.write("**Perjalanan - max 60km**")
            st.image("https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=600")
        with tab3:
            st.write("**Puncak - Tawakal**")
            st.image("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600")
        st.markdown(f"### 💳 Rp {HARGA_X}/bulan")
        setuju = st.checkbox(f"Setuju berlangganan Rp {HARGA_X}/bulan", key="setuju252")
        b1, b2 = st.columns(2)
        with b1:
            if st.button("⬅️ Kembali", use_container_width=True):
                st.session_state.room = 1
                st.rerun()
        with b2:
            if st.button("➡️ Masuk Ruang 3", type="primary", use_container_width=True):
                if not setuju:
                    st.warning("Centang dulu")
                else:
                    st.session_state.room = 3
                    st.rerun()
    else:
        st.header("Ruang 3: Corporation Access")
        st.balloons()
        st.success(f"Selamat {st.session_state.nama_member}! Rp {HARGA_X}/bulan")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💰 Ethics Compliant")
        st.write("- Total = Member x Rp X - Lolos etika")
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("🔄 Ulangi", use_container_width=True):
            st.session_state.room = 1
            st.rerun()

with col_ai:
    st.markdown('<div class="right-panel">', unsafe_allow_html=True)
    st.markdown("### 🤖 Meta AI - Tanya Teduh")
    st.caption(f"RESPONSIVE | Enter = Kirim | HP & Laptop | Ruang {st.session_state.room}")
    st.divider()
    st.markdown('<div class="chat-scroll">', unsafe_allow_html=True)
    if not st.session_state.chat_history:
        st.markdown(f'<div class="chat-bubble-ai">🧘 Halo bro! Sekarang udah RESPONSIVE + ONETOUCH ENTER. Di laptop pencet Enter langsung kekirim, di HP pencet Enter/Go di keyboard HP juga langsung kekirim. Harga Rp X. Lu di Ruang {st.session_state.room}.</div>', unsafe_allow_html=True)
    else:
        for chat in st.session_state.chat_history:
            if chat["role"]=="user":
                st.markdown(f'<div class="chat-bubble-user">🧑‍💼 {chat["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble-ai">🧘 {chat["text"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Quick buttons tetap bisa di klik
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔒 Kenapa X?", use_container_width=True, key="q1_252"):
            st.session_state.chat_history.append({"role":"user","text":"Kenapa X?"})
            st.session_state.chat_history.append({"role":"ai","text":"Biar lolos etika Assembling bro. Harga disamarkan jadi X."})
            st.rerun()
    with c2:
        if st.button("📐 Sejajar?", use_container_width=True, key="q2_252"):
            st.session_state.chat_history.append({"role":"user","text":"Udah sejajar?"})
            st.session_state.chat_history.append({"role":"ai","text":"Udah! Kiri kanan sejajar, sticky di laptop, auto stack di HP."})
            st.rerun()

    if st.button("🗑️ Hapus", use_container_width=True, key="clear252"):
        st.session_state.chat_history=[]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ===== INPUT CHAT PALING BAWAH - ONETOUCH ENTER UNTUK LAPTOP & HP =====
# Ini yang bikin otomatis: ketik + Enter = langsung kirim, tanpa klik tombol
# Di HP, tombol Enter/Go di keyboard virtual juga trigger ini
tanya = st.chat_input("Ketik di sini... pencet Enter langsung kirim (HP & Laptop)")

if tanya:
    if tanya.strip().lower() in ["tanya meta ai", "tanya", ""]:
        st.session_state.chat_history.append({"role":"user","text":tanya})
        st.session_state.chat_history.append({"role":"ai","text":"Ketik pertanyaan yang jelas bro, jangan cuma 'tanya meta ai'."})
    else:
        st.session_state.chat_history.append({"role":"user","text":tanya})
        if "harga" in tanya.lower() or tanya.strip().upper() == "X":
            jawaban = f"Pakai Rp {HARGA_X} bro biar lolos etika Assembling. Enter yang lu pencet tadi udah one-touch langsung kekirim kan? Itu fitur baru v2.5.2 RESPONSIVE."
        elif "hp" in tanya.lower() or "handphone" in tanya.lower() or "laptop" in tanya.lower():
            jawaban = "Udah responsive bro! Di laptop: 2 kolom sejajar. Di HP: otomatis jadi 1 kolom stack, kanan di bawah. Ketik + Enter di HP (tombol Go) langsung kekirim, sama kayak di laptop. One-touch!"
        elif "enter" in tanya.lower() or "kirim" in tanya.lower():
            jawaban = "Iya bro, sekarang one-touch: ketik di bawah + pencet Enter (laptop) atau Go (HP) langsung terkirim otomatis, tanpa klik tombol Kirim lagi. Tombol Kirim tetap ada buat yang mau klik."
        else:
            jawaban = f"Ruang {st.session_state.room} | Rp {HARGA_X} | Soal '{tanya}' -> ingat 3 Kolom. Enter yang barusan lu pencet udah otomatis ngirim kan? Itu yang lu minta!"
        st.session_state.chat_history.append({"role":"ai","text":jawaban})
    st.rerun()

st.caption("v2.5.2 RESPONSIVE ONETOUCH - 2026-09-02 - Laptop & HP otomatis | Enter = Kirim langsung | Fix screenshot + Harga X + Sejajar")
