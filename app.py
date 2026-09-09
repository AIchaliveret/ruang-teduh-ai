
"""
RUANG TEDUH - BUKU 3 LEMBAR V29.1 - Three Way + TTS Speaker ON
Speaker suara ON, Teks bisa jadi suara untuk Employee & Entrepreneur
"""

import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="Ruang Teduh V29.1 - Speaker ON", page_icon="🔊", layout="wide", initial_sidebar_state="collapsed")
USE_MUSIC = False
AUTOPLAY = False

if "email_member" not in st.session_state:
    st.session_state.email_member = ""
if "member_terikat" not in st.session_state:
    st.session_state.member_terikat = False
if "payment_done" not in st.session_state:
    st.session_state.payment_done = False
if "tts_employee_text" not in st.session_state:
    st.session_state.tts_employee_text = "Selamat datang di Ruang Teduh. Saya Employee yang akan membantu Anda memahami SOP kebersihan dan ERP jam 9 tepat."
if "tts_entrepreneur_text" not in st.session_state:
    st.session_state.tts_entrepreneur_text = "Halo Entrepreneur, ini Ruang Boarding. Semua sistem SOP, ERP, OEE 95 persen, KPI dan Alkitab sudah tersimpan systematic di storage hijau."

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.lembar { border-radius: 12px; padding: 24px; margin-bottom: 20px; position: relative; border-left: 3px dashed #bbb; box-shadow: 4px 4px 0px rgba(0,0,0,0.08); }
.lembar-putih { background: #FFFFFF; border-top: 4px solid #9E9E9E; }
.lembar-merah { background: #FFEBEE; border-top: 4px solid #FF5252; }
.lembar-hijau { background: #E8F5E9; border-top: 4px solid #4CAF50; }
.lembar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px dashed rgba(0,0,0,0.1); }
.lembar-label { font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 4px; }
.label-putih { background: #424242; color: white; } .label-merah { background: #FF5252; color: white; } .label-hijau { background: #4CAF50; color: white; }
.flow-box { background: rgba(255,255,255,0.9); border: 2px solid rgba(0,0,0,0.1); border-radius: 8px; padding: 12px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 600; }
.carbon-copy { opacity: 0.7; font-family: 'JetBrains Mono', monospace; font-size: 11px; background: rgba(255,235,59,0.3); padding: 3px 8px; border-radius: 4px; display: inline-block; }
.rak { background: white; border: 2px solid #e0e0e0; border-radius: 8px; padding: 14px; text-align: center; height: 110px; display: flex; flex-direction: column; justify-content: center; }
.rak-icon { font-size: 28px; margin-bottom: 6px; } .rak-title { font-weight: 800; font-size: 13px; } .rak-desc { font-size: 11px; color: #666; margin-top: 4px; font-family: 'JetBrains Mono', monospace; }
.floating-dot { position: fixed; bottom: 24px; right: 24px; width: 56px; height: 56px; background: linear-gradient(135deg, #FF8A65, #FF5722); border-radius: 50%; box-shadow: 0 4px 20px rgba(255,87,34,0.4); display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; z-index: 999; cursor: pointer; animation: pulse 2s infinite; }
@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255,87,34,0.7); } 70% { box-shadow: 0 0 0 12px rgba(255,87,34,0); } 100% { box-shadow: 0 0 0 0 rgba(255,87,34,0); } }
</style>
""", unsafe_allow_html=True)

def tts_speaker_component(text, role, key_id):
    safe_text = text.replace('"', '\\"').replace("'", "\\'").replace("\n", " ").strip()
    if not safe_text:
        safe_text = "Teks kosong"
    if role == "employee":
        rate = "0.9"; pitch = "0.9"; bg = "#FFEBEE"; border = "#FF5252"; icon = "👨‍💼"; label = "EMPLOYEE"
    else:
        rate = "1.05"; pitch = "1.1"; bg = "#E8F5E9"; border = "#4CAF50"; icon = "🚀"; label = "ENTREPRENEUR"
    html_code = f"""
    <div style="background:{bg}; border:2px solid {border}; border-radius:10px; padding:14px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
            <div style="font-weight:800; font-size:12px;">{icon} SPEAKER {label}</div>
            <div style="font-size:10px; background:white; padding:2px 8px; border-radius:10px; border:1px solid {border};">🔊 Web Speech API</div>
        </div>
        <div style="background:white; border-radius:8px; padding:10px; font-size:12px; max-height:70px; overflow-y:auto; border:1px dashed #ccc; margin-bottom:10px; font-family:JetBrains Mono;">
            {text[:220]}{'...' if len(text) > 220 else ''}
        </div>
        <div style="display:flex; gap:8px;">
            <button onclick="speak_{key_id}()" id="btn_{key_id}" style="flex:1; background:{border}; color:white; border:none; padding:10px; border-radius:8px; font-weight:700; cursor:pointer;">🔊 PUTAR SUARA {label}</button>
            <button onclick="stop_{key_id}()" style="background:#424242; color:white; border:none; padding:10px 14px; border-radius:8px; cursor:pointer;">⏹️</button>
        </div>
        <div id="status_{key_id}" style="font-size:10px; color:#666; margin-top:8px; text-align:center;">Siap - Klik PUTAR</div>
    </div>
    <script>
        let utterance_{key_id} = null;
        function speak_{key_id}() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                utterance_{key_id} = new SpeechSynthesisUtterance("{safe_text}");
                utterance_{key_id}.rate = {rate};
                utterance_{key_id}.pitch = {pitch};
                utterance_{key_id}.lang = 'id-ID';
                utterance_{key_id}.onstart = function() {{ document.getElementById('status_{key_id}').innerHTML = '🔊 Berbicara...'; }};
                utterance_{key_id}.onend = function() {{ document.getElementById('status_{key_id}').innerHTML = '✅ Selesai'; }};
                window.speechSynthesis.speak(utterance_{key_id});
            }} else {{ alert('Browser tidak support TTS'); }}
        }}
        function stop_{key_id}() {{ window.speechSynthesis.cancel(); document.getElementById('status_{key_id}').innerHTML = '⏹️ Stop'; }}
    </script>
    """
    components.html(html_code, height=230)

def load_nasehat():
    try:
        if os.path.exists("nasehat_mingguan.txt"):
            with open("nasehat_mingguan.txt", "r", encoding="utf-8") as f:
                return f.read()
        return "Senin: SOP Cek Kebersihan\nSelasa: ERP Jam 9 Tepat\nRabu: OEE 95%\nKamis: KPI Review\nJumat: Alkitab Fondasi"
    except:
        return "Nasehat tidak tersedia"

st.markdown("""
<div style="text-align:center; padding: 10px 0 20px 0;">
    <div style="font-family:'JetBrains Mono'; font-size:11px; letter-spacing:3px; color:#888;">TAVO MALKHUTKHA • V29.1 SPEAKER ON</div>
    <div style="font-size:26px; font-weight:800; margin:6px 0;">📖🔊 BUKU 3 LEMBAR + SPEAKER TTS</div>
    <div style="font-family:'JetBrains Mono'; font-size:11px; color:#fff; background:#4CAF50; display:inline-block; padding:4px 12px; border-radius:20px;">🔊 Speaker ON • Employee & Entrepreneur TTS Active</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📄 PUTIH - TEDUH", "🔴 MERAH - TTS EMPLOYEE", "🟢 HIJAU - TTS ENTREPRENEUR"])

with tab1:
    st.markdown('<div class="lembar lembar-putih"><div class="lembar-header"><div><b>LEMBAR 1 - RUANG TEDUH</b> (Entry Gate)</div><div class="lembar-label label-putih">ASLI</div></div></div>', unsafe_allow_html=True)
    col_qr, col_form = st.columns([1, 2])
    with col_qr:
        st.markdown('<div class="flow-box" style="height:150px; display:flex; flex-direction:column; justify-content:center;"><div style="font-size:40px;">⬜</div><div>QR GATE</div></div>', unsafe_allow_html=True)
    with col_form:
        email_input = st.text_input("Email Member (auto tembus merah & hijau)", value=st.session_state.email_member, placeholder="nama@email.com")
        if st.button("✅ MASUK RUANG TEDUH", type="primary", use_container_width=True):
            if "@" in email_input and "." in email_input:
                st.session_state.email_member = email_input
                st.success(f"✓ {email_input} tercatat di 3 lembar")
                st.balloons()
            else:
                st.error("Email tidak valid")
        if st.session_state.email_member:
            st.info(f"Member: {st.session_state.email_member}")

with tab2:
    st.markdown('<div class="lembar lembar-merah"><div class="lembar-header"><div><b>LEMBAR 2 - RUANG INTERAKSI + SPEAKER EMPLOYEE</b></div><div class="lembar-label label-merah">TEMBUSAN 1 • TTS ON</div></div></div>', unsafe_allow_html=True)
    if not st.session_state.email_member:
        st.warning("⚠️ Isi Lembar Putih dulu"); st.stop()
    st.markdown(f"<div class='carbon-copy'>📋 Copy Putih: {st.session_state.email_member} • Role: Employee</div>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1.2, 0.8])
    with col_left:
        st.markdown("### 👨‍💼 TTS UNTUK EMPLOYEE")
        st.caption("Employee voice: pelan, jelas, SOP oriented - Rate 0.9")
        employee_text = st.text_area("Teks untuk Employee:", value=st.session_state.tts_employee_text, height=120, key="input_emp")
        st.session_state.tts_employee_text = employee_text
        tts_speaker_component(employee_text, "employee", "emp")
        st.selectbox("Pilih Employee", ["Employee A - Sage (SOP)", "Employee B - Beige (ERP)", "Employee C - Orange (OEE)"], key="emp_sel")
        if st.button("🔗 IKAT & LANJUT HIJAU", use_container_width=True):
            st.session_state.member_terikat = True
            st.success("Terikat - Lanjut ke Entrepreneur")
    with col_right:
        st.markdown("**🔊 AUDIO SOP LEGACY**")
        audio_file = "ruang1_V28.1_NO_MUSIC.mp3"
        if os.path.exists(audio_file):
            st.audio(audio_file)
            st.caption("✓ Audio SOP - No Musik Stress")
        else:
            st.info("🔇 Mode Hening - Pakai TTS Speaker")
        st.markdown("**📅 Nasehat Mingguan**")
        st.code(load_nasehat())
        custom_nasehat = st.text_area("Bacakan nasehat custom Employee:", key="nasehat_emp_custom", placeholder="Ketik untuk dibacakan Employee...")
        if custom_nasehat:
            tts_speaker_component(custom_nasehat, "employee", "nasehat_emp")

with tab3:
    st.markdown('<div class="lembar lembar-hijau"><div class="lembar-header"><div><b>LEMBAR 3 - RUANG BOARDING + SPEAKER ENTREPRENEUR</b></div><div class="lembar-label label-hijau">TEMBUSAN 2 • STORAGE + TTS ON</div></div></div>', unsafe_allow_html=True)
    if not st.session_state.email_member:
        st.warning("⚠️ Isi Putih dulu"); st.stop()
    st.markdown(f"<div class='carbon-copy'>📋 Final Copy: {st.session_state.email_member} • {'TERIKAT ✓' if st.session_state.member_terikat else 'Belum'} • Entrepreneur • Storage</div>", unsafe_allow_html=True)
    col_e_left, col_e_right = st.columns([0.8, 1.2])
    with col_e_left:
        st.markdown("### 🗄️ STORAGE - 5 Rak System")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.markdown('<div class="rak" style="border-color:#4CAF50; background:#E8F5E9;"><div class="rak-icon">📜</div><div class="rak-title">SOP</div><div class="rak-desc">Kebersihan</div></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="rak" style="border-color:#4CAF50; background:#E8F5E9;"><div class="rak-icon">🏢</div><div class="rak-title">ERP</div><div class="rak-desc">Jam 9</div></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="rak" style="border-color:#4CAF50; background:#E8F5E9;"><div class="rak-icon">⚙️</div><div class="rak-title">OEE</div><div class="rak-desc">95%</div></div>', unsafe_allow_html=True)
        with c4: st.markdown('<div class="rak" style="border-color:#4CAF50; background:#E8F5E9;"><div class="rak-icon">📈</div><div class="rak-title">KPI</div><div class="rak-desc">Review</div></div>', unsafe_allow_html=True)
        with c5: st.markdown('<div class="rak" style="border-color:#4CAF50; background:#E8F5E9;"><div class="rak-icon">📖</div><div class="rak-title">ALKITAB</div><div class="rak-desc">Fondasi</div></div>', unsafe_allow_html=True)
        st.markdown("---")
        if st.button("✅ BAYAR QRIS - FULL ACCESS", type="primary", use_container_width=True):
            st.session_state.payment_done = True
            st.success("LUNAS - Storage Hijau Tercatat!")
        if st.session_state.payment_done:
            st.code(f"INVOICE LUNAS\nMember: {st.session_state.email_member}\nLembar: 3 Rangkap TTS ON\nStorage: SOP/ERP/OEE/KPI/Alkitab\nTTS: Employee+Entrepreneur\nStatus: FULL ACCESS", language="text")
    with col_e_right:
        st.markdown("### 🚀 TTS UNTUK ENTREPRENEUR")
        st.caption("Entrepreneur voice: energik, cepat, visioner - Rate 1.05")
        entrepreneur_text = st.text_area("Teks untuk Entrepreneur:", value=st.session_state.tts_entrepreneur_text, height=120, key="input_ent")
        st.session_state.tts_entrepreneur_text = entrepreneur_text
        tts_speaker_component(entrepreneur_text, "entrepreneur", "ent")
        st.markdown("---")
        st.markdown("**🎤 TTS CUSTOM**")
        custom_ent = st.text_area("Ketik teks custom Entrepreneur:", placeholder="Hari ini OEE 95 persen...", height=80, key="custom_ent")
        if custom_ent:
            tts_speaker_component(custom_ent, "entrepreneur", "custom_ent2")
        st.markdown("**💬 FULL ACCESS CHAT**")
        if st.session_state.payment_done:
            chat_ent = st.text_input("Chat Entrepreneur:", placeholder="Ketik disini...", key="chat_ent")
            if chat_ent:
                tts_speaker_component(chat_ent, "entrepreneur", "chat_ent_voice")
        else:
            st.info("Bayar QRIS dulu")

st.markdown('<div class="floating-dot">🔊</div>', unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="background:white; border-radius:12px; padding:16px; border:2px solid #eee; text-align:center; font-family:'JetBrains Mono'; font-size:11px;">
<div style="background:#E8F5E9; display:inline-block; padding:6px 14px; border-radius:20px; font-weight:700; color:#2E7D32;">🔊 SPEAKER ON • V29.1 • Employee Slow 0.9 + Entrepreneur Fast 1.05</div>
<div style="margin-top:8px; color:#666;">Web Speech API Native • No pydub • No ffmpeg • No Error Install • 100% Browser</div>
</div>
""", unsafe_allow_html=True)
