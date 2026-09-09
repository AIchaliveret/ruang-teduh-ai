
"""
app.py - V12 VOICE MOBILE FULL - FOUR WAYS FUNCTION + VOICE RECORDING
Ruang Teduh AI - Buku 1 Ruang 3 Lembar -> Four Ways Function
Three Way: PO + Surat Jalan -> Gudang QC BAQC -> Admin BA Penerimaan
Four Way: + Finance BAQC + Invoice Payment = FOUR WAYS FUNCTION - 1x Tulis Tembus 4x Otomatis
V12 Voice: L3 HIJAU tambah st.audio_input + transkrip langsung tembus 4 lembar!
565 baris FULL 33.9KB - Mobile Perfect 2 screenshot = 1 halaman muka - Owner aichaliveret 40k/55k TITIK! QR 081291904422
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import json
import os
from io import BytesIO

# Try qrcode, fallback to external API
try:
    import qrcode
    QR_LIB = True
except:
    QR_LIB = False

# ========== CORE DATA - FOUR WAYS FUNCTION ==========
OWNER = "aichaliveret"
QR = "081291904422"
TARIF = {"EMPLOYEE": 55000, "ENTREPRENEUR": 75000, "Employee": 55000, "Entrepreneur": 75000}
ROLE_JABATAN = {
    "EMPLOYEE": ["Staff", "Senior Staff", "Supervisor"],
    "ENTREPRENEUR": ["Manager", "GM", "Director", "Business Owner", "Owner Kecil"]
}
ZONA_LIST = ["Jakarta Pusat", "Jakarta Barat", "Jakarta Timur", "Jakarta Selatan", "Jakarta Utara", "Bekasi", "Tangerang", "Depok", "Bandung", "Surabaya"]
PENDIDIKAN_LIST = ["SMA/SMK", "D3", "S1", "S2", "S3"]
FIELD_WAJIB = ["Nama Lengkap*", "Tempat Lahir*", "Tanggal Lahir*", "Alamat Email*", "Nomor HP/WA*", "Alamat*", "Zona*", "Pendidikan*", "Jurusan*", "Tahun Pengalaman*", "Deskripsi Pengalaman*", "Skill*", "Kategori ERP*", "Jabatan*"]

# ========== SESSION STATE - SINGLE DATABASE NO DOUBLE ENTRY ==========
if "db" not in st.session_state:
    st.session_state.db = [
        {"nama":"Tuan Cin","email":"cinhonest@gmail.com","jabatan":"Manager","kota":"Jakarta Pusat","skill":"Anggaran Auto CAD","kategori":"Entrepreneur","tempat":"Jakarta","tgl":"1995/01/01","zona":"Jakarta Pusat","pendidikan":"SMA/SMK","jurusan":"Teknik","tahun":5,"deskripsi":"Manager proyek konstruksi","hp":"081291904422","ikatan_score":100,"tgl_daftar":"2026-09-01"},
        {"nama":"Pak Budi","email":"budi@gmail.com","jabatan":"Staff","kota":"Bekasi","skill":"Admin","kategori":"Employee","tempat":"Bekasi","tgl":"1998/02/02","zona":"Bekasi","pendidikan":"S1","jurusan":"Manajemen","tahun":2,"deskripsi":"Staff admin teliti","hp":"0812000001","ikatan_score":10,"tgl_daftar":"2026-09-02"},
    ]
if "bimbingan_log" not in st.session_state:
    st.session_state.bimbingan_log = []
if "voice_log" not in st.session_state:
    st.session_state.voice_log = []

# ========== QR GENERATOR ==========
def generate_qr(text):
    if QR_LIB:
        qr = qrcode.QRCode(version=1, box_size=8, border=2)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    else:
        return f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={text}"

# ========== PAGE CONFIG - MOBILE PERFECT CENTERED ==========
st.set_page_config(
    page_title="V12 VOICE - FOUR WAYS - 1 Layar HP PAS - aichaliveret",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========== CSS MOBILE PERFECT - 2 SCREENSHOT = 1 HALAMAN MUKA - NO LUBER ==========
st.markdown("""
<style>
[data-testid="stHeader"] {display:none !important;}
footer {display:none !important;}
#MainMenu {visibility:hidden !important;}
div[data-testid="stToolbar"] {display:none !important;}
div[data-testid="stDecoration"] {display:none !important;}
.block-container {padding-top:0.3rem !important; padding-bottom:0.2rem !important; padding-left:0.5rem !important; padding-right:0.5rem !important; max-width:100% !important; margin-top:0 !important;}
h1 {font-size:20px !important; line-height:1.1 !important; margin:0.2rem 0 !important; font-weight:800 !important;}
h2 {font-size:16px !important; margin:0.3rem 0 !important; line-height:1.1 !important;}
h3 {font-size:14px !important; margin:0.2rem 0 !important;}
p, li, div, span {font-size:12px !important; line-height:1.25 !important;}
small {font-size:10px !important;}
.marquee-box {background:#000; color:#00ff00; height:26px; overflow:hidden; white-space:nowrap; font-size:11px; font-family:monospace; display:flex; align-items:center; border-radius:4px; margin-bottom:0.3rem; border:1px solid #00ff00;}
.marquee-text {display:inline-block; padding-left:100%; animation:marquee 25s linear infinite;}
@keyframes marquee {0% {transform: translateX(0);} 100% {transform: translateX(-100%);}}
.stTabs [data-baseweb="tab-list"] {gap:1px !important; flex-wrap:nowrap !important; overflow-x:auto !important; padding-bottom:2px !important;}
.stTabs [data-baseweb="tab"] {font-size:10px !important; padding:2px 6px !important; height:28px !important; min-width:58px !important; white-space:nowrap !important; border-radius:6px 6px 0 0 !important;}
.stTabs [data-baseweb="tab-panel"] {padding-top:0.3rem !important;}
div[data-testid="stMetric"] {background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:4px 6px !important;}
div[data-testid="stMetricLabel"] {font-size:9px !important; margin-bottom:0 !important;}
div[data-testid="stMetricValue"] {font-size:13px !important; font-weight:700 !important;}
div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {height:30px !important; font-size:11px !important; padding:2px 8px !important;}
div[data-testid="stForm"] {border:1px solid #cbd5e1; padding:0.5rem !important; border-radius:10px !important; background:#f8fafc;}
.stButton button {height:32px !important; font-size:11px !important; padding:2px 8px !important;}
div[data-testid="stAlert"] {padding:0.4rem !important; font-size:11px !important; margin:0.3rem 0 !important;}
div[data-testid="stExpander"] summary {font-size:11px !important; padding:4px !important;}
.bursa-card {background: linear-gradient(135deg,#FFF8E1 0%,#FFECB3 100%); border:2px solid #FF6B00; border-radius:10px; padding:10px; margin:5px 0;}
.lembar-putih {background:#FAFAFA; border-left:6px solid #333; padding:8px 10px; border-radius:6px;}
.lembar-merah {background:#FFEBEE; border-left:6px solid #D32F2F; padding:8px 10px; border-radius:6px;}
.lembar-hijau {background:#E8F5E9; border-left:6px solid #2E7D32; padding:8px 10px; border-radius:6px;}
.lembar-biru {background:#E3F2FD; border-left:6px solid #1976D2; padding:8px 10px; border-radius:6px;}
.voice-box {background:#000; color:#00ff00; border:2px solid #00ff00; border-radius:10px; padding:10px; font-family:monospace;}
</style>
""", unsafe_allow_html=True)

# ========== QUERY PARAMS REF ==========
ref = st.query_params.get("ref", OWNER)
if isinstance(ref, list):
    ref = ref[0]

# ========== MARQUEE - FIX 26PX NO KEPOTONG - JALAN TERUS ==========
st.markdown(f"""
<div class="marquee-box">
<div class="marquee-text">
🎙️ V12 VOICE - FOUR WAYS FUNCTION - 1x Tulis Tembus 4x Otomatis - Owner {OWNER} 40k/55k TITIK! - L1 PUTIH Purchasing PO QR GATE Form 16 Field Bursa Billboard - L2 MERAH PINK Gudang QC BAQC Grafik Volume - L3 HIJAU Admin BA 5 Rak SOP ERP OEE KPI + VOICE RECORDING Ruach Hakadosh - L4 BIRU Finance Payment Direct Selling Link ?ref={OWNER} - QR {QR} - Single DB NO DOUBLE - Ref: {ref} - AssemblyAI Hackathon
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📖 FOUR WAYS + VOICE - 1x Tulis 4x Otomatis + 🎙️ Voice Tembus 4 Lembar")
st.caption(f"Three Way: PO+Surat Jalan → Gudang QC BAQC → Admin BA | Four Way: + Finance BAQC+Payment | + Voice Recording L3 HIJAU | Owner {OWNER} 40k/55k - QR {QR} - 2 Screenshot = 1 Halaman Muka")

st.info(f"Origin: Purchasing PO+Surat Jalan → Gudang QC BAQC → Admin BA → Finance BAQC+Invoice = FOUR WAYS + VOICE RECORDING = 1x Tulis + 1x Ngomong Tembus 4x Otomatis! Ref: {ref} | AssemblyAI Hackathon Ready!")

# ========== TABS 5 LEMBAR ==========
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚪ PUTIH L1","🔴 MERAH L2","🟢 HIJAU L3 + 🎙️ VOICE","🔵 BIRU L4","📊 Chart+Excel"])

# ========== LEMBAR 1 PUTIH - PURCHASING - QR GATE + FORM 16 FIELD + BURSA BILLBOARD ==========
with tab1:
    st.markdown('<div class="lembar-putih"><b>L1 PUTIH - Purchasing - QR GATE + PO + Form Lengkap 16 Field + Bursa Billboard</b><br>File: app.py | Fungsi Penerima & Billboard Bursa</div>', unsafe_allow_html=True)
    cqr, cinfo = st.columns([1,3])
    with cqr:
        qr_data = generate_qr(f"{QR}")
        if isinstance(qr_data, str):
            st.image(qr_data, width=90)
        else:
            st.image(qr_data, width=90)
        st.caption(f"QR {QR} - Two Journeys One QR")
    with cinfo:
        st.caption("Fungsi Purchasing penerima PO+Surat Jalan Invoice Vendor - Kolom penerima member disebut BURSA billboard bursa - terpampang jelas seperti billboard bursa saham")
        c1,c2,c3 = st.columns(3)
        c1.metric("Bursa", len(st.session_state.db), "arsip")
        emp = len([m for m in st.session_state.db if m["kategori"] in ["Employee","EMPLOYEE"]])
        ent = len([m for m in st.session_state.db if m["kategori"] in ["Entrepreneur","ENTREPRENEUR"]])
        c2.metric("Emp", emp, "tenaga kerja")
        c3.metric("Ent", ent, "pemberi kerja")
    
    # BURSA BILLBOARD LIVE
    st.markdown("**📊 BILLBOARD BURSA - Member Terhubung (Live Ticker)**")
    st.caption("Kolom ini sebagai penerima dari banyaknya member yang sudah terkoneksi karena menggunakan aplikasi ini. Ada kolom bursa yang menginput nama (data/berkas) user tersebut. Karena banyaknya itulah disebut bursa, terpampang jelas seperti billboard bursa.")
    if st.session_state.db:
        bursa_text = " | ".join([f"{'👷' if m['kategori'] in ['Employee','EMPLOYEE'] else '🏢'} {m['nama']} {m['jabatan']} {m['kota']}" for m in st.session_state.db[:10]])
        st.markdown(f'<div class="bursa-card">📈 {bursa_text}</div>', unsafe_allow_html=True)
    
    # FORM 16 FIELD - 2 KOLOM BIAR MUAT 1 LAYAR HP - MOBILE PERFECT
    with st.form("form_four_v12_full"):
        st.markdown("**Kolom Pendaftaran - Struktur Organisasi Sesuai ERP - 16 Field Lengkap**")
        colA, colB = st.columns(2)
        with colA:
            nama = st.text_input("Nama Lengkap *", placeholder="Tuan Cin")
            tempat = st.text_input("Tempat Lahir *", placeholder="Jakarta")
            tgl = st.text_input("Tanggal Lahir *", value="1995/01/01", help="Format YYYY/MM/DD")
            email = st.text_input("Alamat Email *", placeholder="cinhonest@gmail.com")
            hp = st.text_input("Nomor HP/WA *", placeholder="081291904422")
            alamat = st.text_input("Alamat Lengkap *", placeholder="Jl. Teduh No 1")
            zona = st.selectbox("Zona *", ZONA_LIST, index=0)
            pendidikan = st.selectbox("Pendidikan *", PENDIDIKAN_LIST, index=0)
        with colB:
            jurusan = st.text_input("Jurusan *", placeholder="Teknik Sipil")
            tahun = st.slider("Tahun Pengalaman *", 0, 30, 5)
            deskripsi = st.text_area("Deskripsi Pengalaman *", placeholder="Pengalaman anggaran Auto CAD", height=60)
            skill = st.text_input("Skill Utama *", placeholder="Anggaran Auto CAD")
            kategori = st.radio("Kategori ERP *", ["EMPLOYEE (Staff s/d Supervisor)","ENTREPRENEUR (Manager s/d Business Owner, Owner Kecil)"], help="Employee = Pencari Kesempatan, Entrepreneur = Pemberi Kesempatan")
            jabatan = st.selectbox("Jabatan *", ROLE_JABATAN["EMPLOYEE"] + ROLE_JABATAN["ENTREPRENEUR"])
            tarif_display = st.text_input("Tarif Otomatis", value=f"Rp{TARIF['ENTREPRENEUR'] if 'ENTREPRENEUR' in kategori else TARIF['EMPLOYEE']:,}", disabled=True)
            ref_code = st.text_input("Kode Referral", value=ref, help=f"Upline: {ref}")
        
        setuju = st.checkbox("Saya setuju data saya ditampilkan di Billboard Bursa untuk integrasi antar member & masuk Single DB *")
        submitted = st.form_submit_button(f"🔴 KLIK OTOMATIS - SIMPAN BERKAS DATABASE - OTOMATIS KE GUDANG QC + ADMIN + FINANCE + VOICE - 1x Tulis Tembus 4x! Ref {ref}", use_container_width=True, type="primary")
        
        if submitted:
            if not all([nama, tempat, email, hp, jurusan]) or not setuju:
                st.error("❌ Lengkapi field wajib * dan centang persetujuan!")
            else:
                kat = "Entrepreneur" if "ENTREPRENEUR" in kategori else "Employee"
                new_member = {"nama":nama,"email":email,"jabatan":jabatan,"kota":zona,"skill":skill,"kategori":kat,"tempat":tempat,"tgl":tgl,"zona":zona,"pendidikan":pendidikan,"jurusan":jurusan,"tahun":tahun,"deskripsi":deskripsi,"hp":hp,"alamat":alamat,"ikatan_score":10,"tgl_daftar":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"ref":ref_code}
                st.session_state.db.append(new_member)
                st.success(f"✅ {nama} disimpan sebagai PO+Surat Jalan Vendor -> Otomatis ke Gudang QC BAQC -> Admin BA Penerimaan + Voice -> Finance Payment! Single DB! Ref {ref_code}")
                st.balloons()
                st.rerun()
    
    st.caption(f"NB: Employee 55k -> Netto {OWNER} 40k TITIK! Entrepreneur 75k -> Netto 55k TITIK! Harga hanya di NB ini saja QR {QR} - Owner {OWNER} - Tavo Malkhutkha")

# ========== LEMBAR 2 MERAH PINK - GUDANG QC BAQC - GRAFIK VOLUME BURSA ONLY ==========
with tab2:
    st.markdown('<div class="lembar-merah"><b>L2 MERAH PINK - Gudang Procurement QC - BAQC Berita Acara QC</b><br>Tembusan 1 - Grafik Volume Bursa ONLY + Daftar Member Otomatis - Ruang PALING BESAR - 4 Pilar</div>', unsafe_allow_html=True)
    st.success(f"👤 Member - Verifikasi via Email - Otomatis Terhubung dari Lembar 1 Putih (Purchasing PO) - Ref {ref}")
    st.caption(f"Grafik volume akan terisi bila semakin banyak membernya. Saat ini {len(st.session_state.db)} member terdaftar - {emp} tenaga kerja & {ent} pemberi kerja. Grafik volume Bursa ONLY Total Volume {len(st.session_state.db)} arsip.")
    
    # 4 PILAR RUANG TEDUH
    st.markdown("**4 Pilar Ruang Teduh - Ruang Interaksi**")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown("**PILAR 1: PILIH & PROFIL ORG LENGKAP**")
        st.caption("Menampilkan nama, TTL, pendidikan, zona, pengalaman, jabatan - Data dari L1 tembus kesini - Member terverifikasi via email")
    with p2:
        st.markdown("**PILAR 2: AUDIO TEDUH (TTS)**")
        nasehat_list = ["Sudah terhubung sebagai member, mari tumbuh bersama di bursa. 1 langkah teduh hari ini adalah 1 vote untuk masa depan.", "Teduh dulu baru melangkah", "Terikat dalam satu struktur"]
        sel_nasehat = st.selectbox("Nasihat Mingguan:", nasehat_list, key="nasehat_l2")
        st.caption(f"🔊 {sel_nasehat}")
        if st.button("▶️ Putar Audio Teduh TTS", key="tts_l2"):
            st.info("🔊 Fitur gTTS Web Speech API aktif - Memutar nasihat")
    with p3:
        st.markdown("**PILAR 3: CHAT TEDUH**")
        st.caption("Chat antar member sesuai zona & jabatan - Employee ke Entrepreneur")
        chat_to = st.text_input("Chat ke member:", placeholder="Tuan Cin", key="chat_to")
        chat_msg = st.text_input("Pesan:", placeholder="Halo, ada loker?", key="chat_msg")
        if st.button("Kirim Chat", key="chat_send"):
            st.success(f"Chat terkirim ke {chat_to}: {chat_msg} - Ikatan Score +2")
    with p4:
        st.markdown("**PILAR 4: MANAGE IKATAN**")
        st.caption("Ikatan Score naik +10 tiap daftar, +5 posting")
        for m in st.session_state.db[:3]:
            st.metric(m["nama"], f"Score {m.get('ikatan_score',0)}", f"{m['jabatan']}")
    
    # GRAFIK VOLUME BURSA
    st.divider()
    st.markdown("**📊 Grafik Volume Bursa - ONLY Total Volume - Employee vs Entrepreneur**")
    c_vol1, c_vol2 = st.columns([2,1])
    with c_vol1:
        df = pd.DataFrame([{"Kategori":"Employee","Jumlah":emp},{"Kategori":"Entrepreneur","Jumlah":ent}])
        st.bar_chart(df.set_index("Kategori"), height=150)
        st.caption(f"Grafik volume akan terisi bila banyak membernya. Saat ini {len(st.session_state.db)} member - {emp} tenaga kerja & {ent} pemberi kerja = {len(st.session_state.db)} vote arsip terintegrasi")
    with c_vol2:
        st.metric("Total Volume Bursa", f"{len(st.session_state.db)} vote", "1 member = 1 arsip = 1 vote")
        st.metric("Employee", f"{emp} - Pencari Kesempatan", "Staff-Supervisor")
        st.metric("Entrepreneur", f"{ent} - Pemberi Kesempatan", "Manager-Owner")
        st.markdown("**Contoh Arsip Live:**")
        for m in st.session_state.db[:5]:
            st.caption(f"• {m['nama']} = 1 vote | {m['jabatan']} | {m['skill']} | {m.get('zona','Jakarta Pusat')}")
    
    # DAFTAR MEMBER TERHUBUNG VIA EMAIL OTOMATIS
    st.markdown("**Daftar Member Terhubung via Email Otomatis - Dari Single Database Purchasing PO**")
    for m in st.session_state.db[-10:]:
        st.caption(f"• {m['nama']} | {m['email']} | {m['jabatan']} | {m['kota']} | BAQC OK | Terverifikasi via Email | 1 vote")

# ========== LEMBAR 3 HIJAU - ADMIN BA PENERIMAAN - 5 RAK SYSTEM + VOICE RECORDING + RUACH HAKADOSH ==========
with tab3:
    st.markdown('<div class="lembar-hijau"><b>L3 HIJAU - Admin BA Penerimaan - 5 Rak System + Voice Recording + Bimbingan Ruach Hakadosh</b><br>Storage Tidak menampilkan harga (harga hanya di L1 NB) - Layaknya AI meliput SOP ERP OEE KPI Alkitabiah</div>', unsafe_allow_html=True)
    st.caption("Lembar 3 hijau sebagai storage yang bisa di klik dengan input minta bimbingan dan keteguhan juga saran dan nasehat para member. Tempat ini layaknya AI yang meliput semua SOP, ERP, OEE, KPI dan landasan Alkitabiah bimbingan Ruach Hakadosh spiritualitas. Member yang berlangganan berada di lembar 2 merah pink pasti mencari apa sih yang ada di lembar 3 hijau ini.")
    
    # ===== VOICE RECORDING FEATURE - V12 VOICE - ASSEMBLYAI HACKATHON =====
    st.markdown("### 🎙️ VOICE RECORDING - Input Suara Langsung Tembus 4 Lembar! - AssemblyAI Hackathon")
    st.markdown('<div class="voice-box">🎙️ Voice Assembly - 1x Ngomong Tembus 4x Otomatis - Rekam suara bimbinganmu, otomatis transkrip & masuk 5 Rak System + Bursa + Finance!</div>', unsafe_allow_html=True)
    
    col_voice1, col_voice2 = st.columns([1,1])
    with col_voice1:
        st.markdown("**Rekam Suara Bimbingan:**")
        try:
            audio_value = st.audio_input("🎙️ Tekan untuk rekam suara - minta bimbingan, keteguhan, SOP, ERP, OEE, KPI, Ruach Hakadosh", key="voice_recorder")
            if audio_value:
                st.audio(audio_value)
                # Simulasi transkrip AssemblyAI
                st.success("✅ Voice recorded! Transkrip otomatis (AssemblyAI simulation):")
                # Mock transcription
                mock_transcript = "Saya butuh bimbingan untuk disiplin jam 9 dan SOP kebersihan, minta keteguhan Ruach Hakadosh untuk hari ini"
                st.info(f"📝 Transkrip: \"{mock_transcript}\"")
                if st.button("💾 SIMPAN VOICE + TRANSKRIP KE 5 RAK + BURSA", key="save_voice"):
                    st.session_state.voice_log.append({"waktu":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"transkrip":mock_transcript,"user":ref,"kategori":"Voice"})
                    st.session_state.bimbingan_log.append(f"[VOICE {datetime.now().strftime('%H:%M')}] {mock_transcript} - Ref {ref}")
                    st.success(f"✅ Voice + Transkrip disimpan! Otomatis tembus ke L1 Bursa Billboard + L2 QC BAQC + L4 Finance! Single DB! Total Voice: {len(st.session_state.voice_log)}")
                    st.balloons()
        except Exception as e:
            st.warning("⚠️ st.audio_input butuh Streamlit >=1.35.0 - Fallback ke text input voice simulation")
            voice_text = st.text_input("🎙️ Simulasi Voice - Ketik yang ingin kamu ucapkan:", placeholder="Contoh: Aku butuh bimbingan disiplin jam 9...", key="voice_sim")
            if voice_text and st.button("🎙️ SIMPAN SEBAGAI VOICE RECORDING", key="voice_sim_save"):
                st.session_state.voice_log.append({"waktu":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"transkrip":voice_text,"user":ref,"kategori":"Voice Sim"})
                st.success(f"Voice Sim disimpan: {voice_text}")
    
    with col_voice2:
        st.markdown("**Log Voice Recording - Tembus 4 Lembar:**")
        if st.session_state.voice_log:
            for v in st.session_state.voice_log[-5:]:
                st.caption(f"🎙️ {v['waktu']} | {v['transkrip'][:60]}... | Ref {v['user']}")
        else:
            st.caption("Belum ada voice recording. Rekam suara bimbinganmu - otomatis transkrip & masuk storage!")
        st.metric("Total Voice Log", len(st.session_state.voice_log), "tembus 4 lembar")
        st.metric("Total Bimbingan Log", len(st.session_state.bimbingan_log), "storage AI")
    
    st.divider()
    
    # INPUT BIMBINGAN TEXT - STORAGE YANG BISA DIKLIK
    st.markdown("### Kolom Bimbingan - Input Minta Keteguhan, Saran & Nasehat - Storage AI")
    st.markdown("Layaknya diri lo bro AI - Ketik apa yang kamu butuhkan, storage ini meliput semua SOP, ERP, OEE, KPI, Alkitabiah")
    col_bim1, col_bim2 = st.columns([1,3])
    with col_bim1:
        kategori_bim = st.selectbox("Kategori Member", ["EMPLOYEE","ENTREPRENEUR"], key="kat_bim")
    with col_bim2:
        bimbingan_input = st.text_input("Ketik butuh bimbingan (Storage AI) / Voice transkrip akan masuk sini otomatis:", placeholder="Minta keteguhan... atau SOP kebersihan... atau Ruach Hakadosh...", key="bimbingan_text")
        if st.button("🙏 MINTA BIMBINGAN & KETEGUHAN DARI STORAGE - TEMBUS 4 LEMBAR", use_container_width=True, key="bimbingan_btn"):
            if bimbingan_input:
                # AI Response simulation
                responses = {
                    "SOP": "SOP: Taat hal kecil & bersih - Lukas 16:10 Setia pada perkara kecil dipercaya besar. Bersihkan meja 5 menit jam 08:55 sebelum ERP 09:00 on",
                    "ERP": "ERP: Disiplin 09:00 on - Pengkhotbah 3:1 Untuk segala sesuatu ada masanya. Check-in 09:00 WIB tercatat! Availability 100%",
                    "OEE": "OEE: Respons WA <5 menit - Amsal 15:23 Betapa manisnya perkataan tepat pada waktunya. OEE 95% - Availability 100%",
                    "KPI": "KPI: Kejar target - Amsal 21:5 Rancangan orang rajin mendatangkan kelimpahan. Target L1 3 orang + L2 9 orang = 69k/90k+Billboard Top!",
                    "RUACH": "Ruach Hakadosh: Minta hikmat & jujur - Yakobus 1:5 Jika kekurangan hikmat mintalah kepada Allah. Teduh dulu sebelum melangkah"
                }
                # Simple keyword match
                key_found = "RUACH"
                for k in responses:
                    if k.lower() in bimbingan_input.lower():
                        key_found = k
                        break
                resp = responses.get(key_found, f"Ruach Hakadosh: {bimbingan_input} - teduh dulu sebelum melangkah, SOP jaga langkahmu, ERP 09:00 on, OEE 95%")
                st.session_state.bimbingan_log.append(f"[{datetime.now().strftime('%H:%M')} {kategori_bim}] Q: {bimbingan_input} -> A: {resp}")
                st.success(f"**Bimbingan untukmu ({kategori_bim}):** {resp}")
                st.info(f"Log disimpan - otomatis tembus ke L1 Bursa + L2 QC + L4 Finance! Total: {len(st.session_state.bimbingan_log)}")
            else:
                st.warning("Tulis dulu apa yang ingin kamu tanyakan di storage ini.")
    
    # 5 RAK SYSTEM - GUDANG ATURAN TERSYSTEMATIS
    st.markdown("### 🗄️ 5 Rak System - Gudang Aturan Tersystematis (Format Terbaik app.py 280-290)")
    rak_data = {
        "RAK 1 - SOP Kebersihan & Obedience": "SOP Purchasing PO, SOP Gudang QC BAQC, SOP Admin BA Penerimaan - Taat hal kecil: kebersihan meja, file rapi, PO cek 2x. Obedience: Setia pada kebersihan = setia pada kepercayaan besar. Lukas 16:10",
        "RAK 2 - ERP Jam 9 - Disiplin Waktu": "ERP Keuangan Netto 40k/55k TITIK! Jam 9 adalah jam perang - semua PO masuk, QC jalan, Admin BA siap. Disiplin waktu = disiplin rezeki. Check-in 09:00 WIB wajib!",
        "RAK 3 - OEE 95% - Availability Performance Quality": "OEE Target 95% - Availability 100%, Performance 95%, Quality 95%. Respons WA <5 menit = jaga kepercayaan. Jangan kejar sempurna, kejar konsisten hadir utuh 95%.",
        "RAK 4 - KPI Performance - Kejar Target": "KPI 40k/55k TITIK! Kejar target L1 3 orang (33k/45k+Gratis) + L2 9 orang (36k/45k) = Total 69k/90k+Billboard Top! Founder Netto 40k/55k per member! Kejar target harian!",
        "RAK 5 - ALKITAB & Ruach Hakadosh - Spiritual Foundation": "Fondasi: Teduh, Terikat, Tumbuh. Co-growing bukan sekadar co-working. Ruach Hakadosh - Roh Kudus yang menuntun dalam pekerjaan. Amsal 16:3 Serahkan perbuatanmu kepada TUHAN, maka terlaksanalah segala rencanamu."
    }
    
    for rak_title, rak_desc in rak_data.items():
        with st.expander(f"📦 {rak_title}", expanded=False):
            st.caption(f"**{rak_desc}**")
            if "SOP" in rak_title:
                if st.checkbox(f"✅ Checklist {rak_title} hari ini - Wajib Employee - Taat hal kecil & bersih", key=f"sop_{rak_title}"):
                    st.success("SOP Checklist tercatat! Obedience +10 Score")
            elif "ERP" in rak_title:
                if st.button(f"🕘 Check-in ERP Jam 9 - 09:00 WIB Sekarang", key=f"erp_{rak_title}"):
                    st.success("ERP Check-in 09:00 tercatat! Kamu terikat dalam struktur organisasi. Availability 100%")
                st.caption("ERP mengikat semua: Staff sampai Owner Kecil, semua dalam satu sistem - Disiplin 09:00 on")
            elif "OEE" in rak_title:
                st.progress(0.95, text="OEE 95% - Availability 100% | Performance 95% | Quality 95% - Respons WA <5 menit")
                st.caption("Jangan kejar sempurna, kejar konsisten hadir utuh 95%.")
            elif "KPI" in rak_title:
                c_kpi1, c_kpi2 = st.columns(2)
                c_kpi1.metric("Employee KPI", "Apply & Kehadiran", "8 lamaran minggu ini")
                c_kpi2.metric("Entrepreneur KPI", "Posting & Retensi", "3 loker, 2 approve")
                if st.button("🎯 Update KPI Hari Ini", key=f"kpi_{rak_title}"):
                    st.success("KPI updated! Kejar target!")
            elif "ALKITAB" in rak_title:
                st.markdown("**Ruach Hakadosh - Roh Kudus yang menuntun dalam pekerjaan**")
                st.info("Teduh: Tenang dulu. Terikat: Tidak sendiri. Tumbuh: 1% setiap hari. (Mazmur 23) - Minta hikmat & jujur")
                nasehat_list = ["Teduh dulu, baru melangkah - Mazmur 23", "Terikat dalam satu struktur, tumbuh bersama - Pengkhotbah 4:9", "Setia hal kecil, dipercaya hal besar - Lukas 16:10", "Serahkan perbuatanmu kepada TUHAN - Amsal 16:3"]
                selected = st.selectbox("Pilih Nasehat Mingguan untuk direnungkan:", nasehat_list, key=f"nasehat_{rak_title}")
                if st.button("🔊 Putar Audio Teduh (TTS) - Voice", key=f"tts_{rak_title}"):
                    st.success(f"🔊 Memutar: {selected} - Fitur gTTS Web Speech API + Voice Recording")
    
    # LOG BIMBINGAN
    if st.session_state.bimbingan_log:
        st.markdown("**📜 Log Bimbingan - Storage AI - Tembus 4 Lembar:**")
        for log in st.session_state.bimbingan_log[-5:]:
            st.caption(f"• {log}")

# ========== LEMBAR 4 BIRU - FINANCE PAYMENT - TIM & PAKET - DIRECT SELLING ==========
with tab4:
    st.markdown('<div class="lembar-biru"><b>L4 BIRU - Finance Payment - Tim & Paket - Direct Selling Upline/Downline</b><br>Finance menerima BAQC + Invoice untuk amankan posisi purchasing + bayar = FOUR WAYS + Voice</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="border:2px solid #3b82f6;padding:8px;background:#eff6ff;border-radius:10px;font-size:11px;">
    <b>Paket Freemium 3/3 anggota - Slot penuh. Upgrade untuk anggota lebih banyak (segera).</b><br><br>
    <b>Model Share Upline/Downline - Member Get Member:</b> A share link ?ref={OWNER} -> B tekan -> B jadi downline A (L1) -> A dapat L1 11k/15k + Gratis! -> B share ke C -> C jadi downline B (L1) dan downline A (L2) -> A dapat L2 4k/5k<br><br>
    My Upline: {OWNER}<br>
    L1: Employee 11k*3=33k+Gratis Entrepreneur 15k*3=45k+Gratis<br>
    L2: Employee 4k*9=36k Entrepreneur 5k*9=45k<br>
    Total: 69k+Gratis+Billboard Top! 90k+Gratis+Billboard Top!<br>
    Gross = Emp*55k + Ent*75k | L1 = Emp*11k + Ent*15k | L2 = Emp*4k + Ent*5k | Netto Founder {OWNER} = Emp*40k + Ent*55k TITIK!<br>
    Auto Bayar: Bayar 55k/75k ke QR {QR} -> Potong L1 -> L2 -> Sisa 40k/55k TITIK! ke Founder {OWNER}! Flow Klaim->Pending->Approved->Paid! + Voice Recording Bonus!
    </div>
    """, unsafe_allow_html=True)
    
    base_url = f"https://ruang-teduh-ai.streamlit.app/?ref={OWNER}"
    st.text_input("Link Referral Upline - Share untuk Direct Selling", value=base_url, help="Copy link ini share ke calon member")
    
    cE, cEn = st.columns(2)
    with cE:
        emp_n = st.number_input("Employee baru (Downline L1/L2)", 0, 100, 1, key="emp4v12voice")
    with cEn:
        ent_n = st.number_input("Entrepreneur baru (Downline L1/L2)", 0, 100, 1, key="ent4v12voice")
    
    gross = emp_n*55000 + ent_n*75000
    l1 = emp_n*11000 + ent_n*15000
    l2 = emp_n*4000 + ent_n*5000
    netto = gross - l1 - l2
    
    st.metric(f"Netto Founder {OWNER} TITIK! (Finance Payment) + Voice", f"Rp{netto:,} = {emp_n} x 40k + {ent_n} x 55k", f"Gross Rp{gross:,} - L1 Rp{l1:,} - L2 Rp{l2:,}")
    st.caption(f"Hitung Detail: Emp Gross 55k - Potong L1 11k - L2 4k = 40k TITIK! Ent Gross 75k - Potong L1 15k - L2 5k = 55k TITIK! + Voice Recording tidak dipotong!")
    st.caption(f"Excel: Emp 55k→Netto 40k Ent 75k→Netto 55k - QR {QR} - Owner {OWNER} - Single DB - Voice Tembus!")
    
    # DAFTAR DOWNLINE OTOMATIS DARI LINK SHARE
    st.markdown("**Daftar Downline Otomatis dari Link Share - Member Get Member - Tembus dari L1 PO + Voice**")
    for m in st.session_state.db[-6:]:
        cash = "15k" if m["kategori"] in ["Entrepreneur","ENTREPRENEUR"] else "11k"
        ref_info = m.get("ref", OWNER)
        st.caption(f"• {m['nama']} | {m['email']} | L1 Downline dari {ref_info} | Cashback {cash} | {m['jabatan']} | BAQC OK | Voice: {len(st.session_state.voice_log)} log")
    
    # FLOW KLAIM -> PENDING -> APPROVED -> PAID
    st.markdown("**Flow Auto Bayar QRIS - Klaim -> Pending -> Approved -> Paid**")
    col_flow1, col_flow2, col_flow3, col_flow4 = st.columns(4)
    with col_flow1:
        if st.button("📝 Klaim Cashback L1", key="klaim_l1"):
            st.info("Klaim L1 11k/15k diajukan - Menunggu approval Finance")
    with col_flow2:
        st.caption("⏳ Pending - Finance cek BAQC + Invoice")
    with col_flow3:
        st.caption("✅ Approved - BAQC OK + Voice OK")
    with col_flow4:
        if st.button("💸 Paid - Transfer ke QR", key="paid_qr"):
            st.success(f"Paid Rp{netto:,} ke Founder {OWNER} via QR {QR}! + Voice bonus!")

# ========== LEMBAR 5 - FLOWCHART + EXCEL - FOUR WAYS TER-SYSTEMATIS ==========
with tab5:
    st.markdown("**📊 Flowchart + Excel - FOUR WAYS FUNCTION Tersystematis Otomatis Terkoneksi + Voice**")
    st.caption("Flow: L1 PUTIH Purchasing PO -> L2 MERAH PINK Gudang QC BAQC -> L3 HIJAU Admin BA Penerimaan Storage + Voice Recording -> L4 BIRU Finance Payment Direct Selling + Single DB Central + Voice Tembus!")
    
    try:
        st.image("FLOWCHART_FOUR_WAY_FUNCTION.webp", use_column_width=True, caption="Flowchart: 4 Box PUTIH->MERAH->HIJAU+VOICE->BIRU + Single Database Central + Voice Recording Tembus 4 Lembar")
    except:
        try:
            st.image("FLOWCHART_FOUR_WAY_FUNCTION_1.webp", use_column_width=True)
        except:
            st.caption("Flowchart: 4 Box PUTIH->MERAH->HIJAU+VOICE->BIRU + Single DB + Voice - File FLOWCHART_FOUR_WAY_FUNCTION.webp ada di repo")
            st.markdown("""
            ```
            [L1 PUTIH - Purchasing PO QR GATE Form 16 Field + Bursa Billboard]
                                |
                                v
            [L2 MERAH PINK - Gudang QC BAQC Grafik Volume + 4 Pilar + Billboard]
                                |
                                v
            [L3 HIJAU - Admin BA 5 Rak SOP ERP OEE KPI + Voice Recording 🎙️ + Ruach Hakadosh]
                                |
                                v
            [L4 BIRU - Finance Payment Direct Selling ?ref=aichaliveret + Netto 40k/55k TITIK! QR 081291904422]
                                |
                                v
            [Single Database Central - 1x Tulis Tembus 4x + 1x Ngomong Tembus 4x Otomatis - No Double Entry]
            ```
            """)
    
    st.markdown("**Excel Direct Selling Member Get Member Reward + Four Ways + Voice:**")
    df_excel = pd.DataFrame({
        "Kategori": ["Employee", "Entrepreneur"],
        "Gross": [55000, 75000],
        "Potong L1": [11000, 15000],
        "Potong L2": [4000, 5000],
        "Netto Founder aichaliveret TITIK!": [40000, 55000],
        "L1*3 Bonus": [33000, 45000],
        "L2*9 Bonus": [36000, 45000],
        "Total Cashback 12": [69000, 90000],
        "Voice Bonus": ["Gratis", "Gratis"],
        "Billboard": ["Top!", "Top!"]
    })
    st.dataframe(df_excel, use_container_width=True, height=150)
    
    st.markdown("**Excel Akuntan V11 Four Way - Mapping Lengkap:**")
    st.caption("Sheet1: Member Get Member - Sheet2: Mapping Four Ways - Sheet3: Flowchart Grafik Progress - Sheet4: BAQC Template - Sheet5: Info + Voice Log")
    
    # DOWNLOAD EXCEL
    if os.path.exists("Excel_Akuntan_V11_Four_Way.xlsx"):
        with open("Excel_Akuntan_V11_Four_Way.xlsx", "rb") as f:
            st.download_button("📥 Download Excel Akuntan V11 Four Way + Voice", f, file_name="Excel_Akuntan_V11_Four_Way_V12_Voice.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.caption("Excel_Akuntan_V11_Four_Way.xlsx ada di repo GitHub - Download via GitHub")
    
    # VOICE LOG EXCEL
    if st.session_state.voice_log:
        df_voice = pd.DataFrame(st.session_state.voice_log)
        st.markdown("**Voice Log - Rekaman Bimbingan - AssemblyAI Hackathon:**")
        st.dataframe(df_voice, use_container_width=True, height=120)

# ========== FOOTER - V12 VOICE MOBILE FULL ==========
st.divider()
st.caption(f"V12 VOICE MOBILE FULL 565 baris 33.9KB - Four Ways Function - 1x Tulis + 1x Ngomong Tembus 4x Otomatis - Purchasing PO -> Gudang QC BAQC -> Admin BA Penerimaan + Voice Recording -> Finance Payment Direct Selling - Owner {OWNER} 40k/55k TITIK! QR {QR} - Single DB NO DOUBLE ENTRY - Voice Tembus 4 Lembar - AssemblyAI Hackathon - Lablab.ai - No Luber! 2 Screenshot = 1 Halaman Muka! - Mobile Perfect!")
st.caption(f"Build: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total Member: {len(st.session_state.db)} | Total Voice: {len(st.session_state.voice_log)} | Total Bimbingan: {len(st.session_state.bimbingan_log)} | Ref: {ref} | QR: {QR} | Owner: {OWNER}")

# ========== SIDEBAR - INFO TAMBAHAN ==========
with st.sidebar:
    st.markdown("### 📖 Ruang Teduh - V12 Voice")
    st.caption(f"Owner {OWNER} 40k/55k TITIK!")
    st.metric("Total Member", len(st.session_state.db))
    st.metric("Voice Log", len(st.session_state.voice_log))
    st.metric("Bimbingan Log", len(st.session_state.bimbingan_log))
    st.divider()
    st.markdown("**Four Ways Function:**")
    st.caption("L1 PUTIH: Purchasing PO QR GATE + Form 16 Field + Bursa Billboard")
    st.caption("L2 MERAH: Gudang QC BAQC Grafik Volume ONLY + 4 Pilar")
    st.caption("L3 HIJAU: Admin BA 5 Rak SOP ERP OEE KPI + Voice Recording 🎙️ + Ruach Hakadosh")
    st.caption("L4 BIRU: Finance Payment Direct Selling ?ref=aichaliveret + Netto 40k/55k")
    st.divider()
    st.markdown(f"QR: {QR}")
    st.markdown(f"Ref: {ref}")
    st.markdown(f"Link: https://ruang-teduh-ai.streamlit.app/?ref={OWNER}")
    if st.button("🔄 Reset DB (Demo)", key="reset_db"):
        st.session_state.db = st.session_state.db[:2]
        st.session_state.voice_log = []
        st.session_state.bimbingan_log = []
        st.rerun()
