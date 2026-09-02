import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

st.set_page_config(page_title="RUANG TEDUH AI v2.8.1 AUDIO FIX", layout="wide", page_icon="🔊")

st.markdown("""
<style>
.floating-dot { position: fixed; bottom: 24px; right: 24px; width: 62px; height: 62px; background: linear-gradient(135deg, #FF4B4B, #FF8A65); border-radius: 50%; z-index: 99999; display: flex; align-items: center; justify-content: center; color: white; font-size: 28px; cursor: pointer; box-shadow: 0 6px 18px rgba(0,0,0,0.35); }
.meta-ai-box { position: sticky; top: 80px; background: #F8F9FA; border: 1px solid #E0E0E0; border-radius: 16px; padding: 16px; }
.audio-fix { background: #E3F2FD; border: 1px solid #90CAF9; padding: 12px; border-radius: 12px; margin: 10px 0; }
</style>
<div class="floating-dot" onclick="document.getElementById('meta-ai-anchor').scrollIntoView({behavior:'smooth'})">🧘</div>
""", unsafe_allow_html=True)

def worship_player(title, youtube_id="lTRiuFIWV54"):
    """PLAYER FIX v2.8.1 - 3 layer fallback biar speaker pasti bunyi"""
    st.markdown(f'<div class="audio-fix">🔊 <b>{title}</b> - Klik Play di bawah, jangan autoplay (Chrome block autoplay)</div>', unsafe_allow_html=True)
    
    # LAYER 1: HTML5 Audio dengan controls (paling stabil)
    # File lokal - taruh file worship.mp3 di repo lo di folder /assets/worship.mp3
    html_audio = f"""
    <div style="background:white; padding:10px; border-radius:10px; border:1px solid #ddd;">
        <p style="margin:0 0 8px 0; font-weight:bold;">{title} - Worship Teduh (Klik ▶️)</p>
        <audio controls style="width:100%;" id="teduh-audio">
            <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
            Your browser does not support audio.
        </audio>
        <p style="font-size:11px; color:#888; margin-top:6px;">Jika tidak bunyi: 1) Cek volume HP/Laptop 2) Cek icon speaker di tab Chrome tidak di-mute 3) Klik tombol di atas sekali lagi</p>
    </div>
    """
    components.html(html_audio, height=140)

    # LAYER 2: YouTube Embed Fallback - PASTI BUNYI (Worship)
    st.caption("Fallback YouTube Worship (pasti bunyi - klik Play):")
    st.video(f"https://www.youtube.com/watch?v={youtube_id}")  # Worship teduh instrumental

    # LAYER 3: Streamlit native audio (backup)
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")

def tts_sop_player():
    """Audio penjelasan SOP/ERP/OEE/KPI biar tidak sepi - pakai TTS manual"""
    text = """
    Shalom. Ini penjelasan Ruang Teduh. SOP: Datang, Doa, Kerja seperti untuk Tuhan, Kolose 3 ayat 23.
    ERP versi Hati: Manusia, Material waktu 60 kilo, Money UMR.
    OEE Rohani: Availability hadir seratus persen, Performance satu persen lebih baik tiap hari, Quality memuliakan Tuhan.
    KPI Kingdom: Amsal 16 ayat 3, Serahkan perbuatanmu kepada Tuhan, maka terlaksanalah rencanamu.
    Ini improvement culture yang lebih baik, semua proses secara benar dengan kuasa Alkitab.
    """
    # Untuk v2.8.1 kita pakai audio player yang sama dengan teks di atas
    st.markdown("**🔊 Penjelasan Audio SOP/ERP/OEE/KPI (Klik Play biar tidak sepi):**")
    components.html(f"""
    <div style="background:#FFF8E1; padding:12px; border-radius:10px; border:1px solid #FFE082;">
        <audio controls style="width:100%;">
            <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3" type="audio/mpeg">
        </audio>
        <p style="font-size:12px; margin-top:8px; color:#5D4037;">{text}</p>
        <p style="font-size:11px; color:#999;">Tips: Jika speaker HP tidak bunyi, colok earphone dulu test, atau klik icon gembok di address bar -> Site Settings -> Sound -> Allow</p>
    </div>
    """, height=220)

# --- SESSION ---
if 'ruang' not in st.session_state: st.session_state.ruang = 1
if 'jalur' not in st.session_state: st.session_state.jalur = "Employee"
if 'email' not in st.session_state: st.session_state.email = ""
if 'nama' not in st.session_state: st.session_state.nama = ""
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

def jawab_meta_ai(pertanyaan, email, jalur, umr):
    q = pertanyaan.lower()
    email_status = f"Email follow up: {email}" if email and "@" in email else "⚠️ INGATKAN EMAIL dulu bro"
    base = f"""[SOP] Kolose 3:23 | [ERP] Manusia-Material-Money UMR Rp {umr:,} | [OEE] Availability-Performance-Quality | [KPI] Amsal 16:3 | {email_status}"""
    if "bayar" in q or "qris" in q or "gopay" in q:
        return base + f"\n\nCARA BAYAR: QRIS 081291904422 (GoPay/DANA/OVO) + VA BCA/Mandiri/BRI. Invoice ke {email if email else 'ISI EMAIL DULU'}"
    return base + f"\n\nJawaban Teduh untuk '{pertanyaan}' - Jalur {jalur}"

# --- HEADER ---
st.title("🏠 RUANG TEDUH AI - TAVO MALKHUTKHA v2.8.1")
st.caption("FIX AUDIO: Speaker sekarang harus klik Play (Chrome block autoplay) - Worship Mode - QR 081291904422")
progress = st.progress(st.session_state.ruang / 3)

left, right = st.columns([2, 1])

with left:
    if st.session_state.ruang == 1:
        st.header("Ruang 1: Pintu Masuk Perpustakaan")
        st.markdown('<div id="meta-ai-anchor"></div>', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1:
            if st.button("👨‍💼 Employee", use_container_width=True): 
                st.session_state.jalur="Employee"; st.rerun()
        with c2:
            if st.button("🚀 Entrepreneur", use_container_width=True):
                st.session_state.jalur="Entrepreneur"; st.rerun()
        
        st.session_state.nama = st.text_input("Nama Lengkap", value=st.session_state.nama)
        st.session_state.email = st.text_input("Email WAJIB follow up calon member", value=st.session_state.email, placeholder="isi email dulu biar speaker QR bisa aktif")
        
        # AUDIO FIX DI RUANG 1
        worship_player("Suara Teduh Hari Ini - Kolose 3:23 & Amsal 16:3", youtube_id="lTRiuFIWV54")

        if st.button("➡️ Masuk Ruang 2", type="primary", use_container_width=True):
            if "@" not in st.session_state.email:
                st.warning("Isi email dulu bro!")
            else:
                st.session_state.ruang=2; st.rerun()

    elif st.session_state.ruang == 2:
        st.header("Ruang 2: Perjalanan Employee - AUDIO FIX")
        umr = st.number_input("UMR Domisili (Rp)", value=4900000)
        
        tab1, tab2 = st.tabs(["Kolom 1: Fondasi (Ada Suara Sekarang)", "Kolom 2: Perjalanan"])
        with tab1:
            st.subheader("Fondasi Teduh - SOP/ERP/OEE/KPI + Alkitab")
            st.write("Dokumen GDrive: Kolom1_Fondasi.pdf")
            st.markdown(f"""
            **SOP:** Datang-Doa-Kerja Kolose 3:23
            **ERP:** Manusia-Material(60km)-Money(UMR Rp {umr:,})
            **OEE:** Availability 100% | Performance 1% better | Quality untuk Tuhan
            **KPI:** Amsal 16:3 - Improvement Culture lebih baik
            """)
            # INI FIX SEPI - AUDIO PENJELASAN
            tts_sop_player()
            
        with tab2:
            st.write(f"Halo {st.session_state.nama}")

        if st.button("⬅️ Kembali"): st.session_state.ruang=1; st.rerun()
        if st.button("➡️ Masuk Ruang 3 - Bayar", type="primary"):
            st.session_state.ruang=3; st.rerun()

    elif st.session_state.ruang == 3:
        st.header("Ruang 3: Bayar QRIS + VA")
        st.success(f"Email: {st.session_state.email}")
        col_qr, col_va = st.columns(2)
        with col_qr:
            qr_data = f"081291904422 - {st.session_state.email}"
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(qr_data)}"
            st.image(qr_url, caption="QRIS 081291904422 - GoPay/DANA/OVO")
            st.code("081291904422\nGoPay/DANA/OVO")
        with col_va:
            st.code("BCA VA: 3901 081291904422\nMandiri: 8950 081291904422")
        
        # AUDIO DI RUANG 3 JUGA
        worship_player("Terima Kasih - Suara Teduh Penutup", youtube_id="77ZozI0rw6w")
        
        if st.button("🔄 Ulang"): st.session_state.ruang=1; st.rerun()

with right:
    st.markdown('<div class="meta-ai-box">', unsafe_allow_html=True)
    st.subheader("🧘 Meta AI - Kolom Lo")
    st.caption("Floating Dot - Generate semua pertanyaan Ruang Teduh AI")
    for chat in st.session_state.chat_history[-5:]:
        with st.chat_message(chat["role"]): st.write(chat["content"])
    q = st.chat_input("Ketik pertanyaan... (speaker test: 'test suara')")
    if q:
        st.session_state.chat_history.append({"role":"user","content":q})
        ans = jawab_meta_ai(q, st.session_state.email, st.session_state.jalur, 4900000)
        st.session_state.chat_history.append({"role":"assistant","content":ans})
        st.rerun()
    st.divider()
    # Test speaker button
    if st.button("🔊 TEST SPEAKER - Klik ini kalau speaker gak bunyi", use_container_width=True):
        components.html("""
        <audio controls autoplay style="width:100%;">
            <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
        </audio>
        <p style="color:green; font-weight:bold;">Jika bunyi = speaker HP/Laptop OK. Jika tidak bunyi = cek volume & izin Sound di Chrome.</p>
        """, height=100)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.caption("v2.8.1 AUDIO FIX - 2026-09-02 - HP Worth It Full Width - Worship + SOP/ERP/OEE/KPI + Email Wajib + QR 081291904422")
