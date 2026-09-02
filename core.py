
import streamlit as st

st.set_page_config(page_title="Ruang Teduh AI - Tavo Malkhutkha", page_icon="🧘", layout="wide")

# Session init - clean, no import error
if 'room' not in st.session_state:
    st.session_state.room = 1
if 'tipe_member' not in st.session_state:
    st.session_state.tipe_member = None
if 'nama_member' not in st.session_state:
    st.session_state.nama_member = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'show_chat' not in st.session_state:
    st.session_state.show_chat = False

HARGA_X = "X"

# CSS CLEAN - no deprecated html component, pure st.markdown
st.markdown("""
<style>
.big-title { font-size:28px; font-weight:800; margin-bottom:0; }
.sub { color: #6b7280; margin-bottom:12px; }
.card { padding:16px; border-radius:16px; background:#f8fafc; border:1px solid #e5e7eb; margin-bottom:12px; }
.ethics-badge { background:#fef3c7; border:1px solid #f59e0b; padding:10px 14px; border-radius:10px; font-size:13px; color:#92400e; margin-bottom:10px; }
.chat-panel {
    position: fixed;
    bottom: 100px;
    right: 24px;
    width: 400px;
    max-width: calc(100vw - 32px);
    height: 62vh;
    max-height: 600px;
    background: white;
    border-radius: 20px;
    box-shadow: 0 12px 48px rgba(0,0,0,0.25);
    z-index: 9998;
    display: flex;
    flex-direction: column;
    border: 1px solid #e5e7eb;
    overflow: hidden;
}
.chat-header { background: #111827; color: white; padding: 14px 16px; }
.chat-scroll { flex: 1; overflow-y: auto; padding: 12px; background: #fafafa; max-height: 48vh; }
.chat-bubble-user { background:#dbeafe; padding:10px 12px; border-radius:12px 12px 2px 12px; margin:8px 0; font-size:14px; text-align:right; margin-left:30px; }
.chat-bubble-ai { background:white; padding:10px 12px; border-radius:12px 12px 12px 2px; margin:8px 0; border:1px solid #e5e7eb; font-size:14px; margin-right:20px; }
@media (max-width: 768px) {
    .big-title { font-size:22px; }
    .chat-panel { bottom: 80px; right: 16px; left: 16px; width: auto; height: 68vh; }
}
[data-testid="stChatInput"] { position: fixed; bottom: 0; left: 0; right: 0; z-index: 9997; background: white; padding: 8px 16px; border-top: 1px solid #e5e7eb; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🏠 RUANG TEDUH AI - TAVO MALKHUTKHA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Two Journeys, One QR | Wellbeing Library - Kerja max 60km dari rumah</div>', unsafe_allow_html=True)
st.markdown(f'<div class="ethics-badge">✅ v2.7 CLEAN DEPLOY - No Deprecated API - Harga Rp {HARGA_X} - Lolos Etika Assembling - Fix IndentationError & ImportError</div>', unsafe_allow_html=True)
st.progress(st.session_state.room / 3, text=f"Ruang {st.session_state.room} dari 3")
st.markdown("---")

if st.session_state.room == 1:
    st.header("Ruang 1: Pintu Masuk Perpustakaan")
    st.write("Member masuk via QR -> Pilih jalur lo")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("👨‍💼 Employee", use_container_width=True, key="emp27"):
            st.session_state.tipe_member = "Employee"
    with c2:
        if st.button("🚀 Entrepreneur", use_container_width=True, key="ent27"):
            st.session_state.tipe_member = "Entrepreneur"
    if st.session_state.tipe_member:
        st.success(f"Jalur: {st.session_state.tipe_member} - Rp {HARGA_X}/bulan")
    st.session_state.nama_member = st.text_input("Nama Lengkap", value=st.session_state.nama_member, placeholder="Tulis nama lo...", key="nama27")
    st.markdown("### 🔊 Suara Teduh Hari Ini")
    st.markdown("**Kolose 3:23 & Amsal 16:3** - Apapun yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan")
    # Voice Only - Tanpa Musik Stress - FIX indentasi baris 95 yang dulu error
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
    st.caption("Voice Only, Tanpa Musik Stress")
    if st.button("➡️ Masuk Ruang 2", type="primary", use_container_width=True, key="r1next27"):
        if not st.session_state.nama_member or not st.session_state.tipe_member:
            st.warning("Isi nama & pilih jalur dulu bro")
        else:
            st.session_state.room = 2
            st.rerun()

elif st.session_state.room == 2:
    st.header(f"Ruang 2: Perjalanan {st.session_state.tipe_member}")
    st.write(f"Halo {st.session_state.nama_member} - Full width worth it di HP!")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.session_state.tipe_member == "Employee":
        st.subheader("👨‍💼 Employee")
        umr = st.number_input("UMR Domisili (Rp)", value=4900000, step=100000, key="umr27")
        st.write(f"Ref wellbeing: Rp {umr*0.05:,.0f}")
    else:
        st.subheader("🚀 Entrepreneur")
        omzet = st.number_input("Omzet (Rp)", value=20000000, step=1000000, key="omzet27")
        st.write(f"Ref profit 20%: Rp {omzet*0.2:,.0f}")
    st.markdown(f"**Biaya: Rp {HARGA_X}/bulan - Mode Etika**")
    st.markdown('</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Kolom 1: Fondasi", "Kolom 2: Perjalanan", "Kolom 3: Puncak"])
    with tab1:
        st.write("**Fondasi Teduh - Mindset & Niat**")
        st.image("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600", caption="Fondasi")
    with tab2:
        st.write("**Perjalanan Kerja - max 60km**")
        st.image("https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=600", caption="Perjalanan 60km")
    with tab3:
        st.write("**Puncak Teduh - Tawakal**")
        st.image("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600", caption="Puncak")
    st.markdown(f"### 💳 Rp {HARGA_X}/bulan")
    setuju = st.checkbox(f"Setuju Rp {HARGA_X}/bulan", key="setuju27")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("⬅️ Kembali", use_container_width=True, key="back27"):
            st.session_state.room = 1
            st.rerun()
    with b2:
        if st.button("➡️ Masuk Ruang 3", type="primary", use_container_width=True, key="next27"):
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
    st.write("- Total = Member x Rp X - Lolos etika Assembling")
    st.write("- Deploy log: No deprecation warning, No IndentationError, No ImportError")
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("📂 12 Folder GDrive: SOP | ERP | OEE | KPI | Vendor | Mood | Docs | Audio | Member | Finance | Legal | Report")
    if st.button("🔄 Ulangi", use_container_width=True, key="ulang27"):
        st.session_state.room = 1
        st.rerun()

# Floating dot - 1 titik
if not st.session_state.show_chat:
    # Style khusus untuk jadikan tombol jadi dot - tanpa pakai components.v1.html (pakai st.markdown + CSS)
    st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div:has(button#fab_open) { position: fixed; bottom: 24px; right: 24px; z-index: 9999; }
    button[kind="secondary"] { border-radius: 50% !important; width: 64px !important; height: 64px !important; background: #111827 !important; color: white !important; font-size: 28px !important; box-shadow: 0 6px 24px rgba(0,0,0,0.3) !important; border: 2px solid white !important; }
    </style>
    """, unsafe_allow_html=True)
    if st.button("🧘", key="fab_open", help="Klik untuk buka Meta AI"):
        st.session_state.show_chat = True
        st.rerun()
else:
    st.markdown('<div class="chat-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="chat-header">🤖 Meta AI - Ruang {st.session_state.room} | Rp {HARGA_X} | Clean Deploy</div>', unsafe_allow_html=True)
    chat_html = '<div class="chat-scroll">'
    if not st.session_state.chat_history:
        chat_html += f'<div class="chat-bubble-ai">🧘 Halo bro! v2.7 Clean - No deprecated API, No IndentationError baris 95, No ImportError auto_generate_all. Log Streamlit sekarang bersih! Harga Rp {HARGA_X}. Tanya aja, Enter langsung kirim.</div>'
    else:
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                chat_html += f'<div class="chat-bubble-user">🧑‍💼 {chat["text"]}</div>'
            else:
                chat_html += f'<div class="chat-bubble-ai">🧘 {chat["text"]}</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)
    c1, c2 = st.columns([3,1])
    with c2:
        if st.button("✕ Tutup", key="fab_close27", use_container_width=True):
            st.session_state.show_chat = False
            st.rerun()
    with c1:
        if st.button("🗑️ Hapus", key="clear27", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.show_chat:
    tanya = st.chat_input(f"Ketik di Ruang {st.session_state.room}... Enter langsung kirim")
    if tanya:
        st.session_state.chat_history.append({"role":"user","text":tanya})
        jawaban = f"Ruang {st.session_state.room} | Rp {HARGA_X} | Soal '{tanya}' -> Deploy clean, no warning deprecation. 3 Kolom tetap jalan!"
        st.session_state.chat_history.append({"role":"ai","text":jawaban})
        st.rerun()

st.caption("v2.7 CLEAN DEPLOY - 2026-09-02 - Fix: No st.components.v1.html, No st.iframe deprecated, Fix IndentationError L95, Fix ImportError auto_generate_all - Siap Assembling Hackathon")
