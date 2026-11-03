
import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="Ruang Teduh AI - FINAL MIRROR - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH", page_icon="🕊️", layout="wide")

# --- INIT SESSION ---
if "email_log" not in st.session_state:
    st.session_state.email_log = []

if "nasehat_mingguan" not in st.session_state:
    st.session_state.nasehat_mingguan = {
        "etika": """ETIKA KERJA RUANG TEDUH - The Best Interaksi:
1. Jujur dalam CV - Jangan tambah pengalaman palsu. Kejujuran adalah modal utama.
2. Hormat waktu - Datang tepat waktu, OEE 95% dimulai dari disiplin.
3. Saling tolong - Bursa Vote bukan saingan, tapi keluarga. Bantu rekan dapat kerja = koin teduh.
""",
        "sop": """SOP MANAGER - CV Komplit - Pengalaman + Email + WA Pendaftar:
• Wewenang: Kelola 5-10 Staff + 2-3 Supervisor, keputusan strategis, anggaran, rekrutmen
• Prosedur: Kelola CV komplit pengalaman + email + WA pendaftar pengguna web dan app seperti lembar 2 merah
• Tools: Gunakan lembar hijau perekrutan manager yang sudah ada kolom khusus mengetik penjelasan
""",
        "oee": """OEE - Overall Equipment Effectiveness - 95% Target:
• Availability: Hadir hati & fisik 100% - Jangan bawa masalah rumah ke gudang
• Performance: Kerja tanpa ngomel, target 120 Yd / hari - Bak semen 90x120x18cm
• Quality: Ulang salah <2% - Delta E<2 TCS34725, QC IMX219 8MP
• Rumus: OEE = Availability x Performance x Quality = 95%
""",
        "erp": """ERP - Enterprise Resource Planning - Klerikal Jadi Manajemen:
• Kontrol: Dari lembar-lembar Windows/file kecil (clerical) naik jadi management control
• Gudang: Besar 22M vs C12 - Bal/Yard/Kodi pisah - FIFO LIFO Average Accurate
• API: HP/Laptop -> Google Sheets API -> Jurnal_Umum -> Buku_Besar_T
• GPS: Live -6.2088,106.8456 UNIKA Atma Jaya - Sopir Ahmad Subarjo Grand Max
""",
        "kpi": """KPI - Key Performance Indicators:
• Manager: OEE 95%, omzet area 15%, laporan ke Brand Manager, bantu carikan loker via CV komplit ke jugalachaliveret@gmail.com
• Brand Manager: Brand growth 15%, market share, omzet brand, kelola CV Manager & Staff komplit + email + WA pendaftar
• Usahawan: Omzet total, profit, keberlangsungan usaha, spiritual Tavo Malkhutkha, kelola semua jajaran komplit + email + WA pendaftar web dan app
• Bursa Vote: Vote Aktif 8, Sudah Bekerja 4 - Metrics Kecil FINAL - Hemat kuota
""",
        "ruach_hakadosh": """RUACH HAKADOSH - Nasihat Spiritual Mingguan - 2-3 Ayat:
"Jikalau kamu tinggal di dalam Aku dan firman-Ku tinggal di dalam kamu, mintalah apa saja yang kamu kehendaki, dan kamu akan menerimanya." - Yohanes 15:7

"Segala sesuatu yang kamu kehendaki supaya orang perbuat kepadamu, perbuatlah demikian juga kepada mereka." - Matius 7:12

Bekerja bukan hanya untuk omzet, tapi untuk menjadi berkat. Satu orang bangkit = Satu keluarga bangkit = Satu perusahaan bangkit.
"""
    }

if "bursa_vote" not in st.session_state:
    st.session_state.bursa_vote = pd.DataFrame([
        ["Sari Manager", "Jakarta Barat", "S1 Manajemen", "2018-2024 Manager PT ABC 10 Staff omzet 1M", "Leadership, ERP Accurate", "manager@email.com", "081291904422", "Employee", 8, 4],
    ], columns=["Nama", "Tempat Lahir", "Pendidikan", "Pengalaman", "Skill", "Email", "WA", "Status", "Vote Aktif", "Sudah Bekerja"])

# --- FUNGSI EMAIL OTOMATISASI STABLE (TIDAK CRASH) ---
def kirim_email_otomatis_stable(to_email, subject, body_text, mode=""):
    log_entry = {
        "waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "ke": to_email,
        "subject": subject,
        "mode": mode,
        "permintaan": body_text[:200],
        "status": "Queued"
    }
    try:
        # Cek secrets - jika tidak ada, langsung masuk log (tidak crash)
        has_secrets = False
        try:
            if "email" in st.secrets and "smtp_user" in st.secrets["email"]:
                has_secrets = True
        except:
            has_secrets = False
        
        if has_secrets:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            smtp_user = st.secrets["email"]["smtp_user"]
            smtp_pass = st.secrets["email"]["smtp_pass"]
            smtp_host = st.secrets["email"].get("smtp_host", "smtp.gmail.com")
            smtp_port = st.secrets["email"].get("smtp_port", 587)
            
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body_text, 'plain'))
            if "Bursa" in mode:
                msg['Cc'] = "jugalachaliveret@gmail.com, cinhonest@gmail.com"
            
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            recipients = [to_email]
            if "Bursa" in mode:
                recipients += ["jugalachaliveret@gmail.com", "cinhonest@gmail.com"]
            server.sendmail(smtp_user, recipients, msg.as_string())
            server.quit()
            log_entry["status"] = "✅ Terkirim Beneran via SMTP"
            st.session_state.email_log.append(log_entry)
            return True, "✅ Email terkirim beneran via SMTP!"
        else:
            log_entry["status"] = "📝 Otomatis - Masuk Log - Tanpa Klerikal (Setup SMTP untuk kirim Gmail beneran)"
            st.session_state.email_log.append(log_entry)
            return True, "📝 Otomatis - Masuk Log - Tanpa Klerikal (Setup SMTP di Secrets untuk kirim ke Gmail beneran)"
    except Exception as e:
        log_entry["status"] = f"❌ Gagal: {str(e)[:100]}"
        st.session_state.email_log.append(log_entry)
        return False, f"❌ Gagal kirim: {e}"

# --- FUNGSI API VOICE RECORDER STABLE ---
def api_voice_recorder_stable(text):
    try:
        from gtts import gTTS
        clean = text.replace("•"," ").replace("📜"," ").replace("📋"," ").replace("⚙️"," ").replace("🏭"," ").replace("📊"," ").replace("🔥"," ").replace("✅"," ").replace("🔊"," ").replace("🕊️"," ")[:3900]
        tts = gTTS(text=clean, lang='id', slow=False)
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return mp3_fp, None
    except Exception as e:
        return None, str(e)

# --- SIDEBAR ---
menu = st.sidebar.radio("Menu Ruang Teduh", [
    "Lembar Hijau - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH - FINAL",
    "Bursa Vote - Entrepreneur CV Komplit - Metrics Kecil - FINAL",
    "Pencarian Permintaan & Request Penawaran - The Best Interaksi - FINAL",
    "Nasehat Mingguan - Edit SOP OEE ERP KPI RUACH HAKADOSH",
    "Members Ruang Teduh - 4 Kolom Mapping DKI"
])

# === LEMBAR HIJAU - UNTUK MANAGER & BUSINESS OWNER + EMPLOYEE ===
if menu == "Lembar Hijau - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH - FINAL":
    st.title("🕊️ LEMBAR HIJAU - ETIKA & Pembelajaran & Spiritual RUACH HAKADOSH - FINAL")
    st.caption("Untuk Manager & Business Owner + Employee - Biar leader nggak melulu nasehatin - Employee juga dapat nasehat otomatis")
    
    # --- AUTO DAILY 1 HARI 1 NASEHAT DARI 5 NASEHAT ---
    st.markdown("### 📅 Auto Daily - 1 Hari 1 Nasehat Otomatis - Untuk Manager, Business Owner & Employee")
    nasehat_5_keys = ["sop", "oee", "erp", "kpi", "ruach_hakadosh"]
    nasehat_5_labels = {
        "sop": "📋 SOP - Standard Operating Procedure",
        "oee": "⚙️ OEE - Overall Equipment Effectiveness",
        "erp": "🏭 ERP - Enterprise Resource Planning",
        "kpi": "📊 KPI - Key Performance Indicators",
        "ruach_hakadosh": "🔥 RUACH HAKADOSH - Spiritual 2-3 Ayat"
    }
    today = datetime.now()
    day_idx = today.day % 5
    weekday_name = today.strftime("%A")
    today_key = nasehat_5_keys[day_idx]
    today_label = nasehat_5_labels[today_key]
    today_text = st.session_state.nasehat_mingguan[today_key]
    
    with st.container(border=True):
        col_auto1, col_auto2 = st.columns([2,1])
        with col_auto1:
            st.success(f"**Hari ini {weekday_name}, {today.strftime('%d-%m-%Y')} - Nasehat Otomatis: {today_label} - Untuk Manager, Business Owner & Employee**")
            st.markdown(f"<div style='background:#e8f5e9; padding:15px; border-radius:10px; border-left:4px solid #2e7d32;'>{today_text}</div>", unsafe_allow_html=True)
            st.caption("Rotasi 5 nasehat: SOP → OEE → ERP → KPI → RUACH → balik lagi - 1 hari 1 nasehat - Biar employee juga dengar, bukan cuma leader nasehatin")
        with col_auto2:
            st.markdown("**🔊 Auto Play Hari Ini**")
            st.caption(f"Untuk: Manager & Business Owner & Employee - Hari ini: {today_key.upper()}")
            if st.button(f"🔊 PLAY OTOMATIS HARI INI - {today_key.upper()}", key="play_auto_today", type="primary"):
                mp3, err = api_voice_recorder_stable(today_text)
                if mp3:
                    st.audio(mp3, format="audio/mp3")
                    st.download_button(f"📥 Download {today_key.upper()} Hari Ini", data=mp3, file_name=f"{today_key.upper()}_{today.strftime('%Y%m%d')}_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_auto_today")
                    st.success(f"✅ API Voice Recorder membacakan otomatis 1 hari 1 nasehat: {today_label} - Untuk Manager & Business Owner & Employee")
                else:
                    st.error(f"Gagal TTS: {err}. Cek requirements.txt gTTS")
            st.markdown("**Jadwal 5 Nasehat:**")
            st.caption("Tgl 1,6,11,16,21,26,31=SOP\nTgl 2,7,12,17,22,27=OEE\nTgl 3,8,13,18,23,28=ERP\nTgl 4,9,14,19,24,29=KPI\nTgl 5,10,15,20,25,30=RUACH")
    
    st.divider()
    # --- ETIKA & ADVICE UTAMA ---
    st.subheader("📜 ETIKA - Pembelajaran Advices - Mirror Merah")
    st.markdown(st.session_state.nasehat_mingguan["etika"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 SOP - Standard Operating Procedure")
        st.info(st.session_state.nasehat_mingguan["sop"])
        st.subheader("⚙️ OEE - Overall Equipment Effectiveness")
        st.success(st.session_state.nasehat_mingguan["oee"])
    with col2:
        st.subheader("🏭 ERP - Enterprise Resource Planning")
        st.warning(st.session_state.nasehat_mingguan["erp"])
        st.subheader("📊 KPI'S - Key Performance Indicators")
        st.error(st.session_state.nasehat_mingguan["kpi"])
    
    st.divider()
    st.subheader("🔥 RUACH HAKADOSH - 2-3 Ayat - Spiritual - Untuk Manager, Business Owner & Employee")
    st.markdown(f"""<div style="background-color:#e8f5e9; padding:20px; border-radius:10px; border-left:5px solid #2e7d32;">{st.session_state.nasehat_mingguan["ruach_hakadosh"]}</div>""", unsafe_allow_html=True)
    
    # --- API VOICE RECORDER - 5 NASEHAT BISA DIBACAKAN ---
    st.divider()
    st.subheader("🔊 API VOICE RECORDER - AI Membacakan 5 Nasehat SOP OEE ERP KPI RUACH - Untuk Manager, Business Owner & Employee")
    st.caption("Biar leader nggak melulu nasehatin - Employee juga dapat nasehat otomatis via voice")
    
    with st.container(border=True):
        st.info("🎙️ **API Voice Recorder** - Klik PLAY - AI bacakan SOP, OEE, ERP, KPI, RUACH HAKADOSH pakai suara Indonesia - 1 hari 1 nasehat otomatis rolling")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**📋 SOP**")
            if st.button("🔊 PLAY SOP", key="play_sop"):
                mp3, err = api_voice_recorder_stable(st.session_state.nasehat_mingguan["sop"])
                if mp3: 
                    st.audio(mp3, format="audio/mp3")
                    st.download_button("📥 Download SOP.mp3", data=mp3, file_name="SOP_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_sop")
                else: st.error(err)
            st.markdown("**⚙️ OEE**")
            if st.button("🔊 PLAY OEE", key="play_oee"):
                mp3, err = api_voice_recorder_stable(st.session_state.nasehat_mingguan["oee"])
                if mp3: 
                    st.audio(mp3, format="audio/mp3")
                    st.download_button("📥 Download OEE.mp3", data=mp3, file_name="OEE_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_oee")
                else: st.error(err)
        with col2:
            st.markdown("**🏭 ERP**")
            if st.button("🔊 PLAY ERP", key="play_erp"):
                mp3, err = api_voice_recorder_stable(st.session_state.nasehat_mingguan["erp"])
                if mp3: 
                    st.audio(mp3, format="audio/mp3")
                    st.download_button("📥 Download ERP.mp3", data=mp3, file_name="ERP_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_erp")
                else: st.error(err)
            st.markdown("**📊 KPI**")
            if st.button("🔊 PLAY KPI", key="play_kpi"):
                mp3, err = api_voice_recorder_stable(st.session_state.nasehat_mingguan["kpi"])
                if mp3: 
                    st.audio(mp3, format="audio/mp3")
                    st.download_button("📥 Download KPI.mp3", data=mp3, file_name="KPI_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_kpi")
                else: st.error(err)
        with col3:
            st.markdown("**🔥 RUACH HAKADOSH**")
            if st.button("🔊 PLAY RUACH HAKADOSH", key="play_ruach"):
                mp3, err = api_voice_recorder_stable(st.session_state.nasehat_mingguan["ruach_hakadosh"])
                if mp3: 
                    st.audio(mp3, format="audio/mp3")
                    st.download_button("📥 Download RUACH.mp3", data=mp3, file_name="RUACH_HAKADOSH_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_ruach")
                else: st.error(err)
            st.markdown("**📜 ETIKA**")
            if st.button("🔊 PLAY ETIKA", key="play_etika"):
                mp3, err = api_voice_recorder_stable(st.session_state.nasehat_mingguan["etika"])
                if mp3: 
                    st.audio(mp3, format="audio/mp3")
                    st.download_button("📥 Download ETIKA.mp3", data=mp3, file_name="ETIKA_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_etika")
                else: st.error(err)
        st.divider()
        st.markdown("**🎧 PLAY SEMUA - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH - Untuk Manager, Business Owner & Employee**")
        teks_semua = f"{st.session_state.nasehat_mingguan['etika']} . {st.session_state.nasehat_mingguan['sop']} . {st.session_state.nasehat_mingguan['oee']} . {st.session_state.nasehat_mingguan['erp']} . {st.session_state.nasehat_mingguan['kpi']} . {st.session_state.nasehat_mingguan['ruach_hakadosh']}"
        if st.button("🔊 PLAY SEMUA - API Voice Recorder - Untuk Semua", key="play_semua", type="primary"):
            mp3, err = api_voice_recorder_stable(teks_semua)
            if mp3:
                st.audio(mp3, format="audio/mp3")
                st.success("✅ API Voice Recorder membacakan SEMUA - Untuk Manager, Business Owner & Employee!")
                st.download_button("📥 Download SEMUA.mp3", data=mp3, file_name="NASEHAT_MINGGUAN_LENGKAP_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_semua")
            else:
                st.error(f"Gagal TTS: {err}")
        st.toggle("Voice ON - API Voice Recorder Active", value=True, key="voice_on_api")
        st.caption("Siap - Klik PLAY per nasehat - DENGAN SOP, OEE, ERP DAN KPI'S JUGA NASEHAT RUACH HAKADOSH - Untuk Manager, Business Owner & Employee - Biar leader nggak melulu nasehatin - Employee juga dapat nasehat")

    # --- TEKS KECIL FONT 12-14 - INTERNAL MANAGER & BRAND & USAHAWAN ONLY ---
    st.divider()
    st.markdown("""
    <div style="font-size:12px; color:#666; background-color:#f5f5f5; padding:10px; border-radius:5px;">
    <b>Internal MANAGER & BRAND & USAHAWAN ONLY + EMPLOYEE harap isi dan lengkapi CV KOMPLIT + EMAIL + WA PENDAFTAR [PEMBERI KERJA DAN PENCARI KERJA] - FINAL - MIRROR MERAH</b><br>
    📄 CV KOMPLIT - ENTREPRENEUR - MIRROR MERAH : Bursa Vote - Entrepreneur CV Komplit - Metrics Kecil - FINAL<br>
    <i>Laman ini lembar hijau teks font kecil 12-14 - Untuk pemberi kerja dan pencari kerja - FINAL - Mirror Merah - CV Komplit seperti Lembar 2 Merah: Nama + Tempat Lahir + Tgl Lahir + Pendidikan + Pengalaman Kerja + Skill + Email + WA + CV → jugalachaliveret@gmail.com - FINAL - Untuk Manager, Business Owner & Employee</i>
    </div>
    """, unsafe_allow_html=True)

elif menu == "Bursa Vote - Entrepreneur CV Komplit - Metrics Kecil - FINAL":
    st.title("📊 Bursa Vote - Entrepreneur CV Komplit - Metrics Kecil - FINAL")
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader("KELOLA MANAGER & BRAND & USAHAWAN ONLY - CV KOMPLIT + EMAIL + WA PENDAFTAR - FINAL - MIRROR MERAH")
        st.dataframe(st.session_state.bursa_vote, use_container_width=True)
    with col2:
        st.metric("Vote Aktif", "8")
        st.metric("Sudah Bekerja", "4")
        st.caption("Grafik hanya ada 1 di Lembar 1 Putih Pendaftaran - di sini metrics kecil aja - FINAL - Mirror Employee - Hemat kuota")
        with st.container(border=True):
            st.markdown("✅ **Kolom Kejujuran Update - CV Komplit - FINAL**")
            st.write("Centang jika sudah dapat employee - Amsal 12:22")

elif menu == "Pencarian Permintaan & Request Penawaran - The Best Interaksi - FINAL":
    st.title("🔍 Pencarian Permintaan & Request Penawaran Entrepreneur - CV Komplit - FINAL - Mirror Employee - The Best Interaksi")
    st.markdown("""
    <div style="background-color:#fff8e1; padding:10px; border-radius:5px; border:1px dashed #ffb300; font-size:13px;">
    Sebagai Pencari Employee - CV Komplit: Share lowongan via email ke rekan, bursa otomatis berkurang. Sama kayak Employee tapi untuk cari employee. CV komplit pengalaman + email + WA pendaftar web dan app ke jugalachaliveret@gmail.com - FINAL - Untuk Manager, Business Owner & Employee - Otomatis Tanpa Klerikal
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("form_permintaan"):
        st.subheader("Share lowongan via Email ke rekan - CV Komplit:")
        email_rekan = st.text_input("Email Rekan (untuk cari employee / tawarkan lowongan) - CV Komplit", placeholder="rekan@perusahaan.com - untuk cari employee / tawarkan lowongan - CV Komplit")
        st.subheader("Permintaan Lowongan / Request Employee - CV Komplit:")
        permintaan = st.text_area("Dicari Staff Admin, Supervisor Gudang, pengalaman ..., skill ..., email, WA pendaftar...", height=100)
        st.subheader("Penawaran Gaji / Benefit - CV Komplit:")
        penawaran = st.text_area("Gaji 5-7jt, tunjangan, SOP jelas, ERP jelas 9, OEE 95%...", height=80)
        st.divider()
        st.subheader("⚙️ Pilihan Rekrutmen - Untuk Manager & Business Owner:")
        input_bursa = st.checkbox("✅ Input ke Bursa Vote (rekrut via sistem - kurangi Bursa Vote - CC ke jugalachaliveret@gmail.com & cinhonest@gmail.com)", value=True)
        rekrut_independen = st.checkbox("🤝 Rekrut Independen hanya antar sesama rekan (tanpa melalui klerikal kita - peer-to-peer)", value=False)
        st.caption("Jika centang 'Rekrut Independen' saja, maka lowongan hanya terkirim ke email rekan sesama (peer-to-peer), tidak masuk Bursa Vote dan tidak melalui klerikal kita. Jika centang Bursa, masuk Bursa + CC ke admin - otomatis tanpa klerikal.")
        submit = st.form_submit_button("🔴 KIRIM PERMINTAAN & SHARE - KURANGI BURSA VOTE - CV KOMPLIT KE jugalachaliveret@gmail.com - FINAL", type="primary")
        
        if submit:
            if not email_rekan:
                st.error("Isi email rekan dulu sayang!")
            else:
                subject = f"CV KOMPLIT - Permintaan Lowongan - {permintaan[:30]} - Ruang Teduh V7.5 FINAL"
                body_email = f"""
CV KOMPLIT - RUANG TEDUH V7.5 FINAL DUAL ADMIN
========================================
Share lowongan via Email ke rekan - CV Komplit: {email_rekan}
Permintaan Lowongan / Request Employee - CV Komplit: {permintaan}
Penawaran Gaji / Benefit - CV Komplit: {penawaran}
Mode: {'Bursa Vote + Peer-to-Peer' if input_bursa and rekrut_independen else 'Bursa Vote' if input_bursa else 'Rekrut Independen Peer-to-Peer Tanpa Klerikal'}
Waktu: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}
Pengirim: Manager/Business Owner - Bursa Vote System
CC: jugalachaliveret@gmail.com, cinhonest@gmail.com (jika mode Bursa)
Bursa: Total {len(st.session_state.bursa_vote)} | Aktif 8 | Kerja 4
========================================
ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH ada di app - Untuk Manager, Business Owner & Employee
"""
                if input_bursa and not rekrut_independen:
                    ok, msg = kirim_email_otomatis_stable(email_rekan, subject, body_email, mode="Bursa Vote")
                    if ok:
                        st.success(f"✅ Terkirim ke {email_rekan}! Bursa Vote: Aktif - CV komplit tetap ke jugalachaliveret@gmail.com & cinhonest@gmail.com - {msg}")
                        st.balloons()
                    else:
                        st.error(msg)
                elif rekrut_independen and not input_bursa:
                    ok, msg = kirim_email_otomatis_stable(email_rekan, subject, body_email, mode="Rekrut Independen Tanpa Klerikal")
                    if ok:
                        st.success(f"✅ Rekrut Independen: Terkirim hanya ke sesama rekan {email_rekan} (peer-to-peer) - Tanpa Bursa Vote & Tanpa Klerikal - {msg}")
                        st.info("📧 Ini rekrut independen hanya antar sesama rekan saja - tidak masuk Bursa Vote - tidak lewat admin - otomatis tanpa klerikal")
                    else:
                        st.error(msg)
                elif input_bursa and rekrut_independen:
                    ok1, msg1 = kirim_email_otomatis_stable(email_rekan, subject, body_email, mode="Bursa Vote + Independen")
                    if ok1:
                        st.success(f"✅ Terkirim ke Bursa Vote + Rekrut Independen ke {email_rekan} + CC ke jugalachaliveret@gmail.com & cinhonest@gmail.com - {msg1}")
                        st.balloons()
                    else:
                        st.error(msg1)
                else:
                    st.warning("⚠️ Pilih salah satu: Input ke Bursa Vote atau Rekrut Independen")
                
                if st.session_state.email_log:
                    st.divider()
                    st.subheader("📧 Log Email Otomatisasi - Tanpa Klerikal - Peer-to-Peer - Untuk Manager & Business Owner")
                    st.dataframe(pd.DataFrame(st.session_state.email_log).tail(10), use_container_width=True)
                    st.caption("Bukti antar alamat email saling memberikan permintaan dan pengiriman perekrutan - otomatis tanpa klerikal kita - masuk Bursa Vote + ke email rekan")
                
                if True:
                    with st.expander("🔧 Cara Setup Email Otomatis Beneran (biar kekirim ke inbox cinhonest@gmail.com beneran)", expanded=False):
                        st.markdown("""
                        **Biar email beneran masuk inbox, bukan cuma log:**
                        1. Di Streamlit Cloud dashboard → App → Settings → Secrets
                        2. Paste ini:
                        ```toml
                        [email]
                        smtp_user = "jugalachaliveret@gmail.com"
                        smtp_pass = "app_password_gmail_16_karakter"
                        smtp_host = "smtp.gmail.com"
                        smtp_port = 587
                        ```
                        3. Dapatkan app_password: myaccount.google.com → Security → 2-Step → App Passwords
                        4. Save → Reboot App → Test lagi - sekarang email beneran kekirim ke cinhonest@gmail.com!
                        **Sementara ini (tanpa secrets):** Email masuk Log di atas sebagai bukti otomatisasi tanpa klerikal - sudah terotomatisasi antar alamat email, tinggal aktifkan SMTP biar masuk Gmail beneran.
                        """)

elif menu == "Nasehat Mingguan - Edit SOP OEE ERP KPI RUACH HAKADOSH":
    st.title("📝 Nasehat Mingguan - Edit SOP OEE ERP KPI + RUACH HAKADOSH - Terhubung Merah Kuning Hijau")
    st.caption("Semua nasehat (SOP, OEE, ERP dan KPI's serta nasehat Ruach HaKadosh) ini bisa edit di dalam nasehat mingguan ya syst. Koneksi: Lembar Merah + Kuning + Hijau = 1 Nasehat Mingguan - Untuk Manager, Business Owner & Employee")
    st.success("YA ADA! 1 Nasehat Mingguan ini terkoneksi ke 3 lembar: Merah (CV Komplit), Kuning (Bursa Vote), Hijau (Manager/Brand/Usahawan/Employee). Edit di sini, update di semua! Biar leader nggak melulu nasehatin - Employee juga dapat nasehat!")
    with st.container(border=True):
        st.subheader("Edit ETIKA")
        etika = st.text_area("ETIKA - Pembelajaran Advices", value=st.session_state.nasehat_mingguan["etika"], height=150, key="edit_etika")
    with st.container(border=True):
        st.subheader("Edit SOP")
        sop = st.text_area("SOP - Manager Brand Usahawan", value=st.session_state.nasehat_mingguan["sop"], height=120, key="edit_sop")
    with st.container(border=True):
        st.subheader("Edit OEE")
        oee = st.text_area("OEE - Overall Equipment Effectiveness", value=st.session_state.nasehat_mingguan["oee"], height=120, key="edit_oee")
    with st.container(border=True):
        st.subheader("Edit ERP")
        erp = st.text_area("ERP - Enterprise Resource Planning", value=st.session_state.nasehat_mingguan["erp"], height=120, key="edit_erp")
    with st.container(border=True):
        st.subheader("Edit KPI'S")
        kpi = st.text_area("KPI - Key Performance Indicators", value=st.session_state.nasehat_mingguan["kpi"], height=150, key="edit_kpi")
    with st.container(border=True):
        st.subheader("Edit RUACH HAKADOSH - 2-3 Ayat")
        ruach = st.text_area("RUACH HAKADOSH - Spiritual", value=st.session_state.nasehat_mingguan["ruach_hakadosh"], height=200, key="edit_ruach")
    if st.button("💾 SIMPAN NASEHAT MINGGUAN - Update Merah Kuning Hijau - Untuk Manager, Business Owner & Employee", type="primary"):
        st.session_state.nasehat_mingguan = {"etika": etika, "sop": sop, "oee": oee, "erp": erp, "kpi": kpi, "ruach_hakadosh": ruach}
        st.success("✅ Nasehat Mingguan tersimpan! Sudah terkoneksi ke Lembar Merah, Kuning, Hijau - Untuk Manager, Business Owner & Employee - Waspada ya sayang!")
        st.balloons()

elif menu == "Members Ruang Teduh - 4 Kolom Mapping DKI":
    st.title("📁 Members Ruang Teduh - 4 Kolom - Mapping DKI")
    st.dataframe(pd.DataFrame([
        ["Employee", "Chef / Staff / Boss Kios/Ruko/Rukan", "DKI Jakarta (buat hitung UMR) - Jakarta tetap Jakarta", "https://drive.google.com/drive/folders/12n8a5PkcNPQH1rwZxQiRJ9p7376-oKOx"],
        ["Entrepreneur", "Boss Kios/Ruko/Rukan", "DKI Jakarta - Pelamar dari Bandung bisa lihat", "https://drive.google.com/drive/folders/12n8a5PkcNPQH1rwZxQiRJ9p7376-oKOx"],
    ], columns=["status", "skill", "provinsi/kota", "gdrive_folder"]), use_container_width=True)
    st.caption("Untuk Manager, Business Owner & Employee - 4 kolom mapping DKI - tanpa detail tambahan")
