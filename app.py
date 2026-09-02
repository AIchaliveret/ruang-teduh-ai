import streamlit as st
from datetime import datetime, date
import io

st.set_page_config(page_title="Ruang Teduh - Buku 1 Ruang 3 Lembar", layout="wide", page_icon="📖")

# --- SESSION - THREE WAY ---
if "member_db" not in st.session_state:
    st.session_state.member_db = {}
if "bursa_kerja" not in st.session_state:
    st.session_state.bursa_kerja = [
        {"id":1, "posted_by":"Budi - Director", "posted_email":"budi@teduh.id", "role_needed":"Supervisor Kebersihan", "level":"Supervisor", "zona":"Jakarta Selatan", "deskripsi":"Lead tim SOP jam 7-9 pagi, cek kebersihan", "tarif":"2.5jt/bulan"},
        {"id":2, "posted_by":"Sari - Business Owner", "posted_email":"sari@teduh.id", "role_needed":"Staff Barista", "level":"Staff", "zona":"Jakarta Pusat", "deskripsi":"Jam 9-17, handle ERP", "tarif":"1.5jt/bulan"},
    ]
if "current_page" not in st.session_state:
    st.session_state.current_page = "R1"
if "current_user" not in st.session_state:
    st.session_state.current_user = None

NASEHAT = [
    "MINGGU 1: Teduh itu bukan menghindar, tapi mengelola. Kalau pikiran ribut, jangan dilawan, disapa.",
    "MINGGU 2: Employee yang setia bukan yang paling pintar, tapi yang paling konsisten jam 9 pagi.",
    "MINGGU 3: Entrepreneur 50rb bukan biaya, tapi ikatan. Kalau sudah bayar, otak otomatis cari cara balik modal lewat karya.",
    "MINGGU 4: SOP Kebersihan = Cermin Hati. Ruang kotor, rezeki seret.",
    "MINGGU 5: OEE 95% bukan target mesin, tapi target diri. 95% hadir utuh.",
    "MINGGU 6: Bursa Kerja Teduh - Employee butuh wadah, Entrepreneur butuh tenaga. Ketemunya di Ruang Teduh."
]

def get_nasehat():
    return NASEHAT[datetime.now().isocalendar()[1] % len(NASEHAT)]

# --- CSS NCR ---
st.markdown("""
<style>
.ncr-white {background:#ffffff; border:2.5px solid #111; border-left:20px dotted #bbb; padding:24px; border-radius:12px; box-shadow:5px 5px 0 #111;}
.ncr-red {background:#fff2f2; border:2.5px solid #c0392b; border-left:20px dotted #ffb3b3; padding:24px; border-radius:12px; box-shadow:5px 5px 0 #c0392b;}
.ncr-green {background:#f0f8f0; border:2.5px solid #27ae60; border-left:20px dotted #a5d6a7; padding:24px; border-radius:12px; box-shadow:5px 5px 0 #27ae60;}
.carbon {border-top:3px dashed #888; margin:24px 0; text-align:center; color:#666; font-size:11px; letter-spacing:1.2px; background:#fff; padding:4px;}
.org-box {border:1.5px solid #ddd; padding:12px; border-radius:10px; background:#fafafa; margin-bottom:10px;}
</style>
""", unsafe_allow_html=True)

st.title("📖 BUKU 1 RUANG 3 LEMBAR - RUANG TEDUH")
st.caption("Three Way Function - 1x Tulis Tembus 3x | Employee: Staff s/d Supervisor (30k) | Entrepreneur: Manager s/d Business Owner (50k) | Flowchart Tersystematis")

# NAV - DI LUAR FORM, FIX BUG st.button() inside form
c1,c2,c3 = st.columns(3)
with c1:
    if st.button("📄 PUTIH - REGISTRASI ORG", use_container_width=True, type="primary" if st.session_state.current_page=="R1" else "secondary"):
        st.session_state.current_page="R1"; st.rerun()
with c2:
    if st.button("🔴 MERAH - INTERAKSI + BURSA KERJA", use_container_width=True, type="primary" if st.session_state.current_page=="R2" else "secondary"):
        st.session_state.current_page="R2"; st.rerun()
with c3:
    if st.button("🟢 HIJAU - STORAGE 5 RAK", use_container_width=True, type="primary" if st.session_state.current_page=="R3" else "secondary"):
        st.session_state.current_page="R3"; st.rerun()

st.markdown('<div class="carbon">✂️ CARBON COPY - PUTIH (ASLI) -> MERAH (TEMBUSAN 1) -> HIJAU (TEMBUSAN 2) - GARIS PUTUS-PUTUS</div>', unsafe_allow_html=True)

# ================= R1 PUTIH =================
if st.session_state.current_page=="R1":
    st.markdown('<div class="ncr-white">', unsafe_allow_html=True)
    st.subheader("LEMBAR 1 PUTIH - ASLI | REGISTRASI STRUKTUR ORGANISASI PERUSAHAAN")
    st.markdown("**Flow: [QR GATE] -> [FORM LENGKAP: Nama, Tempat & Tgl Lahir, Pengalaman, Pendidikan, Zona, Email, HP] -> [VALIDASI ROLE] -> TEMBUS OTOMATIS**")
    st.info("Konsep terbaru: Form sama untuk semua, bedanya jenjang + tugas + wewenang. Employee = Staff s/d Supervisor (pelaksana). Entrepreneur = Manager s/d Business Owner (pimpinan bisnis utama).")

    col_qr, col_form = st.columns([1,2.3])
    with col_qr:
        st.markdown("#### 📷 QR GATE")
        st.code("RUANG-TEDUH\nORG-STRUCTURE\nBUKU-1-RUANG-3-LEMBAR", language="text")
        st.success("QR Terdeteksi: RT-001-ORG")
        st.markdown("#### 🏢 STRUKTUR ORGANISASI")
        st.markdown("""
        **EMPLOYEE Rp30k/bulan** - Pelaksana
        - Staff
        - Senior Staff
        - Supervisor (max Employee)
        Wewenang: Lamar loker, chat, SOP, ERP Jam 9

        **ENTREPRENEUR Rp50k/bulan** - Pimpinan
        - Manager
        - General Manager
        - Director
        - Business Owner
        Wewenang: Posting loker, approve, Full 5 Rak, KPI, OEE, VA
        """)
        st.markdown("#### 📋 CARA BERLANGGANAN (3 Kolom NCR)")
        st.markdown("| | PUTIH | MERAH | HIJAU |\n|---|---|---|---|\n| Employee 30k | Daftar Org | Lamar Loker | Invoice + SOP/ERP |\n| Entrepreneur 50k | Daftar Org | Posting Loker | VA + 5 Rak Full |")

    with col_form:
        st.markdown("#### 📝 FORM REGISTRASI LENGKAP - SESUAI STRUKTUR PERUSAHAAN")
        st.caption("Wajib: Nama, Tempat & Tgl Lahir, Pengalaman, Pendidikan, Zona Rumah Tinggal, Email, No Telepon - Standar HRD")
        
        # FIX BUG: HANYA form_submit_button DI DALAM FORM
        with st.form("form_org_final", clear_on_submit=False):
            st.markdown("**A. DATA PRIBADI LENGKAP**")
            nama = st.text_input("Nama Lengkap *", placeholder="Budi Santoso")
            col_ttl1, col_ttl2 = st.columns(2)
            with col_ttl1:
                tempat_lahir = st.text_input("Tempat Lahir *", placeholder="Jakarta")
            with col_ttl2:
                tgl_lahir = st.date_input("Tanggal Lahir *", value=date(1995,1,1), min_value=date(1960,1,1), max_value=date(2008,12,31))
            col_k1, col_k2 = st.columns(2)
            with col_k1:
                email = st.text_input("Alamat Email *", placeholder="budi@email.com")
            with col_k2:
                no_hp = st.text_input("Nomor Telepon / WA *", placeholder="081234567890")

            st.markdown("**B. DOMISILI & PENDIDIKAN**")
            zona = st.selectbox("Zona Rumah Tinggal * (untuk mapping bursa kerja)", ["Jakarta Pusat","Jakarta Utara","Jakarta Barat","Jakarta Timur","Jakarta Selatan","Bogor","Depok","Tangerang","Bekasi","Luar Jabodetabek"])
            pendidikan = st.selectbox("Pendidikan Terakhir *", ["SMA/SMK","D3","S1","S2","S3","Lainnya"])
            jurusan = st.text_input("Jurusan / Keahlian", placeholder="Manajemen, Teknik, Barista, Desain, etc")

            st.markdown("**C. PENGALAMAN KERJA**")
            tahun_pengalaman = st.slider("Total Tahun Pengalaman *", 0, 20, 2)
            pengalaman_detail = st.text_area("Deskripsi Pengalaman * (tugas & jabatan sebelumnya)", placeholder="2 tahun Staff Admin di PT X, handle ERP. 1 tahun Supervisor di Cafe Y, lead 3 staff.", height=90)

            st.markdown("**D. JENJANG ORGANISASI & WEWENANG**")
            main_role = st.radio("Kategori Utama *", ["EMPLOYEE - Staff s/d Supervisor (Rp30.000/bulan) - Pelaksana","ENTREPRENEUR - Manager s/d Business Owner (Rp50.000/bulan) - Pimpinan Bisnis Utama"], horizontal=False)
            
            if "EMPLOYEE" in main_role:
                jabatan = st.selectbox("Jabatan Employee *", ["Staff","Senior Staff","Supervisor"])
                wewenang = f"{jabatan} (Employee) - Wewenang: Melamar loker sesuai zona & pendidikan, akses chat teduh, SOP Kebersihan, ERP Jam 9. Tidak bisa posting loker. Jenjang max Supervisor."
                tarif = 30000
                role_code = "employee"
            else:
                jabatan = st.selectbox("Jabatan Entrepreneur *", ["Manager","General Manager","Director","Business Owner - Pimpinan Utama Perusahaan"])
                wewenang = f"{jabatan} (Entrepreneur) - Wewenang: Posting loker untuk Staff-Supervisor, approve lamaran (nama, TTL, pengalaman, pendidikan, zona, email, HP lengkap), kelola KPI/OEE, Full 5 Rak SOP/ERP/OEE95%/KPI/ALKITAB, QRIS VA + Invoice."
                tarif = 50000
                role_code = "entrepreneur"
            
            st.info(f"**Wewenang {jabatan}:** {wewenang}")
            
            st.markdown("---")
            submit_org = st.form_submit_button(f"✅ DAFTARKAN SEBAGAI {jabatan.upper()} - Rp{tarif} - 1X TULIS TEMBUS 3 LEMBAR", use_container_width=True, type="primary")
            
            if submit_org:
                if not nama or not email or not no_hp or not tempat_lahir or not pengalaman_detail:
                    st.error("Lengkapi semua bintang * bro! Nama, Tempat Lahir, Pengalaman, Email, HP wajib.")
                elif "@" not in email:
                    st.error("Email tidak valid")
                else:
                    st.session_state.member_db[email] = {
                        "nama": nama, "tempat_lahir": tempat_lahir, "tgl_lahir": str(tgl_lahir),
                        "email": email, "no_hp": no_hp, "zona": zona, "pendidikan": pendidikan, "jurusan": jurusan,
                        "tahun_pengalaman": tahun_pengalaman, "pengalaman_detail": pengalaman_detail,
                        "main_role": role_code, "jabatan": jabatan, "tarif": tarif, "wewenang": wewenang,
                        "ikatan_score": 0, "joined": datetime.now().isoformat()
                    }
                    st.session_state.current_user = email
                    st.success(f"✅ TERDAFTAR! {nama} sebagai {jabatan} - {role_code.upper()} - Rp{tarif} - Zona {zona}")
                    st.balloons()
                    st.session_state.current_page = "R2"
                    st.rerun()
        
        if st.button("🔄 Reset Form", key="reset_r1"):
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ================= R2 MERAH =================
elif st.session_state.current_page=="R2":
    st.markdown('<div class="ncr-red">', unsafe_allow_html=True)
    st.subheader("LEMBAR 2 MERAH - TEMBUSAN 1 | RUANG INTERAKSI - 4 Pilar + Bursa Kerja Org")
    if not st.session_state.current_user:
        st.warning("Belum daftar di Putih! Balik ke R1.")
        if st.button("Ke R1 Putih"):
            st.session_state.current_page="R1"; st.rerun()
    else:
        m = st.session_state.member_db[st.session_state.current_user]
        st.success(f"👤 {m['nama']} | {m['jabatan']} ({m['main_role'].upper()}) | Zona {m['zona']} | Exp {m['tahun_pengalaman']}th | Ikatan {m['ikatan_score']}")

        p1,p2 = st.columns(2)
        with p1:
            st.markdown("#### PILAR 1: PROFIL LENGKAP ORG")
            st.markdown(f"""
            <div class="org-box">
            <b>Nama:</b> {m['nama']}<br>
            <b>TTL:</b> {m['tempat_lahir']}, {m['tgl_lahir']}<br>
            <b>Kontak:</b> {m['email']} | {m['no_hp']}<br>
            <b>Domisili:</b> {m['zona']} | <b>Pendidikan:</b> {m['pendidikan']} ({m['jurusan']})<br>
            <b>Pengalaman:</b> {m['tahun_pengalaman']}th - {m['pengalaman_detail']}<br>
            <b>Jabatan:</b> {m['jabatan']} | <b>Tarif:</b> Rp{m['tarif']}
            </div>
            """, unsafe_allow_html=True)
            st.caption(m['wewenang'])
        with p2:
            st.markdown("#### PILAR 2: AUDIO TEDUH (Speaker) - Nasehat Mingguan TTS")
            nasehat = get_nasehat()
            st.info(nasehat)
            col_a, col_b = st.columns([1,1])
            with col_a:
                if st.button("🔊 Bacakan dengan Suara", use_container_width=True):
                    try:
                        from gtts import gTTS
                        tts = gTTS(nasehat, lang='id')
                        fp = io.BytesIO()
                        tts.write_to_fp(fp)
                        fp.seek(0)
                        st.audio(fp, format='audio/mp3')
                        st.success("Audio Teduh diputar - sesuai saran lu: text jadi suara speaker")
                    except Exception as e:
                        st.warning(f"gTTS error: {e} - pakai browser TTS fallback")
            with col_b:
                if st.button("📜 Ganti Nasehat"):
                    st.rerun()

        st.markdown("---")
        st.markdown("### 💼 BURSA KERJA TEDUH - SESUAI STRUKTUR ORGANISASI")
        st.markdown("**Employee (Staff-Supervisor) = Pencari Kesempatan | Entrepreneur (Manager-Business Owner) = Pemberi Kesempatan - Data lengkap (nama, TTL, pengalaman, pendidikan, zona, email, HP) terkirim otomatis saat melamar**")
        
        tab_cari, tab_post, tab_member = st.tabs(["🔍 Cari Loker (Sesuai Zona & Jabatan)", "➕ Posting Loker (Wewenang Pimpinan)", "🏢 Org Chart Member"])
        
        with tab_cari:
            st.caption(f"Login sebagai {m['jabatan']} - {'Bisa melamar, data org lengkap lu akan terkirim' if m['main_role']=='employee' else 'Kamu pimpinan, wewenang posting bukan melamar'}")
            for loker in st.session_state.bursa_kerja:
                with st.container(border=True):
                    c1,c2 = st.columns([3,1])
                    with c1:
                        st.markdown(f"**{loker['role_needed']}** - Level: {loker['level']} - Zona: {loker['zona']}")
                        st.caption(f"by {loker['posted_by']} | {loker['deskripsi']} | {loker['tarif']}")
                    with c2:
                        if m['main_role']=='employee':
                            if st.button(f"Lamar #{loker['id']}", key=f"lamar_{loker['id']}_v3"):
                                m['ikatan_score']+=10
                                st.success(f"✅ Lamaran terkirim!\n{m['nama']} ({m['jabatan']}, {m['zona']}, {m['pendidikan']}, Exp {m['tahun_pengalaman']}th) -> {loker['posted_by']}. Ikatan +10")
                        else:
                            st.button("Pimpinan tidak melamar", disabled=True, key=f"dis_{loker['id']}_v3")

        with tab_post:
            if m['main_role']!='entrepreneur':
                st.error(f"❌ Wewenang ditolak: {m['jabatan']} (Employee) tidak bisa posting. Hanya Manager s/d Business Owner (Entrepreneur) yang punya wewenang posting loker.")
            else:
                st.markdown(f"**Form Posting - Wewenang {m['jabatan']}**")
                with st.form("post_loker_final"):
                    judul = st.text_input("Jabatan yang dicari", placeholder="Staff Admin, Senior Barista, Supervisor Toko")
                    level_butuh = st.selectbox("Level dibutuhkan", ["Staff","Senior Staff","Supervisor"])
                    zona_loker = st.selectbox("Zona Penempatan", ["Jakarta Pusat","Jakarta Utara","Jakarta Barat","Jakarta Timur","Jakarta Selatan","Bogor","Depok","Tangerang","Bekasi"])
                    desk = st.text_area("Deskripsi tugas, jam kerja, wewenang")
                    tarif_l = st.text_input("Gaji/Tarif", placeholder="1.5jt/bulan")
                    submit_loker = st.form_submit_button("📢 Posting Loker - Tembus ke Semua Employee")
                    if submit_loker:
                        st.session_state.bursa_kerja.append({"id":len(st.session_state.bursa_kerja)+1,"posted_by":f"{m['nama']} - {m['jabatan']}","posted_email":m['email'],"role_needed":judul,"level":level_butuh,"zona":zona_loker,"deskripsi":desk,"tarif":tarif_l})
                        m['ikatan_score']+=5
                        st.success(f"Loker {judul} ({level_butuh}) Zona {zona_loker} terposting! Semua Employee Staff-Supervisor bisa melamar dengan data lengkap org mereka.")

        with tab_member:
            st.markdown("**Daftar Member - Satu Struktur Organisasi Perusahaan**")
            for email, data in st.session_state.member_db.items():
                st.markdown(f"- **{data['nama']}** | {data['jabatan']} ({data['main_role']}) | TTL: {data['tempat_lahir']}, {data['tgl_lahir']} | {data['zona']} | {data['pendidikan']} | Exp {data['tahun_pengalaman']}th | {data['email']} | {data['no_hp']}")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= R3 HIJAU =================
else:
    st.markdown('<div class="ncr-green">', unsafe_allow_html=True)
    st.subheader("LEMBAR 3 HIJAU - TEMBUSAN 2 | BOARDING / STORAGE - 5 Rak System + QRIS VA")
    st.markdown("**Flow: [QRIS VA] -> [INVOICE] -> [FULL ACCESS] -> [STORAGE 5 RAK]**")
    if st.session_state.current_user:
        m = st.session_state.member_db[st.session_state.current_user]
        c1,c2 = st.columns(2)
        with c1:
            st.metric("QRIS VA", f"VA-{m['nama'][:4].upper()}-{m['zona'][:3].upper()}-TEDUH")
            st.code(f"Tagihan: Rp{m['tarif']} - {m['jabatan']} - {m['main_role']}")
        with c2:
            st.metric("INVOICE", f"INV/{m['jabatan']}/{datetime.now().strftime('%m%y')}")
            st.success(f"LUNAS - Akses: {m['wewenang'][:60]}...")
    else:
        st.info("Daftar di R1 Putih untuk dapat VA & Invoice sesuai jabatan")

    st.markdown("#### 📦 5 RAK SYSTEM - Gudang Aturan Tersystematis")
    r1,r2,r3,r4,r5 = st.columns(5)
    with r1:
        with st.container(border=True):
            st.markdown("**RAK 1: SOP Kebersihan**")
            st.checkbox("Sapu pagi 07:00", value=True, key="sop_v3_1")
            st.checkbox("Pel siang 12:00", key="sop_v3_2")
            st.caption("Wajib Employee: Staff-Supervisor. Pimpinan cek.")
    with r2:
        with st.container(border=True):
            st.markdown("**RAK 2: ERP Jam 9**")
            st.metric("Check-in", "09:00 WIB")
            st.caption("Semua jenjang wajib. Supervisor & Manager monitoring.")
    with r3:
        with st.container(border=True):
            st.markdown("**RAK 3: OEE 95%**")
            st.progress(0.95)
            st.metric("OEE", "95%")
            st.caption("Target diri: 95% hadir utuh")
    with r4:
        with st.container(border=True):
            st.markdown("**RAK 4: KPI Performance**")
            st.write("Employee: Apply + Kehadiran + SOP")
            st.write("Entrepreneur: Posting + Approve + Retensi")
            st.caption("Sesuai wewenang jabatan")
    with r5:
        with st.container(border=True):
            st.markdown("**RAK 5: ALKITAB Fondasi**")
            st.caption("Teduh, Terikat, Tumbuh. Co-growing, bukan co-working. Fondasi semua jabatan.")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="carbon">FLOWCHART THREE WAY SEMPURNA - PUTIH (Form Org Lengkap) --carbon--> MERAH (Bursa Sesuai Jenjang & Zona) --carbon--> HIJAU (VA + 5 Rak Sesuai Wewenang) - Floating Dot Orange Navigasi</div>', unsafe_allow_html=True)
st.caption("Ruang Teduh AI v3.0 - Struktur Organisasi Perusahaan - Siap Assembly Hackathon - Tersystematis")
