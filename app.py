
"""
RUANG TEDUH - BUKU 3 LEMBAR V29.2 - FORM LOKER LENGKAP
Update: Lembar Putih bukan cuma email, tapi form loker lengkap seperti loker:
nama, tempat tgl lahir, WNI, email, whatsapp, pengalaman kerja, pendidikan, skill

Three Way Function tetep: 1x input di Putih tembus ke Merah & Hijau
Speaker TTS Employee & Entrepreneur ON
No database - session state only (nggak input database)
"""

import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import date

st.set_page_config(page_title="Ruang Teduh V29.2 - Form Loker", page_icon="📋", layout="wide", initial_sidebar_state="collapsed")
USE_MUSIC = False

if "member_data" not in st.session_state:
    st.session_state.member_data = {}
if "member_terikat" not in st.session_state:
    st.session_state.member_terikat = False
if "payment_done" not in st.session_state:
    st.session_state.payment_done = False
if "tts_employee_text" not in st.session_state:
    st.session_state.tts_employee_text = "Selamat datang di Ruang Teduh. Data loker Anda sudah kami terima, akan kami kelola sesuai SOP."
if "tts_entrepreneur_text" not in st.session_state:
    st.session_state.tts_entrepreneur_text = "Halo Entrepreneur, data member loker lengkap sudah masuk storage hijau, SOP ERP OEE KPI Alkitab siap."

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.lembar { border-radius: 12px; padding: 24px; margin-bottom: 20px; border-left: 3px dashed #bbb; box-shadow: 4px 4px 0px rgba(0,0,0,0.08); }
.lembar-putih { background: #FFFFFF; border-top: 4px solid #9E9E9E; }
.lembar-merah { background: #FFEBEE; border-top: 4px solid #FF5252; }
.lembar-hijau { background: #E8F5E9; border-top: 4px solid #4CAF50; }
.lembar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px dashed rgba(0,0,0,0.1); }
.lembar-label { font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 4px; }
.label-putih { background: #424242; color: white; } .label-merah { background: #FF5252; color: white; } .label-hijau { background: #4CAF50; color: white; }
.flow-box { background: rgba(255,255,255,0.9); border: 2px solid rgba(0,0,0,0.1); border-radius: 8px; padding: 12px; text-align: center; font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 600; }
.carbon-copy { opacity: 0.8; font-family: 'JetBrains Mono', monospace; font-size: 11px; background: rgba(255,235,59,0.35); padding: 4px 8px; border-radius: 4px; display: inline-block; margin-bottom:6px; }
.rak { background: white; border: 2px solid #e0e0e0; border-radius: 8px; padding: 12px; text-align: center; height: 105px; display: flex; flex-direction: column; justify-content: center; }
.rak-icon { font-size: 26px; margin-bottom: 4px; } .rak-title { font-weight: 800; font-size: 12px; } .rak-desc { font-size: 10px; color: #666; margin-top: 3px; font-family: 'JetBrains Mono', monospace; }
.loker-field { background: #FAFAFA; border: 1px solid #E0E0E0; border-radius: 8px; padding: 8px 12px; margin-bottom: 8px; }
.floating-dot { position: fixed; bottom: 24px; right: 24px; width: 56px; height: 56px; background: linear-gradient(135deg, #FF8A65, #FF5722); border-radius: 50%; box-shadow: 0 4px 20px rgba(255,87,34,0.4); display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; z-index: 999; }
</style>
""", unsafe_allow_html=True)

def tts_component(text, role, key_id):
    safe_text = text.replace('"', '\"').replace("'", "\'").replace("\n", " ").replace("\r", " ").strip()
    if not safe_text:
        safe_text = "Teks kosong"
    if role == "employee":
        rate = "0.9"; pitch = "0.9"; bg = "#FFEBEE"; border = "#FF5252"; icon = "👨‍💼"; label = "EMPLOYEE"
    else:
        rate = "1.05"; pitch = "1.1"; bg = "#E8F5E9"; border = "#4CAF50"; icon = "🚀"; label = "ENTREPRENEUR"
    html_code = f"""
    <div style="background:{bg}; border:2px solid {border}; border-radius:10px; padding:12px; font-family:Inter;">
        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
            <div style="font-weight:800; font-size:11px;">{icon} SPEAKER {label}</div>
            <div style="font-size:9px; background:white; padding:2px 6px; border-radius:8px; border:1px solid {border};">🔊 TTS</div>
        </div>
        <div style="background:white; border-radius:6px; padding:8px; font-size:11px; max-height:60px; overflow-y:auto; border:1px dashed #ccc; margin-bottom:8px; font-family:JetBrains Mono;">
            {text[:180]}{'...' if len(text) > 180 else ''}
        </div>
        <div style="display:flex; gap:6px;">
            <button onclick="speak_{key_id}()" id="btn_{key_id}" style="flex:1; background:{border}; color:white; border:none; padding:8px; border-radius:6px; font-weight:700; cursor:pointer; font-size:11px;">🔊 PUTAR {label}</button>
            <button onclick="stop_{key_id}()" style="background:#424242; color:white; border:none; padding:8px 10px; border-radius:6px; cursor:pointer; font-size:11px;">⏹️</button>
        </div>
        <div id="status_{key_id}" style="font-size:9px; color:#666; margin-top:6px; text-align:center;">Siap</div>
    </div>
    <script>
        function speak_{key_id}() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                let u = new SpeechSynthesisUtterance("{safe_text}");
                u.rate = {rate}; u.pitch = {pitch}; u.lang = 'id-ID';
                u.onstart = function(){{ document.getElementById('status_{key_id}').innerHTML='🔊 Berbicara...'; }};
                u.onend = function(){{ document.getElementById('status_{key_id}').innerHTML='✅ Selesai'; }};
                window.speechSynthesis.speak(u);
            }} else {{ alert('Browser tidak support'); }}
        }}
        function stop_{key_id}() {{ window.speechSynthesis.cancel(); }}
    </script>
    """
    components.html(html_code, height=190)

def load_nasehat():
    try:
        if os.path.exists("nasehat_mingguan.txt"):
            with open("nasehat_mingguan.txt", "r", encoding="utf-8") as f:
                return f.read()
        return "Senin: SOP Kebersihan\nSelasa: ERP Jam 9\nRabu: OEE 95%\nKamis: KPI\nJumat: Alkitab"
    except:
        return "Nasehat tidak tersedia"

# HEADER
st.markdown("""
<div style="text-align:center; padding: 8px 0 16px 0;">
    <div style="font-family:'JetBrains Mono'; font-size:10px; letter-spacing:3px; color:#888;">TAVO MALKHUTKHA • V29.2 FORM LOKER</div>
    <div style="font-size:24px; font-weight:800; margin:4px 0;">📋📖 BUKU 3 LEMBAR - FORM LOKER LENGKAP</div>
    <div style="font-family:'JetBrains Mono'; font-size:10px; color:#fff; background:#424242; display:inline-block; padding:4px 12px; border-radius:20px;">
        No Database • Form Loker: Nama | TTL | WNI | Email | WA | Pengalaman | Pendidikan | Skill • 3 Lembar Tembus
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📄 PUTIH - FORM LOKER LENGKAP", "🔴 MERAH - KELOLA + TTS EMPLOYEE", "🟢 HIJAU - STORAGE + TTS ENTREPRENEUR"])

# ==================== LEMBAR 1 PUTIH - FORM LOKER LENGKAP ====================
with tab1:
    st.markdown('<div class="lembar lembar-putih"><div class="lembar-header"><div><b>LEMBAR 1 - FORM LOKER LENGKAP</b> (Entry Gate - No Database)</div><div class="lembar-label label-putih">ASLI - LOKER</div></div></div>', unsafe_allow_html=True)
    
    # Form Loker
    st.markdown("#### 📝 Form Lamaran / Loker - Lengkap")
    st.caption("Seperti loker bro: nama, tempat tgl lahir, WNI, email, whatsapp, pengalaman kerja, pendidikan, skill. No database, session only, auto tembus ke merah & hijau.")
    
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama Lengkap *", value=st.session_state.member_data.get("nama",""), placeholder="Contoh: Even Garden")
    with col2:
        wni = st.selectbox("Kewarganegaraan *", ["WNI", "WNA", "WNI Keturunan", "Lainnya"], index=0)
    
    col3, col4, col5 = st.columns([1.2, 1, 0.8])
    with col3:
        tempat_lahir = st.text_input("Tempat Lahir *", value=st.session_state.member_data.get("tempat_lahir",""), placeholder="Jakarta")
    with col4:
        tgl_lahir = st.date_input("Tanggal Lahir *", value=st.session_state.member_data.get("tgl_lahir_obj", date(2000,1,1)), min_value=date(1960,1,1), max_value=date(2010,12,31))
    with col5:
        umur = date.today().year - tgl_lahir.year
        st.metric("Umur", f"{umur} th")
    
    col6, col7 = st.columns(2)
    with col6:
        email = st.text_input("Email *", value=st.session_state.member_data.get("email",""), placeholder="nama@email.com")
    with col7:
        whatsapp = st.text_input("WhatsApp *", value=st.session_state.member_data.get("whatsapp",""), placeholder="0812xxxxxx")
    
    col8, col9 = st.columns(2)
    with col8:
        pendidikan = st.selectbox("Pendidikan Terakhir *", ["SMA/SMK", "D1", "D2", "D3", "S1", "S2", "S3", "Lainnya"], index=3)
        pendidikan_detail = st.text_input("Jurusan / Sekolah / Universitas", value=st.session_state.member_data.get("pendidikan_detail",""), placeholder="Contoh: Teknik Informatika - UI")
    with col9:
        pengalaman_tahun = st.selectbox("Pengalaman Kerja", ["Fresh Graduate", "< 1 Tahun", "1-2 Tahun", "3-5 Tahun", "5-10 Tahun", ">10 Tahun"], index=2)
    
    pengalaman_kerja = st.text_area("Pengalaman Kerja * (Cerita lengkap)", value=st.session_state.member_data.get("pengalaman_kerja",""), placeholder="Contoh: 2 tahun di PT XYZ sebagai staff admin, handle SOP kebersihan, ERP...", height=90)
    
    col10, col11 = st.columns(2)
    with col10:
        skill = st.text_area("Skill / Keahlian *", value=st.session_state.member_data.get("skill",""), placeholder="Contoh: SOP, ERP, OEE, KPI, Microsoft Excel, Komunikasi, Leadership", height=80)
    with col11:
        st.markdown("**Alasan Masuk Ruang Teduh**")
        alasan = st.text_area("Alasan / Motivasi", value=st.session_state.member_data.get("alasan",""), placeholder="Kenapa mau masuk Ruang Teduh?", height=80, label_visibility="collapsed")
    
    st.markdown("---")
    if st.button("✅ SIMPAN & MASUK RUANG TEDUH - TEMBUS 3 LEMBAR", type="primary", use_container_width=True):
        if not nama or not tempat_lahir or not email or not whatsapp or not pengalaman_kerja or not skill:
            st.error("⚠️ Lengkapi field bintang * bro: Nama, Tempat Lahir, Email, WA, Pengalaman, Skill wajib isi")
        elif "@" not in email:
            st.error("Email tidak valid")
        else:
            st.session_state.member_data = {
                "nama": nama,
                "tempat_lahir": tempat_lahir,
                "tgl_lahir": tgl_lahir.strftime("%d-%m-%Y"),
                "tgl_lahir_obj": tgl_lahir,
                "umur": umur,
                "wni": wni,
                "email": email,
                "whatsapp": whatsapp,
                "pendidikan": pendidikan,
                "pendidikan_detail": pendidikan_detail,
                "pengalaman_tahun": pengalaman_tahun,
                "pengalaman_kerja": pengalaman_kerja,
                "skill": skill,
                "alasan": alasan
            }
            # For backward compat
            st.session_state.email_member = email
            st.success(f"✅ Berhasil! Data {nama} tercatat di 3 lembar (Putih-Merah-Hijau)")
            st.balloons()
    
    if st.session_state.member_data:
        st.markdown("#### 📋 Data Tersimpan (Carbon Copy)")
        md = st.session_state.member_data
        st.info(f"**{md.get('nama')}** | {md.get('tempat_lahir')}, {md.get('tgl_lahir')} ({md.get('umur')}th) | {md.get('wni')} | {md.get('email')} | WA: {md.get('whatsapp')} | Pendidikan: {md.get('pendidikan')} {md.get('pendidikan_detail')} | Pengalaman: {md.get('pengalaman_tahun')}")

# ==================== LEMBAR 2 MERAH ====================
with tab2:
    st.markdown('<div class="lembar lembar-merah"><div class="lembar-header"><div><b>LEMBAR 2 - RUANG INTERAKSI + KELOLA LOKER</b></div><div class="lembar-label label-merah">TEMBUSAN 1 • TTS EMPLOYEE</div></div></div>', unsafe_allow_html=True)
    if not st.session_state.member_data:
        st.warning("⚠️ Isi dulu Form Loker Lengkap di Lembar Putih"); st.stop()
    
    md = st.session_state.member_data
    st.markdown(f"<div class='carbon-copy'>📋 Carbon Copy Loker: {md['nama']} | {md['email']} | {md['whatsapp']} | {md['wni']} | {md['tempat_lahir']}, {md['tgl_lahir']}</div>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.1, 0.9])
    with col_left:
        st.markdown("### 👨‍💼 KELOLA MEMBER LOKER - EMPLOYEE")
        st.markdown(f"""
        <div style="background:white; border-radius:8px; padding:12px; border:1px solid #FFCDD2; font-size:12px;">
            <b>Nama:</b> {md['nama']}<br/>
            <b>TTL:</b> {md['tempat_lahir']}, {md['tgl_lahir']} ({md['umur']}th) | {md['wni']}<br/>
            <b>Email/WA:</b> {md['email']} / {md['whatsapp']}<br/>
            <b>Pendidikan:</b> {md['pendidikan']} - {md['pendidikan_detail']}<br/>
            <b>Pengalaman:</b> {md['pengalaman_tahun']}<br/>
            <b>Skill:</b> {md['skill']}<br/>
            <b>Pengalaman Detail:</b> {md['pengalaman_kerja'][:150]}...
        </div>
        """, unsafe_allow_html=True)
        
        # Auto generate TTS text from loker data
        auto_employee_text = f"Selamat datang {md['nama']} dari {md['tempat_lahir']}. Data loker Anda umur {md['umur']} tahun, pendidikan {md['pendidikan']} {md['pendidikan_detail']}, pengalaman {md['pengalaman_tahun']}, skill {md['skill']}. Kami akan kelola sesuai SOP dan ERP jam 9 tepat."
        tts_input_emp = st.text_area("Teks TTS Employee (auto dari data loker, bisa edit):", value=auto_employee_text, height=100, key="emp_text_loker")
        tts_component(tts_input_emp, "employee", "emp_loker")
        
        st.markdown("---")
        st.selectbox("Employee Handle Loker", ["Employee A - Sage (SOP)", "Employee B - Beige (ERP)", "Employee C - Orange (OEE)"], key="emp_sel_loker")
        if st.button("🔗 TERIKAT & LANJUT KE BOARDING HIJAU", use_container_width=True):
            st.session_state.member_terikat = True
            st.success(f"{md['nama']} terikat - lanjut storage hijau")
    
    with col_right:
        st.markdown("**📅 Nasehat Mingguan**")
        st.code(load_nasehat())
        st.markdown("**🔊 AUDIO SOP**")
        audio_file = "ruang1_V28.1_NO_MUSIC.mp3"
        if os.path.exists(audio_file):
            st.audio(audio_file)
        else:
            st.info("🔇 Mode Hening - Pakai TTS")

# ==================== LEMBAR 3 HIJAU ====================
with tab3:
    st.markdown('<div class="lembar lembar-hijau"><div class="lembar-header"><div><b>LEMBAR 3 - RUANG BOARDING + STORAGE LOKER</b></div><div class="lembar-label label-hijau">TEMBUSAN 2 • STORAGE + TTS ENTREPRENEUR</div></div></div>', unsafe_allow_html=True)
    if not st.session_state.member_data:
        st.warning("⚠️ Isi Putih dulu"); st.stop()
    
    md = st.session_state.member_data
    st.markdown(f"<div class='carbon-copy'>📋 Final Storage: {md['nama']} | {md['email']} | {md['whatsapp']} | {md['wni']} | Terikat: {'YA' if st.session_state.member_terikat else 'Belum'} | Full Loker Data</div>", unsafe_allow_html=True)
    
    col_e_left, col_e_right = st.columns([0.9, 1.1])
    with col_e_left:
        st.markdown("### 🗄️ STORAGE - 5 Rak System + Data Loker")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.markdown('<div class="rak" style="border-color:#4CAF50; background:#E8F5E9;"><div class="rak-icon">📜</div><div class="rak-title">SOP</div><div class="rak-desc">Loker</div></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="rak" style="border-color:#4CAF50; background:#E8F5E9;"><div class="rak-icon">🏢</div><div class="rak-title">ERP</div><div class="rak-desc">Data</div></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="rak" style="border-color:#4CAF50; background:#E8F5E9;"><div class="rak-icon">⚙️</div><div class="rak-title">OEE</div><div class="rak-desc">95%</div></div>', unsafe_allow_html=True)
        with c4: st.markdown('<div class="rak" style="border-color:#4CAF50; background:#E8F5E9;"><div class="rak-icon">📈</div><div class="rak-title">KPI</div><div class="rak-desc">Loker</div></div>', unsafe_allow_html=True)
        with c5: st.markdown('<div class="rak" style="border-color:#4CAF50; background:#E8F5E9;"><div class="rak-icon">📖</div><div class="rak-title">ALKITAB</div><div class="rak-desc">Fondasi</div></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**📄 INVOICE LOKER LENGKAP**")
        if st.button("✅ BAYAR QRIS - SIMPAN STORAGE HIJAU", type="primary", use_container_width=True):
            st.session_state.payment_done = True
            st.success("LUNAS - Data Loker Masuk Storage Hijau Permanen!")
        
        st.code(f"""INVOICE LOKER - RUANG TEDUH V29.2
Nama: {md['nama']}
TTL: {md['tempat_lahir']}, {md['tgl_lahir']} ({md['umur']}th)
WNI: {md['wni']}
Email: {md['email']}
WA: {md['whatsapp']}
Pendidikan: {md['pendidikan']} - {md['pendidikan_detail']}
Pengalaman: {md['pengalaman_tahun']}
Skill: {md['skill']}
Alasan: {md['alasan'][:80]}...
Lembar: 3 Rangkap Loker
Storage: SOP/ERP/OEE/KPI/Alkitab
Status: {'TERIKAT & LUNAS' if st.session_state.payment_done else 'PENDING'}
""", language="text")
    
    with col_e_right:
        st.markdown("### 🚀 TTS ENTREPRENEUR - DARI DATA LOKER")
        auto_ent_text = f"Halo {md['nama']}, entrepreneur. Anda dari {md['tempat_lahir']}, umur {md['umur']} tahun, {md['wni']}, pendidikan {md['pendidikan']} {md['pendidikan_detail']}, pengalaman {md['pengalaman_tahun']}, skill {md['skill']}. Data loker Anda sudah kami simpan di storage hijau dengan sistem SOP ERP OEE 95 persen KPI dan Alkitab."
        tts_input_ent = st.text_area("Teks TTS Entrepreneur (auto dari loker):", value=auto_ent_text, height=110, key="ent_text_loker")
        tts_component(tts_input_ent, "entrepreneur", "ent_loker")
        
        st.markdown("---")
        st.markdown("**🎤 TTS CUSTOM LOKER**")
        custom_ent = st.text_area("Ketik teks custom Entrepreneur:", placeholder="Contoh: Selamat Even Garden, pengalaman kerja kamu 3 tahun...", height=70, key="custom_ent_loker")
        if custom_ent:
            tts_component(custom_ent, "entrepreneur", "custom_ent")
        
        st.markdown("**💬 FULL ACCESS CHAT**")
        if st.session_state.payment_done:
            chat_ent = st.text_input("Chat Entrepreneur (dari data loker):", placeholder="Ketik...", key="chat_ent_loker")
            if chat_ent:
                tts_component(chat_ent, "entrepreneur", "chat_loker")
        else:
            st.info("Bayar QRIS dulu untuk Full Access")

st.markdown('<div class="floating-dot">📋</div>', unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style="background:white; border-radius:12px; padding:12px; border:2px solid #eee; text-align:center; font-family:'JetBrains Mono'; font-size:10px;">
<div style="background:#424242; color:white; display:inline-block; padding:4px 12px; border-radius:20px; font-weight:700;">📋 FORM LOKER LENGKAP • V29.2 • No Database • Session Only • 3 Lembar Tembus</div>
<div style="margin-top:6px; color:#666;">Field: Nama | Tempat Tgl Lahir | WNI | Email | WA | Pengalaman | Pendidikan | Skill | Alasan</div>
</div>
""", unsafe_allow_html=True)
