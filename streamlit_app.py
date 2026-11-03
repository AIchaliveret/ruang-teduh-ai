
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Ruang Teduh AI - FINAL", page_icon="🕊️", layout="wide")

# --- INIT ---
if "email_log" not in st.session_state:
    st.session_state.email_log = []

if "nasehat_mingguan" not in st.session_state:
    st.session_state.nasehat_mingguan = {
        "etika": """ETIKA KERJA RUANG TEDUH:
1. Jujur dalam CV - Jangan tambah pengalaman palsu
2. Hormat waktu - OEE 95% dimulai disiplin
3. Saling tolong - Bursa Vote keluarga""",
        "sop": """SOP MANAGER:
• Kelola 5-10 Staff + 2-3 Supervisor
• Kelola CV komplit email WA pendaftar""",
        "oee": """OEE 95% Target:
• Availability 100% • Performance 120 Yd/hari • Quality <2%""",
        "erp": """ERP - Klerikal Jadi Manajemen:
• Gudang 22M vs C12 - FIFO LIFO
• GPS -6.2088,106.8456 UNIKA""",
        "kpi": """KPI:
• Manager OEE 95% omzet 15%
• Brand growth 15%
• Usahawan omzet profit""",
        "ruach_hakadosh": """RUACH HAKADOSH:
"Jikalau kamu tinggal di dalam Aku..." - Yohanes 15:7
"Segala sesuatu yang kamu kehendaki..." - Matius 7:12"""
    }

if "bursa_vote" not in st.session_state:
    st.session_state.bursa_vote = pd.DataFrame([
        ["Sari Manager", "Jakarta Barat", "S1 Manajemen", "2018-2024 Manager", "Leadership", "manager@email.com", "081291904422", "Employee", 8, 4],
    ], columns=["Nama", "Tempat Lahir", "Pendidikan", "Pengalaman", "Skill", "Email", "WA", "Status", "Vote Aktif", "Sudah Bekerja"])

def kirim_email_stable(to_email, subject, body, mode=""):
    from io import BytesIO
    log = {
        "waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "ke": to_email,
        "subject": subject,
        "mode": mode,
        "status": "Queued"
    }
    try:
        smtp_user = None
        smtp_pass = None
        admin_email = "jugalachaliveret@gmail.com"
        try:
            if "email" in st.secrets:
                cfg = st.secrets["email"]
                smtp_user = cfg.get("smtp_user") or cfg.get("sender_email")
                smtp_pass = cfg.get("smtp_pass") or cfg.get("sender_password")
                admin_email = cfg.get("admin1") or cfg.get("admin2") or "jugalachaliveret@gmail.com"
        except:
            pass
        
        if smtp_user and smtp_pass:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            if "Bursa" in mode:
                msg['Cc'] = admin_email
            
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            recips = [to_email]
            if "Bursa" in mode:
                recips.append(admin_email)
            server.sendmail(smtp_user, recips, msg.as_string())
            server.quit()
            log["status"] = f"✅ Terkirim ke {to_email} via {smtp_user}"
            st.session_state.email_log.append(log)
            return True, f"✅ Terkirim beneran ke {to_email} + CC {admin_email}!"
        else:
            log["status"] = f"📝 Log - Tanpa Klerikal - ke {to_email} (Set Secrets SMTP untuk kirim Gmail beneran)"
            st.session_state.email_log.append(log)
            return True, f"📝 Otomatis Masuk Log (Tanpa Klerikal) - ke {to_email}. Set Secrets untuk kirim Gmail beneran ke inbox."
    except Exception as e:
        log["status"] = f"❌ {str(e)[:100]}"
        st.session_state.email_log.append(log)
        return False, f"❌ Gagal: {e}"

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

# --- MENU ---
menu = st.sidebar.radio("Menu", [
    "Lembar Hijau - FINAL",
    "Bursa Vote - FINAL",
    "Pencarian Permintaan - FINAL",
    "Nasehat Mingguan - Edit",
    "Members"
])

if menu == "Lembar Hijau - FINAL":
    st.title("🕊️ LEMBAR HIJAU - Untuk Manager, Business Owner & Employee - FINAL")
    
    # AUTO DAILY 1 HARI 1 NASEHAT - 5 NASEHAT
    st.markdown("### 📅 Auto Daily - 1 Hari 1 Nasehat")
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
            st.success(f"Hari ini {today.strftime('%A %d-%m-%Y')} - {today_label} - Untuk Manager, Business Owner & Employee")
            st.info(today_text)
        with c2:
            if st.button(f"🔊 PLAY HARI INI - {today_key.upper()}", type="primary", key="play_today"):
                mp3, err = voice_api(today_text)
                if mp3:
                    st.audio(mp3, format="audio/mp3")
                    st.download_button(f"📥 Download {today_key}", data=mp3, file_name=f"{today_key}_{today.strftime('%Y%m%d')}.mp3", mime="audio/mp3", key="dl_today")
                else:
                    st.error(f"gTTS error: {err}. Cek requirements.txt ada gTTS")
            st.caption("Tgl 1,6,11=SOP | 2,7,12=OEE | 3,8,13=ERP | 4,9,14=KPI | 5,10,15=RUACH")
    
    st.divider()
    st.subheader("📜 ETIKA")
    st.write(st.session_state.nasehat_mingguan["etika"])
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 SOP")
        st.info(st.session_state.nasehat_mingguan["sop"])
        st.subheader("⚙️ OEE")
        st.success(st.session_state.nasehat_mingguan["oee"])
    with col2:
        st.subheader("🏭 ERP")
        st.warning(st.session_state.nasehat_mingguan["erp"])
        st.subheader("📊 KPI")
        st.error(st.session_state.nasehat_mingguan["kpi"])
    st.subheader("🔥 RUACH HAKADOSH")
    st.success(st.session_state.nasehat_mingguan["ruach_hakadosh"])
    
    st.divider()
    st.subheader("🔊 API Voice Recorder - 5 Nasehat")
    st.caption("Untuk Manager, Business Owner & Employee - Biar leader nggak melulu nasehatin")
    with st.container(border=True):
        c1,c2,c3 = st.columns(3)
        with c1:
            if st.button("🔊 PLAY SOP", key="psop"):
                mp3,err=voice_api(st.session_state.nasehat_mingguan["sop"])
                if mp3: st.audio(mp3, format="audio/mp3")
                else: st.error(err)
            if st.button("🔊 PLAY OEE", key="poee"):
                mp3,err=voice_api(st.session_state.nasehat_mingguan["oee"])
                if mp3: st.audio(mp3, format="audio/mp3")
                else: st.error(err)
        with c2:
            if st.button("🔊 PLAY ERP", key="perp"):
                mp3,err=voice_api(st.session_state.nasehat_mingguan["erp"])
                if mp3: st.audio(mp3, format="audio/mp3")
                else: st.error(err)
            if st.button("🔊 PLAY KPI", key="pkpi"):
                mp3,err=voice_api(st.session_state.nasehat_mingguan["kpi"])
                if mp3: st.audio(mp3, format="audio/mp3")
                else: st.error(err)
        with c3:
            if st.button("🔊 PLAY RUACH", key="pruach"):
                mp3,err=voice_api(st.session_state.nasehat_mingguan["ruach_hakadosh"])
                if mp3: st.audio(mp3, format="audio/mp3")
                else: st.error(err)
            if st.button("🔊 PLAY ETIKA", key="petika"):
                mp3,err=voice_api(st.session_state.nasehat_mingguan["etika"])
                if mp3: st.audio(mp3, format="audio/mp3")
                else: st.error(err)
        if st.button("🔊 PLAY SEMUA", key="pall", type="primary"):
            all_text = " ".join(st.session_state.nasehat_mingguan.values())
            mp3,err=voice_api(all_text)
            if mp3: 
                st.audio(mp3, format="audio/mp3")
                st.download_button("📥 Download SEMUA", data=mp3, file_name="SEMUA_NASEHAT.mp3", mime="audio/mp3", key="dl_all")
            else: st.error(err)
    
    st.divider()
    st.markdown('<div style="font-size:12px; color:#666; background:#f5f5f5; padding:10px; border-radius:5px;">Internal MANAGER & BRAND & USAHAWAN + EMPLOYEE ONLY - CV KOMPLIT + EMAIL + WA → jugalachaliveret@gmail.com ONLY - SINGLE ADMIN</div>', unsafe_allow_html=True)

elif menu == "Bursa Vote - FINAL":
    st.title("📊 Bursa Vote - FINAL - SINGLE ADMIN jugalachaliveret@gmail.com")
    st.dataframe(st.session_state.bursa_vote, use_container_width=True)
    st.metric("Vote Aktif", "8")
    st.metric("Sudah Bekerja", "4")

elif menu == "Pencarian Permintaan - FINAL":
    st.title("🔍 Pencarian Permintaan - FINAL")
    with st.form("form"):
        email_rekan = st.text_input("Email Rekan", placeholder="cinhonest@gmail.com")
        permintaan = st.text_area("Permintaan Lowongan", value="butuh beberapa tenaga kerja sales staff ditempatkan di keutamaan kali kerukut jakarta pusat")
        penawaran = st.text_area("Penawaran Gaji", value="4000000")
        input_bursa = st.checkbox("✅ Input ke Bursa Vote + CC ke jugalachaliveret@gmail.com (single admin)", value=True)
        rekrut_independen = st.checkbox("🤝 Rekrut Independen hanya antar rekan (tanpa klerikal)", value=False)
        submit = st.form_submit_button("🔴 KIRIM PERMINTAAN & SHARE - SINGLE ADMIN", type="primary")
        if submit:
            if not email_rekan:
                st.error("Isi email rekan dulu")
            else:
                subject = f"CV KOMPLIT - {permintaan[:30]} - V7.8"
                body = f"Email Rekan: {email_rekan}\nPermintaan: {permintaan}\nGaji: {penawaran}\nMode: Bursa={input_bursa} Independen={rekrut_independen}\nAdmin: jugalachaliveret@gmail.com ONLY"
                if input_bursa and not rekrut_independen:
                    ok,msg = kirim_email_stable(email_rekan, subject, body, "Bursa Vote")
                    if ok: 
                        st.success(f"✅ {msg} - Terkirim ke {email_rekan}! Bursa 4→3")
                        st.balloons()
                    else: st.error(msg)
                elif rekrut_independen and not input_bursa:
                    ok,msg = kirim_email_stable(email_rekan, subject, body, "Independen")
                    if ok: st.success(f"✅ Rekrut Independen ke {email_rekan} - Tanpa Bursa & Tanpa Klerikal - {msg}")
                    else: st.error(msg)
                elif input_bursa and rekrut_independen:
                    ok,msg = kirim_email_stable(email_rekan, subject, body, "Bursa+Independen")
                    if ok: st.success(f"✅ Bursa + Independen ke {email_rekan} + CC jugalachaliveret@gmail.com - {msg}")
                    else: st.error(msg)
                else:
                    st.warning("Pilih Bursa atau Independen")
                
                if st.session_state.email_log:
                    st.dataframe(pd.DataFrame(st.session_state.email_log).tail(10), use_container_width=True)

elif menu == "Nasehat Mingguan - Edit":
    st.title("📝 Nasehat Mingguan - Edit")
    for k in st.session_state.nasehat_mingguan:
        st.session_state.nasehat_mingguan[k] = st.text_area(k.upper(), value=st.session_state.nasehat_mingguan[k], key=f"edit_{k}")
    if st.button("💾 SIMPAN", type="primary"):
        st.success("Tersimpan! Untuk Manager, Business Owner & Employee")
        st.balloons()

else:
    st.title("📁 Members")
    st.write("Untuk Manager, Business Owner & Employee")
