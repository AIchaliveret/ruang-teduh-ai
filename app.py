
"""
RUANG TEDUH - BUKU 3 LEMBAR V29.3 - BURSA VOTE + KONDISI JABATAN
Update:
- Lembar Merah = Employee = Staff + Supervisor ONLY
- Lembar Hijau = Entrepreneur = Manager + Brand Manager + Usahawan ONLY
- Bursa Vote: 1 login = 1 vote, 2 login = 2 vote dst, grafik volume bursa
- Bursa berkurang karena sharing via email ke teman (sudah bekerja)
- Form Loker Lengkap: nama, tempat tgl lahir, WNI, email, WA, pengalaman, pendidikan, skill + Jabatan
- No Database - session only
"""

import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import date, datetime
import random

st.set_page_config(page_title="Ruang Teduh V29.3 - Bursa Vote", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

# ========== SESSION STATE - BURSA ==========
if "member_data" not in st.session_state:
    st.session_state.member_data = {}
if "member_terikat" not in st.session_state:
    st.session_state.member_terikat = False
if "payment_done" not in st.session_state:
    st.session_state.payment_done = False

# BURSA SYSTEM
if "bursa_total_login" not in st.session_state:
    st.session_state.bursa_total_login = 12  # simulasi awal ada 12 orang
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

def add_bursa_login():
    """Tiap login = +1 vote bursa"""
    st.session_state.bursa_total_login += 1
    st.session_state.bursa_active_vote += 1
    now = datetime.now().strftime("%H:%M")
    st.session_state.bursa_history.append({
        "jam": now,
        "vote": st.session_state.bursa_active_vote,
        "bekerja": st.session_state.bursa_sudah_bekerja
    })
    # keep last 10
    if len(st.session_state.bursa_history) > 10:
        st.session_state.bursa_history = st.session_state.bursa_history[-10:]

def share_email_reduce_bursa(email_teman):
    """Sharing via email = vote bursa berkurang, pindah ke sudah bekerja"""
    if st.session_state.bursa_active_vote > 0:
        st.session_state.bursa_active_vote -= 1
        st.session_state.bursa_sudah_bekerja += 1
        now = datetime.now().strftime("%H:%M")
        st.session_state.bursa_history.append({
            "jam": now,
            "vote": st.session_state.bursa_active_vote,
            "bekerja": st.session_state.bursa_sudah_bekerja
        })
        st.session_state.bursa_share_log.append({
            "waktu": now,
            "ke": email_teman,
            "oleh": st.session_state.member_data.get("nama","Member")
        })
        if len(st.session_state.bursa_history) > 10:
            st.session_state.bursa_history = st.session_state.bursa_history[-10:]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.lembar { border-radius: 12px; padding: 22px; margin-bottom: 18px; border-left: 3px dashed #bbb; box-shadow: 4px 4px 0px rgba(0,0,0,0.08); }
.lembar-putih { background: #FFFFFF; border-top: 4px solid #9E9E9E; }
.lembar-merah { background: #FFEBEE; border-top: 4px solid #FF5252; }
.lembar-hijau { background: #E8F5E9; border-top: 4px solid #4CAF50; }
.lembar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 2px dashed rgba(0,0,0,0.1); }
.lembar-label { font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700; padding: 4px 10px; border-radius: 4px; }
.label-putih { background: #424242; color: white; } .label-merah { background: #FF5252; color: white; } .label-hijau { background: #4CAF50; color: white; }
.bursa-card { background: linear-gradient(135deg, #FFF9C4, #FFEB3B); border: 2px solid #FBC02D; border-radius: 12px; padding: 14px; text-align: center; }
.bursa-vote { font-size: 32px; font-weight: 800; color: #F57F17; }
.bursa-label { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #666; }
.jabatan-badge { display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 10px; font-weight: 700; margin: 2px; }
.badge-staff { background: #FFCDD2; color: #C62828; } .badge-supervisor { background: #F8BBD0; color: #AD1457; }
.badge-manager { background: #C8E6C9; color: #2E7D32; } .badge-brand { background: #A5D6A7; color: #1B5E20; } .badge-usahawan { background: #81C784; color: #0D3311; }
.rak { background: white; border: 2px solid #e0e0e0; border-radius: 8px; padding: 10px; text-align: center; height: 95px; display: flex; flex-direction: column; justify-content: center; }
.rak-icon { font-size: 22px; margin-bottom: 3px; } .rak-title { font-weight: 800; font-size: 11px; } .rak-desc { font-size: 9px; color: #666; font-family: 'JetBrains Mono', monospace; }
</style>
""", unsafe_allow_html=True)

def tts_comp(text, role, key_id):
    safe = text.replace('"', '\"').replace("'", "\'").replace("\n", " ").strip()[:250]
    if not safe:
        safe = "Teks kosong"
    if role == "employee":
        rate = "0.9"; bg = "#FFEBEE"; border = "#FF5252"; icon = "👨‍💼"; label = "EMPLOYEE STAFF/SUPERVISOR"
    else:
        rate = "1.05"; bg = "#E8F5E9"; border = "#4CAF50"; icon = "🚀"; label = "ENTREPRENEUR MANAGER/BRAND/USAHAWAN"
    html = f"""
    <div style="background:{bg}; border:2px solid {border}; border-radius:10px; padding:10px; font-family:Inter;">
        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <div style="font-weight:800; font-size:10px;">{icon} {label}</div>
            <div style="font-size:8px; background:white; padding:2px 6px; border-radius:8px; border:1px solid {border};">🔊 TTS</div>
        </div>
        <div style="background:white; border-radius:6px; padding:6px; font-size:10px; max-height:50px; overflow-y:auto; border:1px dashed #ccc; margin-bottom:6px; font-family:JetBrains Mono;">{text[:160]}...</div>
        <div style="display:flex; gap:4px;">
            <button onclick="speak_{key_id}()" style="flex:1; background:{border}; color:white; border:none; padding:6px; border-radius:6px; font-weight:700; cursor:pointer; font-size:10px;">🔊 PUTAR</button>
            <button onclick="window.speechSynthesis.cancel()" style="background:#424242; color:white; border:none; padding:6px 8px; border-radius:6px; cursor:pointer;">⏹️</button>
        </div>
    </div>
    <script>
        function speak_{key_id}() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                let u = new SpeechSynthesisUtterance("{safe}");
                u.rate = {rate}; u.lang = 'id-ID';
                window.speechSynthesis.speak(u);
            }}
        }}
    </script>
    """
    components.html(html, height=160)

# HEADER
st.markdown("""
<div style="text-align:center; padding: 6px 0 12px 0;">
    <div style="font-family:'JetBrains Mono'; font-size:9px; letter-spacing:3px; color:#888;">TAVO MALKHUTKHA • V29.3 BURSA VOTE</div>
    <div style="font-size:22px; font-weight:800; margin:3px 0;">📊📖 BUKU 3 LEMBAR - BURSA + KONDISI JABATAN</div>
    <div style="font-family:'JetBrains Mono'; font-size:9px; color:#fff; background:#424242; display:inline-block; padding:3px 10px; border-radius:20px;">
        Merah=Staff+Supervisor | Hijau=Manager+Brand Manager+Usahawan | Bursa: Login=Vote | Share Email=Berkurang
    </div>
</div>
""", unsafe_allow_html=True)

# BURSA DASHBOARD ATAS - SELALU MUNCUL
b1, b2, b3, b4 = st.columns(4)
with b1:
    st.markdown(f'<div class="bursa-card"><div class="bursa-label">TOTAL LOGIN</div><div class="bursa-vote">{st.session_state.bursa_total_login}</div><div class="bursa-label">Orang</div></div>', unsafe_allow_html=True)
with b2:
    st.markdown(f'<div class="bursa-card" style="background:linear-gradient(135deg,#FFEBEE,#FF5252); border-color:#FF5252;"><div class="bursa-label" style="color:white;">BURSA AKTIF VOTE</div><div class="bursa-vote" style="color:white;">{st.session_state.bursa_active_vote}</div><div class="bursa-label" style="color:white;">Vote di Bursa</div></div>', unsafe_allow_html=True)
with b3:
    st.markdown(f'<div class="bursa-card" style="background:linear-gradient(135deg,#E8F5E9,#4CAF50); border-color:#4CAF50;"><div class="bursa-label" style="color:white;">SUDAH BEKERJA</div><div class="bursa-vote" style="color:white;">{st.session_state.bursa_sudah_bekerja}</div><div class="bursa-label" style="color:white;">Via Share Email</div></div>', unsafe_allow_html=True)
with b4:
    total = st.session_state.bursa_total_login
    persen = int((st.session_state.bursa_sudah_bekerja / total * 100) if total>0 else 0)
    st.markdown(f'<div class="bursa-card" style="background:linear-gradient(135deg,#E3F2FD,#2196F3); border-color:#2196F3;"><div class="bursa-label" style="color:white;">KONVERSI BURSA</div><div class="bursa-vote" style="color:white;">{persen}%</div><div class="bursa-label" style="color:white;">Bekerja / Total</div></div>', unsafe_allow_html=True)

# Grafik Bursa Volume
st.markdown("#### 📈 Grafik Volume Nilai Orang Banyak Login Dalam Bursa")
if st.session_state.bursa_history:
    import pandas as pd
    df = pd.DataFrame(st.session_state.bursa_history)
    st.line_chart(df, x="jam", y=["vote", "bekerja"], color=["#FF5252", "#4CAF50"])
    st.caption("Merah = Vote Bursa Aktif (belum bekerja) | Hijau = Sudah Bekerja (via share email ke teman/rekan) - Bursa otomatis berkurang")

tab1, tab2, tab3 = st.tabs(["📄 PUTIH - FORM LOKER + JABATAN", "🔴 MERAH - EMPLOYEE Staff/Supervisor", "🟢 HIJAU - ENTREPRENEUR Manager/Brand/Usahawan"])

# ==================== LEMBAR 1 PUTIH - FORM LOKER + JABATAN ====================
with tab1:
    st.markdown('<div class="lembar lembar-putih"><div class="lembar-header"><div><b>LEMBAR 1 - FORM LOKER + JABATAN + BURSA VOTE</b> (1 Login = 1 Vote)</div><div class="lembar-label label-putih">ASLI - LOKER BURSA</div></div></div>', unsafe_allow_html=True)
    
    st.markdown("#### 📝 Form Loker Lengkap + Kondisi Jabatan")
    st.caption("Merah untuk Staff & Supervisor saja. Hijau untuk Manager, Brand Manager, Usahawan. Tiap login = 1 vote bursa.")
    
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama Lengkap *", value=st.session_state.member_data.get("nama",""), placeholder="Even Garden")
    with col2:
        jabatan = st.selectbox("Jabatan / Posisi Dilamar * (Kondisi Lembar)", 
            ["Staff", "Supervisor", "Manager", "Brand Manager", "Usahawan / Entrepreneur"],
            index=0,
            help="Staff & Supervisor -> Masuk Lembar Merah Employee. Manager, Brand Manager, Usahawan -> Masuk Lembar Hijau Entrepreneur"
        )
        # Show badge
        if jabatan in ["Staff", "Supervisor"]:
            st.markdown(f'<span class="jabatan-badge badge-staff">🔴 Akan masuk MERAH - Employee (Staff/Supervisor)</span>' if jabatan=="Staff" else '<span class="jabatan-badge badge-supervisor">🔴 Akan masuk MERAH - Employee (Supervisor)</span>', unsafe_allow_html=True)
        else:
            if jabatan == "Manager":
                st.markdown('<span class="jabatan-badge badge-manager">🟢 Akan masuk HIJAU - Entrepreneur (Manager)</span>', unsafe_allow_html=True)
            elif jabatan == "Brand Manager":
                st.markdown('<span class="jabatan-badge badge-brand">🟢 Akan masuk HIJAU - Entrepreneur (Brand Manager)</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="jabatan-badge badge-usahawan">🟢 Akan masuk HIJAU - Entrepreneur (Usahawan)</span>', unsafe_allow_html=True)
    
    col3, col4, col5 = st.columns([1.2, 1, 0.8])
    with col3:
        tempat_lahir = st.text_input("Tempat Lahir *", value=st.session_state.member_data.get("tempat_lahir",""), placeholder="Jakarta")
    with col4:
        tgl_lahir = st.date_input("Tgl Lahir *", value=st.session_state.member_data.get("tgl_lahir_obj", date(2000,1,1)), min_value=date(1960,1,1), max_value=date(2010,12,31))
    with col5:
        umur = date.today().year - tgl_lahir.year
        st.metric("Umur", f"{umur} th")
    
    col6, col7, col8 = st.columns([0.8, 1.1, 1.1])
    with col6:
        wni = st.selectbox("WNI *", ["WNI", "WNA", "Lainnya"])
    with col7:
        email = st.text_input("Email *", value=st.session_state.member_data.get("email",""), placeholder="nama@email.com")
    with col8:
        whatsapp = st.text_input("WhatsApp *", value=st.session_state.member_data.get("whatsapp",""), placeholder="0812xxx")
    
    col9, col10 = st.columns(2)
    with col9:
        pendidikan = st.selectbox("Pendidikan *", ["SMA/SMK", "D3", "S1", "S2", "S3", "Lainnya"], index=2)
        pendidikan_detail = st.text_input("Jurusan/Universitas", value=st.session_state.member_data.get("pendidikan_detail",""), placeholder="Teknik Informatika - UI")
    with col10:
        pengalaman_tahun = st.selectbox("Pengalaman", ["Fresh Graduate", "<1 Th", "1-2 Th", "3-5 Th", "5-10 Th", ">10 Th"])
    
    pengalaman_kerja = st.text_area("Pengalaman Kerja *", value=st.session_state.member_data.get("pengalaman_kerja",""), placeholder="2 tahun di PT XYZ...", height=70)
    skill = st.text_area("Skill *", value=st.session_state.member_data.get("skill",""), placeholder="SOP, ERP, OEE, KPI, Excel...", height=60)
    
    st.markdown("---")
    if st.button("✅ SIMPAN & MASUK BURSA - 1 LOGIN = 1 VOTE", type="primary", use_container_width=True):
        if not nama or not tempat_lahir or not email or not whatsapp:
            st.error("Lengkapi bintang * bro")
        else:
            is_employee = jabatan in ["Staff", "Supervisor"]
            is_entrepreneur = jabatan in ["Manager", "Brand Manager", "Usahawan / Entrepreneur"]
            
            st.session_state.member_data = {
                "nama": nama, "jabatan": jabatan, "is_employee": is_employee, "is_entrepreneur": is_entrepreneur,
                "tempat_lahir": tempat_lahir, "tgl_lahir": tgl_lahir.strftime("%d-%m-%Y"), "tgl_lahir_obj": tgl_lahir, "umur": umur,
                "wni": wni, "email": email, "whatsapp": whatsapp,
                "pendidikan": pendidikan, "pendidikan_detail": pendidikan_detail,
                "pengalaman_tahun": pengalaman_tahun, "pengalaman_kerja": pengalaman_kerja, "skill": skill
            }
            add_bursa_login()
            st.success(f"✅ {nama} ({jabatan}) masuk Bursa! Total Login: {st.session_state.bursa_total_login} | Vote Aktif: {st.session_state.bursa_active_vote} | {'-> Akan ke MERAH Employee (Staff/Supervisor)' if is_employee else '-> Akan ke HIJAU Entrepreneur (Manager/Brand/Usahawan)'}")
            st.balloons()
    
    if st.session_state.member_data:
        md = st.session_state.member_data
        st.info(f"**{md['nama']}** ({md['jabatan']}) | {md['tempat_lahir']}, {md['tgl_lahir']} | {md['email']} | {md['wni']} | Bursa Vote Aktif: {st.session_state.bursa_active_vote}")

# ==================== LEMBAR 2 MERAH - EMPLOYEE ONLY ====================
with tab2:
    st.markdown('<div class="lembar lembar-merah"><div class="lembar-header"><div><b>LEMBAR 2 - RUANG INTERAKSI - EMPLOYEE ONLY (Staff & Supervisor)</b></div><div class="lembar-label label-merah">MERAH - STAFF/SUPERVISOR SAJA</div></div></div>', unsafe_allow_html=True)
    
    if not st.session_state.member_data:
        st.warning("Isi Form Loker Putih dulu"); st.stop()
    
    md = st.session_state.member_data
    
    # KONDISI JABATAN
    if not md.get("is_employee"):
        st.error(f"⚠️ Maaf {md['nama']}, jabatan Anda {md['jabatan']} adalah Manager/Brand Manager/Usahawan. Anda seharusnya masuk LEMBAR HIJAU Entrepreneur, bukan Merah. Lembar Merah hanya untuk Staff & Supervisor.")
        st.info("Silakan ke tab HIJAU - ENTREPRENEUR untuk Manager, Brand Manager, Usahawan")
        st.stop()
    
    st.markdown(f"<div style='background:#FFCDD2; padding:8px; border-radius:8px; font-size:11px; font-family:JetBrains Mono;'>✅ KONDISI TERPENUHI: {md['nama']} | Jabatan: {md['jabatan']} | ✅ Termasuk Staff/Supervisor -> Layak Masuk MERAH Employee</div>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.1, 0.9])
    with col_left:
        st.markdown("### 👨‍💼 KELOLA STAFF & SUPERVISOR ONLY")
        st.markdown(f"""
        <div style="background:white; border-radius:8px; padding:10px; border:1px solid #FFCDD2; font-size:11px;">
            <b>Nama:</b> {md['nama']} | <b>Jabatan:</b> <span class="jabatan-badge badge-staff">{md['jabatan']}</span><br/>
            <b>TTL:</b> {md['tempat_lahir']}, {md['tgl_lahir']} ({md['umur']}th) | {md['wni']}<br/>
            <b>Email/WA:</b> {md['email']} / {md['whatsapp']}<br/>
            <b>Pendidikan:</b> {md['pendidikan']} - {md['pendidikan_detail']}<br/>
            <b>Skill:</b> {md['skill']}<br/>
        </div>
        """, unsafe_allow_html=True)
        
        auto_emp = f"Selamat datang {md['nama']}, jabatan {md['jabatan']}. Anda masuk kategori Staff Supervisor di Lembar Merah Employee. Data umur {md['umur']} tahun, skill {md['skill']} akan kami kelola SOP ERP."
        tts_comp(auto_emp, "employee", "emp_cond")
        
        st.markdown("---")
        st.markdown("**🔗 Sharing Email - Kurangi Bursa Vote (Sudah Bekerja)**")
        email_teman = st.text_input("Share info loker via Email ke teman/rekan:", placeholder="teman@email.com", key="share_emp")
        if st.button("📧 SHARE & KURANGI BURSA VOTE", key="share_btn_emp"):
            if "@" in email_teman:
                share_email_reduce_bursa(email_teman)
                st.success(f"✅ Shared ke {email_teman}! Bursa Vote berkurang: {st.session_state.bursa_active_vote} | Sudah Bekerja: {st.session_state.bursa_sudah_bekerja}")
                st.toast(f"Vote bursa berkurang karena {md['nama']} sudah sharing ke {email_teman} - sudah bekerja")
            else:
                st.error("Email teman tidak valid")
        
        if st.session_state.bursa_share_log:
            st.markdown("**Log Share (Bursa Berkurang):**")
            for log in st.session_state.bursa_share_log[-3:]:
                st.caption(f"{log['waktu']} - {log['oleh']} share ke {log['ke']} -> Bursa -1, Bekerja +1")
    
    with col_right:
        st.markdown("**📊 Bursa Vote - Employee**")
        st.metric("Vote Aktif di Bursa", st.session_state.bursa_active_vote)
        st.metric("Sudah Bekerja (via Share)", st.session_state.bursa_sudah_bekerja)
        st.info("Semakin banyak share via email ke teman/rekan, semakin berkurang vote bursa karena sudah bekerja")

# ==================== LEMBAR 3 HIJAU - ENTREPRENEUR ONLY ====================
with tab3:
    st.markdown('<div class="lembar lembar-hijau"><div class="lembar-header"><div><b>LEMBAR 3 - RUANG BOARDING - ENTREPRENEUR ONLY (Manager, Brand Manager, Usahawan)</b></div><div class="lembar-label label-hijau">HIJAU - MANAGER/BRAND/USAHAWAN</div></div></div>', unsafe_allow_html=True)
    
    if not st.session_state.member_data:
        st.warning("Isi Putih dulu"); st.stop()
    
    md = st.session_state.member_data
    
    # KONDISI JABATAN
    if not md.get("is_entrepreneur"):
        st.error(f"⚠️ Maaf {md['nama']}, jabatan Anda {md['jabatan']} adalah Staff/Supervisor. Anda seharusnya masuk LEMBAR MERAH Employee, bukan Hijau. Lembar Hijau hanya untuk Manager, Brand Manager, Usahawan.")
        st.info("Silakan ke tab MERAH - EMPLOYEE untuk Staff & Supervisor")
        st.stop()
    
    st.markdown(f"<div style='background:#C8E6C9; padding:8px; border-radius:8px; font-size:11px; font-family:JetBrains Mono;'>✅ KONDISI TERPENUHI: {md['nama']} | Jabatan: {md['jabatan']} | ✅ Termasuk Manager/Brand Manager/Usahawan -> Layak Masuk HIJAU Entrepreneur</div>", unsafe_allow_html=True)
    
    col_e_left, col_e_right = st.columns([0.9, 1.1])
    with col_e_left:
        st.markdown("### 🗄️ STORAGE + BURSA MANAGER")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.markdown('<div class="rak"><div class="rak-icon">📜</div><div class="rak-title">SOP</div><div class="rak-desc">Manager</div></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="rak"><div class="rak-icon">🏢</div><div class="rak-title">ERP</div><div class="rak-desc">Brand</div></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="rak"><div class="rak-icon">⚙️</div><div class="rak-title">OEE</div><div class="rak-desc">Usahawan</div></div>', unsafe_allow_html=True)
        with c4: st.markdown('<div class="rak"><div class="rak-icon">📈</div><div class="rak-title">KPI</div><div class="rak-desc">Bursa</div></div>', unsafe_allow_html=True)
        with c5: st.markdown('<div class="rak"><div class="rak-icon">📖</div><div class="rak-title">ALKITAB</div><div class="rak-desc">Fondasi</div></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**📄 INVOICE + BURSA VOTE**")
        if st.button("✅ BAYAR QRIS - SIMPAN & TAMBAH BURSA", type="primary", use_container_width=True):
            st.session_state.payment_done = True
            st.success(f"LUNAS - {md['nama']} ({md['jabatan']}) Masuk Storage Hijau + Bursa")
        
        st.code(f"""INVOICE BURSA V29.3
Nama: {md['nama']}
Jabatan: {md['jabatan']} (Entrepreneur)
TTL: {md['tempat_lahir']}, {md['tgl_lahir']}
WNI: {md['wni']}
Email: {md['email']} | WA: {md['whatsapp']}
Pendidikan: {md['pendidikan']} - {md['pendidikan_detail']}
Bursa Total Login: {st.session_state.bursa_total_login} vote
Bursa Aktif: {st.session_state.bursa_active_vote} vote
Sudah Bekerja: {st.session_state.bursa_sudah_bekerja} (via share)
Storage: SOP/ERP/OEE/KPI/Alkitab
Status: {'LUNAS & BURSA AKTIF' if st.session_state.payment_done else 'PENDING'}
""", language="text")
        
        st.markdown("**🔗 Share Email - Bursa Berkurang**")
        email_teman_h = st.text_input("Share via Email ke rekan:", placeholder="rekan@bisnis.com", key="share_hijau")
        if st.button("📧 SHARE INFO - KURANGI BURSA", key="share_hijau_btn"):
            if "@" in email_teman_h:
                share_email_reduce_bursa(email_teman_h)
                st.success(f"Shared! Bursa Vote: {st.session_state.bursa_active_vote} -> Sudah Bekerja: {st.session_state.bursa_sudah_bekerja}")
            else:
                st.error("Email tidak valid")
    
    with col_e_right:
        st.markdown("### 🚀 TTS ENTREPRENEUR - MANAGER/BRAND/USAHAWAN")
        auto_ent = f"Halo {md['nama']}, jabatan {md['jabatan']}. Anda kategori Manager Brand Manager Usahawan masuk Lembar Hijau Entrepreneur. Umur {md['umur']} tahun, pengalaman {md['pengalaman_tahun']}, skill {md['skill']}. Bursa saat ini total {st.session_state.bursa_total_login} vote, aktif {st.session_state.bursa_active_vote}, sudah bekerja {st.session_state.bursa_sudah_bekerja}."
        tts_comp(auto_ent, "entrepreneur", "ent_cond")
        
        st.markdown("---")
        st.markdown("**📊 Grafik Bursa Volume - Manager View**")
        if st.session_state.bursa_history:
            import pandas as pd
            df = pd.DataFrame(st.session_state.bursa_history)
            st.bar_chart(df, x="jam", y=["vote", "bekerja"], color=["#FF5252", "#4CAF50"])
            st.caption("Volume nilai orang banyak login dalam bursa. Merah = vote aktif. Hijau = sudah bekerja via share email, bursa berkurang.")
        
        st.markdown("**Log Bursa Share:**")
        for log in st.session_state.bursa_share_log[-5:]:
            st.caption(f"{log['waktu']} {log['oleh']} -> {log['ke']}")

# ========== CSV EXPORT ==========
st.markdown("---")
st.markdown("#### 📥 Export CSV Bursa Vote - Download Data")
col_csv1, col_csv2 = st.columns(2)
with col_csv1:
    if st.session_state.bursa_history:
        import pandas as pd
        df_bursa = pd.DataFrame(st.session_state.bursa_history)
        csv_bursa = df_bursa.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Download CSV Bursa Vote",
            data=csv_bursa,
            file_name=f"bursa_vote_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            help="File CSV berisi jam, vote aktif, sudah bekerja - bisa dibuka di Excel"
        )
        st.caption(f"Isi: {len(df_bursa)} baris data bursa - Total Login {st.session_state.bursa_total_login} vote")
    else:
        st.info("Belum ada data bursa")

with col_csv2:
    if st.session_state.member_data:
        import pandas as pd
        # Data member + bursa
        data_export = {
            "Nama": [st.session_state.member_data.get("nama","")],
            "Jabatan": [st.session_state.member_data.get("jabatan","")],
            "Kategori": ["Employee (Staff/Supervisor)" if st.session_state.member_data.get("is_employee") else "Entrepreneur (Manager/Brand/Usahawan)"],
            "Tempat_Lahir": [st.session_state.member_data.get("tempat_lahir","")],
            "Tgl_Lahir": [st.session_state.member_data.get("tgl_lahir","")],
            "WNI": [st.session_state.member_data.get("wni","")],
            "Email": [st.session_state.member_data.get("email","")],
            "WhatsApp": [st.session_state.member_data.get("whatsapp","")],
            "Pendidikan": [st.session_state.member_data.get("pendidikan","")],
            "Pengalaman_Tahun": [st.session_state.member_data.get("pengalaman_tahun","")],
            "Skill": [st.session_state.member_data.get("skill","")],
            "Bursa_Total_Login": [st.session_state.bursa_total_login],
            "Bursa_Aktif_Vote": [st.session_state.bursa_active_vote],
            "Bursa_Sudah_Bekerja": [st.session_state.bursa_sudah_bekerja],
        }
        df_member = pd.DataFrame(data_export)
        csv_member = df_member.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="👤 Download CSV Data Loker + Bursa",
            data=csv_member,
            file_name=f"loker_{st.session_state.member_data.get('nama','member')}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            help="File CSV berisi data loker lengkap + status bursa"
        )
        st.caption(f"Data: {st.session_state.member_data.get('nama')} ({st.session_state.member_data.get('jabatan')})")
    else:
        st.info("Isi Form Loker Putih dulu")

st.markdown("---")
st.markdown(f"""
<div style="background:white; border-radius:12px; padding:12px; border:2px solid #eee; text-align:center; font-family:'JetBrains Mono'; font-size:9px;">
<div style="background:#424242; color:white; display:inline-block; padding:4px 12px; border-radius:20px; font-weight:700;">📊 BURSA VOTE • V29.3 • Merah=Staff/Supervisor | Hijau=Manager/Brand/Usahawan | Login=Vote | Share Email=Berkurang</div>
<div style="margin-top:6px;">Total Login: {st.session_state.bursa_total_login} vote | Aktif: {st.session_state.bursa_active_vote} | Bekerja: {st.session_state.bursa_sudah_bekerja} | Grafik Volume Bursa</div>
</div>
""", unsafe_allow_html=True)
