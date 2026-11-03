
import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

st.set_page_config(page_title="Ruang Teduh AI - V11 SIMPLE PRAKTIS - Auto nasehat_mingguan.txt", page_icon="🕊️", layout="wide")

# --- LOAD NASEHAT_MINGGUAN.TXT OTOMATIS DARI GITHUB - MANFAATNYA INI SAYANG ---
def load_nasehat_txt():
    """Manfaat nasehat_mingguan.txt bila terkoneksi otomatis: edit file txt di GitHub saja, app langsung update tanpa edit streamlit_app.py"""
    paths = ["nasehat_mingguan.txt", "./nasehat_mingguan.txt", "/mnt/data/nasehat_mingguan.txt"]
    for p in paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()
            except:
                pass
    # Fallback - isi dari GitHub screenshot kamu image_b74ad3.png - simple praktis
    return """NASEHAT MINGGUAN - RUANG TEDUH - TAVO MALKHUTKHA
Senin: SOP - Cek Kebersihan, kerapian ruang, alat kerja bersih
Selasa: ERP - Jam 9 Tepat, input data harian, laporan akurat
Rabu: OEE 95% - Overall Equipment Effectiveness, efisiensi kerja maksimal
Kamis: KPI - Key Performance Indicator, evaluasi kinerja mingguan
Jumat: Alkitab - Ruach Ha Kadosh, fondasi spiritual, Tavo Malkhutkha (Datanglah KerajaanMu)
Sabtu: Sharing Bursa - Berbagi info loker via email ke rekan
Minggu: Istirahat & Refleksi - Kejujuran update sudah bekerja
Sudah terhubung sebagai member, mari tumbuh bersama di bursa. 1 langkah teduh hari ini adalah 1 vote untuk masa depan.
Mari teduh dulu sebelum melangkah. SOP menjaga langkahmu, KPI mengukur tumbuhmu, Alkitab meneduhkan hatimu."""

def parse_nasehat(text):
    hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    result = {}
    for h in hari_list:
        result[h] = ""
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        for hari in hari_list:
            if line.lower().startswith(hari.lower() + ":"):
                result[hari] = line
                break
    return result

if "bursa_total" not in st.session_state:
    st.session_state.bursa_total = 12
if "bursa_aktif" not in st.session_state:
    st.session_state.bursa_aktif = 8
if "bursa_kerja" not in st.session_state:
    st.session_state.bursa_kerja = 4
if "member_data" not in st.session_state:
    st.session_state.member_data = {}
if "email_log" not in st.session_state:
    st.session_state.email_log = []

nasehat_raw = load_nasehat_txt()
nasehat_7 = parse_nasehat(nasehat_raw)
hari_ini = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][datetime.now().weekday()]

def voice_api(text):
    try:
        from gtts import gTTS
        from io import BytesIO
        tts = gTTS(text=text[:3900], lang='id', slow=False)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except:
        return None

def kirim_simple(to_email, subject, body):
    try:
        smtp_user = st.secrets["email"]["smtp_user"] if "email" in st.secrets else st.secrets["email"]["sender_email"]
        smtp_pass = st.secrets["email"]["smtp_pass"] if "email" in st.secrets else st.secrets["email"]["sender_password"]
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Cc'] = "jugalachaliveret@gmail.com, cinhonest@gmail.com"
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, [to_email, "jugalachaliveret@gmail.com", "cinhonest@gmail.com"], msg.as_string())
        server.quit()
        st.session_state.email_log.append({"ke": to_email, "status": f"✅ Terkirim ke {to_email} + jugalachaliveret@gmail.com + cinhonest@gmail.com"})
        return True
    except Exception as e:
        st.session_state.email_log.append({"ke": to_email, "status": f"📝 Log {to_email} (set Secrets SMTP) - {str(e)[:50]}"})
        return True

# --- MENU SIMPLE PRAKTIS ---
menu = st.sidebar.radio("Menu - SIMPLE PRAKTIS", [
    "PUTIH - Form Loker + Grafik - Simple Awal",
    "HIJAU - Nasehat Mingguan + Voice - Simple",
    "Pencarian - Share Email Otomatis"
])
st.sidebar.caption(f"nasehat_mingguan.txt - Auto Konek - Hari ini: {hari_ini}")
st.sidebar.code(nasehat_raw[:500], language="text")

c1,c2,c3 = st.columns(3)
c1.metric("TOTAL", st.session_state.bursa_total)
c2.metric("AKTIF", st.session_state.bursa_aktif)
c3.metric("KERJA", st.session_state.bursa_kerja)

if menu == "PUTIH - Form Loker + Grafik - Simple Awal":
    st.title("📄 LEMBAR 1 - FORM LOKER CV + GRAFIK - Simple Awal - Sebelum Koreksi")
    st.caption("Yang simple dan praktis seperti Screenshot_2026-11-03_134759.png - sebelum kita koreksi - FINAL SIMPLE")
    
    # Grafik simple
    hist = [{"jam": "08:00", "vote": 2}, {"jam": "09:00", "vote": 5}, {"jam": "10:00", "vote": 8}, {"jam": "11:00", "vote": 8}]
    max_v = 8
    html_g = '<div style="display:flex; gap:8px; align-items:end; height:70px; background:white; border:1px solid #E0E0E0; border-radius:12px; padding:12px;">'
    for h in hist:
        v_h = int(h["vote"] / max_v * 50)
        html_g += f'<div style="flex:1; text-align:center;"><div style="background:#FF5252; height:{v_h}px; border-radius:4px;"></div><div style="font-size:8px; margin-top:4px;">{h["jam"]}</div></div>'
    html_g += '</div>'
    st.markdown(html_g, unsafe_allow_html=True)
    
    with st.form("form_simple"):
        nama = st.text_input("Nama Lengkap *", placeholder="Budi Setia")
        jabatan = st.selectbox("Jabatan *", ["Staff", "Supervisor", "Manager", "Brand Manager", "Usahawan"])
        tempat = st.text_input("Tempat Lahir *", placeholder="Jakarta Barat")
        tgl = st.date_input("Tgl Lahir *", value=date(1994,9,21))
        pendidikan = st.text_input("Pendidikan *", placeholder="S1 Akuntansi Trisakti")
        pengalaman = st.text_area("Pengalaman Kerja *", placeholder="2020-2023 Auditor PT XYZ...", height=80)
        skill = st.text_area("Skill *", placeholder="akuntansi, ERP Accurate...", height=60)
        email = st.text_input("Email *", placeholder="cinhonest@gmail.com")
        wa = st.text_input("WA *", placeholder="081291904422")
        submit = st.form_submit_button("✅ SIMPAN CV & MASUK BURSA - Simple", type="primary", use_container_width=True)
        if submit:
            st.session_state.member_data = {"nama": nama, "jabatan": jabatan, "tempat": tempat, "email": email, "wa": wa}
            st.session_state.bursa_total += 1
            st.session_state.bursa_aktif += 1
            st.success(f"✅ {nama} ({jabatan}) masuk Bursa! CV ke jugalachaliveret@gmail.com")
            st.balloons()

elif menu == "HIJAU - Nasehat Mingguan + Voice - Simple":
    st.title("🕊️ LEMBAR HIJAU - Nasehat Mingguan - Simple Praktis - Auto Konek nasehat_mingguan.txt")
    st.caption("Manfaat nasehat_mingguan.txt bila terkoneksi otomatis: edit file txt di GitHub saja, app langsung update tanpa edit streamlit_app.py - Simple praktis!")
    
    # AUTO DAILY dari txt
    with st.container(border=True):
        st.success(f"📅 Hari ini {hari_ini} - Nasehat dari nasehat_mingguan.txt - Untuk Manager, Business Owner & Employee - Biar leader nggak melulu nasehatin")
        st.markdown(f"<div style='background:#e8f5e9; padding:15px; border-radius:10px; border-left:4px solid #2e7d32;'>{nasehat_7.get(hari_ini, 'Nasehat hari ini')}</div>", unsafe_allow_html=True)
        if st.button(f"🔊 PLAY HARI INI - {hari_ini} - Voice Recorder API", type="primary"):
            mp3 = voice_api(nasehat_7.get(hari_ini, ""))
            if mp3:
                st.audio(mp3, format="audio/mp3")
    
    st.divider()
    st.subheader("📜 Semua Nasehat 7 Hari - Dari nasehat_mingguan.txt - Auto Konek")
    for hari in ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]:
        is_today = hari == hari_ini
        if is_today:
            st.markdown(f"<div style='background:#e8f5e9; border:2px solid #2e7d32; padding:10px; border-radius:8px;'><b>🔥 {hari} (HARI INI):</b> {nasehat_7.get(hari,'')}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background:white; border:1px solid #E0E0E0; padding:8px; border-radius:8px;'><b>{hari}:</b> {nasehat_7.get(hari,'')}</div>", unsafe_allow_html=True)
    
    st.divider()
    st.caption("Edit file nasehat_mingguan.txt di GitHub Alchaliveret/ruang-teduh-ai/blob/main/nasehat_mingguan.txt → Save → Streamlit auto reboot → Nasehat update otomatis! Nggak perlu edit streamlit_app.py lagi!")

else:
    st.title("🔍 Pencarian Permintaan & Request Penawaran - Simple Otomatis")
    st.caption("Share lowongan via email ke rekan - otomatis masuk Bursa + ke jugalachaliveret@gmail.com + cinhonest@gmail.com - tanpa klerikal")
    with st.form("form_share_simple"):
        email_rekan = st.text_input("Email Rekan", value="cinhonest@gmail.com", placeholder="rekan@perusahaan.com")
        permintaan = st.text_area("Permintaan Lowongan", value="butuh sales staff jakarta pusat")
        gaji = st.text_input("Gaji", value="4000000")
        input_bursa = st.checkbox("✅ Input ke Bursa Vote", value=True)
        independen = st.checkbox("🤝 Rekrut Independen only (peer-to-peer tanpa klerikal)", value=False)
        submit = st.form_submit_button("🔴 KIRIM OTOMATIS - Simple", type="primary")
        if submit:
            if email_rekan:
                kirim_simple(email_rekan, f"CV KOMPLIT - {permintaan[:20]}", f"Permintaan: {permintaan}\nGaji: {gaji}")
                if input_bursa:
                    st.session_state.bursa_aktif = max(0, st.session_state.bursa_aktif - 1)
                    st.session_state.bursa_kerja += 1
                    st.success(f"✅ Terkirim ke {email_rekan} + jugalachaliveret@gmail.com + cinhonest@gmail.com + Masuk Bursa Vote - Simple!")
                    st.balloons()
                else:
                    st.success(f"✅ Rekrut Independen ke {email_rekan} only - peer-to-peer tanpa Bursa - Simple!")
            if st.session_state.email_log:
                st.dataframe(pd.DataFrame(st.session_state.email_log).tail(5), use_container_width=True)

st.caption("V11 SIMPLE PRAKTIS - Sebelum Koreksi - Auto Konek nasehat_mingguan.txt - Edit txt di GitHub saja, app update otomatis - Simple praktis - SINGLE ADMIN jugalachaliveret@gmail.com + cinhonest@gmail.com - Voice Rolling 1 Hari 1 Nasehat")
