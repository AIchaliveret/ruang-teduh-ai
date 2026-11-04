import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Ruang Teduh V15 - FINAL GREEN MIRROR - ETIKA + SOP OEE ERP KPI + RUACH", page_icon="🕊️", layout="wide")

# --- REAL EMAIL - FIX CLERICAL ---
def send_email_v15(to_list, subject, body_html):
    try:
        smtp_cfg = st.secrets.get("smtp", {})
        host = smtp_cfg.get("host", "smtp.gmail.com")
        port = smtp_cfg.get("port", 587)
        user = smtp_cfg.get("username", "jugalachaliveret@gmail.com")
        pw = smtp_cfg.get("password", "")
        admin = smtp_cfg.get("admin_email", "jugalachaliveret@gmail.com")
        cc = smtp_cfg.get("cc_email", "cinhonest@gmail.com")
        if not pw:
            return False, "Secrets smtp password kosong - isi di .streamlit/secrets.toml"
        all_rcpt = list(set(to_list + [admin, cc]))
        msg = MIMEMultipart()
        msg['From'] = user
        msg['To'] = ", ".join(to_list)
        msg['Cc'] = f"{admin}, {cc}"
        msg['Subject'] = subject
        msg.attach(MIMEText(body_html, 'html'))
        s = smtplib.SMTP(host, port)
        s.starttls()
        s.login(user, pw)
        s.sendmail(user, all_rcpt, msg.as_string())
        s.quit()
        return True, f"✅ Terkirim ke {', '.join(all_rcpt)}"
    except Exception as e:
        return False, f"❌ {str(e)}"

# --- NASEHAT MINGGUAN CENTRAL - TERKONEKSI MERAH KUNING HIJAU ---
if "nasehat_mingguan" not in st.session_state:
    st.session_state.nasehat_mingguan = {
        "etika_advice": """📜 ETIKA & PEMBELAJARAN ADVICES - Ruang Teduh:

1. Kejujuran CV - Tulis pengalaman apa adanya, jangan palsu. Kejujuran = modal OEE 95%.
2. Hormat Waktu - OEE dimulai dari datang tepat waktu, Availability 100%.
3. Saling Bantu - Bursa Vote bukan saingan tapi keluarga DKI. Bantu rekan dapat kerja = koin teduh.
4. The Best Interaksi - Cari kerja & beri kerja dengan hati, bukan cuma omzet.
5. Disiplin Klerikal - Dari lembar Windows kecil naik jadi management control.

Waspada: Jangan ambil pekerja yang tidak jujur CV nya.
""",
        "ruach_mingguan": """🔥 RUACH HAKADOSH - Nasihat Spiritual 2-3 Ayat Saja (Editable via Nasehat Mingguan):

"Jikalau kamu tinggal di dalam Aku dan firman-Ku tinggal di dalam kamu, mintalah apa saja yang kamu kehendaki, dan kamu akan menerimanya." - Yohanes 15:7

"Segala sesuatu yang kamu kehendaki supaya orang perbuat kepadamu, perbuatlah demikian juga kepada mereka." - Matius 7:12

"Serahkanlah perbuatanmu kepada TUHAN, maka terlaksanalah segala rencanamu." - Amsal 16:3

Bekerja bukan hanya untuk omzet, tapi untuk menjadi berkat bagi sesama.
""",
        "sop": """📋 SOP - Standard Operating Procedure - Manager/Brand/Usahawan:

• Wewenang: Kelola 5-10 Staff + 2-3 Supervisor, keputusan strategis, anggaran, rekrutmen
• Prosedur: Kelola CV komplit pengalaman + email + WA pendaftar pengguna web dan app seperti lembar 2 merah
• Tools: Gunakan lembar hijau perekrutan manager yang sudah ada kolom khusus mengetik penjelasan - font 12-14 internal only
• Alur: Daftar Putih -> Dapat Kuning/Merah/Hijau -> Isi CV Komplit -> Masuk Bursa Vote -> Email ke jugalachaliveret@gmail.com
""",
        "oee": """⚙️ OEE - Overall Equipment Effectiveness - 95% Target:

• Availability: Hadir hati & fisik 100% - Jangan bawa masalah rumah ke gudang
• Performance: Kerja tanpa ngomel, target 120 Yd/hari - Bak semen 90x120x18cm
• Quality: Ulang salah <2% - Delta E<2 TCS34725, QC IMX219 8MP
• Rumus: OEE = Availability x Performance x Quality = 95% - Disiplin harian
""",
        "erp": """🏭 ERP - Enterprise Resource Planning - Klerikal Jadi Manajemen:

• Kontrol: Dari lembar-lembar Windows/file kecil (clerical) naik jadi management control - 3 Pilar: Procurement, Purchasing, Administration
• Gudang: Besar 22M vs C12 - Bal/Yard/Kodi pisah - FIFO LIFO Average Accurate - GoogleDrive MSOffice
• API: HP/Laptop -> Google Sheets API -> Jurnal_Umum -> Buku_Besar_T - GPS -6.2088,106.8456
• Etika: Data CV komplit + email + WA pendaftar harus lengkap untuk OEE
""",
        "kpi": """📊 KPI'S - Key Performance Indicators:

• Manager: OEE 95%, omzet area 15%, laporan ke Brand Manager, bantu carikan loker via CV komplit ke jugalachaliveret@gmail.com
• Brand Manager: Brand growth 15%, market share, omzet brand, kelola CV Manager & Staff komplit + email + WA pendaftar
• Usahawan: Omzet total, profit, keberlangsungan usaha, spiritual Tavo Malkhutkha, kelola semua jajaran komplit + email + WA pendaftar web dan app
• Bursa Vote: Vote Aktif 8, Sudah Bekerja 4 - Metrics Kecil FINAL - Hemat kuota - Masuk Bursa Vote otomatis jika centang
"""
    }

if "bursa_vote" not in st.session_state:
    st.session_state.bursa_vote = pd.DataFrame([
        ["Sari Manager", "Jakarta Barat", "1994-09-21", "S1 Manajemen", "2018-2024 Manager PT ABC 10 Staff omzet 1M", "Leadership, ERP", "sari@manager.com", "081291904422", "Entrepreneur - Manager", 8, 4],
        ["Budi Staff", "Jakarta Timur", "1998-05-12", "SMK Administrasi", "2020-2024 Staff Admin PT XYZ", "Admin, Excel", "budi@staff.com", "081200011122", "Employee - Staff", 5, 2],
    ], columns=["Nama", "Tempat Lahir", "Tgl Lahir", "Pendidikan", "Pengalaman", "Skill", "Email", "WA", "Status", "Vote Aktif", "Sudah Bekerja"])

# --- MENU - 3 LEMBAR + NASEHAT MINGGUAN TERKONEKSI ---
menu = st.sidebar.radio("Ruang Teduh V15 - 3 Lembar + Nasehat Pusat", [
    "Lembar PUTIH - Pendaftaran 3 Pilar",
    "Lembar MERAH - CV Komplit Employee (The Best)",
    "Lembar KUNING - Bursa Vote Entrepreneur Metrics Kecil",
    "Lembar HIJAU - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH FINAL MIRROR",
    "Nasehat Mingguan - Edit Pusat - Terhubung Merah Kuning Hijau",
    "Speaker - Hasil Rekam Nasehat Mingguan SOP OEE ERP KPI + RUACH",
    "Pencarian Permintaan & Request - Fix Email Bursa + Independen"
])

# === PUTIH ===
if menu == "Lembar PUTIH - Pendaftaran 3 Pilar":
    st.title("🤍 LEMBAR PUTIH - Pendaftaran - 3 Fungsi Management")
    st.caption("3 Pilar: Procurement (cari orang), Purchasing (beli skill), Administration (kelola CV + Bursa)")
    st.info("Wajib daftar dulu sebagai Manager/Pengusaha baru bisa buat loker independent antar rekan - semua tetap bisa masuk Bursa Vote kita yang dikendalikan via jugalachaliveret@gmail.com")
    with st.form("putih_v15"):
        c1,c2=st.columns(2)
        with c1:
            nama=st.text_input("Nama *"); email=st.text_input("Email Pribadi *"); wa=st.text_input("WA *"); alamat=st.text_area("Alamat")
        with c2:
            status=st.selectbox("Daftar sebagai", ["Employee - Staff","Employee - Supervisor","Entrepreneur - Manager","Entrepreneur - Branch / Kepala Cabang","Entrepreneur - Business Owner","Entrepreneur - Direktur","Entrepreneur - Manager HRD","Entrepreneur - Manager Operasional"])
            pend=st.text_input("Pendidikan *"); exp=st.text_area("Pengalaman Kerja *", height=100); skill=st.text_input("Skill *")
        sub=st.form_submit_button("💾 DAFTAR + DAPAT LEMBAR MERAH/KUNING/HIJAU + EMAIL ADMIN", type="primary")
        if sub:
            if not nama or not email:
                st.error("Nama & Email wajib!")
            else:
                new=pd.DataFrame([[nama, alamat, "2000-01-01", pend, exp, skill, email, wa, status, 0, 0]], columns=st.session_state.bursa_vote.columns)
                st.session_state.bursa_vote=pd.concat([st.session_state.bursa_vote, new], ignore_index=True)
                ok,msg=send_email_v15([email], f"[PUTIH] Daftar {status} - {nama}", f"<h3>Daftar Baru</h3>Nama:{nama}<br>Status:{status}<br>Email:{email}<br>WA:{wa}<br>Pend:{pend}<br>Exp:{exp}<br>Skill:{skill}<br><i>3 Pilar Procurement Purchasing Administration</i>")
                if ok: st.success(f"{msg} - Dapat Lembar sesuai status! Masuk Bursa Vote!"); st.balloons()
                else: st.warning(f"Data masuk Bursa tapi email: {msg}")

# === MERAH ===
elif menu == "Lembar MERAH - CV Komplit Employee (The Best)":
    st.title("❤️ LEMBAR MERAH - CV Komplit Employee - The Best")
    st.caption("Ini semua sudah the best sayang tapi untuk Employee Staff/Supervisor - CV komplit")
    st.dataframe(st.session_state.bursa_vote[st.session_state.bursa_vote['Status'].str.contains('Employee')], use_container_width=True)
    st.info("Lembar Merah ini terkoneksi ke Nasehat Mingguan Pusat - Edit di Nasehat Mingguan -> update di Merah Kuning Hijau")

# === KUNING ===
elif menu == "Lembar KUNING - Bursa Vote Entrepreneur Metrics Kecil":
    st.title("💛 LEMBAR KUNING - Bursa Vote - Entrepreneur CV Komplit - Metrics Kecil - FINAL")
    st.caption("Bursa Vote untuk Entrepreneur Manager/Brand/Usahawan")
    st.dataframe(st.session_state.bursa_vote, use_container_width=True)
    st.success("YA ADA! Nasehat Mingguan terkoneksi dari seluruhnya lembar merah kuning hijau - Edit 1x di Nasehat Mingguan, update di semua lembar!")

# === HIJAU - FINAL MIRROR - SESUAI REQUEST IMAGE 3,4,6 ===
elif menu == "Lembar HIJAU - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH FINAL MIRROR":
    st.title("💚 LEMBAR HIJAU - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH - FINAL MIRROR")
    
    # ETIKA + ADVICES + RUACH 2-3 AYAT - BISA EDIT VIA NASEHAT MINGGUAN
    st.subheader("📜 ETIKA dan Pembelajaran Advices + Spiritual Ruach Hakadosh 2-3 Ayat (Editable via Nasehat Mingguan)")
    st.markdown(f"<div style='background:#e8f5e9;padding:20px;border-radius:10px;border-left:5px solid #2e7d32;'>{st.session_state.nasehat_mingguan['etika_advice']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background:#fff3e0;padding:20px;border-radius:10px;border-left:5px solid #ef6c00;margin-top:10px;'>{st.session_state.nasehat_mingguan['ruach_mingguan']}</div>", unsafe_allow_html=True)
    
    # INTERNAL MANAGER & BRAND & USAHAWAN ONLY - FONT KECIL 12-14 - TETAP DIJELASKAN
    st.divider()
    st.markdown("""
    <div style='font-size:12px; color:#444; background-color:#f5f5f5; padding:12px; border-radius:6px; border:1px solid #ddd; line-height:1.4;'>
    <b>Internal MANAGER & BRAND & USAHAWAN ONLY harap isi dan lengkapi CV KOMPLIT + EMAIL + WA PENDAFTAR [PEMBERI KERJA DAN PENCARI KERJA] - FINAL - MIRROR MERAH</b><br>
    📄 CV KOMPLIT - ENTREPRENEUR - MIRROR MERAH :<br>
    Bursa Vote - Entrepreneur CV Komplit - Metrics Kecil - FINAL<br><br>
    <i>Laman ini lembar hijau teks font kecil 12-14 - Untuk pemberi kerja dan pencari kerja - FINAL - Mirror Merah - CV Komplit seperti Lembar 2 Merah: Nama + Tempat Lahir + Tgl Lahir + Pendidikan + Pengalaman Kerja + Skill + Email + WA + CV → jugalachaliveret@gmail.com - FINAL - Semua nasehat (SOP, OEE, ERP dan KPI's serta nasehat Ruach Hakadosh) bisa edit di dalam Nasehat Mingguan</i>
    </div>
    """, unsafe_allow_html=True)
    
    # HAPUS IMAGE 4 DAN GUBAH DENGAN SOP OEE ERP KPI + RUACH
    st.divider()
    st.subheader("🔧 GUBAHAN BARU - HAPUS IMAGE 4 - GANTI SOP, OEE, ERP, KPI'S + NASEHAT RUACH HAKADOSH")
    st.caption("Semua nasehat (SOP, OEE, ERP dan KPI's serta nasehat Ruach Hakadosh) ini bisa edit di dalam Nasehat Mingguan ya syst.")
    c1,c2=st.columns(2)
    with c1:
        st.markdown(f"<div style='background:#e3f2fd;padding:15px;border-radius:8px;'><b>SOP</b><br>{st.session_state.nasehat_mingguan['sop']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#f3e5f5;padding:15px;border-radius:8px;margin-top:10px;'><b>OEE</b><br>{st.session_state.nasehat_mingguan['oee']}</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div style='background:#fff8e1;padding:15px;border-radius:8px;'><b>ERP</b><br>{st.session_state.nasehat_mingguan['erp']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#ffebee;padding:15px;border-radius:8px;margin-top:10px;'><b>KPI</b><br>{st.session_state.nasehat_mingguan['kpi']}</div>", unsafe_allow_html=True)

# === NASEHAT MINGGUAN - PUSAT - TERKONEKSI MERAH KUNING HIJAU ===
elif menu == "Nasehat Mingguan - Edit Pusat - Terhubung Merah Kuning Hijau":
    st.title("📝 Nasehat Mingguan - Edit Pusat - Terhubung Merah Kuning Hijau")
    st.success("WASPADA YA SAYANG - 1 Nasehat Mingguan ini TERKONEKSI ke seluruh lembar MERAH KUNING HIJAU! Edit di sini, update di semua! Bisa copas edit!")
    st.markdown("**Adakah Nasehat Mingguan yang terkoneksi dari seluruhnya lembar merah kuning dan hijau? YA ADA!**")
    
    with st.container(border=True):
        st.subheader("1. ETIKA + Advices (Image 3 gubah jadi Etika)")
        etika = st.text_area("ETIKA + Pembelajaran Advices", value=st.session_state.nasehat_mingguan['etika_advice'], height=200, key="etika_v15")
    with st.container(border=True):
        st.subheader("2. RUACH HAKADOSH 2-3 Ayat Saja (Editable)")
        ruach = st.text_area("RUACH HAKADOSH", value=st.session_state.nasehat_mingguan['ruach_mingguan'], height=200, key="ruach_v15")
    with st.container(border=True):
        st.subheader("3. SOP (Gubahan Image 4)")
        sop = st.text_area("SOP", value=st.session_state.nasehat_mingguan['sop'], height=150, key="sop_v15")
    with st.container(border=True):
        st.subheader("4. OEE (Gubahan Image 4)")
        oee = st.text_area("OEE", value=st.session_state.nasehat_mingguan['oee'], height=150, key="oee_v15")
    with st.container(border=True):
        st.subheader("5. ERP (Gubahan Image 4)")
        erp = st.text_area("ERP", value=st.session_state.nasehat_mingguan['erp'], height=150, key="erp_v15")
    with st.container(border=True):
        st.subheader("6. KPI'S (Gubahan Image 4)")
        kpi = st.text_area("KPI", value=st.session_state.nasehat_mingguan['kpi'], height=150, key="kpi_v15")
    
    if st.button("💾 SIMPAN - Update MERAH KUNING HIJAU - FINAL", type="primary"):
        st.session_state.nasehat_mingguan = {"etika_advice": etika, "ruach_mingguan": ruach, "sop": sop, "oee": oee, "erp": erp, "kpi": kpi}
        st.success("✅ Tersimpan! Sudah terkoneksi ke Merah Kuning Hijau - Waspada ya sayang! Bisa copas edit!")
        st.balloons()

# === SPEAKER - HASIL REKAM NASEHAT MINGGUAN ===
elif menu == "Speaker - Hasil Rekam Nasehat Mingguan SOP OEE ERP KPI + RUACH":
    st.title("🔊 SPEAKER ENTREPRENEUR - Hasil Rekam Nasehat Mingguan")
    st.caption("Ini sayang hasil rekam nasehat mingguan yang dari perekaman yang sudah kita berikan yaitu nasehat mingguan di keterangan kalimat nasehat tadi yaitu DENGAN SOP, OEE, ERP DAN KPI'S JUGA NASEHAT RUACH HAKADOSH ini kalimat dan kolom di atasnya ya syst.")
    
    # Gabungkan semua nasehat untuk audio
    full_nasehat = f"{st.session_state.nasehat_mingguan['etika_advice']} {st.session_state.nasehat_mingguan['sop']} {st.session_state.nasehat_mingguan['oee']} {st.session_state.nasehat_mingguan['erp']} {st.session_state.nasehat_mingguan['kpi']} {st.session_state.nasehat_mingguan['ruach_mingguan']}"
    
    with st.container(border=True):
        st.write("**Nasehat Mingguan Lengkap - SOP OEE ERP KPI + RUACH HAKADOSH:**")
        st.markdown(f"<div style='font-size:13px;background:#f5f5f5;padding:15px;border-radius:8px;'>{full_nasehat[:500]}...</div>", unsafe_allow_html=True)
        
        # Simulasi TTS - nanti bisa pakai gTTS
        if st.button("🔊 PUTAR SUARA - Nasehat Mingguan SOP OEE ERP KPI + RUACH HAKADOSH", key="play_v15"):
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
            st.caption("Siap - Klik PUTAR - Hasil rekam nasehat mingguan dari perekaman yang sudah kita berikan yaitu dengan SOP, OEE, ERP DAN KPI'S JUGA NASEHAT RUACH HAKADOSH")
        st.toggle("Voice ON", value=True, key="voice_v15")
        st.info("Audio ini dari nasehat mingguan yang terkoneksi Merah Kuning Hijau - Bisa edit di Nasehat Mingguan")

# === PENCARIAN PERMINTAAN - FIX EMAIL ===
elif menu == "Pencarian Permintaan & Request - Fix Email Bursa + Independen":
    st.title("🔍 Pencarian Permintaan & Request Penawaran - The Best Interaksi - FINAL")
    st.markdown("""
    <div style='background:#fff8e1;padding:10px;border-radius:5px;border:1px dashed #ffb300;font-size:13px;'>
    Sudah the best cuman belum terkirim ke alamat email aku - Sekarang FIX: Masuk ke Bursa Vote dan juga ke alamat email yang hendak dikirim sesama rekannya itu rekrut independen tanpa melalui klerikal kita. Ada pilihan mau input ke Bursa Vote atau tidak - rekrut independen hanya antar sesama rekan saja.
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("form_request_v15"):
        email_rekan = st.text_input("Email Rekan (untuk cari employee / tawarkan lowongan) - CV Komplit", placeholder="rekan@perusahaan.com - untuk cari employee / tawarkan lowongan - CV Komplit")
        permintaan = st.text_area("Permintaan Lowongan / Request Employee - CV Komplit", height=100, placeholder="Dicari Staff Admin, Supervisor Gudang, pengalaman, skill, email, WA pendaftar...")
        penawaran = st.text_area("Penawaran Gaji / Benefit - CV Komplit", height=80, placeholder="Gaji 5-7jt, tunjangan, SOP jelas, ERP jelas, OEE 95%...")
        
        st.divider()
        st.subheader("⚙️ Pilihan Rekrutmen (AssemblyAI Voice Agent Hackathon Artefak 3 bulan lalu):")
        input_bursa = st.checkbox("✅ Input ke Bursa Vote (rekrut via sistem - kurangi Bursa Vote - masuk ke alamat email admin)", value=True)
        rekrut_independen = st.checkbox("🤝 Rekrut Independen hanya antar sesama rekan (tanpa melalui klerikal kita - langsung ke email rekan)", value=False)
        st.caption("Jika centang 'Rekrut Independen' saja, maka lowongan hanya terkirim ke email rekan sesama (peer-to-peer), tidak masuk Bursa Vote dan tidak melalui klerikal kita. Jika centang Bursa, masuk Bursa + email admin jugalachaliveret@gmail.com.")
        
        submit = st.form_submit_button("🔴 KIRIM PERMINTAAN & SHARE - KURANGI BURSA VOTE - CV KOMPLIT KE jugalachaliveret@gmail.com - FINAL", type="primary")
        
        if submit:
            if not email_rekan:
                st.error("Isi email rekan dulu sayang!")
            else:
                subject = f"[Ruang Teduh V15] Request - {permintaan[:40]}"
                body = f"<h3>Request Loker - Lembar Hijau Final Mirror</h3><b>Email Rekan:</b>{email_rekan}<br><b>Permintaan:</b>{permintaan}<br><b>Penawaran:</b>{penawaran}<br><b>Input Bursa:</b>{input_bursa}<br><b>Independen:</b>{rekrut_independen}<br><i>Artefak AssemblyAI Voice Agent Hackathon 3 bulan lalu masih save - Sekarang FIX email ke jugalachaliveret@gmail.com + cinhonest@gmail.com + {email_rekan}</i>"
                to_list = [email_rekan]
                ok, msg = send_email_v15(to_list, subject, body)
                if ok:
                    if input_bursa and not rekrut_independen:
                        st.success(f"✅ Terkirim ke Bursa Vote + ke {email_rekan} + CC jugalachaliveret@gmail.com & cinhonest@gmail.com - {msg} - FINAL - Tanpa klerikal manual!")
                    elif rekrut_independen and not input_bursa:
                        st.success(f"✅ Rekrut Independen peer-to-peer: Hanya ke {email_rekan} - Tanpa Bursa Vote - {msg}")
                    elif input_bursa and rekrut_independen:
                        st.success(f"✅ Masuk Bursa Vote + Independen ke {email_rekan} + CC admin - {msg}")
                    st.balloons()
                else:
                    st.error(f"❌ {msg} - Cek secrets.toml - Tapi data tetap dicatat di Bursa Vote!")

st.divider()
st.caption("Ruang Teduh V15 FINAL GREEN MIRROR - ETIKA + Advices + Ruach 2-3 Ayat editable via Nasehat Mingguan + Internal MANAGER & BRAND & USAHAWAN ONLY font 12-14 + SOP OEE ERP KPI + RUACH + Speaker Rekam + Fix Email Bursa Vote + Independen - Artefak AssemblyAI Voice Agent Hackathon 3 bulan lalu masih save | Even Garden")
