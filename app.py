import streamlit as st
import io
from gtts import gTTS
import os

st.set_page_config(page_title="Ruang Teduh AI", page_icon="🌿", layout="centered")

# SESSION
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

def tts_player(text, label=""):
    try:
        tts = gTTS(text, lang='id', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3', autoplay=False)
        if label:
            st.caption(f"🔊 {label}")
    except Exception as e:
        st.error(f"Audio error: {e}")

def load_nasehat_default():
    # Coba baca dari file nasehat_mingguan.txt yang bisa lo edit di Github 1 minggu 2-3x
    if os.path.exists("nasehat_mingguan.txt"):
        try:
            with open("nasehat_mingguan.txt", "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
                if lines:
                    return lines
        except:
            pass
    # Default kalau file belum ada
    return [
        "Minggu ini: Dari mata turun ke hati, kerja adalah ibadah - Kolose 3:23",
        "SOP hari ini: 5 menit lebih awal, checklist 5S, lapor harian",
        "ERP: Cek stok realtime di GDrive, sinkron Github",
        "OEE: Jaga Availability 90%, Quality 99% - jiwa lestari di proses",
        "KPI: Fokus 3 hal - kehadiran, penyelesaian task, kolaborasi",
        "Spiritual MALKHUTKHA: Staff jadi Leader, bukan soal gaji tapi skill naik",
        "Hackathon hari ini: Assemblying suara kebaikan, bersaing dengan kasih"
    ]

def render_r3():
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0a3d2e,#1a6d4e);padding:20px;border-radius:15px;color:white;border:2px solid gold">
    <h2>🌟 RUANG 3 - MEMBER AREA TETAP</h2>
    <p>Full Bimbingan Suara • Teks Nasehat Gonta-Ganti Mingguan • Visual Optional</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    
    tier = st.session_state.last_tier or "Employee 20rb/bulan"
    st.success(f"✅ Member Aktif: {tier} | Pesan awal: \"{st.session_state.last_pesan[:50]}...\"")
    
    # Load nasehat
    if not st.session_state.nasehat_list:
        st.session_state.nasehat_list = load_nasehat_default()
    
    st.markdown("### 📜 Teks Nasehat Minggu Ini (Bisa Dibaca Jadi Suara)")
    st.caption("Edit file `nasehat_mingguan.txt` di Github 1 minggu 2-3x atau 1x seminggu - auto update jadi suara. Visual gak usah dipaksain kalo gak perlu.")
    
    # Toggle visual
    show_visual = st.checkbox("Tampilkan Visual Mata->Hati->Brain (optional)", value=False)
    if show_visual:
        try:
            st.image("perjalanan_cinta_petunjuk.webp", use_container_width=True)
        except:
            st.info("Visual: Dari mata datangnya kasih, diterima hati dan brain, jiwa lestari")
    
    st.divider()
    
    # List nasehat dengan suara
    for i, nasehat in enumerate(st.session_state.nasehat_list):
        col1, col2 = st.columns([4,1])
        with col1:
            st.write(f"**{i+1}. {nasehat}**")
        with col2:
            if st.button("🔊", key=f"tts_r3_{i}"):
                tts_player(nasehat, f"Nasehat {i+1}")
    
    st.divider()
    
    if st.button("🏆 Bacakan SEMUA Nasehat Minggu Ini (Assemblying Hackathon)", type="primary", use_container_width=True):
        all_text = " ".join(st.session_state.nasehat_list)
        tts_player(all_text, "Full Bimbingan Mingguan - All Indikator SOP ERP OEE KPI")
    
    st.markdown("### ✏️ Ganti Teks Nasehat Cepat (Tanpa Ngoding)")
    new_nasehat = st.text_area("Tulis nasehat baru (1 baris = 1 nasehat, enter untuk baru)", height=150, 
                               placeholder="Contoh:\nSenin: Fokus SOP kebersihan\nSelasa: ERP update stok\nRabu: OEE check mesin")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➕ Tambah ke R3", use_container_width=True):
            if new_nasehat:
                added = [line.strip() for line in new_nasehat.split("\n") if line.strip()]
                st.session_state.nasehat_list.extend(added)
                st.success(f"Ditambah {len(added)} nasehat! Sekarang total {len(st.session_state.nasehat_list)}")
                st.rerun()
    with c2:
        if st.button("🔄 Reset ke Default File", use_container_width=True):
            st.session_state.nasehat_list = load_nasehat_default()
            st.rerun()
    
    st.divider()
    colA, colB = st.columns(2)
    with colA:
        if st.button("⬅️ Kembali ke R1", use_container_width=True):
            st.session_state.page = "R1"
            st.rerun()
    with colB:
        if st.button("⬅️ Kembali ke R2", use_container_width=True):
            st.session_state.page = "R2"
            st.rerun()

def render_r1_r2(ruang_name):
    # Header
    ayat = "Kolose 3:23 - Bekerja untuk Tuhan..." if ruang_name=="R1" else "Kolose 3:23 Advance - Level MALKHUTKHA"
    st.markdown(f"""
    <div style="background:#0a3d2e;padding:20px;border-radius:15px;color:white;border:2px solid #2ecc71">
    <h3>🎧 Suara Halus Ruang Teduh • v3.3 - R3 Ready</h3>
    <p><b>PERFECT FINAL • Memikat</b><br>Dari mata turun ke hati • Halus di kuping • Backsound embun pagi</p>
    <small>{ayat}</small>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    
    if ruang_name=="R2" and st.session_state.last_pesan:
        st.success(f"📩 Pesan Member dari R1 (Tier: {st.session_state.last_tier}):")
        st.info(f"\"{st.session_state.last_pesan}\"")
        if st.button("🔊 Bacakan Pesan Member di R2 (Halus)", key="bacakan_member_r2", type="primary"):
            tts_player(st.session_state.last_pesan, "Membacakan pesan member")
        st.divider()
    
    # Bimbingan singkat di R1 R2
    tier_sample = st.session_state.last_tier or ("Employee 20rb/bulan" if ruang_name=="R1" else "Entrepreneur 30rb/bulan")
    st.markdown(f"**Tier aktif:** {tier_sample}")
    
    # FORM R2 LOCKED - SAMA PERSIS KAYAK SCREENSHOT LO 22:24
    st.subheader(f"📝 Form Aktif Ruang {ruang_name[-1]} (v3.3) - Form R2 Locked")
    
    with st.form(f"form_{ruang_name}_v33", clear_on_submit=False):
        tier = st.selectbox("Pilih Tier", ["Employee 20rb/bulan", "Entrepreneur 30rb/bulan"], key=f"tier_{ruang_name}_v33")
        pesan = st.text_area("Pesan ke Admin Email & WA", 
                             placeholder="Ketik pesan dan kesan lo di sini...", 
                             key=f"pesan_{ruang_name}_v33", height=120,
                             value=st.session_state.last_pesan if ruang_name=="R1" else "")
        
        col1, col2 = st.columns(2)
        with col1:
            submit_admin = st.form_submit_button("Kirim ke Admin", use_container_width=True, type="primary")
        with col2:
            label_submit = f"Submit {ruang_name} & Lanjut" if ruang_name=="R1" else f"Submit {ruang_name}"
            submit_next = st.form_submit_button(label_submit, use_container_width=True)

        if submit_admin:
            if pesan:
                st.success(f"Terkirim ke Admin: {pesan[:60]}... | Tier: {tier}")
            else:
                st.warning("Tulis pesannya dulu bro")

        if submit_next:
            if pesan:
                st.session_state.last_pesan = pesan
                st.session_state.last_tier = tier
                if ruang_name == "R1":
                    st.session_state.page = "R2"
                    st.rerun()
                else:
                    # Di R2 Submit = jadi member
                    st.session_state.is_member = True
                    st.session_state.page = "R3"
                    st.rerun()
            else:
                st.warning("Tulis pesan dulu bro")

    # PAYMENT AREA KHUSUS R2
    if ruang_name=="R2":
        st.divider()
        st.markdown("### 💳 Pembayaran Member - 20rb / 30rb")
        st.write("Terima pembayaran dengan gopay dan ovo dan dana dan app akun lainnya cuman klik qr kode. Via bank bisa virtual nggak (bca BNI dll)")
        
        try:
            col_qr1, col_qr2 = st.columns(2)
            with col_qr1:
                st.image("qr_payment.png", caption="QR Gopay Ovo Dana", use_container_width=True)
            with col_qr2:
                st.info("**BCA Virtual:** 1234567890\n**BNI Virtual:** 9876543210\n**Gopay/Ovo/Dana:** Scan QR")
                st.write("Employee 20rb/bulan\nEntrepreneur 30rb/bulan")
        except:
            st.info("Upload file qr_payment.png untuk QR Gopay Ovo Dana")
        
        if st.button("✅ Saya Sudah Transfer - Masuk Ruang 3 (Member)", type="primary", use_container_width=True):
            st.session_state.is_member = True
            st.session_state.page = "R3"
            st.rerun()

    st.write("")
    if ruang_name == "R1":
        if st.button("➡️ Masuk ke Ruang 2 (R2)", key="to_r2_v33", use_container_width=True):
            st.session_state.page = "R2"
            st.rerun()
        if st.session_state.is_member:
            if st.button("🌟 Langsung ke Ruang 3 (Sudah Member)", key="to_r3_from_r1", use_container_width=True):
                st.session_state.page = "R3"
                st.rerun()
    else:
        if st.button("⬅️ Kembali ke R1", key="kembali_r1_v33", use_container_width=True):
            st.session_state.page = "R1"
            st.rerun()
        if st.button("🌟 Masuk Ruang 3", key="to_r3_from_r2", use_container_width=True):
            st.session_state.page = "R3"
            st.rerun()

# ROUTER
if st.session_state.page == "R3":
    render_r3()
elif st.session_state.page == "R1":
    render_r1_r2("R1")
else:
    render_r1_r2("R2")
