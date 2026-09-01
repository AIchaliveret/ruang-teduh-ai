import streamlit as st
import io
from gtts import gTTS
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Ruang Teduh AI", page_icon="🌿", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "R1"
if "last_pesan" not in st.session_state:
    st.session_state.last_pesan = ""
if "last_tier" not in st.session_state:
    st.session_state.last_tier = ""
if "is_member" not in st.session_state:
    st.session_state.is_member = False
if "nasehat_list" not in st.session_state:
    st.session_state.nasehat_list = []

def tts_player(text, label="", autoplay=False):
    try:
        tts = gTTS(text, lang='id', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3', autoplay=autoplay)
        if label: st.caption(f"🔊 {label}")
    except Exception as e:
        st.error(f"Audio error: {e}")

def send_email_auto(pesan, tier, pengirim_info="Member"):
    """Kirim email 100% auto via Gmail App Password yang ada di Secrets"""
    try:
        # Cek apakah secrets sudah disetting
        if "email" not in st.secrets:
            return False, "Secrets belum disetting. Ikuti step di bawah."
        
        sender_email = st.secrets["email"]["sender_email"]  # email lo yang buat ngirim
        sender_password = st.secrets["email"]["sender_password"]  # App Password 16 huruf
        admin1 = st.secrets["email"]["admin1"]
        admin2 = st.secrets["email"]["admin2"]
        
        # Buat email
        subject = f"[Ruang Teduh] Pesan Baru - {tier} - {pengirim_info}"
        body = f"""
        Ada pesan baru dari Ruang Teduh AI:
        
        Tier: {tier}
        Pengirim: {pengirim_info}
        Waktu: Otomatis dari app
        
        Pesan:
        {pesan}
        
        ---
        Balas ke: {admin1}, {admin2}
        WA Admin: {st.secrets['email'].get('wa2','081291904422')}
        """
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = f"{admin1}, {admin2}"
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Kirim via Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return True, f"Email terkirim ke {admin1} & {admin2}"
    except KeyError as e:
        return False, f"Secrets kurang: {e}. Cek format TOML."
    except Exception as e:
        return False, f"Gagal kirim: {e}. Cek App Password."

def load_nasehat():
    if os.path.exists("nasehat_mingguan.txt"):
        try:
            with open("nasehat_mingguan.txt","r",encoding="utf-8") as f:
                lines=[l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
                if lines: return lines
        except: pass
    return ["Senin: SOP cek kebersihan", "Selasa: ERP update stok jam 9 pagi", "Rabu: OEE mesin 1 harus 95%"]

def load_renungan():
    if os.path.exists("renungan_harian.txt"):
        try:
            with open("renungan_harian.txt","r",encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip()]
        except: pass
    return ["SENIN: Renungan Alkitab - Matius 11:28", "SELASA: Yeremia 29:11"]

def render_r3():
    st.markdown("""<div style="background:linear-gradient(135deg,#0a3d2e,#1a6d4e);padding:20px;border-radius:15px;color:white;border:2px solid gold"><h2>🌟 RUANG 3 - MEMBER AREA TETAP v3.5 - EMAIL 100% AUTO</h2></div>""", unsafe_allow_html=True)
    st.success(f"✅ Member Aktif: {st.session_state.last_tier} | Email Admin Auto Konek")
    
    st.markdown("### 🎵 Musik Teduh")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    
    if st.checkbox("Tampilkan Visual Mata->Hati->Brain", value=True):
        try: st.image("perjalanan_cinta_petunjuk.webp", use_container_width=True)
        except: st.info("Visual: Mata->Hati->Brain->Jiwa Lestari")

    st.markdown("### 📜 Teks Nasehat Mingguan")
    if not st.session_state.nasehat_list:
        st.session_state.nasehat_list = load_nasehat()
    for i,n in enumerate(st.session_state.nasehat_list):
        c1,c2 = st.columns([4,1])
        with c1: st.write(f"**{i+1}. {n}**")
        with c2:
            if st.button("🔊", key=f"tts_n_{i}"): tts_player(n, f"Nasehat {i+1}")
    if st.button("🏆 Bacakan SEMUA Nasehat", type="primary", use_container_width=True):
        tts_player(" ".join(st.session_state.nasehat_list), "Full Mingguan")

    st.divider()
    st.markdown("### 🙏 Renungan Harian Senin-Minggu + Nasehat Sehat")
    for i,r in enumerate(load_renungan()):
        hari = r.split(":")[0]
        with st.expander(f"{hari} - Klik untuk dengar", expanded=(i==0)):
            st.write(r)
            if st.button(f"🔊 Bacakan {hari}", key=f"renung_{i}"):
                tts_player(r, f"Renungan {hari}")

    st.divider()
    if st.button("⬅️ Kembali ke R1", use_container_width=True):
        st.session_state.page="R1"; st.rerun()

def render_r1_r2(ruang_name):
    st.markdown("""<div style="background:#0a3d2e;padding:20px;border-radius:15px;color:white;border:2px solid #2ecc71"><h3>🎧 Ruang Teduh • v3.5 - EMAIL 100% AUTO</h3></div>""", unsafe_allow_html=True)
    st.write("")
    
    if ruang_name=="R2" and st.session_state.last_pesan:
        st.success(f"📩 Pesan dari R1 (Tier: {st.session_state.last_tier}):")
        st.info(f"\"{st.session_state.last_pesan}\"")

    st.subheader(f"📝 Form Ruang {ruang_name[-1]} (v3.5)")

    with st.form(f"form_{ruang_name}_v35", clear_on_submit=False):
        tier = st.selectbox("Pilih Tier", ["Employee 20rb/bulan","Entrepreneur 30rb/bulan"], key=f"tier_{ruang_name}_v35")
        pesan = st.text_area("Pesan ke Admin Email & WA", placeholder="Tulis pesan...", key=f"pesan_{ruang_name}_v35", height=150, value=st.session_state.last_pesan if ruang_name=="R1" else "")
        
        st.info("📧 Email Admin Aktif:\n- jugalachaliveret@gmail.com (Member)\n- asuveleikha@gmail.com (Ruang Teduh) - 081291904422")

        c1,c2 = st.columns(2)
        with c1: submit_admin = st.form_submit_button("Kirim ke Admin (Auto Email)", use_container_width=True, type="primary")
        with c2: submit_next = st.form_submit_button(f"Submit {ruang_name} & Lanjut" if ruang_name=="R1" else f"Submit {ruang_name}", use_container_width=True)

        if submit_admin:
            if pesan:
                # Coba kirim auto
                success, msg = send_email_auto(pesan, tier, f"Tier {tier}")
                if success:
                    st.success(f"✅ {msg}")
                    st.balloons()
                else:
                    st.warning(f"⚠️ {msg}")
                    st.info("Fallback: Pakai mailto (klik di bawah) atau setting Secrets dulu (lihat panduan)")
                    st.markdown(f"[📧 Klik untuk buka Gmail](mailto:jugalachaliveret@gmail.com,asuveleikha@gmail.com?subject=Pesan {tier}&body={pesan})")
            else:
                st.warning("Tulis pesan dulu bro")

        if submit_next:
            if pesan:
                st.session_state.last_pesan=pesan; st.session_state.last_tier=tier
                if ruang_name=="R1": st.session_state.page="R2"; st.rerun()
                else: st.session_state.is_member=True; st.session_state.page="R3"; st.rerun()
            else: st.warning("Tulis pesan dulu")

    if ruang_name=="R2":
        st.divider()
        st.markdown("### 💳 Pembayaran Member")
        try: st.image("qr_payment.png", caption="QR Gopay Ovo Dana BCA BNI", use_container_width=True)
        except: st.warning("Upload qr_payment.png")
        st.write("BCA VA: 1234567890 | BNI VA: 9876543210 | WA: 081291904422")
        if st.button("✅ Saya Sudah Transfer - Masuk Ruang 3", type="primary", use_container_width=True):
            st.session_state.is_member=True; st.session_state.page="R3"; st.rerun()

    if ruang_name=="R1":
        if st.button("➡️ Masuk ke Ruang 2", use_container_width=True):
            st.session_state.page="R2"; st.rerun()
    else:
        if st.button("⬅️ Kembali ke R1", use_container_width=True):
            st.session_state.page="R1"; st.rerun()

if st.session_state.page=="R3": render_r3()
elif st.session_state.page=="R1": render_r1_r2("R1")
else: render_r1_r2("R2")
