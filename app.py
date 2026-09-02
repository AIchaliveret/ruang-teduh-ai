
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
if 'show_chat' not in st.session_state:
    st.session_state.show_chat = False

HARGA_X = "X"

# ===== CSS FLOATING DOT - 1 TITIK TERLIHAT =====
st.markdown("""
<style>
.big-title { font-size:28px; font-weight:800; margin-bottom:0; }
.sub { color: #6b7280; margin-bottom:12px; }
.card { padding:16px; border-radius:16px; background:#f8fafc; border:1px solid #e5e7eb; margin-bottom:12px; }
.ethics-badge { background:#fef3c7; border:1px solid #f59e0b; padding:10px 14px; border-radius:10px; font-size:13px; color:#92400e; margin-bottom:10px; }

/* FLOATING DOT - 1 TITIK KECIL */
.fab-container {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 9999;
}
.fab-dot {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: #111827;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.3);
    cursor: pointer;
    border: 2px solid white;
    transition: all 0.2s;
}
.fab-dot:hover { transform: scale(1.05); box-shadow: 0 8px 28px rgba(0,0,0,0.4); }
.fab-label {
    position: absolute;
    bottom: 70px;
    right: 0;
    background: #111827;
    color: white;
    padding: 6px 10px;
    border-radius: 8px;
    font-size: 12px;
    white-space: nowrap;
    display: none;
}
.fab-container:hover .fab-label { display: block; }

/* CHAT PANEL FULL - MUNCUL PAS KLIK DOT */
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
.chat-header {
    background: #111827;
    color: white;
    padding: 14px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.chat-scroll { flex: 1; overflow-y: auto; padding: 12px; background: #fafafa; }
.chat-bubble-user { background:#dbeafe; padding:10px 12px; border-radius:12px 12px 2px 12px; margin:8px 0; font-size:14px; text-align:right; margin-left: 30px; }
.chat-bubble-ai { background:white; padding:10px 12px; border-radius:12px 12px 12px 2px; margin:8px 0; border:1px solid #e5e7eb; font-size:14px; margin-right: 20px; }
.chat-input-area { padding: 10px; border-top: 1px solid #e5e7eb; background: white; }

/* HP RESPONSIVE - DOT TETEP KELIATAN, PANEL FULL */
@media (max-width: 768px) {
    .big-title { font-size:22px; }
    .fab-container { bottom: 16px; right: 16px; }
    .fab-dot { width: 56px; height: 56px; font-size: 24px; }
    .chat-panel {
        bottom: 80px;
        right: 16px;
        left: 16px;
        width: auto;
        max-width: none;
        height: 68vh;
    }
}

/* SEMBUNYIKAN DEFAULT CHAT INPUT STYLE BIAR RAPI */
[data-testid="stChatInput"] { position: fixed; bottom: 0; left: 0; right: 0; z-index: 9997; background: white; padding: 8px 16px; border-top: 1px solid #e5e7eb; }
</style>
""", unsafe_allow_html=True)

# HEADER - FULL WIDTH, BIAR HP FULL KELIATAN
st.markdown('<div class="big-title">🏠 RUANG TEDUH AI - TAVO MALKHUTKHA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Two Journeys, One QR | Wellbeing Library - Kerja max 60km dari rumah</div>', unsafe_allow_html=True)
st.markdown(f'<div class="ethics-badge">🔒 v2.6 FLOATING DOT - 1 Titik Terlihat - Klik Dot untuk Full Chat - HP & Laptop Otomatis - Harga Rp {HARGA_X} - Lolos Etika</div>', unsafe_allow_html=True)
st.progress(st.session_state.room / 3, text=f"Ruang {st.session_state.room} dari 3")

# ===== MAIN CONTENT FULL WIDTH - BIAR HP WORTHED =====
st.markdown("---")

if st.session_state.room == 1:
    st.header("Ruang 1: Pintu Masuk Perpustakaan")
    st.write("Member masuk via QR -> Pilih jalur lo")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("👨‍💼 Employee", use_container_width=True, key="emp26"):
            st.session_state.tipe_member = "Employee"
    with c2:
        if st.button("🚀 Entrepreneur", use_container_width=True, key="ent26"):
            st.session_state.tipe_member = "Entrepreneur"
    if st.session_state.tipe_member:
        st.success(f"Jalur: {st.session_state.tipe_member} - Rp {HARGA_X}/bulan")
    st.session_state.nama_member = st.text_input("Nama Lengkap", value=st.session_state.nama_member, placeholder="Tulis nama lo...", key="nama26")
    st.markdown("### 🔊 Suara Teduh Hari Ini")
    st.markdown("**Kolose 3:23 & Amsal 16:3** - Apapun yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
    st.caption("Visual + teks + audio - full di HP")
    if st.button("➡️ Masuk Ruang 2", type="primary", use_container_width=True):
        if not st.session_state.nama_member or not st.session_state.tipe_member:
            st.warning("Isi nama & pilih jalur dulu")
        else:
            st.session_state.room = 2
            st.rerun()

elif st.session_state.room == 2:
    st.header(f"Ruang 2: Perjalanan {st.session_state.tipe_member}")
    st.write(f"Halo {st.session_state.nama_member} - Full width di HP, worth it!")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.session_state.tipe_member=="Employee":
        st.subheader("👨‍💼 Employee")
        umr = st.number_input("UMR Domisili (Rp)", value=4900000, step=100000, key="umr26")
        st.write(f"Ref: Rp {umr*0.05:,.0f}")
    else:
        st.subheader("🚀 Entrepreneur")
        omzet = st.number_input("Omzet (Rp)", value=20000000, step=1000000, key="omzet26")
        st.write(f"Ref profit: Rp {omzet*0.2:,.0f}")
    st.markdown(f"**Biaya: Rp {HARGA_X}/bulan - Mode Etika**")
    st.markdown('</div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Kolom 1: Fondasi", "Kolom 2: Perjalanan", "Kolom 3: Puncak"])
    with tab1:
        st.write("**Fondasi Teduh - Mindset & Niat**")
        st.image("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600")
        st.write("Dokumen GDrive: Kolom1_Fondasi.pdf")
    with tab2:
        st.write("**Perjalanan Kerja - max 60km dari rumah**")
        st.image("https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=600")
        st.write("Dokumen GDrive: Kolom2_Perjalanan.pdf")
    with tab3:
        st.write("**Puncak Teduh - Tawakal**")
        st.image("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=600")
        st.write("Dokumen GDrive: Kolom3_Puncak.pdf")
    st.markdown(f"### 💳 Rp {HARGA_X}/bulan")
    setuju = st.checkbox(f"Setuju Rp {HARGA_X}/bulan", key="setuju26")
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
    st.subheader("💰 Ethics Compliant - Full Width")
    st.write("- Total = Member x Rp X")
    st.write("- Di HP full screen, dot AI tetap di pojok")
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("📂 12 Folder GDrive: SOP | ERP | OEE | KPI | Vendor | Mood | Docs | Audio | Member | Finance | Legal | Report")
    if st.button("🔄 Ulangi", use_container_width=True):
        st.session_state.room = 1
        st.rerun()

# ===== FLOATING DOT - 1 TITIK TERLIHAT =====
# Tombol dot kecil yang selalu terlihat di pojok kanan bawah

# Jika chat tertutup, tampilkan dot
if not st.session_state.show_chat:
    # Buat container untuk dot
    st.markdown("""
    <div class="fab-container">
        <div class="fab-label">Klik untuk tanya Meta AI</div>
    </div>
    """, unsafe_allow_html=True)
    # Tombol Streamlit yang diposisikan jadi dot
    col_fab1, col_fab2, col_fab3 = st.columns([10,1,1])
    with col_fab3:
        # CSS khusus untuk tombol ini jadi dot
        st.markdown("""
        <style>
        div[data-testid="column"]:has(button[kind="secondary"]) button {
            position: fixed !important;
            bottom: 24px !important;
            right: 24px !important;
            width: 64px !important;
            height: 64px !important;
            border-radius: 50% !important;
            background: #111827 !important;
            color: white !important;
            font-size: 28px !important;
            z-index: 9999 !important;
            box-shadow: 0 6px 24px rgba(0,0,0,0.3) !important;
            border: 2px solid white !important;
        }
        @media (max-width: 768px) {
            div[data-testid="column"]:has(button[kind="secondary"]) button {
                bottom: 16px !important;
                right: 16px !important;
                width: 56px !important;
                height: 56px !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("🧘", key="fab_open", help="Klik untuk buka Meta AI"):
            st.session_state.show_chat = True
            st.rerun()
else:
    # Jika chat terbuka, tampilkan panel full
    st.markdown('<div class="chat-panel">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="chat-header">
        <span>🤖 Meta AI - Ruang {st.session_state.room} | Rp {HARGA_X}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat scroll area - render dari session
    chat_html = '<div class="chat-scroll">'
    if not st.session_state.chat_history:
        chat_html += f'<div class="chat-bubble-ai">🧘 Halo bro! Gua sekarang jadi 1 titik kecil di pojok kanan bawah. Klik dot tadi, sekarang full chat kebuka. Di HP juga worth it, full width library lu tetep keliatan. Harga Rp {HARGA_X}. Tanya apa aja, Enter langsung kirim!</div>'
    else:
        for chat in st.session_state.chat_history:
            if chat["role"]=="user":
                chat_html += f'<div class="chat-bubble-user">🧑‍💼 {chat["text"]}</div>'
            else:
                chat_html += f'<div class="chat-bubble-ai">🧘 {chat["text"]}</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)
    
    # Tombol close di dalam panel
    c_close1, c_close2 = st.columns([3,1])
    with c_close2:
        if st.button("✕ Tutup", key="fab_close", use_container_width=True):
            st.session_state.show_chat = False
            st.rerun()
    with c_close1:
        if st.button("🗑️ Hapus", key="clear26", use_container_width=True):
            st.session_state.chat_history=[]
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tetap tampilkan dot kecil untuk close? Tidak, pakai tombol tutup di atas

# ===== CHAT INPUT - ONETOUCH ENTER - SELALU AKTIF =====
# Input ini muncul di bawah, tapi cuma aktif pas panel kebuka biar one-touch
if st.session_state.show_chat:
    tanya = st.chat_input(f"Ketik di Ruang {st.session_state.room}... Enter langsung kirim (HP & Laptop)")
    if tanya:
        if tanya.strip().lower() in ["tanya meta ai", "tanya", ""]:
            st.session_state.chat_history.append({"role":"user","text":tanya})
            st.session_state.chat_history.append({"role":"ai","text":"Ketik pertanyaan yang jelas bro."})
        else:
            st.session_state.chat_history.append({"role":"user","text":tanya})
            if "harga" in tanya.lower() or tanya.strip().upper()=="X":
                jawaban = f"Pakai Rp {HARGA_X} bro biar lolos etika. Dot yang lu klik tadi itu 1 titik kecil biar di HP full library keliatan. Enter yang barusan udah one-touch kan?"
            elif "hp" in tanya.lower() or "worth" in tanya.lower() or "titik" in tanya.lower() or "dot" in tanya.lower():
                jawaban = f"Udah worth it bro! Sekarang 1 titik dot kecil di pojok kanan bawah, klik baru full chat kebuka. Di HP library full width, dot tetep keliatan di pojok. Di laptop juga sama. Ini yang lu mau kan?"
            else:
                jawaban = f"Ruang {st.session_state.room} | Rp {HARGA_X} | Soal '{tanya}' -> 3 Kolom: Fondasi (Kolose 3:23), Perjalanan (60km), Puncak (tawakal). Dot chat udah bener kan?"
            st.session_state.chat_history.append({"role":"ai","text":jawaban})
        st.rerun()

st.caption("v2.6 FLOATING DOT - 2026-09-02 - 1 Titik Kecil Klik -> Full Chat - HP Worth It Full Width + Laptop - Harga X - No Prompt Format")
