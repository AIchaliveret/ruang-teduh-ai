
"""
RUANG TEDUH - V29.4 - FIX HIJAU MANAGE + VOICE + SHARE + KEJUJURAN
- Lembar Hijau: Manage & selevelnya + keterangan keberadaannya (Manager, Brand Manager, Usahawan)
- Share ke rekan via email include di Employee & Entrepreneur (pencarian permintaan & penawaran)
- Voice di Hijau FIX
- Bursa terintegrasi: 1 daftar = 1 vote, berkurang bila sudah diterima kerja
- Kolom kecil kejujuran: Sudah Diterima Kerja -> share & kurangi bursa
- Kotak tambahan dibawah untuk update jujur
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import date, datetime
import json

st.set_page_config(page_title="Ruang Teduh V29.4 - Manage Hijau + Voice Fix", page_icon="📗", layout="wide", initial_sidebar_state="collapsed")

# SESSION
if "member_data" not in st.session_state:
    st.session_state.member_data = {}
if "member_terikat" not in st.session_state:
    st.session_state.member_terikat = False
if "payment_done" not in st.session_state:
    st.session_state.payment_done = False
if "bursa_total_login" not in st.session_state:
    st.session_state.bursa_total_login = 12
if "bursa_active_vote" not in st.session_state:
    st.session_state.bursa_active_vote = 8
if "bursa_sudah_bekerja" not in st.session_state:
    st.session_state.bursa_sudah_bekerja = 4
if "bursa_history" not in st.session_state:
    st.session_state.bursa_history = [
        {"jam": "08:00", "vote": 2, "bekerja": 0},
        {"jam": "09:00", "vote": 5, "bekerja": 1},
        {"jam": "10:00", "vote": 8, "bekerja": 2},
        {"jam": "11:00", "vote": 8, "bekerja": 4},
    ]
if "bursa_share_log" not in st.session_state:
    st.session_state.bursa_share_log = []
if "sudah_diterima_kerja" not in st.session_state:
    st.session_state.sudah_diterima_kerja = False

def add_bursa_login():
    st.session_state.bursa_total_login += 1
    st.session_state.bursa_active_vote += 1
    now = datetime.now().strftime("%H:%M")
    st.session_state.bursa_history.append({"jam": now, "vote": st.session_state.bursa_active_vote, "bekerja": st.session_state.bursa_sudah_bekerja})
    if len(st.session_state.bursa_history) > 12:
        st.session_state.bursa_history = st.session_state.bursa_history[-12:]

def reduce_bursa_share(email_teman, alasan="share"):
    if st.session_state.bursa_active_vote > 0:
        st.session_state.bursa_active_vote -= 1
        st.session_state.bursa_sudah_bekerja += 1
        now = datetime.now().strftime("%H:%M")
        st.session_state.bursa_history.append({"jam": now, "vote": st.session_state.bursa_active_vote, "bekerja": st.session_state.bursa_sudah_bekerja})
        st.session_state.bursa_share_log.append({"waktu": now, "ke": email_teman, "oleh": st.session_state.member_data.get("nama","Member"), "alasan": alasan})
        if len(st.session_state.bursa_history) > 12:
            st.session_state.bursa_history = st.session_state.bursa_history[-12:]

def tts_fixed(text, role, key_id):
    # FIX voice - remove quotes and escape properly
    clean = text.replace('"','').replace("'","").replace("\n"," ").replace("\r"," ").strip()
    clean = clean[:300]
    if not clean:
        clean = "Teks kosong"
    if role == "employee":
        rate = "0.9"; bg = "#FFEBEE"; border = "#FF5252"; icon = "👨‍💼"; label = "EMPLOYEE Staff/Supervisor"
    else:
        rate = "1.05"; bg = "#E8F5E9"; border = "#4CAF50"; icon = "🚀"; label = "ENTREPRENEUR Manager/Brand/Usahawan"
    # Use json dumps for safe JS string
    js_text = json.dumps(clean)
    html = f"""
    <div style="background:{bg}; border:2px solid {border}; border-radius:10px; padding:12px; font-family:Inter,sans-serif;">
        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
            <div style="font-weight:800; font-size:10px;">{icon} SPEAKER {label}</div>
            <div style="font-size:8px; background:white; padding:2px 6px; border-radius:8px; border:1px solid {border};">🔊 Voice ON</div>
        </div>
        <div style="background:white; border-radius:6px; padding:8px; font-size:11px; max-height:60px; overflow-y:auto; border:1px dashed #ccc; margin-bottom:8px; font-family:JetBrains Mono;">{clean[:180]}...</div>
        <div style="display:flex; gap:6px;">
            <button onclick="speak_{key_id}()" id="btn_{key_id}" style="flex:1; background:{border}; color:white; border:none; padding:10px; border-radius:8px; font-weight:700; cursor:pointer; font-size:11px;">🔊 PUTAR SUARA {label.split()[0]}</button>
            <button onclick="window.speechSynthesis.cancel()" style="background:#424242; color:white; border:none; padding:10px 12px; border-radius:8px; cursor:pointer;">⏹️</button>
        </div>
        <div id="status_{key_id}" style="font-size:9px; color:#666; margin-top:6px; text-align:center;">Siap - Klik PUTAR, suara aktif</div>
    </div>
    <script>
        function speak_{key_id}() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var txt = {js_text};
                var u = new SpeechSynthesisUtterance(txt);
                u.rate = {rate};
                u.lang = 'id-ID';
                u.volume = 1;
                u.onstart = function(){{ document.getElementById('status_{key_id}').innerHTML='🔊 Berbicara... Voice ON'; }};
                u.onend = function(){{ document.getElementById('status_{key_id}').innerHTML='✅ Selesai - Voice OFF'; }};
                window.speechSynthesis.speak(u);
            }} else {{
                alert('Browser tidak support voice, pakai Chrome');
            }}
        }}
    </script>
    """
    components.html(html, height=210)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.lembar { border-radius: 12px; padding: 22px; margin-bottom: 18px; border-left: 3px dashed #bbb; box-shadow: 4px 4px 0px rgba(0,0,0,0.08); }
.lembar-putih { background: #FFFFFF; border-top: 4px solid #9E9E9E; }
.lembar-merah { background: #FFEBEE; border-top: 4px solid #FF5252; }
.lembar-hijau { background: #E8F5E9; border-top: 4px solid #4CAF50; }
.bursa-card { background: linear-gradient(135deg, #FFF9C4, #FFEB3B); border: 2px solid #FBC02D; border-radius: 12px; padding: 14px; text-align: center; }
.bursa-vote { font-size: 30px; font-weight: 800; color: #F57F17; }
.bursa-label { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #666; }
.jabatan-badge { display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 10px; font-weight: 700; margin: 2px; }
.badge-staff { background: #FFCDD2; color: #C62828; } .badge-supervisor { background: #F8BBD0; color: #AD1457; }
.badge-manager { background: #C8E6C9; color: #2E7D32; } .badge-brand { background: #A5D6A7; color: #1B5E20; } .badge-usahawan { background: #81C784; color: #0D3311; }
.rak { background: white; border: 2px solid #e0e0e0; border-radius: 8px; padding: 10px; text-align: center; height: 95px; display: flex; flex-direction: column; justify-content: center; }
.rak-icon { font-size: 22px; } .rak-title { font-weight: 800; font-size: 11px; } .rak-desc { font-size: 9px; color: #666; font-family: 'JetBrains Mono', monospace; }
.kotak-keberadaan { background: white; border: 1px solid #A5D6A7; border-radius: 10px; padding: 12px; margin: 8px 0; }
.kotak-share { background: #FFF3E0; border: 2px dashed #FF9800; border-radius: 10px; padding: 12px; margin: 10px 0; }
.kotak-jujur { background: #E8F5E9; border: 2px solid #4CAF50; border-radius: 10px; padding: 12px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div style="text-align:center; padding: 6px 0 12px 0;">
    <div style="font-family:'JetBrains Mono'; font-size:9px; letter-spacing:3px; color:#888;">TAVO MALKHUTKHA • V29.4 FIX HIJAU MANAGE + VOICE</div>
    <div style="font-size:22px; font-weight:800; margin:3px 0;">📗📖 BUKU 3 LEMBAR - HIJAU MANAGE + VOICE FIX + KEJUJURAN</div>
    <div style="font-family:'JetBrains Mono'; font-size:9px; color:#fff; background:#4CAF50; display:inline-block; padding:3px 10px; border-radius:20px;">
        Merah=Staff/Supervisor | Hijau=Manager/Brand/Usahawan + Manage | Voice ON Employee & Entrepreneur | Bursa Vote + Share Email
    </div>
</div>
""", unsafe_allow_html=True)

# BURSA DASHBOARD
b1, b2, b3, b4 = st.columns(4)
with b1:
    st.markdown(f'<div class="bursa-card"><div class="bursa-label">TOTAL LOGIN</div><div class="bursa-vote">{st.session_state.bursa_total_login}</div><div class="bursa-label">Orang = Vote</div></div>', unsafe_allow_html=True)
with b2:
    st.markdown(f'<div class="bursa-card" style="background:linear-gradient(135deg,#FFEBEE,#FF5252); border-color:#FF5252;"><div class="bursa-label" style="color:white;">BURSA AKTIF VOTE</div><div class="bursa-vote" style="color:white;">{st.session_state.bursa_active_vote}</div><div class="bursa-label" style="color:white;">Belum Bekerja</div></div>', unsafe_allow_html=True)
with b3:
    st.markdown(f'<div class="bursa-card" style="background:linear-gradient(135deg,#E8F5E9,#4CAF50); border-color:#4CAF50;"><div class="bursa-label" style="color:white;">SUDAH BEKERJA</div><div class="bursa-vote" style="color:white;">{st.session_state.bursa_sudah_bekerja}</div><div class="bursa-label" style="color:white;">Via Share Email</div></div>', unsafe_allow_html=True)
with b4:
    total = st.session_state.bursa_total_login
    persen = int((st.session_state.bursa_sudah_bekerja / total * 100) if total>0 else 0)
    st.markdown(f'<div class="bursa-card" style="background:linear-gradient(135deg,#E3F2FD,#2196F3); border-color:#2196F3;"><div class="bursa-label" style="color:white;">KONVERSI</div><div class="bursa-vote" style="color:white;">{persen}%</div><div class="bursa-label" style="color:white;">Bekerja / Total</div></div>', unsafe_allow_html=True)

st.markdown("#### 📈 Grafik Volume Nilai Orang Banyak Login Dalam Bursa")
if st.session_state.bursa_history:
    import pandas as pd
    df = pd.DataFrame(st.session_state.bursa_history)
    st.line_chart(df, x="jam", y=["vote", "bekerja"], color=["#FF5252", "#4CAF50"])
    st.caption("Merah = Vote Bursa Aktif (belum bekerja) | Hijau = Sudah Bekerja (via share email + kejujuran update) - Bursa otomatis berkurang")

tab1, tab2, tab3 = st.tabs(["📄 PUTIH - FORM LOKER + JABATAN", "🔴 MERAH - EMPLOYEE Staff/Supervisor + Share", "🟢 HIJAU - MANAGE Manager/Brand/Usahawan + Voice Fix"])

# TAB 1 PUTIH
with tab1:
    st.markdown('<div class="lembar lembar-putih"><div style="display:flex; justify-content:space-between;"><div><b>LEMBAR 1 - FORM LOKER + JABATAN + BURSA VOTE</b></div><div style="background:#424242; color:white; padding:4px 10px; border-radius:4px; font-family:JetBrains Mono; font-size:10px;">ASLI - LOKER BURSA</div></div></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama Lengkap *", value=st.session_state.member_data.get("nama",""), placeholder="Budi Setia")
    with col2:
        jabatan = st.selectbox("Jabatan / Posisi *", ["Staff", "Supervisor", "Manager", "Brand Manager", "Usahawan / Entrepreneur"], index=0, help="Staff & Supervisor -> Merah Employee. Manager, Brand Manager, Usahawan -> Hijau Entrepreneur Manage")
        if jabatan in ["Staff", "Supervisor"]:
            st.markdown('<span class="jabatan-badge badge-staff">🔴 Merah Employee</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="jabatan-badge badge-manager">🟢 Hijau Entrepreneur Manage</span>', unsafe_allow_html=True)
    
    col3, col4, col5 = st.columns([1.2, 1, 0.8])
    with col3:
        tempat_lahir = st.text_input("Tempat Lahir *", value=st.session_state.member_data.get("tempat_lahir",""), placeholder="Jakarta Barat")
    with col4:
        tgl_lahir = st.date_input("Tgl Lahir *", value=st.session_state.member_data.get("tgl_lahir_obj", date(1994,9,21)), min_value=date(1960,1,1), max_value=date(2010,12,31))
    with col5:
        umur = date.today().year - tgl_lahir.year
        st.metric("Umur", f"{umur} th")
    
    col6, col7, col8 = st.columns([0.8, 1.1, 1.1])
    with col6:
        wni = st.selectbox("WNI *", ["WNI", "WNA", "Lainnya"])
    with col7:
        email = st.text_input("Email *", value=st.session_state.member_data.get("email",""), placeholder="nama@email.com")
    with col8:
        whatsapp = st.text_input("WhatsApp *", value=st.session_state.member_data.get("whatsapp",""), placeholder="08129xxxx")
    
    col9, col10 = st.columns(2)
    with col9:
        pendidikan = st.selectbox("Pendidikan *", ["SMA/SMK", "D3", "S1", "S2", "S3", "Lainnya"], index=2)
        pendidikan_detail = st.text_input("Jurusan/Universitas", value=st.session_state.member_data.get("pendidikan_detail",""), placeholder="S1 Akuntansi Trisakti")
    with col10:
        pengalaman_tahun = st.selectbox("Pengalaman", ["Fresh Graduate", "<1 Th", "1-2 Th", "3-5 Th", "5-10 Th", ">10 Th"])
    
    pengalaman_kerja = st.text_area("Pengalaman Kerja *", value=st.session_state.member_data.get("pengalaman_kerja",""), placeholder="MS Excel, ERP, Accurate...", height=70)
    skill = st.text_area("Skill *", value=st.session_state.member_data.get("skill",""), placeholder="MS Excel, Software ERP...", height=60)
    
    if st.button("✅ SIMPAN & MASUK BURSA - 1 LOGIN = 1 VOTE", type="primary", use_container_width=True):
        if not nama or not tempat_lahir or not email or not whatsapp:
            st.error("Lengkapi bintang *")
        else:
            is_emp = jabatan in ["Staff", "Supervisor"]
            is_ent = jabatan in ["Manager", "Brand Manager", "Usahawan / Entrepreneur"]
            st.session_state.member_data = {
                "nama": nama, "jabatan": jabatan, "is_employee": is_emp, "is_entrepreneur": is_ent,
                "tempat_lahir": tempat_lahir, "tgl_lahir": tgl_lahir.strftime("%d-%m-%Y"), "tgl_lahir_obj": tgl_lahir, "umur": umur,
                "wni": wni, "email": email, "whatsapp": whatsapp,
                "pendidikan": pendidikan, "pendidikan_detail": pendidikan_detail,
                "pengalaman_tahun": pengalaman_tahun, "pengalaman_kerja": pengalaman_kerja, "skill": skill
            }
            add_bursa_login()
            st.success(f"✅ {nama} ({jabatan}) masuk Bursa! Total: {st.session_state.bursa_total_login} | Aktif: {st.session_state.bursa_active_vote}")
            st.balloons()

# TAB 2 MERAH - EMPLOYEE
with tab2:
    st.markdown('<div class="lembar" style="background:#FFEBEE; border-top:4px solid #FF5252;"><div style="display:flex; justify-content:space-between;"><div><b>LEMBAR 2 - RUANG INTERAKSI - EMPLOYEE ONLY (Staff & Supervisor)</b></div><div style="background:#FF5252; color:white; padding:4px 10px; border-radius:4px; font-size:10px;">MERAH - STAFF/SUPERVISOR</div></div></div>', unsafe_allow_html=True)
    
    if not st.session_state.member_data:
        st.warning("Isi Form Loker Putih dulu"); st.stop()
    md = st.session_state.member_data
    if not md.get("is_employee"):
        st.error(f"Maaf {md['nama']}, jabatan {md['jabatan']} = Manager/Brand/Usahawan. Harusnya masuk HIJAU Entrepreneur, bukan Merah.")
        st.info("Ke tab HIJAU - ENTREPRENEUR")
        st.stop()
    
    st.markdown(f'<div style="background:#FFCDD2; padding:8px; border-radius:8px; font-size:11px; font-family:JetBrains Mono;">✅ KONDISI: {md["nama"]} | {md["jabatan"]} | Staff/Supervisor -> Merah Employee</div>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.1, 0.9])
    with col_left:
        st.markdown("### 👨‍💼 KELOLA STAFF & SUPERVISOR ONLY")
        st.markdown(f"""
        <div style="background:white; border-radius:8px; padding:12px; border:1px solid #FFCDD2; font-size:11px;">
            <b>Nama:</b> {md['nama']} | <b>Jabatan:</b> <span class="jabatan-badge badge-supervisor">{md['jabatan']}</span><br/>
            <b>TTL:</b> {md['tempat_lahir']}, {md['tgl_lahir']} ({md['umur']}th) | {md['wni']}<br/>
            <b>Email/WA:</b> {md['email']} / {md['whatsapp']}<br/>
            <b>Pendidikan:</b> {md['pendidikan']} - {md['pendidikan_detail']}<br/>
            <b>Skill:</b> {md['skill']}<br/>
        </div>
        """, unsafe_allow_html=True)
        
        # Voice Employee FIX
        auto_emp = f"Selamat datang {md['nama']}, jabatan {md['jabatan']}. Anda masuk Staff Supervisor di Merah Employee. Umur {md['umur']} tahun, skill {md['skill']}. Bursa aktif {st.session_state.bursa_active_vote} vote."
        tts_fixed(auto_emp, "employee", "emp_v4")
        
        st.markdown("---")
        st.markdown("#### 🔍 Pencarian Permintaan & Request Penawaran Employee")
        st.markdown('<div class="kotak-share"><b>Sebagai Pencari Kerja:</b> Anda bisa kirim & share ke rekan dan temannya memenuhi kebutuhannya mencari employee yang mau bekerja. Juga permintaan mencari kerja via email.</div>', unsafe_allow_html=True)
        
        # Share via email - Employee
        email_teman = st.text_input("📧 Share info loker Employee via Email ke teman/rekan:", placeholder="teman@email.com - untuk cari kerja / tawarkan jasa", key="share_emp_v4")
        permintaan = st.text_area("Permintaan / Request Penawaran sebagai Pencari Kerja:", placeholder="Contoh: Saya mencari pekerjaan Staff Admin, skill Excel ERP, bersedia ditempatkan di Jakarta...", height=70, key="permintaan_emp")
        if st.button("📧 KIRIM & SHARE - KURANGI BURSA VOTE (Sudah Bekerja?)", key="share_btn_emp_v4"):
            if "@" in email_teman:
                reduce_bursa_share(email_teman, "Employee Share")
                st.success(f"✅ Shared ke {email_teman}! Bursa: {st.session_state.bursa_active_vote} | Sudah Bekerja: {st.session_state.bursa_sudah_bekerja}")
            else:
                st.error("Email tidak valid")
    
    with col_right:
        st.markdown("**📊 Bursa Vote - Employee**")
        st.metric("Vote Aktif di Bursa", st.session_state.bursa_active_vote)
        st.metric("Sudah Bekerja (via Share)", st.session_state.bursa_sudah_bekerja)
        
        # Kolom Kejujuran
        st.markdown('<div class="kotak-jujur"><b>✅ Kolom Kejujuran Update</b><br/>Centang jika sudah diterima kerja, bursa otomatis berkurang</div>', unsafe_allow_html=True)
        sudah_kerja_emp = st.checkbox("✅ Saya Sudah Diterima Kerja (Update Jujur)", value=st.session_state.sudah_diterima_kerja, key="jujur_emp")
        if sudah_kerja_emp and not st.session_state.sudah_diterima_kerja:
            st.session_state.sudah_diterima_kerja = True
            if st.session_state.bursa_active_vote > 0:
                reduce_bursa_share(md['email'], "Sudah Diterima Kerja - Kejujuran")
                st.success("Terima kasih kejujurannya! Bursa berkurang -1, sudah bekerja +1")
                st.balloons()
        
        if st.session_state.bursa_share_log:
            st.markdown("**Log Share:**")
            for log in st.session_state.bursa_share_log[-3:]:
                st.caption(f"{log['waktu']} {log['oleh']} -> {log['ke']} ({log['alasan']})")

# TAB 3 HIJAU - ENTREPRENEUR MANAGE
with tab3:
    st.markdown('<div class="lembar" style="background:#E8F5E9; border-top:4px solid #4CAF50;"><div style="display:flex; justify-content:space-between;"><div><b>LEMBAR 3 - RUANG BOARDING - MANAGE & SELEVELNYA (Manager, Brand Manager, Usahawan)</b></div><div style="background:#4CAF50; color:white; padding:4px 10px; border-radius:4px; font-size:10px;">HIJAU - MANAGE</div></div></div>', unsafe_allow_html=True)
    
    if not st.session_state.member_data:
        st.warning("Isi Putih dulu"); st.stop()
    md = st.session_state.member_data
    if not md.get("is_entrepreneur"):
        st.error(f"Maaf {md['nama']}, jabatan {md['jabatan']} = Staff/Supervisor. Harusnya masuk MERAH Employee.")
        st.info("Ke tab MERAH - EMPLOYEE")
        st.stop()
    
    st.markdown(f'<div style="background:#C8E6C9; padding:8px; border-radius:8px; font-size:11px; font-family:JetBrains Mono;">✅ KONDISI: {md["nama"]} | {md["jabatan"]} | Manager/Brand/Usahawan -> Hijau Manage Entrepreneur</div>', unsafe_allow_html=True)
    
    # Keterangan keberadaannya - FIX yang diminta
    st.markdown("#### 📍 Keterangan Keberadaan - Manage & Selevelnya")
    st.markdown("""
    <div class="kotak-keberadaan">
        <b>🟢 LEMBAR HIJAU UNTUK:</b><br/>
        • <b>Manager:</b> Mengelola tim Staff & Supervisor, bertanggung jawab OEE 95%, KPI, ERP Jam 9 Tepat, SOP Kebersihan Senin<br/>
        • <b>Brand Manager:</b> Mengelola brand, strategi marketing, koordinasi dengan Manager, laporan ke Usahawan<br/>
        • <b>Usahawan / Entrepreneur:</b> Pemilik usaha, pengambil keputusan tertinggi, fondasi Alkitab Tavo Malkhutkha, storage SOP ERP OEE KPI Alkitab permanen<br/>
        <br/>
        <b>Peran di Bursa:</b> Mencari employee yang mau bekerja, membuat permintaan lowongan, request penawaran employee via email share ke rekan
    </div>
    """, unsafe_allow_html=True)
    
    col_e_left, col_e_right = st.columns([1, 1])
    with col_e_left:
        st.markdown("### 🗄️ KELOLA MANAGER & BRAND & USAHAWAN ONLY")
        st.markdown(f"""
        <div style="background:white; border-radius:8px; padding:12px; border:1px solid #A5D6A7; font-size:11px;">
            <b>Nama:</b> {md['nama']} | <b>Jabatan:</b> <span class="jabatan-badge badge-manager">{md['jabatan']}</span><br/>
            <b>TTL:</b> {md['tempat_lahir']}, {md['tgl_lahir']} ({md['umur']}th) | {md['wni']}<br/>
            <b>Email/WA:</b> {md['email']} / {md['whatsapp']}<br/>
            <b>Pendidikan:</b> {md['pendidikan']} - {md['pendidikan_detail']}<br/>
            <b>Skill Manage:</b> {md['skill']}<br/>
            <b>Bursa:</b> Total {st.session_state.bursa_total_login} vote | Aktif {st.session_state.bursa_active_vote} | Bekerja {st.session_state.bursa_sudah_bekerja}
        </div>
        """, unsafe_allow_html=True)
        
        # Voice Entrepreneur FIX - ini yang belum bunyi tadi
        auto_ent = f"Halo {md['nama']}, jabatan {md['jabatan']}. Anda masuk kategori Manager Brand Manager Usahawan di Lembar Hijau Manage. Anda mengelola tim, OEE 95 persen, KPI, ERP. Bursa total {st.session_state.bursa_total_login} vote, aktif {st.session_state.bursa_active_vote}, sudah bekerja {st.session_state.bursa_sudah_bekerja}. Silakan share via email ke rekan."
        tts_fixed(auto_ent, "entrepreneur", "ent_v4_fix")
        
        st.markdown("---")
        st.markdown("#### 🔍 Pencarian Employee Yang Mau Bekerja (Permintaan & Penawaran)")
        st.markdown('<div class="kotak-share"><b>Sebagai Manager/Brand Manager/Usahawan:</b> Anda bisa kirim & share ke rekan dan temannya memenuhi kebutuhannya mencari employee yang mau bekerja. Permintaan lowongan & request penawaran employee via email.</div>', unsafe_allow_html=True)
        
        # Share via email - Entrepreneur
        email_rekan = st.text_input("📧 Share info lowongan Manager via Email ke rekan/teman:", placeholder="rekan@perusahaan.com - untuk cari employee", key="share_hijau_v4")
        permintaan_manager = st.text_area("Permintaan Lowongan / Request Employee yang Dicari:", placeholder="Contoh: Dicari Staff Admin, Supervisor Gudang, skill Excel ERP Accurate, penempatan Jakarta Barat, segera...", height=80, key="permintaan_manager")
        penawaran_manager = st.text_area("Penawaran Gaji / Benefit untuk Employee:", placeholder="Contoh: Gaji 5-7jt, tunjangan, SOP jelas, ERP jam 9 tepat, OEE 95%...", height=70, key="penawaran_manager")
        
        if st.button("📧 KIRIM PERMINTAAN & SHARE - KURANGI BURSA", key="share_hijau_btn_v4", type="primary"):
            if "@" in email_rekan:
                reduce_bursa_share(email_rekan, f"Manager {md['jabatan']} cari employee")
                st.success(f"✅ Permintaan terkirim ke {email_rekan}! Bursa: {st.session_state.bursa_active_vote} | Bekerja: {st.session_state.bursa_sudah_bekerja}")
            else:
                st.error("Email rekan tidak valid")
    
    with col_e_right:
        st.markdown("### 📊 Bursa + Kejujuran + Grafik")
        st.metric("Vote Aktif di Bursa", st.session_state.bursa_active_vote)
        st.metric("Sudah Bekerja", st.session_state.bursa_sudah_bekerja)
        
        # Kolom kecil kejujuran
        st.markdown('<div class="kotak-jujur"><b>✅ Kolom Kejujuran - Update Sudah Diterima Kerja</b><br/>Centang jika pendaftar ternyata sudah diterima kerja (jujur), bursa berkurang otomatis</div>', unsafe_allow_html=True)
        col_j1, col_j2 = st.columns(2)
        with col_j1:
            sudah_diterima = st.checkbox("✅ Sudah Diterima Kerja", value=st.session_state.sudah_diterima_kerja, key="jujur_hijau", help="Kejujuran update: ternyata sudah diterima kerja")
        with col_j2:
            perusahaan = st.text_input("Di perusahaan mana?", placeholder="PT XYZ", key="perusahaan_jujur")
        
        if sudah_diterima and st.button("📝 UPDATE KEJUJURAN - KURANGI BURSA", key="btn_jujur_hijau"):
            if not st.session_state.sudah_diterima_kerja:
                st.session_state.sudah_diterima_kerja = True
                reduce_bursa_share(md['email'], f"Sudah Diterima di {perusahaan} - Kejujuran")
                st.success(f"Terima kasih kejujuran {md['nama']}! Update: Sudah diterima di {perusahaan}. Bursa -1, Bekerja +1")
                st.balloons()
        
        st.markdown("---")
        st.markdown("**📊 Grafik Bursa Volume**")
        if st.session_state.bursa_history:
            import pandas as pd
            df = pd.DataFrame(st.session_state.bursa_history)
            st.bar_chart(df, x="jam", y=["vote", "bekerja"], color=["#FF5252", "#4CAF50"])
        
        st.markdown("**Log Share & Bursa:**")
        for log in st.session_state.bursa_share_log[-4:]:
            st.caption(f"{log['waktu']} {log['oleh']} -> {log['ke']} | {log['alasan']}")

# CSV EXPORT
st.markdown("---")
st.markdown("#### 📥 Export CSV Bursa Vote")
col_csv1, col_csv2 = st.columns(2)
with col_csv1:
    if st.session_state.bursa_history:
        import pandas as pd
        df_bursa = pd.DataFrame(st.session_state.bursa_history)
        csv_bursa = df_bursa.to_csv(index=False).encode('utf-8')
        st.download_button(label="📊 Download CSV Bursa", data=csv_bursa, file_name=f"bursa_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")
with col_csv2:
    if st.session_state.member_data:
        import pandas as pd
        data_export = {
            "Nama": [st.session_state.member_data.get("nama","")],
            "Jabatan": [st.session_state.member_data.get("jabatan","")],
            "Email": [st.session_state.member_data.get("email","")],
            "Bursa_Total": [st.session_state.bursa_total_login],
            "Bursa_Aktif": [st.session_state.bursa_active_vote],
            "Bursa_Bekerja": [st.session_state.bursa_sudah_bekerja],
        }
        df_m = pd.DataFrame(data_export)
        csv_m = df_m.to_csv(index=False).encode('utf-8')
        st.download_button(label="👤 Download CSV Loker", data=csv_m, file_name=f"loker_{st.session_state.member_data.get('nama','')}.csv", mime="text/csv")

st.markdown(f"""
<div style="background:white; border-radius:12px; padding:12px; border:2px solid #eee; text-align:center; font-family:'JetBrains Mono'; font-size:9px;">
<div style="background:#4CAF50; color:white; display:inline-block; padding:4px 12px; border-radius:20px; font-weight:700;">📗 V29.4 FIX • Hijau Manage + Voice ON • Merah & Hijau Share Email + Bursa + Kejujuran</div>
<div style="margin-top:6px;">Total: {st.session_state.bursa_total_login} | Aktif: {st.session_state.bursa_active_vote} | Bekerja: {st.session_state.bursa_sudah_bekerja} | Voice Employee & Entrepreneur ON</div>
</div>
""", unsafe_allow_html=True)
