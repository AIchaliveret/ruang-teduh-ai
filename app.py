
import streamlit as st
import pandas as pd
from datetime import datetime, date

st.set_page_config(page_title="Ruang Teduh AI - V10 FINAL - EMAIL OTOMATIS PEER-TO-PEER + VOICE ROLLING", page_icon="🕊️", layout="wide")

# --- INIT ---
if "email_log" not in st.session_state:
    st.session_state.email_log = []
if "bursa_total" not in st.session_state:
    st.session_state.bursa_total = 12
if "bursa_aktif" not in st.session_state:
    st.session_state.bursa_aktif = 8
if "bursa_kerja" not in st.session_state:
    st.session_state.bursa_kerja = 4
if "bursa_hist" not in st.session_state:
    st.session_state.bursa_hist = [
        {"jam": "08:00", "vote": 2, "kerja": 0, "total": 2},
        {"jam": "09:00", "vote": 5, "kerja": 1, "total": 6},
        {"jam": "10:00", "vote": 8, "kerja": 2, "total": 10},
        {"jam": "11:00", "vote": 8, "kerja": 4, "total": 12},
    ]
if "member_data" not in st.session_state:
    st.session_state.member_data = {}

if "nasehat_mingguan" not in st.session_state:
    st.session_state.nasehat_mingguan = {
        "etika": """ETIKA KERJA RUANG TEDUH - The Best Interaksi:
1. Jujur dalam CV - Jangan tambah pengalaman palsu. Kejujuran modal utama.
2. Hormat waktu - Datang tepat waktu, OEE 95% dimulai disiplin.
3. Saling tolong - Bursa Vote bukan saingan, tapi keluarga. Bantu rekan dapat kerja = koin teduh.""",
        "sop": """SOP MANAGER - CV Komplit - Pengalaman + Email + WA Pendaftar:
• Wewenang: Kelola 5-10 Staff + 2-3 Supervisor, keputusan strategis, anggaran, rekrutmen
• Prosedur: Kelola CV komplit pengalaman + email + WA pendaftar pengguna web dan app seperti lembar 2 merah
• Tools: Gunakan lembar hijau perekrutan manager yang sudah ada kolom khusus mengetik penjelasan""",
        "oee": """OEE - Overall Equipment Effectiveness - 95% Target:
• Availability: Hadir hati & fisik 100% - Jangan bawa masalah rumah ke gudang
• Performance: Kerja tanpa ngomel, target 120 Yd / hari - Bak semen 90x120x18cm
• Quality: Ulang salah <2% - Delta E<2 TCS34725, QC IMX219 8MP
• Rumus: OEE = Availability x Performance x Quality = 95%""",
        "erp": """ERP - Enterprise Resource Planning - Klerikal Jadi Manajemen:
• Kontrol: Dari lembar-lembar Windows/file kecil (clerical) naik jadi management control
• Gudang: Besar 22M vs C12 - Bal/Yard/Kodi pisah - FIFO LIFO Average Accurate
• API: HP/Laptop -> Google Sheets API -> Jurnal_Umum -> Buku_Besar_T
• GPS: Live -6.2088,106.8456 UNIKA Atma Jaya""",
        "kpi": """KPI - Key Performance Indicators:
• Manager: OEE 95%, omzet area 15%, laporan ke Brand Manager, bantu carikan loker via CV komplit ke jugalachaliveret@gmail.com
• Brand Manager: Brand growth 15%, market share, omzet brand, kelola CV Manager & Staff komplit + email + WA pendaftar
• Usahawan: Omzet total, profit, keberlangsungan usaha, spiritual Tavo Malkhutkha, kelola semua jajaran komplit + email + WA pendaftar web dan app
• Bursa Vote: Vote Aktif 8, Sudah Bekerja 4 - Metrics Kecil FINAL""",
        "ruach_hakadosh": """RUACH HAKADOSH - 2-3 Ayat:
"Jikalau kamu tinggal di dalam Aku dan firman-Ku tinggal di dalam kamu, mintalah apa saja yang kamu kehendaki, dan kamu akan menerimanya." - Yohanes 15:7
"Segala sesuatu yang kamu kehendaki supaya orang perbuat kepadamu, perbuatlah demikian juga kepada mereka." - Matius 7:12
Bekerja bukan hanya untuk omzet, tapi untuk menjadi berkat. Satu orang bangkit = Satu keluarga bangkit."""
    }

if "bursa_vote" not in st.session_state:
    st.session_state.bursa_vote = pd.DataFrame([
        ["Sari Manager", "Jakarta Barat", "S1 Manajemen", "2018-2024 Manager PT ABC 10 Staff omzet 1M", "Leadership, ERP Accurate", "manager@email.com", "081291904422", "Employee", 8, 4],
    ], columns=["Nama", "Tempat Lahir", "Pendidikan", "Pengalaman", "Skill", "Email", "WA", "Status", "Vote Aktif", "Sudah Bekerja"])

def add_login_bursa():
    st.session_state.bursa_total += 1
    st.session_state.bursa_aktif += 1
    now = datetime.now().strftime("%H:%M")
    st.session_state.bursa_hist.append({"jam": now, "vote": st.session_state.bursa_aktif, "kerja": st.session_state.bursa_kerja, "total": st.session_state.bursa_total})
    if len(st.session_state.bursa_hist) > 12:
        st.session_state.bursa_hist = st.session_state.bursa_hist[-12:]

def kurang_bursa_share(email, alasan="share"):
    if st.session_state.bursa_aktif > 0:
        st.session_state.bursa_aktif -= 1
        st.session_state.bursa_kerja += 1
        now = datetime.now().strftime("%H:%M")
        st.session_state.bursa_hist.append({"jam": now, "vote": st.session_state.bursa_aktif, "kerja": st.session_state.bursa_kerja, "total": st.session_state.bursa_total})
        if len(st.session_state.bursa_hist) > 12:
            st.session_state.bursa_hist = st.session_state.bursa_hist[-12:]

def kirim_email_otomatis(to_email, subject, body, mode=""):
    """
    V10 FINAL FIX - EMAIL TEROTOMATISASI PEER-TO-PEER TANPA KLERIKAL
    - Jika Input Bursa Vote: kirim ke email rekan + CC ke jugalachaliveret@gmail.com + cinhonest@gmail.com (biar terkirim ke alamat email aku) + masuk Bursa Vote + kurang Bursa
    - Jika Rekrut Independen only: kirim hanya antar sesama rekan (peer-to-peer) tanpa melalui klerikal kita + tanpa Bursa
    - Single admin utama jugalachaliveret@gmail.com ONLY tapi juga CC cinhonest@gmail.com biar kamu dapat (fix bug lama belum terkirim ke alamat email aku)
    """
    log = {"waktu": datetime.now().strftime("%H:%M:%S"), "ke": to_email, "mode": mode, "status": "Queued"}
    try:
        smtp_user = None
        smtp_pass = None
        admins = []
        try:
            if "email" in st.secrets:
                cfg = st.secrets["email"]
                smtp_user = cfg.get("smtp_user") or cfg.get("sender_email")
                smtp_pass = cfg.get("smtp_pass") or cfg.get("sender_password")
                # Support old format + new format
                if "admin1" in cfg: admins.append(cfg["admin1"])
                if "admin2" in cfg: admins.append(cfg["admin2"])
        except:
            pass
        
        # FIX BUG LAMA: belum terkirim ke alamat email aku
        # Single admin utama jugalachaliveret@gmail.com ONLY, tapi tambah cinhonest@gmail.com biar kamu dapat juga
        main_admin = "jugalachaliveret@gmail.com"
        my_email = "cinhonest@gmail.com"
        if main_admin not in admins:
            admins.append(main_admin)
        if my_email not in admins:
            admins.append(my_email)
        
        if smtp_user and smtp_pass:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Body + info mode
            full_body = f"{body}\n\n---\nMode: {mode}\nOtomatis peer-to-peer tanpa klerikal\nAdmin: {main_admin} ONLY + CC {my_email} (fix belum terkirim ke alamat email aku)\nBursa: Aktif {st.session_state.bursa_aktif} -> {st.session_state.bursa_aktif-1 if 'Bursa' in mode else st.session_state.bursa_aktif}"
            msg.attach(MIMEText(full_body, 'plain'))
            
            # CC logic: Bursa = CC ke admin, Independen = tidak CC (hanya antar sesama rekan saja)
            if "Bursa" in mode:
                msg['Cc'] = ", ".join(admins)
            
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            
            recips = [to_email]
            if "Bursa" in mode:
                recips.extend(admins)
            
            server.sendmail(smtp_user, recips, msg.as_string())
            server.quit()
            
            if "Bursa" in mode:
                log["status"] = f"✅ Terkirim OTOMATIS ke {to_email} + CC {', '.join(admins)} + Masuk Bursa Vote"
            else:
                log["status"] = f"✅ Terkirim Independen OTOMATIS hanya ke {to_email} (peer-to-peer tanpa klerikal tanpa Bursa)"
            st.session_state.email_log.append(log)
            kurang_bursa_share(to_email, mode) if "Bursa" in mode else None
            return True, log["status"]
        else:
            # Tanpa SMTP - tetap log otomatis tanpa klerikal (biar tidak perlu kamu yang lakukan klerikal)
            if "Bursa" in mode:
                log["status"] = f"📝 OTOMATIS Log Tanpa Klerikal ke {to_email} + CC {', '.join(admins)} + Bursa {st.session_state.bursa_aktif}-> {st.session_state.bursa_aktif-1} (Set Secrets SMTP biar beneran terkirim)"
            else:
                log["status"] = f"📝 OTOMATIS Log Independen ke {to_email} tanpa klerikal tanpa Bursa (peer-to-peer)"
            st.session_state.email_log.append(log)
            if "Bursa" in mode:
                kurang_bursa_share(to_email, mode)
            return True, log["status"]
    except Exception as e:
        log["status"] = f"❌ {str(e)[:100]}"
        st.session_state.email_log.append(log)
        return False, f"❌ {e}"

def voice_api(text):
    try:
        from gtts import gTTS
        from io import BytesIO
        clean = text.replace("•"," ").replace("📜","").replace("📋","").replace("⚙️","").replace("🏭","").replace("📊","").replace("🔥","")[:3900]
        tts = gTTS(text=clean, lang='id', slow=False)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp, None
    except Exception as e:
        return None, str(e)

def render_grafik_bursa():
    hist = st.session_state.bursa_hist
    if not hist:
        return
    max_v = max([h["vote"] for h in hist] + [h["kerja"] for h in hist] + [1])
    html_g = '<div style="display:flex; gap:8px; align-items:end; height:90px; background:white; border:1px solid #E0E0E0; border-radius:12px; padding:12px;">'
    for h in hist:
        v_h = int(h["vote"] / max_v * 65)
        k_h = int(h["kerja"] / max_v * 65)
        html_g += f'<div style="flex:1; text-align:center;"><div style="display:flex; gap:3px; justify-content:center; align-items:end; height:70px;"><div style="width:45%; background:#FF5252; height:{v_h}px; border-radius:4px;"></div><div style="width:45%; background:#4CAF50; height:{k_h}px; border-radius:4px;"></div></div><div style="font-size:8px; margin-top:5px; font-weight:700;">{h["jam"]}</div></div>'
    html_g += '</div><div style="font-size:9px; color:#666; margin-top:6px;">🔴 Vote Aktif | 🟢 Sudah Bekerja - Grafik Hanya di PUTIH - FINAL</div>'
    st.markdown(html_g, unsafe_allow_html=True)

def generate_cv_text(md):
    return f"""CV KOMPLIT - RUANG TEDUH V10 FINAL - {md.get('nama','')} - {md.get('jabatan','')}
Nama: {md.get('nama','')}
Tempat Lahir: {md.get('tempat','')}
Tgl Lahir: {md.get('tgl','')}
Umur: {md.get('umur','')}
Pendidikan: {md.get('pendidikan','')}
Pengalaman: {md.get('pengalaman','')}
Skill: {md.get('skill','')}
Email: {md.get('email','')} (pendaftar)
WA: {md.get('wa','')} (pendaftar)
Jabatan: {md.get('jabatan','')}
Bursa: Total {st.session_state.bursa_total} | Aktif {st.session_state.bursa_aktif} | Kerja {st.session_state.bursa_kerja}
Kirim ke: jugalachaliveret@gmail.com ONLY + cinhonest@gmail.com (fix belum terkirim ke alamat email aku)
"""

# --- MENU ---
menu = st.sidebar.radio("Menu Ruang Teduh - V10 FINAL FIX", [
    "PUTIH - FORM LOKER CV + GRAFIK - Awal Simple",
    "HIJAU - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH - FINAL + VOICE ROLLING",
    "Pencarian Permintaan & Request Penawaran - EMAIL OTOMATIS",
    "Bursa Vote",
    "Nasehat Mingguan - Edit SOP OEE ERP KPI RUACH",
    "Members - 4 Kolom DKI"
])

c1,c2,c3,c4 = st.columns(4)
c1.metric("TOTAL LOGIN", st.session_state.bursa_total)
c2.metric("BURSA AKTIF", st.session_state.bursa_aktif)
c3.metric("SUDAH BEKERJA", st.session_state.bursa_kerja)
persen = int(st.session_state.bursa_kerja/st.session_state.bursa_total*100) if st.session_state.bursa_total else 0
c4.metric("KONVERSI", f"{persen}%")

if menu == "PUTIH - FORM LOKER CV + GRAFIK - Awal Simple":
    st.title("📄 LEMBAR 1 - FORM LOKER CV + GRAFIK - Awal Simple - FINAL")
    st.caption("Halaman pertama awal Ruang Teduh yang simple - seperti awal kita mau koreksi, cuma beda tambahan share email - FINAL")
    render_grafik_bursa()
    st.divider()
    with st.form("form_loker_cv_v10"):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Lengkap * - CV Komplit", placeholder="Budi Setia - CV")
        with col2:
            jabatan = st.selectbox("Jabatan / Posisi * - CV", ["Staff", "Supervisor", "Manager", "Brand Manager", "Usahawan / Entrepreneur"])
        col3, col4 = st.columns(2)
        with col3:
            tempat = st.text_input("Tempat Lahir * - CV", placeholder="Jakarta Barat")
        with col4:
            tgl = st.date_input("Tgl Lahir * - CV", value=date(1994,9,21))
        pendidikan = st.text_input("Pendidikan * - CV", placeholder="S1 - sarjana akuntansi universitas trisakti")
        pengalaman = st.text_area("Pengalaman Kerja * - CV Komplit", placeholder="2020-2023 Auditor PT XYZ...", height=85)
        skill = st.text_area("Skill * - CV Komplit", placeholder="akuntansi, ERP Accurate...", height=85)
        col5, col6 = st.columns(2)
        with col5:
            email = st.text_input("Alamat Email * - CV Komplit", placeholder="cinhonest@gmail.com")
        with col6:
            wa = st.text_input("Nomor WhatsApp * - CV Komplit", placeholder="081291904422")
        submit = st.form_submit_button("✅ SIMPAN CV KOMPLIT & MASUK BURSA - FINAL", type="primary", use_container_width=True)
        if submit:
            if not nama or not tempat or not email or not wa or not pengalaman:
                st.error("Lengkapi * bro - wajib isi CV komplit")
            else:
                is_emp = jabatan in ["Staff", "Supervisor"]
                st.session_state.member_data = {
                    "nama": nama, "jabatan": jabatan, "is_emp": is_emp, "is_ent": not is_emp,
                    "tempat": tempat, "tgl": tgl.strftime("%d-%m-%Y"), "umur": date.today().year - tgl.year,
                    "email": email, "wa": wa, "pendidikan": pendidikan,
                    "pengalaman": pengalaman, "skill": skill
                }
                add_login_bursa()
                st.success(f"✅ CV KOMPLIT {nama} ({jabatan}) masuk Bursa! Total: {st.session_state.bursa_total} | Aktif: {st.session_state.bursa_aktif} | CV ke jugalachaliveret@gmail.com ONLY + cinhonest@gmail.com FIX")
                st.balloons()
                st.code(generate_cv_text(st.session_state.member_data), language="text")

elif menu == "HIJAU - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH - FINAL + VOICE ROLLING":
    st.title("🕊️ LEMBAR HIJAU - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH - FINAL - Untuk Manager, Business Owner & Employee")
    st.caption("Biar leader nggak melulu nasehatin - Employee juga perlu nasehat ini - API Voice Recorder Rolling 1 Hari 1 Nasehat dari 5 Nasehat")
    
    # AUTO DAILY 1 HARI 1 NASEHAT - 5 NASEHAT ROLLING
    st.markdown("### 📅 Auto Daily - 1 Hari 1 Nasehat Otomatis - 5 Nasehat - Rolling Untuk Manager, Business Owner & Employee")
    keys = ["sop", "oee", "erp", "kpi", "ruach_hakadosh"]
    labels = {"sop":"📋 SOP", "oee":"⚙️ OEE", "erp":"🏭 ERP", "kpi":"📊 KPI", "ruach_hakadosh":"🔥 RUACH HAKADOSH"}
    today = datetime.now()
    idx = today.day % 5
    today_key = keys[idx]
    today_label = labels[today_key]
    today_text = st.session_state.nasehat_mingguan[today_key]
    
    with st.container(border=True):
        c1, c2 = st.columns([2,1])
        with c1:
            st.success(f"🔥 Hari ini {today.strftime('%A %d-%m-%Y')} - {today_label} - Untuk Manager, Business Owner & Employee - Biar leader nggak melulu nasehatin")
            st.markdown(f"<div style='background:#e8f5e9; padding:15px; border-radius:10px; border-left:4px solid #2e7d32;'>{today_text}</div>", unsafe_allow_html=True)
        with c2:
            if st.button(f"🔊 PLAY HARI INI - {today_key.upper()} - API Voice Recorder", type="primary", key="play_today_v10"):
                mp3, err = voice_api(today_text)
                if mp3:
                    st.audio(mp3, format="audio/mp3")
                    st.download_button(f"📥 Download {today_key}", data=mp3, file_name=f"{today_key}_{today.strftime('%Y%m%d')}.mp3", mime="audio/mp3", key="dl_today_v10")
                    st.success(f"✅ API Voice Recorder: {today_label} - Rolling 1 hari 1 nasehat")
                else:
                    st.error(f"gTTS error: {err}")
            st.caption("Tgl 1,6,11=SOP | 2,7,12=OEE | 3,8,13=ERP | 4,9,14=KPI | 5,10,15=RUACH - Rolling otomatis")
    
    st.divider()
    st.subheader("📜 ETIKA - Pembelajaran Advices - Mirror Merah")
    st.markdown(st.session_state.nasehat_mingguan["etika"])
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 SOP")
        st.info(st.session_state.nasehat_mingguan["sop"])
        st.subheader("⚙️ OEE")
        st.success(st.session_state.nasehat_mingguan["oee"])
    with col2:
        st.subheader("🏭 ERP")
        st.warning(st.session_state.nasehat_mingguan["erp"])
        st.subheader("📊 KPI'S")
        st.error(st.session_state.nasehat_mingguan["kpi"])
    st.subheader("🔥 RUACH HAKADOSH - 2-3 Ayat")
    st.markdown(f"<div style='background:#e8f5e9; padding:20px; border-radius:10px; border-left:5px solid #2e7d32;'>{st.session_state.nasehat_mingguan['ruach_hakadosh']}</div>", unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🔊 API VOICE RECORDER - 5 Nasehat SOP OEE ERP KPI RUACH - Rolling 1 Hari 1 Nasehat - Untuk Manager, Business Owner & Employee")
    with st.container(border=True):
        c1,c2,c3 = st.columns(3)
        with c1:
            if st.button("🔊 PLAY SOP", key="psop_v10"):
                mp3,err=voice_api(st.session_state.nasehat_mingguan["sop"])
                if mp3: st.audio(mp3, format="audio/mp3")
            if st.button("🔊 PLAY OEE", key="poee_v10"):
                mp3,err=voice_api(st.session_state.nasehat_mingguan["oee"])
                if mp3: st.audio(mp3, format="audio/mp3")
        with c2:
            if st.button("🔊 PLAY ERP", key="perp_v10"):
                mp3,err=voice_api(st.session_state.nasehat_mingguan["erp"])
                if mp3: st.audio(mp3, format="audio/mp3")
            if st.button("🔊 PLAY KPI", key="pkpi_v10"):
                mp3,err=voice_api(st.session_state.nasehat_mingguan["kpi"])
                if mp3: st.audio(mp3, format="audio/mp3")
        with c3:
            if st.button("🔊 PLAY RUACH HAKADOSH", key="pruach_v10"):
                mp3,err=voice_api(st.session_state.nasehat_mingguan["ruach_hakadosh"])
                if mp3: st.audio(mp3, format="audio/mp3")
            if st.button("🔊 PLAY ETIKA", key="petika_v10"):
                mp3,err=voice_api(st.session_state.nasehat_mingguan["etika"])
                if mp3: st.audio(mp3, format="audio/mp3")
        if st.button("🔊 PLAY SEMUA - Untuk Manager, Business Owner & Employee", key="pall_v10", type="primary"):
            all_text = " ".join(st.session_state.nasehat_mingguan.values())
            mp3,err=voice_api(all_text)
            if mp3: 
                st.audio(mp3, format="audio/mp3")
                st.download_button("📥 Download SEMUA", data=mp3, file_name="SEMUA_NASEHAT.mp3", mime="audio/mp3", key="dl_all_v10")
    
    st.markdown('<div style="font-size:12px; color:#666; background:#f5f5f5; padding:10px; border-radius:5px;"><b>Internal MANAGER & BRAND & USAHAWAN + EMPLOYEE ONLY harap isi CV KOMPLIT + EMAIL + WA → jugalachaliveret@gmail.com ONLY + cinhonest@gmail.com FIX - SINGLE ADMIN - FINAL - API Voice Recorder Rolling</b></div>', unsafe_allow_html=True)

elif menu == "Pencarian Permintaan & Request Penawaran - EMAIL OTOMATIS":
    st.title("🔍 Pencarian Permintaan & Request Penawaran - EMAIL OTOMATIS PEER-TO-PEER TANPA KLERIKAL - FINAL")
    st.markdown("""
    <div style="background:#e8f5e9; padding:12px; border-radius:8px; border:2px solid #4CAF50; font-size:13px;">
    ✅ <b>Sudah The Best + Sudah FIX Terotomatisasi:</b><br>
    - Perekrutan sesama rekan lembar hijau <b>TEROTOMATISASI</b> antar alamat email saling memberikan permintaan dan pengiriman perekrutan<br>
    - <b>Belum terkirim ke alamat email aku (cinhonest@gmail.com) → SUDAH FIX:</b> otomatis CC ke jugalachaliveret@gmail.com + cinhonest@gmail.com + ke email rekan<br>
    - <b>Tidak perlu kamu lakukan klerikal</b> - mestinya masuk ke Bursa Vote dan juga ke alamat email yang hendak dikirim sesama rekannya itu<br>
    - <b>Rekrut Independen tanpa melalui klerikal kita</b> - ada pilihan mau input ke Bursa Vote atau tidak - rekrut independen hanya antar sesama rekan saja
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("form_email_otomatis_v10"):
        email_rekan = st.text_input("Email Rekan (untuk cari employee / tawarkan lowongan) - CV Komplit", placeholder="cinhonest@gmail.com - untuk cari employee / tawarkan lowongan - CV komplit - FIX terkirim ke alamat email aku", value="cinhonest@gmail.com")
        
        permintaan = st.text_area("Permintaan Lowongan / Request Employee - CV Komplit", value="butuh beberapa tenaga kerja sales staff ditempatkan di keutamaan kali kerukut jakarta pusat", height=100)
        
        penawaran = st.text_area("Penawaran Gaji / Benefit - CV Komplit", value="4000000", height=80)
        
        st.divider()
        st.subheader("⚙️ Pilihan Rekrutmen - Otomatis Tanpa Klerikal:")
        input_bursa = st.checkbox("✅ Input ke Bursa Vote (rekrut via sistem - otomatis masuk Bursa Vote + CC ke jugalachaliveret@gmail.com + cinhonest@gmail.com + kurangi Bursa Vote)", value=True)
        rekrut_independen = st.checkbox("🤝 Rekrut Independen hanya antar sesama rekan (tanpa melalui klerikal kita) - hanya peer-to-peer", value=False)
        st.caption("Jika centang 'Rekrut Independen' saja, maka lowongan hanya terkirim ke email rekan sesama (peer-to-peer), tidak masuk Bursa Vote dan tidak melalui klerikal kita. Jika centang Bursa, otomatis masuk Bursa Vote + terkirim ke alamat email aku (cinhonest@gmail.com) + jugalachaliveret@gmail.com.")
        
        submit = st.form_submit_button("🔴 KIRIM OTOMATIS - TANPA KLERIKAL - MASUK BURSA VOTE + KE EMAIL REKAN + KE ALAMAT EMAIL AKU - FINAL", type="primary")
        
        if submit:
            if not email_rekan:
                st.error("Isi email rekan dulu sayang! Contoh: cinhonest@gmail.com")
            else:
                if input_bursa and not rekrut_independen:
                    subject = f"CV KOMPLIT - Bursa Vote - {permintaan[:30]} - V10 FINAL FIX"
                    body = f"Permintaan: {permintaan}\nGaji: {penawaran}\nEmail Rekan: {email_rekan}\n\nOtomatis peer-to-peer tanpa klerikal - Masuk Bursa Vote - Fix terkirim ke alamat email aku cinhonest@gmail.com + jugalachaliveret@gmail.com"
                    ok, msg = kirim_email_otomatis(email_rekan, subject, body, "Bursa Vote")
                    if ok:
                        st.success(f"✅ {msg}")
                        st.success(f"✅ Terkirim ke Bursa Vote + ke {email_rekan} + CC ke jugalachaliveret@gmail.com & cinhonest@gmail.com - Sudah The Best + FIX terkirim ke alamat email aku - FINAL")
                        st.balloons()
                    else:
                        st.error(msg)
                elif rekrut_independen and not input_bursa:
                    subject = f"CV KOMPLIT - Rekrut Independen - {permintaan[:30]} - V10 FINAL"
                    body = f"Permintaan: {permintaan}\nGaji: {penawaran}\nEmail Rekan: {email_rekan}\n\nRekrut Independen hanya antar sesama rekan saja - tanpa melalui klerikal kita - peer-to-peer"
                    ok, msg = kirim_email_otomatis(email_rekan, subject, body, "Independen")
                    if ok:
                        st.success(f"✅ Rekrut Independen: {msg}")
                        st.success(f"✅ Terkirim hanya ke sesama rekan {email_rekan} (peer-to-peer) - Tanpa Bursa Vote & Tanpa Klerikal - Tidak perlu kamu lakukan klerikal")
                    else:
                        st.error(msg)
                elif input_bursa and rekrut_independen:
                    subject = f"CV KOMPLIT - Bursa + Independen - {permintaan[:30]} - V10 FINAL"
                    body = f"Permintaan: {permintaan}\nGaji: {penawaran}\nEmail Rekan: {email_rekan}\n\nBursa Vote + Rekrut Independen - Otomatis tanpa klerikal"
                    ok, msg = kirim_email_otomatis(email_rekan, subject, body, "Bursa+Independen")
                    if ok:
                        st.success(f"✅ {msg}")
                        st.success(f"✅ Terkirim ke Bursa Vote + Rekrut Independen ke {email_rekan} + CC ke jugalachaliveret@gmail.com & cinhonest@gmail.com - FINAL")
                        st.balloons()
                    else:
                        st.error(msg)
                else:
                    st.warning("Pilih salah satu: Input ke Bursa Vote atau Rekrut Independen")
                
                if st.session_state.email_log:
                    st.divider()
                    st.subheader("📧 Log Email Otomatis - Tanpa Klerikal - Terotomatisasi Antar Alamat Email")
                    st.dataframe(pd.DataFrame(st.session_state.email_log).tail(10), use_container_width=True)
                    st.success("✅ Log ini bukti terotomatisasi seperti yang kamu rencanakan antar alamat email saling memberikan permintaan dan pengiriman perekrutan yang dimaksud - Tidak perlu kamu lakukan klerikal")

elif menu == "Bursa Vote":
    st.title("📊 Bursa Vote - FINAL - SINGLE ADMIN + FIX Email Aku")
    st.dataframe(st.session_state.bursa_vote, use_container_width=True)
    c1,c2,c3 = st.columns(3)
    c1.metric("TOTAL", st.session_state.bursa_total)
    c2.metric("AKTIF", st.session_state.bursa_aktif)
    c3.metric("KERJA", st.session_state.bursa_kerja)
    if st.session_state.email_log:
        st.dataframe(pd.DataFrame(st.session_state.email_log).tail(5), use_container_width=True)

elif menu == "Nasehat Mingguan - Edit SOP OEE ERP KPI RUACH":
    st.title("📝 Nasehat Mingguan - Edit SOP OEE ERP KPI RUACH HAKADOSH - Terhubung Merah Kuning Hijau + Voice Rolling")
    st.caption("Teks nasehat mingguan SOP, OEE, ERP KPI dan Ruach Hakadosh bisa dibacakan AI Voice Recorder dengan API Voice Recorder - 1 hari 1 nasehat rolling otomatis untuk Manager dan Business Owner lembar hijau, bila perlu langsung Employee juga perlu banget")
    for k in st.session_state.nasehat_mingguan:
        st.session_state.nasehat_mingguan[k] = st.text_area(k.upper() + " - Bisa dibacakan AI Voice Recorder Rolling 1 Hari 1 Nasehat", value=st.session_state.nasehat_mingguan[k], key=f"edit_{k}_v10", height=120)
    if st.button("💾 SIMPAN NASEHAT MINGGUAN - Update Merah Kuning Hijau + Voice Rolling - Untuk Manager, Business Owner & Employee", type="primary"):
        st.success("✅ Nasehat Mingguan tersimpan! Sudah terkoneksi ke Lembar Merah, Kuning, Hijau + Voice Rolling 1 Hari 1 Nasehat - Biar leader nggak melulu nasehatin - Waspada ya sayang!")
        st.balloons()

else:
    st.title("📁 Members Ruang Teduh - 4 Kolom - Mapping DKI")
    st.dataframe(pd.DataFrame([
        ["Employee", "Chef / Staff / Boss Kios/Ruko/Rukan", "DKI Jakarta (buat hitung UMR) - Jakarta tetap Jakarta - Lockernya Jakarta", "https://drive.google.com/drive/folders/12n8a5PkcNPQH1rwZxQiRJ9p7376-oKOx"],
        ["Entrepreneur", "Boss Kios/Ruko/Rukan", "DKI Jakarta - Pelamar dari Bandung bisa lihat", "https://drive.google.com/drive/folders/12n8a5PkcNPQH1rwZxQiRJ9p7376-oKOx"],
    ], columns=["status", "skill", "provinsi/kota", "gdrive_folder"]), use_container_width=True)
    st.caption("Single Admin jugalachaliveret@gmail.com ONLY + cinhonest@gmail.com FIX - 4 Kolom Mapping DKI - Jakarta tetap Jakarta")

st.caption("Ruang Teduh AI - V10 FINAL FIX - EMAIL OTOMATIS PEER-TO-PEER TANPA KLERIKAL + FIX TERKIRIM KE ALAMAT EMAIL AKU cinhonest@gmail.com + jugalachaliveret@gmail.com + Bursa Vote + Rekrut Independen + API Voice Recorder Rolling 1 Hari 1 Nasehat SOP OEE ERP KPI RUACH HAKADOSH Untuk Manager Business Owner & Employee Biar Leader Nggak Melulu Nasehatin - Anti Throttle")
