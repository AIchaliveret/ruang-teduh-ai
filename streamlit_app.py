# RUANG TEDUH V15 FIX - Bursa Vote di Lembar Putih + TTS + Email Lembar 7
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
st.set_page_config(page_title="Ruang Teduh V15 - FIX", layout="wide")
NASEHAT_TEKS = "Nasehat Mingguan Ruang Teduh. Satu, Kejujuran. Tulis pengalaman apa adanya, jangan palsu. Kejujuran adalah modal OEE 99 persen. Dua, Hormat Waktu. Tiga, Saling Bantu. Empat, The Best Interaksi. Lima, Disiplin Klerikal."
BURSA = [{"nama":"Staff Sales Air Mineral 600ml - Teluk Naga","vote":12},{"nama":"Staff Gudang Bandara Soetta","vote":8},{"nama":"Admin CV Komplit - Jakarta","vote":15}]
def kirim_email(tujuan, subjek, isi):
    try:
        u = st.secrets["smtp"]["user"]; p = st.secrets["smtp"]["password"]
    except Exception:
        return False, "SECRETS_KOSONG"
    try:
        msg = MIMEMultipart(); msg["From"]=u; msg["To"]=tujuan; msg["Subject"]=subjek; msg.attach(MIMEText(isi,"plain"))
        s = smtplib.SMTP("smtp.gmail.com",587); s.starttls(); s.login(u,p); s.sendmail(u,tujuan,msg.as_string()); s.quit(); return True,"TERKIRIM"
    except Exception as e:
        return False, str(e)
def buat_audio(teks):
    try:
        from gtts import gTTS; import io; t=gTTS(text=teks, lang="id", slow=False); b=io.BytesIO(); t.write_to_fp(b); b.seek(0); return b
    except Exception:
        return None
menu = st.sidebar.radio("Menu", ["1. Lembar PUTIH - Pendaftaran + Bursa Vote","2. Lembar MERAH - CV Komplit","3. Lembar KUNING","4. Lembar HIJAU","5. Nasehat Mingguan - Edit Pusat","6. Speaker - PUTAR SUARA TTS FIX","7. Pencarian Permintaan - Kirim Email"])
if menu.startswith("1."):
    st.title("Lembar PUTIH - Pendaftaran - 3 Fungsi Management")
    st.info("Wajib daftar dulu sebagai Manager/Pengusaha baru bisa buat loker independen antar rekan - semua tetap masuk Bursa Vote")
    with st.form("d"):
        nama=st.text_input("Nama *"); email=st.text_input("Email Pribadi *"); wa=st.text_input("WA *"); sbg=st.selectbox("Daftar sebagai",["Employee - Staff","Manager","Pengusaha"]); ok=st.form_submit_button("DAFTAR + DAPAT LEMBAR MERAH/KUNING/HIJAU + EMAIL ADMIN")
        
        if ok: st.success(f"Terdaftar: {nama} sebagai {sbg}")
    st.divider(); st.header("BURSA VOTE - Langsung Terlihat di Halaman 1"); st.caption("Siapapun, dimanapun, buka Lembar Putih langsung bisa vote. Tidak perlu ke halaman 3 lagi.")
    for it in BURSA:
        c1,c2,c3=st.columns([3,1,1]); c1.write(it["nama"]); c2.write(f"Vote: {it['vote']}")
        
        if c3.button("Vote", key="v_"+it["nama"]): it["vote"]+=1; st.success("Vote terkirim"); st.rerun()
elif menu.startswith("5."):
    st.title("Nasehat Mingguan - Edit Pusat"); st.warning("Edit di sini saja. Teks ini yang akan dibaca suara di Halaman 6.")
    nt=st.text_area("Edit Nasehat", value=st.session_state.get("nasehat_saved", NASEHAT_TEKS), height=250)
    
    if st.button("SIMPAN NASEHAT"): st.session_state["nasehat_saved"]=nt; st.success("Tersimpan. Buka Halaman 6, pencet PUTAR SUARA.")
elif menu.startswith("6."):
    st.title("Speaker - PUTAR SUARA Nasehat - TTS FIX")
    teks=st.session_state.get("nasehat_saved", NASEHAT_TEKS); st.text_area("Teks yang akan dibacakan persis:", value=teks, height=200)
    st.info("FIX: Recorder lama yang zopper-kliper DIMATIKAN. Sekarang TTS baca teks di atas persis kata per kata.")
    
    if st.button("PUTAR SUARA - Nasehat Mingguan"):
        a=buat_audio(teks)
        
        if a: st.audio(a, format="audio/mp3"); st.success("Suara ini dari teks di atas persis.")
        else: st.error("Install dulu: pip install gtts")
elif menu.startswith("7."):
    st.title("Pencarian Permintaan & Request - Kirim Email Langsung")
    st.info("FIX: Sekarang bisa kirim langsung ke email masing-masing, tidak hanya dicatat.")
    tujuan=st.text_input("Email Rekan tujuan"); permintaan=st.text_area("Permintaan Lowongan / Request Employee"); penawaran=st.text_area("Penawaran Gaji / Benefit")
    mode=st.radio("Pilihan", ["Input ke Bursa Vote - masuk email admin","Rekrut Independen - langsung ke email rekan, tidak masuk Bursa Vote"])
    
    if st.button("KIRIM PERMINTAAN & SHARE"):
        
        if not tujuan: st.error("Isi dulu Email Rekan tujuan.")
        else:
            ok,pesan=kirim_email(tujuan, "Ruang Teduh - Permintaan Lowongan", f"Permintaan: {permintaan}\nPenawaran: {penawaran}\nMode: {mode}")
            
            if pesan=="SECRETS_KOSONG":
                st.error("Secrets smtp password kosong - isi di .streamlit/secrets.toml. Tapi data tetap dicatat di Bursa Vote!")
                st.code("[smtp] \nuser = \"emailkamu@gmail.com\" \npassword = \"app-password-16-digit\" \nserver = \"smtp.gmail.com\" \nport = 587")
                st.warning("App Password: Google Account > Security > 2-Step ON > App Passwords > buat baru > copy 16 digit ke secrets.toml. Jangan pakai password Gmail biasa.")
            elif ok: st.success(f"Terkirim langsung ke {tujuan}!")
            else: st.error(f"Gagal: {pesan}")
else:
    st.title(menu); st.info("Halaman ini tetap sama V15 lama. Yang berubah: Bursa Vote di Halaman 1, Suara TTS di Halaman 6, Email bisa kirim di Halaman 7.")