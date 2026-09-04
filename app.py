"""
app.py - BUKU 1 RUANG 3 LEMBAR - NCR SYSTEM 1x Tulis Tembus 3x Otomatis
Versi: Sesuai instruksi detail user - Kolom saja tanpa point, harga hanya di NB
Lembar 1 Putih: Billboard Bursa + Pendaftaran 2 bagian + Nasehat Ajakan + NB Harga
Lembar 2 Merah Pink: Nasehat + Grafik Volume Bursa + Syarat Wajib
Lembar 3 Hijau: Storage 5 Rak + Input Bimbingan Ruach Hakadosh
"""

import streamlit as st
from datetime import datetime, date
import qrcode
from io import BytesIO
import json

from core import (
    TARIF, ROLE_JABATAN, ZONA_LIST, PENDIDIKAN_LIST, FIELD_WAJIB,
    Member, load_members, save_member, get_bursa_billboard, get_bursa_stats,
    get_5_rak_storage, get_bimbingan_ai_response
)

st.set_page_config(
    page_title="Ruang Teduh - Buku 1 Ruang 3 Lembar",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .carbon-line { border-top: 3px dashed #999; margin:25px 0; position:relative; }
    .carbon-line::after { content:'✂️ CARBON COPY - 1x Tulis Tembus 3x Otomatis - NCR SYSTEM'; position:absolute; top:-10px; left:50%; transform:translateX(-50%); background:white; padding:0 12px; font-size:10px; color:#777; letter-spacing:1px; }
    .lembar-putih { background:#FAFAFA; border:2px solid #333; border-left:8px solid #333; padding:15px; border-radius:8px; }
    .lembar-merah { background:#FFF5F5; border:2px solid #D32F2F; border-left:8px solid #D32F2F; padding:15px; border-radius:8px; }
    .lembar-hijau { background:#F1F8E9; border:2px solid #2E7D32; border-left:8px solid #2E7D32; padding:15px; border-radius:8px; }
    .bursa-billboard { background: linear-gradient(135deg,#FFFDE7 0%,#FFF9C4 100%); border:2px solid #FF6B00; border-radius:12px; padding:15px; }
    .bursa-header { background:#FF6B00; color:white; padding:10px 15px; border-radius:8px; font-weight:bold; margin:-15px -15px 15px -15px; }
    .member-ticker { background:white; border:1px solid #FFB74D; border-radius:20px; padding:6px 14px; margin:4px; display:inline-block; font-size:13px; }
    .kolom-keterangan { background:white; border:1px solid #E0E0E0; border-radius:10px; padding:15px; margin:10px 0; }
    .nb-box { background:#FFF3E0; border:2px dashed #FF6B00; border-radius:10px; padding:15px; }
    .floating-nav { position:fixed; bottom:20px; right:20px; z-index:9999; }
    .dot { width:65px; height:65px; border-radius:50%; background:#FF6B00; color:white; border:none; font-weight:bold; box-shadow:0 4px 15px rgba(255,107,0,0.4); margin:5px; }
</style>
""", unsafe_allow_html=True)

if "current_lembar" not in st.session_state:
    st.session_state.current_lembar = "PUTIH"
if "sudah_daftar" not in st.session_state:
    st.session_state.sudah_daftar = False

def generate_qr(data: str):
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# HEADER - BUKU 1 RUANG 3 LEMBAR
st.markdown("# 📖 BUKU 1 RUANG 3 LEMBAR")
st.markdown("### THREE WAY FUNCTION ASLI - NCR SYSTEM | 1x Tulis Tembus 3x Otomatis")
st.caption("Tavo Malkhutkha: Two Journeys, One QR - Ruang Teduh AI")

# NAVIGASI FLOATING DOT ORANGE
c1,c2,c3,c4 = st.columns([1,1,1,5])
with c1:
    if st.button("⚪\nPUTIH", use_container_width=True):
        st.session_state.current_lembar = "PUTIH"
with c2:
    if st.button("🔴\nMERAH PINK", use_container_width=True):
        st.session_state.current_lembar = "MERAH"
with c3:
    if st.button("🟢\nHIJAU", use_container_width=True):
        st.session_state.current_lembar = "HIJAU"

st.markdown('<div class="carbon-line"></div>', unsafe_allow_html=True)

# =========================================
# LEMBAR 1 PUTIH - ASLI | RUANG TEDUH PINTU DEPAN
# =========================================
if st.session_state.current_lembar == "PUTIH":
    st.markdown('<div class="lembar-putih"><h2>LEMBAR 1 PUTIH - ASLI | RUANG TEDUH - Pintu Depan</h2><p>File: app.py | Flow: [QR GATE] -> [FORM ORG LENGKAP] -> [VALIDASI] - Fungsi Penerima & Billboard Bursa</p></div>', unsafe_allow_html=True)

    # QR GATE
    col_qr, col_desc = st.columns([1,3])
    with col_qr:
        qr_img = generate_qr("https://ruang-teduh.ai/qr-gate")
        st.image(qr_img, width=180, caption="QR GATE - Scan Masuk")
    with col_desc:
        st.markdown("**[QR GATE]** - Dua perjalanan, satu QR. Scan untuk masuk sebagai Employee atau Entrepreneur sesuai struktur ERP.")

    st.divider()

    # KOLOM BURSA - Penerima banyak member terkoneksi, billboard
    st.markdown("### Kolom Bursa - Billboard Member Terhubung")
    st.markdown('<div class="kolom-keterangan">', unsafe_allow_html=True)
    st.markdown("Kolom ini sebagai penerima dari banyaknya member yang sudah terkoneksi karena menggunakan aplikasi ini. Ada kolom bursa yang menginput nama (data/berkas) user tersebut. Karena banyaknya itulah disebut bursa, terpampang jelas seperti billboard bursa. Selanjutnya disebut **BURSA**. Kita memberikan jasa ini untuk para member saling terintegrasi dalam bursa dan mendapatkan manfaat.")
    
    stats = get_bursa_stats()
    m1,m2,m3 = st.columns(3)
    m1.metric("Total Arsip di Bursa", f"{stats['total']} member", "1 member = 1 arsip = 1 vote")
    m2.metric("Employee di Bursa", f"{stats['employee']} tenaga kerja")
    m3.metric("Entrepreneur di Bursa", f"{stats['entrepreneur']} pemberi kerja")
    
    members = get_bursa_billboard()
    if members:
        st.markdown('<div class="bursa-billboard"><div class="bursa-header">📊 BURSA TEDUH - PAPAN BILLBOARD MEMBER (Live Ticker)</div>', unsafe_allow_html=True)
        for m in members[:30]:
            icon = "👷" if m["kategori"]=="EMPLOYEE" else "🏢"
            st.markdown(f'<span class="member-ticker">{icon} {m["nama"]} | {m["jabatan"]} | {m["zona"]} | {m["skill"]} | {m["tahun_pengalaman"]}th | {m["pendidikan"]}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Bursa masih kosong. Jadilah arsip pertama yang terpampang di billboard.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # KOLOM PENDAFTARAN - 2 Bagian Employee & Entrepreneur, ERP, auto masuk lembar 2
    st.markdown("### Kolom Pendaftaran - Struktur Organisasi Sesuai ERP")
    st.markdown('<div class="kolom-keterangan">', unsafe_allow_html=True)
    st.markdown("Kolom ini menampilkan keterangan semua orang kita sebut para member menjadi dua bagian yaitu **Employee juga Entrepreneur** sesuai struktur usaha umum mengikuti ERP termasuk pengusaha, owner kecil masuk dalam ERP. Klik otomatis sudah berlangganan dan masuk ke dalam **Lembar 2 Merah Pink**. Setelah berlangganan terjadi secara langsung otomatis baik Employee maupun Entrepreneur berada di ruang Merah Pink. Lembar selanjutnya yaitu Lembar 3 Hijau sebagai storage tempat kita menjelaskan dan memberikan bimbingan dan nasehat semua yaitu SOP, ERP, OEE, KPI yang sesuai dan berlandaskan Alkitabiah bimbingan Ruach Hakadosh spiritual.")
    
    # FORM - TIDAK ADA st.button di dalam form, hanya form_submit_button
    with st.form("form_lembar_putih", clear_on_submit=False):
        cA,cB = st.columns(2)
        with cA:
            nama = st.text_input("Nama Lengkap *")
            tempat_lahir = st.text_input("Tempat Lahir *")
            tgl_lahir = st.date_input("Tanggal Lahir *", value=date(1995,1,1), min_value=date(1960,1,1), max_value=date(2006,12,31))
            email = st.text_input("Alamat Email *")
            hp = st.text_input("Nomor HP/WA *")
            alamat_kependudukan = st.text_area("Alamat Kependudukan (KTP/Domisili) *", height=70)
        with cB:
            zona = st.selectbox("Zona Rumah Tinggal *", ZONA_LIST)
            pendidikan = st.selectbox("Pendidikan Terakhir *", PENDIDIKAN_LIST)
            jurusan = st.text_input("Jurusan *")
            tahun_pengalaman = st.slider("Tahun Pengalaman *", 0, 20, 2)
            deskripsi_pengalaman = st.text_area("Deskripsi Pengalaman Kerja Lengkap *", height=70)
            skill = st.text_input("Skill Utama (contoh: Admin, Sales, Desain) *")
        
        st.markdown("**Pilih Struktur ERP**")
        kategori = st.radio("Kategori Member *", ["EMPLOYEE (Staff s/d Supervisor - Pelaksana)", "ENTREPRENEUR (Manager s/d Business Owner - Pimpinan termasuk Owner Kecil)"], horizontal=False)
        kategori_val = "EMPLOYEE" if "EMPLOYEE" in kategori else "ENTREPRENEUR"
        jabatan = st.selectbox(f"Jabatan untuk {kategori_val} *", ROLE_JABATAN[kategori_val])
        
        st.caption("Pengingat: Ada biaya berlangganan bulanan untuk akses bursa terintegrasi. Detail harga ada di kolom NB bawah.")
        setuju = st.checkbox("Saya setuju data saya masuk Billboard Bursa dan terintegrasi *")
        
        submit = st.form_submit_button("🔘 KLIK OTOMATIS BERLANGGANAN & MASUK KE LEMBAR 2 MERAH PINK", use_container_width=True, type="primary")
        
        if submit:
            if not all([nama, tempat_lahir, email, hp, alamat_kependudukan, jurusan, skill, deskripsi_pengalaman]) or not setuju:
                st.error("Lengkapi semua field wajib bertanda *")
            else:
                new_member = Member(
                    nama=nama, tempat_lahir=tempat_lahir, tgl_lahir=str(tgl_lahir),
                    email=email, hp=hp, alamat_kependudukan=alamat_kependudukan,
                    zona=zona, pendidikan=pendidikan, jurusan=jurusan,
                    tahun_pengalaman=tahun_pengalaman, deskripsi_pengalaman=deskripsi_pengalaman,
                    skill=skill, kategori=kategori_val, jabatan=jabatan,
                    tarif=TARIF[kategori_val], tgl_daftar=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                save_member(new_member)
                st.success(f"✅ {nama} - Data tembus otomatis! Kamu sebagai {jabatan} sudah masuk Lembar 2 Merah Pink & Billboard Bursa.")
                st.session_state.sudah_daftar = True
                st.session_state.current_lembar = "MERAH"
                st.balloons()
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # KOLOM NASEHAT AJAKAN 1-2 KALIMAT
    st.markdown("### Kolom Nasehat Bimbingan")
    st.markdown('<div class="kolom-keterangan" style="background:#E8F5E9;">', unsafe_allow_html=True)
    st.markdown("**Mari teduh dulu sebelum melangkah. Di Ruang Teduh, SOP menjaga langkahmu, KPI mengukur tumbuhmu, dan Alkitab meneduhkan hatimu. Daftar sekarang, terintegrasi di bursa, dan rasakan manfaat terikat dalam satu keluarga kerja.**")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # KOLOM NB - SYARAT BERLANGGANAN - HARGA HANYA DI SINI
    st.markdown("### NB: Kolom Syarat & Ketentuan Berlangganan Bulanan")
    st.markdown('<div class="nb-box">', unsafe_allow_html=True)
    st.markdown("""
    **Syarat sebagai member mesti berlangganan bulanan:**
    
    - **Employee Rp 55.000 / bulan** - Untuk Staff, Senior Staff, Supervisor (Pencari Kesempatan)
    - **Entrepreneur Rp 75.000 / bulan** - Untuk Manager, GM, Director, Business Owner, Owner Kecil / Pengusaha (Pemberi Kesempatan)
    
    **Cara Berlangganan:**
    Transfer via **GoPay, OVO, DANA, Bank Transfer**
    
    **QR Code & No HP Pembayaran:** 081291904422
    
    Setelah klik otomatis berlangganan di kolom pendaftaran atas, kamu langsung terintegrasi di Billboard Bursa dan masuk ke Lembar 2 Merah Pink. Biaya ini untuk jasa integrasi bursa agar saling mendapat manfaat.
    
    *Catatan: Harga member hanya ditampilkan di kolom NB ini saja, tidak di tempat lain.*
    """)
    col_qr_pay, col_pay_info = st.columns([1,2])
    with col_qr_pay:
        qr_pay = generate_qr("081291904422 - GOPAY OVO DANA BANK - RUANG TEDUH")
        st.image(qr_pay, width=180, caption="QR Pay 081291904422 - GoPay OVO DANA Bank")
    with col_pay_info:
        st.info("💳 Scan QR atau transfer manual ke 081291904422. Konfirmasi otomatis masuk bursa.")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# LEMBAR 2 MERAH PINK - RUANG INTERAKSI - PALING BESAR
# =========================================
elif st.session_state.current_lembar == "MERAH":
    st.markdown('<div class="lembar-merah"><h2>LEMBAR 2 MERAH PINK - TEMBUSAN 1 | RUANG INTERAKSI</h2><p>File: core.py + nasehat_mingguan.txt | Ruang PALING BESAR - 4 Pilar + Bursa Kerja Teduh - Member Sudah Terdaftar & Terikat</p></div>', unsafe_allow_html=True)

    stats = get_bursa_stats()
    members = get_bursa_billboard()

    # KOLOM NASEHAT 1-2 KALIMAT
    st.markdown("### Kolom Nasehat")
    st.markdown('<div class="kolom-keterangan" style="background:#FFEBEE;">', unsafe_allow_html=True)
    st.markdown("**Sudah membayar dan terikat berarti sudah memilih tumbuh bersama. Di bursa ini 1 arsip = 1 vote = 1 kesempatan yang Tuhan percayakan.**")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # KOLOM BURSA TENAGA KERJA + GRAFIK VOLUME
    st.markdown("### Kolom Bursa Tenaga Kerja & Grafik Volume")
    st.markdown('<div class="kolom-keterangan">', unsafe_allow_html=True)
    st.markdown("Kolom ini menjelaskan bursa tenaga kerja berapa banyak member yang sudah terdaftar. **1 member (Pak Budi) mewakili 1 arsip yang bernilai 1 vote** dan diumumkan secara nilai di bursa. Bila semakin banyak mendaftar akan semakin banyak yang terlihat. Bagi Entrepreneur juga demikian 1 nilai adalah 1 member yang mendaftar sebagai Entrepreneur (Pak Bambang direktur), 1 nilai tambahan lagi sebagai member terdaftar (Pak Johan owner/usahawan) jadi kolom grafik volume menampilkan 1+1=2 member terdaftar dalam bursa, dst.")
    
    c_vol1, c_vol2 = st.columns([2,1])
    with c_vol1:
        # Grafik Volume sederhana pakai bar_chart
        import pandas as pd
        chart_data = pd.DataFrame({
            "Kategori": ["Employee", "Entrepreneur"],
            "Jumlah Arsip (Vote)": [stats["employee"], stats["entrepreneur"]]
        })
        st.bar_chart(chart_data, x="Kategori", y="Jumlah Arsip (Vote)", color="#FF6B00")
        st.caption(f"Grafik Volume Bursa: Total {stats['total']} vote - {stats['employee']} Employee + {stats['entrepreneur']} Entrepreneur = {stats['total_vote']} arsip terintegrasi")
    with c_vol2:
        st.metric("Total Volume Bursa", f"{stats['total_vote']} vote")
        st.metric("Employee", f"{stats['employee']} - contoh: Pak Budi (Staff)")
        st.metric("Entrepreneur", f"{stats['entrepreneur']} - contoh: Pak Bambang (Direktur) + Pak Johan (Owner) = 2")
        if members:
            st.markdown("**Contoh Arsip Live:**")
            for m in members[:5]:
                st.markdown(f"- {m['nama']} = 1 vote | {m['jabatan']} | Skill: {m['skill']}")

    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # KOLOM SYARAT WAJIB ISI
    st.markdown("### Kolom Syarat & Ketentuan Member Terintegrasi")
    st.markdown('<div class="kolom-keterangan">', unsafe_allow_html=True)
    st.markdown("Bagian dalam lembar 2 merah pink ini kolom syarat. Kolom keterangan yang wajib diisi para member terdaftar:")
    
    for idx, field in enumerate(FIELD_WAJIB, 1):
        st.markdown(f"**{idx}. {field}**")
    
    st.markdown("---")
    st.markdown("**Tambahan yang mesti terlampir agar terintegrasi maksimal (saran sistematis):**")
    st.markdown("""
    - **Foto Profil Terbaru** - Agar dikenal di Billboard Bursa
    - **CV / Portofolio Link (Google Drive / LinkedIn)** - Mempercepat dilamar Entrepreneur
    - **Akun LinkedIn / Instagram Profesional** - Validasi skill
    - **Surat Keterangan / Sertifikat Skill** (opsional tapi prioritas di bursa)
    - **Referensi Kerja / Atasan Sebelumnya** (opsional)
    - **Status Ketersediaan:** Full-time / Part-time / Freelance
    - **Ekspektasi Gaji / Fee** (opsional, hanya terlihat oleh Entrepreneur)
    
    Semua data ini otomatis menjadi **1 arsip bernilai 1 vote** di bursa dan langsung terkoneksi secara terintegrasi antar Employee dan Entrepreneur.
    """)
    
    # Tampilkan semua member dengan detail lengkap
    if members:
        st.markdown("#### Daftar Lengkap Arsip Terintegrasi di Bursa")
        for m in members:
            with st.expander(f"{m['nama']} - {m['jabatan']} - {m['zona']} - {m['skill']} - {m['kategori']} - 1 vote"):
                st.json(m)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# LEMBAR 3 HIJAU - BOARDING / STORAGE - 5 RAK + BIMBINGAN AI
# =========================================
else:
    st.markdown('<div class="lembar-hijau"><h2>LEMBAR 3 HIJAU - TEMBUSAN 2 | BOARDING / STORAGE</h2><p>File: README.md + 5 Rak System | Storage - Tidak menampilkan harga (harga hanya di Lembar 1 Putih NB)</p></div>', unsafe_allow_html=True)

    st.markdown("Kolom ini sebagai storage yang bisa di klik dengan input minta bimbingan dan keteguhan juga saran dan nasehat para member. Tempat ini layaknya diri lo bro AI yang meliput semua SOP, ERP, OEE, KPI dan landasan Alkitabiah bimbingan dan tuntunan Ruach Hakadosh spiritualitas.")

    # INPUT BIMBINGAN - STORAGE YANG BISA DIKLIK
    st.markdown("### Kolom Bimbingan - Input Minta Keteguhan, Saran & Nasehat")
    st.markdown('<div class="kolom-keterangan" style="background:#E8F5E9; border:2px solid #2E7D32;">', unsafe_allow_html=True)
    st.markdown("**Layaknya AI Mentor - Ketik apa yang kamu rasakan, butuh bimbingan SOP, ERP, OEE, KPI atau tuntunan Ruach Hakadosh**")
    
    bimbingan_input = st.text_area("Tulis bimbingan yang kamu butuhkan:", placeholder="Contoh: Aku bimbang melamar kerja, butuh keteguhan... atau Jelaskan SOP kebersihan... atau Aku butuh nasehat Alkitab untuk kerja hari ini...", height=100)
    
    col_bim1, col_bim2 = st.columns([1,3])
    with col_bim1:
        kategori_bim = st.selectbox("Kategori Member", ["EMPLOYEE", "ENTREPRENEUR"])
    with col_bim2:
        if st.button("🙏 MINTA BIMBINGAN & KETEGUHAN DARI STORAGE", use_container_width=True, type="primary"):
            if bimbingan_input:
                response = get_bimbingan_ai_response(bimbingan_input, kategori_bim)
                st.success(f"**Bimbingan untukmu ({kategori_bim}):** {response}")
            else:
                st.warning("Tulis dulu apa yang ingin kamu tanyakan di storage ini.")
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown("### 5 Rak System - Gudang Aturan Tersystematis (Ikutin format app.py 280-290 terbaik)")
    rak_data = get_5_rak_storage()
    
    for rak_title, rak_desc in rak_data.items():
        with st.expander(f"📦 {rak_title}", expanded=False):
            st.markdown(f"**{rak_desc}**")
            if "SOP" in rak_title:
                st.checkbox("✅ Checklist SOP Kebersihan & Obedience hari ini - Taat hal kecil", key=f"sop_{rak_title}")
                st.caption("Obedience: Setia pada kebersihan = setia pada kepercayaan besar. (Lukas 16:10)")
            elif "ERP" in rak_title:
                if st.button("🕘 Check-in ERP Jam 9 - 09:00 WIB", key=f"erp_{rak_title}"):
                    st.success("ERP Check-in 09:00 tercatat! Kamu terikat dalam struktur organisasi.")
                st.caption("ERP mengikat semua: Staff sampai Owner Kecil, semua dalam satu sistem.")
            elif "OEE" in rak_title:
                st.progress(0.95, text="OEE 95% - Availability 100% | Performance 95% | Quality 95%")
                st.caption("Jangan kejar sempurna, kejar konsisten hadir utuh 95%.")
            elif "KPI" in rak_title:
                c_kpi1, c_kpi2 = st.columns(2)
                c_kpi1.metric("Employee KPI", "Apply & Kehadiran", "8 lamaran minggu ini")
                c_kpi2.metric("Entrepreneur KPI", "Posting & Retensi", "3 loker, 2 approve")
            elif "ALKITAB" in rak_title:
                st.markdown("**Ruach Hakadosh - Roh Kudus yang menuntun dalam pekerjaan**")
                st.info("Teduh: Tenang dulu. Terikat: Tidak sendiri. Tumbuh: 1% setiap hari. (Mazmur 23)")
                # Audio Teduh
                nasehat_list = ["Teduh dulu, baru melangkah", "Terikat dalam satu struktur, tumbuh bersama", "Setia hal kecil, dipercaya hal besar"]
                selected = st.selectbox("Pilih Nasehat Mingguan untuk direnungkan:", nasehat_list, key=f"nasehat_{rak_title}")
                if st.button("🔊 Putar Audio Teduh (TTS)", key=f"tts_{rak_title}"):
                    st.success(f"🔊 Memutar: {selected} - Fitur gTTS Web Speech API")

st.markdown('<div class="carbon-line"></div>', unsafe_allow_html=True)
st.caption("© Ruang Teduh AI - Buku 1 Ruang 3 Lembar | NCR System 1x Tulis Tembus 3x Otomatis | Floating Dot Orange | Tarif hanya di Lembar 1 Putih NB: Employee 55k Entrepreneur 75k via GoPay OVO DANA Bank QR 081291904422 | Billboard Bursa Terintegrasi")
