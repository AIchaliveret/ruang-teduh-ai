
"""
RUANG TEDUH V29.6 - ENTREPRENEUR = EMPLOYEE THE BEST (MIRROR)
- Lembar 2 Employee the best -> Lembar 3 Entrepreneur dibuat SAMA PERSIS
- Beda: Jabatan, Wewenang, Tanggung Jawab
- Employee: Staff & Supervisor - Pelaksana SOP
- Entrepreneur: Manager, Brand Manager, Usahawan - Pengelola & Pengambil Keputusan
- Voice ON dua-duanya, Share Email, Kolom Kejujuran, Bursa Vote
- Hemat Kuota LITE tetap
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import date, datetime
import json

st.set_page_config(page_title="Ruang Teduh V29.6 - Mirror Best", page_icon="📗", layout="wide", initial_sidebar_state="collapsed")

# SESSION
if "member_data" not in st.session_state:
    st.session_state.member_data = {}
if "bursa_total" not in st.session_state:
    st.session_state.bursa_total = 12
if "bursa_aktif" not in st.session_state:
    st.session_state.bursa_aktif = 8
if "bursa_kerja" not in st.session_state:
    st.session_state.bursa_kerja = 4
if "bursa_hist" not in st.session_state:
    st.session_state.bursa_hist = [
        {"jam": "08:00", "vote": 2, "kerja": 0},
        {"jam": "09:00", "vote": 5, "kerja": 1},
        {"jam": "10:00", "vote": 8, "kerja": 2},
        {"jam": "11:00", "vote": 8, "kerja": 4},
    ]
if "bursa_log" not in st.session_state:
    st.session_state.bursa_log = []
if "jujur" not in st.session_state:
    st.session_state.jujur = False

def add_login():
    st.session_state.bursa_total += 1
    st.session_state.bursa_aktif += 1
    now = datetime.now().strftime("%H:%M")
    st.session_state.bursa_hist.append({"jam": now, "vote": st.session_state.bursa_aktif, "kerja": st.session_state.bursa_kerja})
    if len(st.session_state.bursa_hist) > 10:
        st.session_state.bursa_hist = st.session_state.bursa_hist[-10:]

def kurang_bursa(email, alasan):
    if st.session_state.bursa_aktif > 0:
        st.session_state.bursa_aktif -= 1
        st.session_state.bursa_kerja += 1
        now = datetime.now().strftime("%H:%M")
        st.session_state.bursa_hist.append({"jam": now, "vote": st.session_state.bursa_aktif, "kerja": st.session_state.bursa_kerja})
        st.session_state.bursa_log.append({"waktu": now, "ke": email, "oleh": st.session_state.member_data.get("nama","-"), "alasan": alasan})
        if len(st.session_state.bursa_hist) > 10:
            st.session_state.bursa_hist = st.session_state.bursa_hist[-10:]

def tts_mirror(text, role, key_id):
    clean = text.replace('"','').replace("'","").replace("\n"," ").replace("\r"," ").strip()[:250]
    if not clean:
        clean = "Halo"
    js_txt = json.dumps(clean)
    rate = "0.9" if role=="emp" else "1.05"
    bg = "#FFEBEE" if role=="emp" else "#E8F5E9"
    border = "#FF5252" if role=="emp" else "#4CAF50"
    label = "EMPLOYEE Staff/Supervisor" if role=="emp" else "ENTREPRENEUR Manager/Brand/Usahawan"
    icon = "👨‍💼" if role=="emp" else "🚀"
    html = f"""
    <div style="background:{bg}; border:2px solid {border}; border-radius:10px; padding:12px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <div style="font-weight:800; font-size:11px;">👤 SPEAKER {label}</div>
            <div style="font-size:8px; background:white; padding:2px 6px; border-radius:8px; border:1px solid {border};">🔊 Voice ON</div>
        </div>
        <div style="background:white; border-radius:6px; padding:8px; font-size:11px; max-height:55px; overflow:auto; border:1px dashed #ccc; margin-bottom:8px;">{clean[:170]}...</div>
        <div style="display:flex; gap:6px;">
            <button onclick="speak_{key_id}()" style="flex:1; background:{border}; color:white; border:none; padding:10px; border-radius:8px; font-weight:700; cursor:pointer;">🔊 PUTAR SUARA {role.upper()}</button>
            <button onclick="window.speechSynthesis.cancel()" style="background:#424242; color:white; border:none; padding:10px 12px; border-radius:8px;">⏹️</button>
        </div>
        <div id="st_{key_id}" style="font-size:9px; text-align:center; margin-top:6px; color:#666;">Selesai - Voice OFF</div>
    </div>
    <script>
        function speak_{key_id}(){{
            if('speechSynthesis' in window){{
                window.speechSynthesis.cancel();
                var u = new SpeechSynthesisUtterance({js_txt});
                u.rate={rate}; u.lang='id-ID';
                u.onstart=function(){{document.getElementById('st_{key_id}').innerHTML='🔊 Berbicara...';}};
                u.onend=function(){{document.getElementById('st_{key_id}').innerHTML='✅ Selesai - Voice OFF';}};
                window.speechSynthesis.speak(u);
            }}
        }}
    </script>
    """
    components.html(html, height=185)

st.markdown("""
<style>
.lembar{border-radius:12px; padding:20px; margin-bottom:16px; border-left:3px dashed #bbb; box-shadow:2px 2px 0px rgba(0,0,0,0.06);}
.lembar-putih{background:#FFF; border-top:4px solid #9E9E9E;}
.lembar-merah{background:#FFEBEE; border-top:4px solid #FF5252;}
.lembar-hijau{background:#E8F5E9; border-top:4px solid #4CAF50;}
.bursa-card{background:#FFF9C4; border:2px solid #FBC02D; border-radius:10px; padding:12px; text-align:center;}
.bursa-vote{font-size:28px; font-weight:800; color:#F57F17;}
.bursa-label{font-size:10px; color:#666;}
.kotak-jujur{background:#E8F5E9; border:2px solid #4CAF50; border-radius:10px; padding:12px; margin:10px 0;}
.kotak-share{background:#FFF3E0; border:2px dashed #FF9800; border-radius:10px; padding:12px; margin:10px 0;}
.kotak-wewenang{background:white; border:1px solid #ddd; border-radius:10px; padding:12px; margin:8px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:6px 0 10px 0;">
    <div style="font-size:10px; letter-spacing:2px; color:#888;">TAVO MALKHUTKHA • V29.6 MIRROR BEST</div>
    <div style="font-size:20px; font-weight:800;">📗 BUKU 3 LEMBAR - EMPLOYEE THE BEST = ENTREPRENEUR THE BEST (MIRROR)</div>
    <div style="font-size:9px; color:#fff; background:#4CAF50; display:inline-block; padding:3px 10px; border-radius:20px;">Lembar 2 & 3 Sama Persis • Beda Jabatan & Wewenang • Voice Fix • Bursa Vote • Hemat Kuota</div>
</div>
""", unsafe_allow_html=True)

# BURSA DASHBOARD
c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="bursa-card"><div class="bursa-label">TOTAL LOGIN</div><div class="bursa-vote">{st.session_state.bursa_total}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="bursa-card" style="background:#FFEBEE; border-color:#FF5252;"><div class="bursa-label">BURSA AKTIF VOTE</div><div class="bursa-vote" style="color:#C62828;">{st.session_state.bursa_aktif}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="bursa-card" style="background:#E8F5E9; border-color:#4CAF50;"><div class="bursa-label">SUDAH BEKERJA</div><div class="bursa-vote" style="color:#2E7D32;">{st.session_state.bursa_kerja}</div></div>', unsafe_allow_html=True)
with c4:
    persen = int(st.session_state.bursa_kerja/st.session_state.bursa_total*100) if st.session_state.bursa_total else 0
    st.markdown(f'<div class="bursa-card" style="background:#E3F2FD; border-color:#2196F3;"><div class="bursa-label">KONVERSI</div><div class="bursa-vote" style="color:#1565C0;">{persen}%</div></div>', unsafe_allow_html=True)

# Grafik lite
st.markdown("#### 📈 Grafik Volume Nilai Orang Banyak Login Dalam Bursa")
hist = st.session_state.bursa_hist
if hist:
    max_v = max([h["vote"] for h in hist] + [h["kerja"] for h in hist] + [1])
    html_g = '<div style="display:flex; gap:6px; align-items:end; height:100px; background:white; border:1px solid #eee; border-radius:8px; padding:10px;">'
    for h in hist:
        v_h = int(h["vote"]/max_v*80)
        k_h = int(h["kerja"]/max_v*80)
        html_g += f'<div style="flex:1; text-align:center;"><div style="display:flex; gap:2px; justify-content:center; align-items:end;"><div style="width:45%; background:#FF5252; height:{v_h}px; border-radius:3px;"></div><div style="width:45%; background:#4CAF50; height:{k_h}px; border-radius:3px;"></div></div><div style="font-size:8px; margin-top:4px;">{h["jam"]}</div></div>'
    html_g += '</div><div style="font-size:9px; color:#666; margin-top:4px;">Merah = Vote Bursa Aktif (belum bekerja) | Hijau = Sudah Bekerja (via share email + kejujuran) - Bursa otomatis berkurang</div>'
    st.markdown(html_g, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📄 PUTIH - FORM LOKER + JABATAN", "🔴 MERAH - EMPLOYEE Staff/Supervisor (THE BEST)", "🟢 HIJAU - ENTREPRENEUR Manager/Brand/Usahawan (MIRROR BEST)"])

# TAB 1 PUTIH
with tab1:
    st.markdown('<div class="lembar lembar-putih"><b>LEMBAR 1 - FORM LOKER + JABATAN + BURSA VOTE (1 Login = 1 Vote)</b></div>', unsafe_allow_html=True)
    with st.form("form_loker"):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Lengkap *", placeholder="Budi Setia")
        with col2:
            jabatan = st.selectbox("Jabatan / Posisi *", ["Staff", "Supervisor", "Manager", "Brand Manager", "Usahawan / Entrepreneur"], help="Staff & Supervisor -> Merah Employee (Pelaksana). Manager, Brand Manager, Usahawan -> Hijau Entrepreneur (Pengelola)")
        
        col3, col4 = st.columns(2)
        with col3:
            tempat = st.text_input("Tempat Lahir *", placeholder="Jakarta Barat")
        with col4:
            tgl = st.date_input("Tgl Lahir *", value=date(1994,9,21))
        
        col5, col6 = st.columns(2)
        with col5:
            email = st.text_input("Email *", placeholder="cinhonest@gmail.com")
        with col6:
            wa = st.text_input("WhatsApp *", placeholder="081291904422")
        
        pendidikan = st.text_input("Pendidikan *", placeholder="S1 - sarjana akuntansi universitas trisakti")
        skill = st.text_area("Skill *", placeholder="akuntansi dan auditor berbasis komputerisasi dan soft ware erp accurate", height=60)
        
        submit = st.form_submit_button("✅ SIMPAN & MASUK BURSA - 1 LOGIN = 1 VOTE", type="primary", use_container_width=True)
        if submit:
            if not nama or not tempat or not email:
                st.error("Lengkapi *")
            else:
                is_emp = jabatan in ["Staff", "Supervisor"]
                st.session_state.member_data = {
                    "nama": nama, "jabatan": jabatan, "is_emp": is_emp, "is_ent": not is_emp,
                    "tempat": tempat, "tgl": tgl.strftime("%d-%m-%Y"), "tgl_obj": tgl,
                    "umur": date.today().year - tgl.year, "email": email, "wa": wa,
                    "pendidikan": pendidikan, "skill": skill
                }
                add_login()
                st.success(f"✅ {nama} ({jabatan}) masuk Bursa! Total: {st.session_state.bursa_total}")

# TAB 2 MERAH - THE BEST (dari screenshot)
with tab2:
    st.markdown('<div class="lembar lembar-merah" style="display:flex; justify-content:space-between;"><div><b>LEMBAR 2 - RUANG INTERAKSI - EMPLOYEE ONLY (Staff & Supervisor)</b></div><div style="background:#FF5252; color:white; padding:4px 10px; border-radius:4px; font-size:10px;">MERAH - STAFF/SUPERVISOR SAJA</div></div>', unsafe_allow_html=True)
    if not st.session_state.member_data:
        st.warning("Isi Putih dulu"); st.stop()
    md = st.session_state.member_data
    if not md.get("is_emp"):
        st.error(f"Maaf {md['nama']} ({md['jabatan']}) = Manager/Brand/Usahawan, harusnya HIJAU"); st.stop()
    
    st.markdown(f'<div style="background:#FFCDD2; padding:8px; border-radius:8px; font-size:11px; font-family:monospace;">✅ KONDISI: {md["nama"]} | {md["jabatan"]} | Staff/Supervisor → Merah Employee</div>', unsafe_allow_html=True)
    
    # ===== MIRROR LAYOUT: Kiri Kelola + Speaker, Kanan Bursa + Kejujuran =====
    col_kiri, col_kanan = st.columns([1.1, 0.9])
    with col_kiri:
        st.markdown("### 👤 KELOLA STAFF & SUPERVISOR ONLY")
        st.markdown(f"""
        <div style="background:white; padding:12px; border-radius:8px; border:1px solid #FFCDD2; font-size:11px;">
            <b>Nama:</b> {md['nama']} | <b>Jabatan:</b> <span style="background:#FFCDD2; color:#C62828; padding:2px 8px; border-radius:12px; font-size:10px; font-weight:700;">{md['jabatan']}</span><br/>
            <b>TTL:</b> {md['tempat']}, {md['tgl']} ({md['umur']}th) | WNI<br/>
            <b>Email/WA:</b> {md['email']} / {md['wa']}<br/>
            <b>Pendidikan:</b> {md['pendidikan']}<br/>
            <b>Skill:</b> {md['skill']}<br/>
        </div>
        """, unsafe_allow_html=True)
        
        # Wewenang & Tanggung Jawab Employee
        st.markdown("""
        <div class="kotak-wewenang">
            <b>🔴 Wewenang & Tanggung Jawab EMPLOYEE (Staff & Supervisor):</b><br/>
            • <b>Wewenang:</b> Melaksanakan SOP kebersihan, ERP jam 9 tepat, OEE 95%, KPI harian<br/>
            • <b>Tanggung Jawab:</b> Pelaksana lapangan, laporan ke Manager, disiplin, kejujuran update sudah bekerja<br/>
            • <b>Fokus:</b> Kerja sesuai SOP, tidak mengambil keputusan strategis
        </div>
        """, unsafe_allow_html=True)
        
        tts_mirror(f"Selamat datang {md['nama']} jabatan {md['jabatan']} Anda masuk Staff Supervisor di Merah Employee Umur {md['umur']} tahun skill {md['skill']} bursa aktif {st.session_state.bursa_aktif} vote", "emp", "emp_best")
    
    with col_kanan:
        st.markdown("### 📊 Bursa Vote - Employee")
        st.markdown("**Vote Aktif di Bursa**")
        st.markdown(f"# {st.session_state.bursa_aktif}")
        st.markdown("**Sudah Bekerja (via Share)**")
        st.markdown(f"# {st.session_state.bursa_kerja}")
        
        st.markdown("""
        <div class="kotak-jujur">
            <b>✅ Kolom Kejujuran Update</b><br/>
            Centang jika sudah diterima kerja, bursa otomatis berkurang
        </div>
        """, unsafe_allow_html=True)
        jujur_emp = st.checkbox("✅ Saya Sudah Diterima Kerja (Update Jujur)", key="jujur_emp_best")
        if jujur_emp and not st.session_state.jujur:
            st.session_state.jujur = True
            kurang_bursa(md['email'], "Sudah Diterima - Jujur Employee")
            st.success("Terima kasih jujur! Bursa -1, Kerja +1")
            st.balloons()
        
        if st.session_state.bursa_log:
            st.markdown("**Log Share:**")
            for log in st.session_state.bursa_log[-3:]:
                st.caption(f"{log['waktu']} {log['oleh']} -> {log['ke']}")
    
    st.markdown("---")
    st.markdown("### 🔍 Pencarian Permintaan & Request Penawaran Employee")
    st.markdown("""
    <div class="kotak-share">
        <b>Sebagai Pencari Kerja:</b> Anda bisa kirim & share ke rekan dan temannya memenuhi kebutuhannya mencari employee yang mau bekerja. Juga permintaan mencari kerja via email.
    </div>
    """, unsafe_allow_html=True)
    with st.form("share_emp_best"):
        email_t = st.text_input("📧 Share info loker Employee via Email ke teman/rekan:", placeholder="teman@email.com - untuk cari kerja / tawarkan jasa", key="share_emp_best_input")
        permintaan_emp = st.text_area("Permintaan / Request sebagai Pencari Kerja:", placeholder="Saya mencari pekerjaan Staff Admin, Supervisor...", height=70)
        btn_emp = st.form_submit_button("📧 KIRIM & SHARE - KURANGI BURSA VOTE (Sudah Bekerja?)")
        if btn_emp and "@" in email_t:
            kurang_bursa(email_t, "Employee cari kerja - permintaan & penawaran")
            st.success(f"✅ Shared ke {email_t}! Bursa: {st.session_state.bursa_aktif} | Kerja: {st.session_state.bursa_kerja}")

# TAB 3 HIJAU - MIRROR SAMA PERSIS SEPERTI MERAH
with tab3:
    st.markdown('<div class="lembar lembar-hijau" style="display:flex; justify-content:space-between;"><div><b>LEMBAR 3 - RUANG BOARDING - ENTREPRENEUR ONLY (Manager, Brand Manager, Usahawan)</b></div><div style="background:#4CAF50; color:white; padding:4px 10px; border-radius:4px; font-size:10px;">HIJAU - MANAGER/BRAND/USAHAWAN</div></div>', unsafe_allow_html=True)
    if not st.session_state.member_data:
        st.warning("Isi Putih dulu"); st.stop()
    md = st.session_state.member_data
    if not md.get("is_ent"):
        st.error(f"Maaf {md['nama']} ({md['jabatan']}) = Staff/Supervisor, harusnya MERAH Employee"); st.stop()
    
    st.markdown(f'<div style="background:#C8E6C9; padding:8px; border-radius:8px; font-size:11px; font-family:monospace;">✅ KONDISI: {md["nama"]} | {md["jabatan"]} | Manager/Brand/Usahawan → Hijau Entrepreneur</div>', unsafe_allow_html=True)
    
    # ===== MIRROR LAYOUT SAMA PERSIS KAYAK MERAH =====
    col_kiri_h, col_kanan_h = st.columns([1.1, 0.9])
    with col_kiri_h:
        st.markdown("### 🚀 KELOLA MANAGER & BRAND MANAGER & USAHAWAN ONLY")
        st.markdown(f"""
        <div style="background:white; padding:12px; border-radius:8px; border:1px solid #A5D6A7; font-size:11px;">
            <b>Nama:</b> {md['nama']} | <b>Jabatan:</b> <span style="background:#C8E6C9; color:#2E7D32; padding:2px 8px; border-radius:12px; font-size:10px; font-weight:700;">{md['jabatan']}</span><br/>
            <b>TTL:</b> {md['tempat']}, {md['tgl']} ({md['umur']}th) | WNI<br/>
            <b>Email/WA:</b> {md['email']} / {md['wa']}<br/>
            <b>Pendidikan:</b> {md['pendidikan']}<br/>
            <b>Skill Manage:</b> {md['skill']}<br/>
            <b>Bursa:</b> Total {st.session_state.bursa_total} | Aktif {st.session_state.bursa_aktif} | Kerja {st.session_state.bursa_kerja}
        </div>
        """, unsafe_allow_html=True)
        
        # Wewenang & Tanggung Jawab Entrepreneur - BEDA DENGAN EMPLOYEE
        st.markdown("""
        <div class="kotak-wewenang" style="border-color:#4CAF50; background:#F1F8E9;">
            <b>🟢 Wewenang & Tanggung Jawab ENTREPRENEUR (Manager, Brand Manager, Usahawan) - BERBEDA DENGAN EMPLOYEE:</b><br/>
            • <b>Wewenang:</b> Mengelola tim Staff & Supervisor, mengambil keputusan strategis, OEE 95%, KPI, ERP, SOP, anggaran, rekrutmen<br/>
            • <b>Tanggung Jawab:</b> Pengelola, bertanggung jawab atas hasil tim, Brand, omzet, storage SOP ERP OEE KPI Alkitab permanen<br/>
            • <b>Fokus:</b> Keputusan strategis, leadership, usahawan - TIDAK hanya pelaksana, tapi pengarah<br/>
            • <b>Beda dengan Employee:</b> Employee pelaksana SOP, Entrepreneur pengelola & pengambil keputusan + usahawan pemilik
        </div>
        """, unsafe_allow_html=True)
        
        # Voice Entrepreneur - SAMA KAYAK EMPLOYEE
        tts_mirror(f"Halo {md['nama']} jabatan {md['jabatan']} Anda masuk Manager Brand Manager Usahawan di Hijau Manage Umur {md['umur']} tahun skill {md['skill']} Bursa total {st.session_state.bursa_total} aktif {st.session_state.bursa_aktif} kerja {st.session_state.bursa_kerja} Silakan share via email", "ent", "ent_best_mirror")
    
    with col_kanan_h:
        st.markdown("### 📊 Bursa Vote - Entrepreneur")
        st.markdown("**Vote Aktif di Bursa**")
        st.markdown(f"# {st.session_state.bursa_aktif}")
        st.markdown("**Sudah Bekerja (via Share)**")
        st.markdown(f"# {st.session_state.bursa_kerja}")
        
        st.markdown("""
        <div class="kotak-jujur">
            <b>✅ Kolom Kejujuran Update</b><br/>
            Centang jika sudah diterima kerja / sudah dapat employee, bursa otomatis berkurang
        </div>
        """, unsafe_allow_html=True)
        jujur_ent = st.checkbox("✅ Saya Sudah Diterima Kerja / Sudah Dapat Employee (Update Jujur)", key="jujur_ent_best")
        if jujur_ent and not st.session_state.jujur:
            st.session_state.jujur = True
            kurang_bursa(md['email'], "Sudah Diterima - Jujur Entrepreneur")
            st.success("Terima kasih jujur! Bursa -1, Kerja +1")
            st.balloons()
        
        if st.session_state.bursa_log:
            st.markdown("**Log Share & Bursa:**")
            for log in st.session_state.bursa_log[-3:]:
                st.caption(f"{log['waktu']} {log['oleh']} -> {log['ke']} | {log['alasan']}")
    
    st.markdown("---")
    st.markdown("### 🔍 Pencarian Permintaan & Request Penawaran Entrepreneur")
    st.markdown("""
    <div class="kotak-share">
        <b>Sebagai Pencari Employee (Manager/Brand/Usahawan):</b> Anda bisa kirim & share ke rekan dan temannya memenuhi kebutuhannya mencari employee yang mau bekerja. Permintaan lowongan & request penawaran employee via email - SAMA KAYAK EMPLOYEE tapi untuk cari employee.
    </div>
    """, unsafe_allow_html=True)
    with st.form("share_ent_best"):
        email_r = st.text_input("📧 Share info lowongan Entrepreneur via Email ke rekan/teman:", placeholder="rekan@perusahaan.com - untuk cari employee / tawarkan lowongan", key="share_ent_best_input")
        permintaan_ent = st.text_area("Permintaan Lowongan / Request Employee yang Dicari:", placeholder="Dicari Staff Admin, Supervisor Gudang, skill Excel ERP Accurate...", height=70)
        penawaran_ent = st.text_area("Penawaran Gaji / Benefit untuk Employee:", placeholder="Gaji 5-7jt, tunjangan, SOP jelas, ERP jam 9 tepat...", height=60)
        btn_ent = st.form_submit_button("📧 KIRIM PERMINTAAN & SHARE - KURANGI BURSA VOTE (Sudah Bekerja?)", type="primary")
        if btn_ent and "@" in email_r:
            kurang_bursa(email_r, f"Entrepreneur {md['jabatan']} cari employee - permintaan & penawaran")
            st.success(f"✅ Permintaan terkirim ke {email_r}! Bursa: {st.session_state.bursa_aktif} | Kerja: {st.session_state.bursa_kerja}")

st.markdown(f"""
<div style="background:white; border-radius:10px; padding:10px; border:1px solid #eee; text-align:center; font-size:9px; margin-top:12px;">
<div style="background:#4CAF50; color:white; display:inline-block; padding:4px 10px; border-radius:20px; font-weight:700;">V29.6 MIRROR BEST • Employee The Best = Entrepreneur The Best • Wewenang Beda • Voice ON • Bursa Vote • Hemat Kuota</div>
<div style="margin-top:4px;">Total: {st.session_state.bursa_total} | Aktif: {st.session_state.bursa_aktif} | Kerja: {st.session_state.bursa_kerja} | Merah & Hijau Sama Persis</div>
</div>
""", unsafe_allow_html=True)
