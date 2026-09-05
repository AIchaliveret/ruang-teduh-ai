import streamlit as st
import pandas as pd
from datetime import datetime
import qrcode
from PIL import Image
import io

st.set_page_config(page_title="Ruang Teduh - KOMITMEN OS", layout="wide", page_icon="📄")

# --- CSS ANTI-MAINAN - PROFESSIONAL NCR ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.ncr-card {
    border-radius: 16px; padding: 24px; border: 1px solid #E5E7EB;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05); position: relative; overflow: hidden;
}
.ncr-putih { background: #FFFFFF; border-left: 8px solid #111827; }
.ncr-pink { background: #FFF1F2; border-left: 8px solid #BE123C; }
.ncr-hijau { background: #ECFDF5; border-left: 8px solid #059669; }
.carbon-line {
    border-top: 2px dashed #9CA3AF; margin: 16px 0; position: relative;
}
.carbon-line::after {
    content: '✂ carbon copy - tembus otomatis'; font-size: 10px; color: #9CA3AF;
    position: absolute; top: -10px; left: 50%; transform: translateX(-50%);
    background: white; padding: 0 8px; font-family: 'JetBrains Mono';
}
.floating-dot {
    position: fixed; bottom: 24px; right: 24px; width: 64px; height: 64px;
    background: #F97316; border-radius: 50%; box-shadow: 0 8px 24px rgba(249,115,22,0.4);
    display: flex; align-items: center; justify-content: center; z-index: 9999;
    animation: pulse 2s infinite;
}
@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
.billboard { background: #111827; color: #10B981; font-family: 'JetBrains Mono'; padding: 12px; border-radius: 8px; overflow: hidden; white-space: nowrap; }
.ticker { display: inline-block; animation: ticker 20s linear infinite; }
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
.nb-box { background: #FEF3C7; border: 2px solid #F59E0B; border-radius: 12px; padding: 16px; }
.metric-card { background: white; border-radius: 12px; padding: 16px; border: 1px solid #E5E7EB; text-align: center; }
</style>
<div class="floating-dot">🟠</div>
""", unsafe_allow_html=True)

# --- INIT SESSION ---
if 'members' not in st.session_state:
    st.session_state.members = [
        {"nama":"Pak Budi","role":"Employee","skill":"ERP Jam 9","zona":"Jakarta","arsip":1,"vote":1,"status":"Berlangganan"},
        {"nama":"Pak Bambang","role":"Entrepreneur","skill":"Direktur","zona":"Surabaya","arsip":1,"vote":1,"status":"Berlangganan"},
        {"nama":"Pak Johan","role":"Entrepreneur","skill":"Owner Kecil","zona":"Bandung","arsip":1,"vote":1,"status":"Berlangganan"},
    ]

# --- HELPER QR ---
def make_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# --- HEADER ---
c1, c2 = st.columns([3,1])
with c1:
    st.markdown("## Ruang Teduh - KOMITMEN OS")
    st.markdown("**Buku 1 Ruang 3 Lembar - NCR System 1x Tulis Tembus 3x Otomatis**")
    st.caption("Tavo Malkhutkha: Two Journeys, One QR | Wellbeing AI for Future of Work | Owner: Even Garden")
with c2:
    st.metric("Total Bursa", f"{len(st.session_state.members)} arsip", f"{len(st.session_state.members)} vote")
    
st.markdown('<div class="billboard"><div class="ticker">📢 BURSA LIVE: Pak Budi 1 vote | Pak Bambang 1 vote | Pak Johan 1 vote | Total {} member terkoneksi | Employee Rp55k | Entrepreneur Rp75k | Mari teduh dulu, SOP menjaga langkahmu, KPI mengukur tumbuhmu | </div></div>'.format(len(st.session_state.members)), unsafe_allow_html=True)
st.write("")

# --- LEMBAR 1 PUTIH - ASLI ---
with st.container():
    st.markdown('<div class="ncr-card ncr-putih">', unsafe_allow_html=True)
    st.markdown("### LEMBAR 1 PUTIH - ASLI | Pintu Depan + Billboard Bursa")
    
    col_form, col_info = st.columns([2,1])
    
    with col_form:
        st.markdown("**[QR GATE] -> [FORM ORG LENGKAP] -> [VALIDASI] ---carbon copy---> 3 LEMBAR TEMBUS OTOMATIS**")
        with st.form("form_org_lengkap", clear_on_submit=False):
            st.markdown("#### Kolom Pendaftaran - Employee & Entrepreneur (ERP Structure)")
            f1, f2 = st.columns(2)
            with f1:
                nama = st.text_input("Nama Lengkap *", placeholder="Even Garden")
                tempat_lahir = st.text_input("Tempat Lahir")
                tgl_lahir = st.date_input("Tanggal Lahir", value=datetime(1990,1,1))
                email = st.text_input("Alamat Email *")
                hp = st.text_input("HP / WA *", placeholder="0812xxxx")
                zona = st.selectbox("Zona", ["Jakarta","Surabaya","Bandung","Jogja","Lainnya"])
                role = st.selectbox("Kategori Member *", ["Employee","Entrepreneur"])
            with f2:
                alamat = st.text_area("Alamat Kependudukan")
                pendidikan = st.selectbox("Pendidikan", ["SMA","D3","S1","S2","S3"])
                jurusan = st.text_input("Jurusan")
                pengalaman = st.text_area("Pengalaman Kerja")
                skill = st.text_input("Skill Utama *", placeholder="ERP Jam 9 / OEE 95%")
                linkedin = st.text_input("LinkedIn")
                ekspektasi = st.text_input("Ekspektasi Gaji / Value")

            st.markdown("##### Tambahan Sistematis")
            t1, t2, t3 = st.columns(3)
            with t1:
                foto = st.file_uploader("Foto Profil", type=['jpg','png'])
                cv = st.file_uploader("CV / Portofolio", type=['pdf','docx'])
            with t2:
                status = st.selectbox("Status Ketersediaan", ["Available","Terikat","Freelance"])
                referensi = st.text_input("Referensi")
            with t3:
                kependudukan = st.text_input("NIK / Kependudukan")

            st.markdown("---")
            st.markdown("**Kolom Nasehat Bimbingan:** *Mari teduh dulu, SOP menjaga langkahmu, KPI mengukur tumbuhmu, Alkitab meneduhkan hatimu.*")
            
            submitted = st.form_submit_button("✅ Klik Otomatis Berlangganan & Tembus 3 Lembar", use_container_width=True, type="primary")
            if submitted:
                if not nama or not email or not hp or not skill:
                    st.error("Wajib isi: Nama, Email, HP, Skill")
                else:
                    new_member = {"nama":nama,"role":role,"skill":skill,"zona":zona,"arsip":1,"vote":1,"status":"Berlangganan","email":email,"hp":hp}
                    st.session_state.members.append(new_member)
                    st.success(f"1x Tulis Berhasil! {nama} -> Tembus 3 Lembar Otomatis! 1 arsip = 1 vote")
                    st.balloons()

    with col_info:
        st.markdown("#### Kolom Bursa (Penerima)")
        st.info("Sebagai penerima dari banyaknya member yang sudah terkoneksi karena menggunakan aplikasi ini. Ada kolom bursa yang menginput nama (data/berkas) user. Karena banyaknya itulah disebut bursa, terpampang jelas seperti billboard bursa.")
        
        df = pd.DataFrame(st.session_state.members)
        st.dataframe(df[['nama','role','skill','vote']], use_container_width=True, height=200)
        
        # Grafik Volume
        st.markdown("**Grafik Volume Bursa**")
        chart_data = pd.DataFrame({"member": [m['nama'] for m in st.session_state.members], "vote": [m['vote'] for m in st.session_state.members]})
        st.bar_chart(chart_data, x="member", y="vote")
        
        st.markdown('<div class="nb-box">', unsafe_allow_html=True)
        st.markdown("**NB Kolom Syarat Berlangganan (HARGA HANYA DI SINI)**")
        st.markdown("Ketentuan member mesti berlangganan bulanan:")
        st.markdown("- **Employee Rp55.000**")
        st.markdown("- **Entrepreneur Rp75.000**")
        st.markdown("Cara berlangganan transfer via GoPay, OVO, DANA, Bank")
        st.markdown("**QR Code: 081291904422**")
        qr_bytes = make_qr("081291904422 - GoPay OVO DANA - Employee 55k Entrepreneur 75k")
        st.image(qr_bytes, caption="Scan untuk Berlangganan", width=200)
        st.caption("Jangan tampilkan harga di tempat lain, hanya di NB ini. Saat member klik otomatis berlangganan.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="carbon-line"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")
# --- LEMBAR 2 MERAH PINK ---
st.markdown('<div class="ncr-card ncr-pink">', unsafe_allow_html=True)
st.markdown("### LEMBAR 2 MERAH PINK - TEMBUSAN 1 | Ruang Interaksi - PALING BESAR")
st.caption("File: core.py + nasehat_mingguan.txt | Skema: Member sudah terdaftar & membayar & terikat, langsung terkoneksi terintegrasi")

c1, c2, c3 = st.columns(3)
c1.markdown('<div class="metric-card"><h2>{}</h2><small>Total Arsip / Vote</small></div>'.format(len(st.session_state.members)), unsafe_allow_html=True)
c2.markdown('<div class="metric-card"><h2>{}</h2><small>Employee</small></div>'.format(len([m for m in st.session_state.members if m['role']=='Employee'])), unsafe_allow_html=True)
c3.markdown('<div class="metric-card"><h2>{}</h2><small>Entrepreneur</small></div>'.format(len([m for m in st.session_state.members if m['role']=='Entrepreneur'])), unsafe_allow_html=True)

st.markdown("**Kolom Nasehat:** *Sudah membayar dan terikat berarti sudah memilih tumbuh bersama.*")

st.markdown("#### Kolom Bursa Tenaga Kerja + Grafik Volume")
st.markdown("Menjelaskan bursa tenaga kerja berapa banyak member terdaftar, contoh 1 nilai Pak Budi, bila semakin banyak mendaftar semakin banyak terlihat. Entrepreneur Pak Bambang direktur, Pak Johan owner, 1+1=2 member terdaftar dalam bursa, dst.")

df_full = pd.DataFrame(st.session_state.members)
st.dataframe(df_full, use_container_width=True)

st.markdown('<div class="carbon-line"></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.write("")
# --- LEMBAR 3 HIJAU ---
st.markdown('<div class="ncr-card ncr-hijau">', unsafe_allow_html=True)
st.markdown("### LEMBAR 3 HIJAU - TEMBUSAN 2 | Boarding / Storage - 5 Rak System")
st.caption("Jangan tampilkan harga di sini, sepakat di Lembar 1 Putih NB. Sebagai storage yang bisa di klik dengan input minta bimbingan")

tab1, tab2, tab3, tab4, tab5, tab_ai = st.tabs(["RAK 1 SOP", "RAK 2 ERP", "RAK 3 OEE", "RAK 4 KPI", "RAK 5 ALKITAB", "AI Mentor"])

with tab1:
    st.markdown("**RAK 1 SOP Kebersihan & Obedience**")
    st.markdown("- SOP Kebersihan: Bersihkan ruang kerja sebelum mulai")
    st.markdown("- SOP Obedience: Ikuti instruksi dengan setia")
    st.markdown("- Format app.py 280-290")
with tab2:
    st.markdown("**RAK 2 ERP Jam 9**")
    st.markdown("- ERP: Semua owner kecil masuk dalam ERP")
    st.markdown("- Jam 9: Disiplin waktu, komitmen jam 9 pagi standup")
with tab3:
    st.markdown("**RAK 3 OEE 95%**")
    st.markdown("- Overall Equipment Effectiveness target 95%")
    st.markdown("- Fokus: Availability, Performance, Quality")
with tab4:
    st.markdown("**RAK 4 KPI**")
    st.markdown("- KPI mengukur tumbuhmu")
    st.markdown("- Input: 1 arsip = 1 vote = nilai bursa")
with tab5:
    st.markdown("**RAK 5 ALKITAB & Ruach Hakadosh**")
    st.markdown("- Landasan Alkitabiah bimbingan tuntunan Ruach Hakadosh spiritualitas")
    st.markdown("- Ayat: 'Hati yang gembira adalah obat yang manjur'")
with tab_ai:
    st.markdown("**Input Bimbingan AI Mentor**")
    bimbingan = st.text_area("Minta bimbingan dan keteguhan juga saran dan nasehat")
    if st.button("Kirim ke Storage"):
        st.success("Bimbingan tersimpan di Lembar 3 Hijau - akan dibalas oleh Ruach Hakadosh")

st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
st.caption("Flowchart: [QR GATE] -> [FORM ORG LENGKAP] -> [VALIDASI] ---carbon copy garis putus---> 3 LEMBAR TEMBUS OTOMATIS | No st.button inside st.form - only form_submit_button | Tarif hanya di NB Lembar 1")
