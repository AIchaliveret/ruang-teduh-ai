import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import BytesIO

st.set_page_config(page_title="Ruang Teduh AI - FINAL MIRROR - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH", page_icon="🕊️", layout="wide")

# --- FUNGSI EMAIL OTOMATISASI TANPA KLERIKAL ---
def kirim_email_otomatis(to_email, subject, body_text, mode=""):
    """Kirim email beneran via SMTP jika secrets ada, fallback log jika tidak"""
    # Simpan ke log bursa untuk audit
    if "email_log" not in st.session_state:
        st.session_state.email_log = []
    
    log_entry = {
        "waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "ke": to_email,
        "subject": subject,
        "mode": mode,
        "permintaan": body_text[:200],
        "status": "Queued"
    }
    
    try:
        # Cek apakah ada secrets email di Streamlit Cloud
        if "email" in st.secrets and "smtp_user" in st.secrets["email"]:
            smtp_user = st.secrets["email"]["smtp_user"]
            smtp_pass = st.secrets["email"]["smtp_pass"]
            smtp_host = st.secrets["email"].get("smtp_host", "smtp.gmail.com")
            smtp_port = st.secrets["email"].get("smtp_port", 587)
            
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body_text, 'plain'))
            
            # CC ke admin jika mode Bursa
            if "Bursa" in mode:
                msg['Cc'] = "jugalachaliveret@gmail.com, cinhonest@gmail.com"
            
            server = smtplib.SMTP(smtp_host, smtp_port)
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
            # Fallback: Simulasi tapi masuk log + tampilkan cara setup
            log_entry["status"] = "📝 Simulasi (Secrets belum di-set)"
            st.session_state.email_log.append(log_entry)
            return True, "📝 Simulasi terkirim (masuk log) - Setup SMTP di Streamlit Secrets untuk kirim beneran"
    except Exception as e:
        log_entry["status"] = f"❌ Gagal: {str(e)[:100]}"
        st.session_state.email_log.append(log_entry)
        return False, f"❌ Gagal kirim: {e}"

# Init email_log
if "email_log" not in st.session_state:
    st.session_state.email_log = []

# --- INIT NASEHAT MINGGUAN (Editable) ---
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

# --- SIDEBAR ---
menu = st.sidebar.radio("Menu Ruang Teduh", [
    "Lembar Hijau - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH - FINAL",
    "Bursa Vote - Entrepreneur CV Komplit - Metrics Kecil - FINAL",
    "Pencarian Permintaan & Request Penawaran - The Best Interaksi - FINAL",
    "Nasehat Mingguan - Edit SOP OEE ERP KPI RUACH HAKADOSH",
    "Members Ruang Teduh - 4 Kolom Mapping DKI"
])

# === LEMBAR HIJAU - EDITED SESUAI REQUEST ===
if menu == "Lembar Hijau - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH - FINAL":
    st.title("🕊️ LEMBAR HIJAU - ETIKA & Pembelajaran & Spiritual RUACH HAKADOSH - FINAL")
    
    # --- AUTO DAILY 1 HARI 1 NASEHAT DARI 5 NASEHAT - SOP OEE ERP KPI RUACH ---
    st.markdown("### 📅 Auto Daily - 1 Hari 1 Nasehat Otomatis")
    # 5 nasehat: SOP, OEE, ERP, KPI, RUACH HAKADOSH - rotating per hari
    nasehat_5_keys = ["sop", "oee", "erp", "kpi", "ruach_hakadosh"]
    nasehat_5_labels = {
        "sop": "📋 SOP - Standard Operating Procedure",
        "oee": "⚙️ OEE - Overall Equipment Effectiveness",
        "erp": "🏭 ERP - Enterprise Resource Planning",
        "kpi": "📊 KPI - Key Performance Indicators",
        "ruach_hakadosh": "🔥 RUACH HAKADOSH - Spiritual 2-3 Ayat"
    }
    # Hitung hari ini - 1 hari 1 nasehat otomatis
    today = datetime.now()
    day_idx = today.day % 5  # 0-4 rotating setiap tanggal
    weekday_name = today.strftime("%A")
    today_key = nasehat_5_keys[day_idx]
    today_label = nasehat_5_labels[today_key]
    today_text = st.session_state.nasehat_mingguan[today_key]
    
    with st.container(border=True):
        col_auto1, col_auto2 = st.columns([2,1])
        with col_auto1:
            st.success(f"**Hari ini {weekday_name}, {today.strftime('%d-%m-%Y')} - Nasehat Otomatis: {today_label}**")
            st.markdown(f"<div style='background:#e8f5e9; padding:15px; border-radius:10px; border-left:4px solid #2e7d32;'>{today_text}</div>", unsafe_allow_html=True)
            st.caption(f"Rotasi otomatis 5 nasehat: SOP → OEE → ERP → KPI → RUACH → balik lagi - 1 hari 1 nasehat")
        with col_auto2:
            # API Voice Recorder Otomatis Hari Ini
            def api_voice_daily(text):
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
            
            st.markdown("**🔊 Auto Play Hari Ini**")
            if st.button(f"🔊 PLAY OTOMATIS HARI INI - {today_key.upper()}", key="play_auto_today", type="primary"):
                mp3, err = api_voice_daily(today_text)
                if mp3:
                    st.audio(mp3, format="audio/mp3")
                    st.download_button(f"📥 Download {today_key.upper()} Hari Ini", data=mp3, file_name=f"{today_key.upper()}_{today.strftime('%Y%m%d')}_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_auto_today")
                    st.success(f"✅ API Voice Recorder membacakan otomatis 1 hari 1 nasehat: {today_label}")
                else:
                    st.error(err)
            else:
                # Preview auto play - generate saat load (auto)
                try:
                    mp3_preview, _ = api_voice_daily(today_text[:500])
                    if mp3_preview:
                        st.audio(mp3_preview, format="audio/mp3")
                        st.caption("🔊 Preview otomatis hari ini - klik PLAY di atas untuk full")
                except:
                    pass
            
            st.markdown("**Jadwal Rotasi 5 Nasehat:**")
            st.caption("Tgl 1,6,11,16,21,26,31 = SOP\nTgl 2,7,12,17,22,27 = OEE\nTgl 3,8,13,18,23,28 = ERP\nTgl 4,9,14,19,24,29 = KPI\nTgl 5,10,15,20,25,30 = RUACH")
    
    st.divider()
    # --- ETIKA & ADVICE UTAMA (BISA DIEDIT VIA NASEHAT MINGGUAN) ---
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
    st.subheader("🔥 RUACH HAKADOSH - 2-3 Ayat - Spiritual")
    st.markdown(f"""
    <div style="background-color:#e8f5e9; padding:20px; border-radius:10px; border-left:5px solid #2e7d32;">
    {st.session_state.nasehat_mingguan["ruach_hakadosh"]}
    </div>
    """, unsafe_allow_html=True)
    
    # --- SPEAKER ENTREPRENEUR - API VOICE RECORDER - BISA BACAKAN PER NASEHAT ---
    st.divider()
    st.subheader("🔊 API VOICE RECORDER - AI Membacakan Nasehat Mingguan SOP OEE ERP KPI RUACH HAKADOSH - TII System")
    
    # Fungsi API Voice Recorder - gTTS Indonesia
    def api_voice_recorder(text, filename, lang='id'):
        """API Voice Recorder - gTTS Indonesia - Bersihkan simbol"""
        try:
            from gtts import gTTS
            clean = text.replace("•"," ").replace("📜"," ").replace("📋"," ").replace("⚙️"," ").replace("🏭"," ").replace("📊"," ").replace("🔥"," ").replace("✅"," ").replace("🔊"," ").replace("🕊️"," ")[:3900]
            tts = gTTS(text=clean, lang=lang, slow=False)
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            return mp3_fp, None
        except Exception as e:
            return None, str(e)
    
    with st.container(border=True):
        st.write("CV Komplit Entrepreneur Contoh Sari Manager jabatan Manager tempat lahir Jakarta Barat tanggal lahir 21-09-1994 pendidikan S1 Manajemen pengalaman kerja 2018-2024 Manager...")
        st.info("🎙️ **API Voice Recorder** - Pilih nasehat mingguan di bawah, klik PLAY - AI akan bacakan SOP, OEE, ERP, KPI, RUACH HAKADOSH pakai suara Indonesia - Sesuai screenshot fdd300")
        
        # 6 Tombol PLAY terpisah - sesuai permintaan sayang
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**📜 ETIKA**")
            st.caption(st.session_state.nasehat_mingguan["etika"][:100]+"...")
            if st.button("🔊 PLAY ETIKA", key="play_etika"):
                mp3, err = api_voice_recorder(st.session_state.nasehat_mingguan["etika"], "etika.mp3")
                if mp3: 
                    st.audio(mp3, format="audio/mp3")
                    st.download_button("📥 Download ETIKA.mp3", data=mp3, file_name="ETIKA_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_etika")
                else: st.error(err)
            
            st.markdown("**📋 SOP**")
            st.caption(st.session_state.nasehat_mingguan["sop"][:100]+"...")
            if st.button("🔊 PLAY SOP", key="play_sop"):
                mp3, err = api_voice_recorder(st.session_state.nasehat_mingguan["sop"], "sop.mp3")
                if mp3: 
                    st.audio(mp3, format="audio/mp3")
                    st.download_button("📥 Download SOP.mp3", data=mp3, file_name="SOP_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_sop")
                else: st.error(err)
                
        with col2:
            st.markdown("**⚙️ OEE**")
            st.caption(st.session_state.nasehat_mingguan["oee"][:100]+"...")
            if st.button("🔊 PLAY OEE", key="play_oee"):
                mp3, err = api_voice_recorder(st.session_state.nasehat_mingguan["oee"], "oee.mp3")
                if mp3: 
                    st.audio(mp3, format="audio/mp3")
                    st.download_button("📥 Download OEE.mp3", data=mp3, file_name="OEE_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_oee")
                else: st.error(err)
            
            st.markdown("**🏭 ERP**")
            st.caption(st.session_state.nasehat_mingguan["erp"][:100]+"...")
            if st.button("🔊 PLAY ERP", key="play_erp"):
                mp3, err = api_voice_recorder(st.session_state.nasehat_mingguan["erp"], "erp.mp3")
                if mp3: 
                    st.audio(mp3, format="audio/mp3")
                    st.download_button("📥 Download ERP.mp3", data=mp3, file_name="ERP_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_erp")
                else: st.error(err)
        
        with col3:
            st.markdown("**📊 KPI**")
            st.caption(st.session_state.nasehat_mingguan["kpi"][:100]+"...")
            if st.button("🔊 PLAY KPI", key="play_kpi"):
                mp3, err = api_voice_recorder(st.session_state.nasehat_mingguan["kpi"], "kpi.mp3")
                if mp3: 
                    st.audio(mp3, format="audio/mp3")
                    st.download_button("📥 Download KPI.mp3", data=mp3, file_name="KPI_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_kpi")
                else: st.error(err)
            
            st.markdown("**🔥 RUACH HAKADOSH**")
            st.caption(st.session_state.nasehat_mingguan["ruach_hakadosh"][:100]+"...")
            if st.button("🔊 PLAY RUACH HAKADOSH", key="play_ruach"):
                mp3, err = api_voice_recorder(st.session_state.nasehat_mingguan["ruach_hakadosh"], "ruach.mp3")
                if mp3: 
                    st.audio(mp3, format="audio/mp3")
                    st.download_button("📥 Download RUACH.mp3", data=mp3, file_name="RUACH_HAKADOSH_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_ruach")
                else: st.error(err)
        
        st.divider()
        # PLAY SEMUA - Gabungan ETIKA + SOP OEE ERP KPI RUACH
        st.markdown("**🎧 PLAY SEMUA - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH**")
        teks_semua = f"{st.session_state.nasehat_mingguan['etika']} . {st.session_state.nasehat_mingguan['sop']} . {st.session_state.nasehat_mingguan['oee']} . {st.session_state.nasehat_mingguan['erp']} . {st.session_state.nasehat_mingguan['kpi']} . {st.session_state.nasehat_mingguan['ruach_hakadosh']}"
        st.text_area("Preview SEMUA nasehat (editable di menu Nasehat Mingguan):", value=teks_semua[:1200], height=100, key="preview_semua", disabled=True)
        if st.button("🔊 PLAY SEMUA - AI Voice Recorder API - TII System", key="play_semua", type="primary"):
            mp3, err = api_voice_recorder(teks_semua, "semua.mp3")
            if mp3:
                st.audio(mp3, format="audio/mp3")
                st.success("✅ API Voice Recorder TII System membacakan SEMUA Nasehat Mingguan - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH - Ini kalimat dan kolom di atasnya ya syst!")
                st.download_button("📥 Download SEMUA.mp3", data=mp3, file_name="NASEHAT_MINGGUAN_LENGKAP_Ruang_Teduh.mp3", mime="audio/mp3", key="dl_semua")
            else:
                st.error(f"Gagal TTS: {err}. Pastikan requirements.txt ada gTTS==2.4.0")
        
        st.toggle("Voice ON - API Voice Recorder Active", value=True, key="voice_on_api")
        st.caption("Siap - Klik PLAY per nasehat - Hasil rekam nasehat mingguan dari perekaman yang sudah kita berikan yaitu DENGAN SOP, OEE, ERP DAN KPI'S JUGA NASEHAT RUACH HAKADOSH - ini kalimat dan kolom di atasnya ya syst. - API Voice Recorder gTTS Indonesia - TII System")

    # --- TEKS KECIL FONT 12-14 - INTERNAL MANAGER & BRAND & USAHAWAN ONLY - TETAP DIJELASKAN ---
    st.divider()
    st.markdown("""
    <div style="font-size:12px; color:#666; background-color:#f5f5f5; padding:10px; border-radius:5px;">
    <b>Internal MANAGER & BRAND & USAHAWAN ONLY harap isi dan lengkapi CV KOMPLIT + EMAIL + WA PENDAFTAR [PEMBERI KERJA DAN PENCARI KERJA] - FINAL - MIRROR MERAH</b><br>
    📄 CV KOMPLIT - ENTREPRENEUR - MIRROR MERAH : Bursa Vote - Entrepreneur CV Komplit - Metrics Kecil - FINAL<br>
    <i>Laman ini lembar hijau teks font kecil 12-14 - Untuk pemberi kerja dan pencari kerja - FINAL - Mirror Merah - CV Komplit seperti Lembar 2 Merah: Nama + Tempat Lahir + Tgl Lahir + Pendidikan + Pengalaman Kerja + Skill + Email + WA + CV → jugalachaliveret@gmail.com - FINAL</i>
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
    Sebagai Pencari Employee - CV Komplit: Share lowongan via email ke rekan, bursa otomatis berkurang. Sama kayak Employee tapi untuk cari employee. CV komplit pengalaman + email + WA pendaftar web dan app ke jugalachaliveret@gmail.com - FINAL
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
        # PILIHAN REKRUT INDEPENDEN
        st.subheader("⚙️ Pilihan Rekrutmen:")
        input_bursa = st.checkbox("✅ Input ke Bursa Vote (rekrut via sistem - kurangi Bursa Vote)", value=True)
        rekrut_independen = st.checkbox("🤝 Rekrut Independen hanya antar sesama rekan (tanpa melalui klerikal kita)", value=False)
        st.caption("Jika centang 'Rekrut Independen' saja, maka lowongan hanya terkirim ke email rekan sesama (peer-to-peer), tidak masuk Bursa Vote dan tidak melalui klerikal kita.")
        
        submit = st.form_submit_button("🔴 KIRIM PERMINTAAN & SHARE - KURANGI BURSA VOTE - CV KOMPLIT KE jugalachaliveret@gmail.com - FINAL", type="primary")
        
        if submit:
            if not email_rekan:
                st.error("Isi email rekan dulu sayang!")
            else:
                # Buat body email otomatisasi peer-to-peer
                subject = f"CV KOMPLIT - Permintaan Lowongan - {permintaan[:30]} - Ruang Teduh V7.2 FINAL"
                body_email = f"""
CV KOMPLIT - RUANG TEDUH V7.20 FINAL DUAL ADMIN
========================================
Share lowongan via Email ke rekan - CV Komplit: {email_rekan}
Permintaan Lowongan / Request Employee - CV Komplit: {permintaan}
Penawaran Gaji / Benefit - CV Komplit: {penawaran}

Mode: {'Bursa Vote + Peer-to-Peer' if input_bursa and rekrut_independen else 'Bursa Vote' if input_bursa else 'Rekrut Independen Peer-to-Peer Tanpa Klerikal'}
Waktu: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}
Pengirim: Manager/Bursa Vote System
CC: jugalachaliveret@gmail.com, cinhonest@gmail.com (jika mode Bursa)

Bursa: Total {len(st.session_state.bursa_vote)} | Aktif {st.session_state.bursa_vote['Vote Aktif'].sum() if 'Vote Aktif' in st.session_state.bursa_vote else 8} | Kerja {st.session_state.bursa_vote['Sudah Bekerja'].sum() if 'Sudah Bekerja' in st.session_state.bursa_vote else 4}
========================================
ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH ada di app.
"""
                
                # Logika kirim otomatisasi tanpa klerikal
                if input_bursa and not rekrut_independen:
                    # Mode 1: Bursa Vote saja - kirim ke rekan + CC ke admin
                    ok, msg = kirim_email_otomatis(email_rekan, subject, body_email, mode="Bursa Vote")
                    if ok:
                        # Kurangi Bursa Vote otomatis
                        st.session_state.bursa_vote.loc[0, 'Vote Aktif'] = st.session_state.bursa_vote.loc[0, 'Vote Aktif'] - 1 if st.session_state.bursa_vote.loc[0, 'Vote Aktif'] > 0 else 0
                        st.success(f"✅ Terkirim ke {email_rekan}! Bursa: {st.session_state.bursa_vote.loc[0, 'Vote Aktif']} - CV komplit tetap ke jugalachaliveret@gmail.com & cinhonest@gmail.com - {msg}")
                        st.balloons()
                    else:
                        st.error(msg)
                        
                elif rekrut_independen and not input_bursa:
                    # Mode 2: Rekrut Independen saja - HANYA antar rekan, tanpa klerikal kita
                    ok, msg = kirim_email_otomatis(email_rekan, subject, body_email, mode="Rekrut Independen Tanpa Klerikal")
                    if ok:
                        st.success(f"✅ Rekrut Independen: Terkirim hanya ke sesama rekan {email_rekan} (peer-to-peer) - Tanpa Bursa Vote & Tanpa Klerikal - {msg}")
                        st.info("📧 Ini rekrut independen hanya antar sesama rekan saja - tidak masuk Bursa Vote - tidak lewat admin")
                    else:
                        st.error(msg)
                        
                elif input_bursa and rekrut_independen:
                    # Mode 3: Kedua-duanya - Bursa + Independen
                    ok1, msg1 = kirim_email_otomatis(email_rekan, subject, body_email, mode="Bursa Vote + Independen")
                    if ok1:
                        st.session_state.bursa_vote.loc[0, 'Vote Aktif'] = st.session_state.bursa_vote.loc[0, 'Vote Aktif'] - 1 if st.session_state.bursa_vote.loc[0, 'Vote Aktif'] > 0 else 0
                        st.success(f"✅ Terkirim ke Bursa Vote + Rekrut Independen ke {email_rekan} + CC ke jugalachaliveret@gmail.com & cinhonest@gmail.com - {msg1}")
                        st.balloons()
                    else:
                        st.error(msg1)
                else:
                    st.warning("⚠️ Pilih salah satu: Input ke Bursa Vote atau Rekrut Independen - biar jelas antar alamat email saling memberikan permintaan")
                
                # Tampilkan log email otomatisasi
                if st.session_state.email_log:
                    st.divider()
                    st.subheader("📧 Log Email Otomatisasi - Tanpa Klerikal - Peer-to-Peer")
                    st.dataframe(pd.DataFrame(st.session_state.email_log).tail(10), use_container_width=True)
                    st.caption("Ini log bukti antar alamat email saling memberikan permintaan dan pengiriman perekrutan - otomatis tanpa klerikal kita")
                
                # Info setup SMTP jika belum
                if "email" not in st.secrets:
                    with st.expander("🔧 Cara Setup Email Otomatis Beneran (biar kekirim ke inbox cinhonest@gmail.com beneran)", expanded=False):
                        st.markdown("""
                        **Biar email beneran masuk inbox, bukan cuma simulasi:**
                        1. Di Streamlit Cloud dashboard → App → Settings → Secrets
                        2. Paste ini:
                        ```toml
                        [email]
                        smtp_user = "jugalachaliveret@gmail.com"
                        smtp_pass = "app_password_gmail_16_karakter"
                        smtp_host = "smtp.gmail.com"
                        smtp_port = 587
                        ```
                        3. Dapatkan app_password: myaccount.google.com → Security → 2-Step → App Passwords → buat baru
                        4. Save → Reboot App → Test lagi - sekarang email beneran kekirim!
                        
                        **Sementara ini (tanpa secrets):** Email masuk ke Log di atas sebagai bukti otomatisasi tanpa klerikal - sudah terotomatisasi antar alamat email, tinggal aktifkan SMTP biar masuk Gmail beneran.
                        """)


elif menu == "Nasehat Mingguan - Edit SOP OEE ERP KPI RUACH HAKADOSH":
    st.title("📝 Nasehat Mingguan - Edit SOP OEE ERP KPI + RUACH HAKADOSH - Terhubung Merah Kuning Hijau")
    st.caption("Semua nasehat (SOP, OEE, ERP dan KPI's serta nasehat Ruach HaKadosh) ini bisa edit di dalam nasehat mingguan ya syst. Koneksi: Lembar Merah + Kuning + Hijau = 1 Nasehat Mingguan")
    
    st.subheader("Apakah ada nasehat mingguan yang terkoneksi dari seluruhnya lembar merah kuning dan hijau?")
    st.success("YA ADA! 1 Nasehat Mingguan ini terkoneksi ke 3 lembar: Merah (CV Komplit), Kuning (Bursa Vote), Hijau (Manager/Brand/Usahawan). Edit di sini, update di semua!")
    
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
    
    if st.button("💾 SIMPAN NASEHAT MINGGUAN - Update Merah Kuning Hijau", type="primary"):
        st.session_state.nasehat_mingguan = {
            "etika": etika,
            "sop": sop,
            "oee": oee,
            "erp": erp,
            "kpi": kpi,
            "ruach_hakadosh": ruach
        }
        st.success("✅ Nasehat Mingguan tersimpan! Sudah terkoneksi ke Lembar Merah, Kuning, Hijau - Waspada ya sayang!")
        st.balloons()

elif menu == "Members Ruang Teduh - 4 Kolom Mapping DKI":
    st.title("📁 Members Ruang Teduh - 4 Kolom - Mapping DKI")
    st.dataframe(pd.DataFrame([
        ["Employee", "Chef / Staff / Boss Kios/Ruko/Rukan", "DKI Jakarta (buat hitung UMR) - Jakarta tetap Jakarta - Lockernya Jakarta", "https://drive.google.com/drive/folders/12n8a5PkcNPQH1rwZxQiRJ9p7376-oKOx"],
        ["Entrepreneur", "Boss Kios/Ruko/Rukan", "DKI Jakarta - Pelamar dari Bandung bisa lihat", "https://drive.google.com/drive/folders/12n8a5PkcNPQH1rwZxQiRJ9p7376-oKOx"],
    ], columns=["status", "skill", "provinsi/kota", "gdrive_folder"]), use_container_width=True)
    st.caption("Ya sayang ini sudah bagus banget - tanpa detail kios/ruko/rukan tambahan - sudah ada kolom khusus mengetik penjelasan di lembar hijau perekrutan manager")

st.divider()
st.caption("Ruang Teduh AI - FINAL MIRROR - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH - Editable Nasehat Mingguan - Koneksi Merah Kuning Hijau - Bursa Vote + Rekrut Independen Peer-to-Peer - Fix Email ke cinhonest@gmail.com & jugalachaliveret@gmail.com | Even Garden x Vultr Agent Rush Team 5")
