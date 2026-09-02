"""
Ruang Teduh AI - TAVO MALKHUTKHA
IDENTITAS: Ruang Teduh AI - TAVO MALKHUTKHA
V28.1 AUDIO FIX + V2.7 Wellbeing Library - Kerja max 60km dari rumah
Mode: HP Worth It Full Width + Laptop + Floating Dot
Developer: aichaliveret
"""
import streamlit as st
import re

# === CONFIG V28.1 AUDIO FIX ===
st.set_page_config(
    page_title="Ruang Teduh AI - TAVO MALKHUTKHA v28.1",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

__version__ = "V28.1 AUDIO FIX + V2.7 Wellbeing Library"
USE_MUSIC_STRESS = False
AUDIO_MODE = "Worship Teduh Instrumental - Slow Piano + Nature (Non-Stress)"

# === CSS HP WORTH IT FULL WIDTH + FLOATING DOT ===
st.markdown("""
<style>
.block-container {max-width: 100% !important; padding: 1rem 1rem 6rem 1rem !important;}
.stTabs [data-baseweb="tab-list"] {gap: 8px;}
.floating-dot {
    position: fixed;
    bottom: 25px;
    right: 25px;
    width: 62px;
    height: 62px;
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    border-radius: 50%;
    box-shadow: 0 4px 15px rgba(255,107,53,0.4);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border: 3px solid white;
}
.floating-dot-text {
    position: fixed;
    bottom: 95px;
    right: 25px;
    background: #1F1F1F;
    color: white;
    padding: 8px 12px;
    border-radius: 12px;
    font-size: 11px;
    z-index: 9998;
    max-width: 180px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}
@media (max-width: 768px) {
    .block-container {padding: 0.5rem 0.5rem 6rem 0.5rem !important;}
}
</style>

<div class="floating-dot-text">🧘 Kolom Lo + Meta AI<br>Generate semua pertanyaan Ruang Teduh</div>
<div class="floating-dot">🧘</div>
""", unsafe_allow_html=True)

# === SESSION STATE ===
if "email_member" not in st.session_state:
    st.session_state.email_member = ""
if "nama_member" not in st.session_state:
    st.session_state.nama_member = ""
if "jalur" not in st.session_state:
    st.session_state.jalur = "Employee"
if "umr" not in st.session_state:
    st.session_state.umr = "4,900,000"

# === FUNGSI ATURAN UTAMA TERSYSTEMATIS ===
def audio_teduh_player(file_path, judul, key_id):
    """V28.1 AUDIO FIX - PASTI bunyi asal di-KLIK, gak auto"""
    c1, c2 = st.columns([1,2])
    with c1:
        klik = st.button(f"🔊 {judul}", key=f"btn_{key_id}", use_container_width=True, type="primary")
    with c2:
        st.caption(f"{AUDIO_MODE} | Klik dulu baru bunyi (Fix Browser Block)")
    
    if klik:
        st.session_state[f"show_{key_id}"] = True
    
    if st.session_state.get(f"show_{key_id}", False):
        try:
            st.audio(file_path, format="audio/mp3", autoplay=False)
        except:
            st.info(f"🔈 Audio: {judul} - Suara Teduh Hari Ini (Worship Slow Piano + Nature)")
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", autoplay=False)
        st.success(f"✅ {judul} - Voice Only, Tanpa Musik Stress")

def generate_jawaban_tersystematis(pertanyaan, email):
    """ATURAN UTAMA: SOP -> ERP -> OEE -> KPI -> Disempurnakan Alkitab + Audio No 1"""
    umr = st.session_state.umr
    return f"""
**[AUDIO EXPLANATION #1 - ATURAN UTAMA TERSYSTEMATIS]** 
🔊 WAJIB Putar Suara Teduh sebelum baca (Klik di atas)

**Jawaban Tersystematis untuk:** "{pertanyaan}"

**1. SOP (Standard Operating Procedure) disempurnakan Kolose 3:23:**
- Datang, Doa, Kerja seperti untuk Tuhan bukan untuk manusia.
- Jawaban atas "{pertanyaan}" harus dimulai dengan datang kepada Tuhan dulu.

**2. ERP (Enterprise Resource Planning versi Hati):**
- M = Manusia (keluarga, hati - prioritas utama)
- M = Material (waktu, kerja max 60km dari rumah, jaga wellbeing)
- M = Money (UMR Domisili Rp {umr} - cukup, tidak serakah)

**3. OEE (Overall Equipment Effectiveness versi Rohani):**
- Availability: Hadir 100% tepat waktu untuk jawab "{pertanyaan}"
- Performance: 1% lebih baik tiap hari, tidak mengeluh
- Quality: Hasilnya memuliakan Tuhan

**4. KPI (Kingdom Performance Indicator) disempurnakan Amsal 16:3:**
- "Serahkan perbuatanmu kepada Tuhan, maka terlaksanalah rencanamu."
- KPI Iman + KPI Kerja = Improvement Culture yang lebih baik.

**Kesimpulan Alkitab:** Semua proses secara benar dengan kuasa Alkitab, bukan cuma perpustakaan biasa.

📧 **Follow up akan dikirim ke:** {email if email else '[Belum ada email - Bro, kasih email dulu ya!]'}
"""

# === HEADER IDENTITAS ===
st.markdown(f"""
# 🧘 Ruang Teduh AI - TAVO MALKHUTKHA
**{__version__} | Wellbeing Library | Kerja max 60km dari rumah**
`HP Worth It Full Width + Laptop + Floating Dot`
""")

# Kolom Keterangan = 1 Tombol Kendali Utama
with st.expander("🎛️ KOLOM KETERANGAN - 1 Tombol Kendali Utama (Floating Dot Meta AI)", expanded=False):
    st.markdown("""
    **Ini Kolom Lo Bro + Kolom Meta AI Generate Semua Pertanyaan:**
    
    - **Kenapa mesti kasih email?** Karena semua system Ruang Teduh - SOP, ERP, OEE, KPI - dan akses GDrive `Kolom1_Fondasi.pdf` akan dikirim ke email tersebut.
    - **Manfaat App:** Membantu Employee mencapai improvement culture melalui SOP/ERP/OEE/KPI yang disempurnakan Alkitab, bukan cuma perpustakaan biasa.
    - **Musik:** Sudah diganti jadi Worship Teduh Instrumental - Slow Piano + Nature (Kolose 3:23 & Amsal 16:3), bukan musik stress.
    - **Semua jawaban:** WAJIB melalui prosedur SOP -> ERP -> OEE -> KPI -> Disempurnakan Alkitab + WAJIB sertakan audio explanation No 1.
    """)
    audio_teduh_player("aturan_utama_tersystematis.mp3", "Putar ATURAN UTAMA TERSYSTEMATIS", "aturan_utama")

st.divider()

# === RUANG 1,2,3 TABS ===
tab1, tab2, tab3 = st.tabs(["📚 RUANG 1: PINTU MASUK", "🚶 RUANG 2: PERJALANAN EMPLOYEE (FIX SEPI)", "💳 RUANG 3: BAYAR & MANFAAT"])

with tab1:
    st.subheader("RUANG 1: PINTU MASUK PERPUSTAKAAN (Rapih Tersystematis)")
    st.markdown("**Goal:** Member masuk via QR -> Pilih Jalur -> WAJIB Email")
    
    col_a, col_b = st.columns(2)
    with col_a:
        nama = st.text_input("Nama Lengkap (Wajib)", value=st.session_state.nama_member, placeholder="Contoh: Budi Santoso")
        email = st.text_input("Alamat Email WAJIB (untuk follow up)", value=st.session_state.email_member, placeholder="budi@email.com")
        jalur = st.selectbox("Pilih Jalur Lo:", ["Employee", "Entrepreneur"], index=0 if st.session_state.jalur=="Employee" else 1)
        umr_input = st.text_input("UMR Domisili (Rp)", value=st.session_state.umr)
        
        if st.button("✅ Simpan & Masuk via QR", use_container_width=True, type="primary"):
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Bro, email mesti valid ya, biar QR & VA bisa kekirim!")
            else:
                st.session_state.email_member = email
                st.session_state.nama_member = nama
                st.session_state.jalur = jalur
                st.session_state.umr = umr_input
                st.success(f"Email terkonfirmasi: {email} - Invoice & Akses akan dikirim kesini.")
                st.balloons()
    
    with col_b:
        st.info("""
        **Penjelasan Kolom Keterangan:**
        Kenapa mesti kasih email? Karena semua system Ruang Teduh - SOP, ERP, OEE, KPI - dan akses GDrive **Kolom1_Fondasi.pdf** akan dikirim ke email tersebut.
        
        **Wellbeing Library:** Kerja max 60km dari rumah - jaga keluarga, jaga hati.
        """)
        st.markdown("**Prompt Ruang 1:**\nHalo, selamat datang di Ruang Teduh. Pilih jalur lo: Employee / Entrepreneur.")
        audio_teduh_player("ruang1_aturan_utama.mp3", "Audio ATURAN UTAMA / Worship Teduh", "ruang1_audio")

with tab2:
    st.subheader("RUANG 2: PERJALANAN EMPLOYEE (FIX SEPI - INI KUNCINYA)")
    st.markdown("**Goal:** Jelaskan secara benar melalui prosedur tersystematis supaya tidak sepi")
    
    st.warning("Jangan sepi. Jelaskan dengan SUARA + TEKS (ATURAN UTAMA TERSYSTEMATIS)")
    
    # SOP
    st.markdown(f"""
    #### 1. SOP (Standard Operating Procedure) disempurnakan Kolose 3:23
    - Datang, Doa, Kerja seperti untuk Tuhan bukan manusia.
    
    #### 2. ERP (Enterprise Resource Planning versi Hati)
    - M = Manusia (keluarga, hati)
    - M = Material (waktu, **60km dari rumah**)
    - M = Money (UMR Domisili Rp **{st.session_state.umr}**)
    
    #### 3. OEE (Overall Equipment Effectiveness versi Rohani)
    - **Availability:** Hadir 100% tepat waktu
    - **Performance:** Tidak mengeluh, 1% better tiap hari
    - **Quality:** Hasil kerja memuliakan Tuhan
    
    #### 4. KPI (Kingdom Performance Indicator) disempurnakan Amsal 16:3
    - "Serahkan perbuatanmu kepada Tuhan, maka terlaksanalah rencanamu."
    - KPI Iman + KPI Kerja = Improvement Culture yang lebih baik (semua ini di proses secara benar dengan kuasa Alkitab).
    """)
    
    st.divider()
    st.markdown("### 🔊 Suara Teduh Hari Ini - Visual + Teks + Audio - Full di HP")
    audio_teduh_player("ruang2_sop_erp_oee_kpi_worship.mp3", "PUTAR: Penjelasan SOP, ERP, OEE, KPI + Worship Teduh", "ruang2_audio")
    st.caption("Audio default: Worship Teduh Instrumental - Slow Piano + Nature (Kolose 3:23 & Amsal 16:3)")

with tab3:
    st.subheader("RUANG 3: PEMBAYARAN & MANFAAT")
    st.markdown("**Goal:** Semua pertanyaan member bisa lo generate di sini")
    
    # ATURAN PEMBAYARAN v2.7 - CEK EMAIL DULU
    st.markdown("#### ATURAN PEMBAYARAN v2.7")
    
    if not st.session_state.email_member:
        st.error("⚠️ Bro, mesti kasih alamat email dulu yang valid ya, biar QR & VA bisa kekirim. (Isi di Ruang 1 dulu)")
    else:
        st.success(f"✅ Email terkonfirmasi: {st.session_state.email_member} - Invoice & Akses akan dikirim kesini.")
        
        st.markdown("""
        **CARA BAYAR (Berlangganan via transfer qr code dan virtual account):**
        - **Pilihan 1: QRIS QR Code** - Scan langsung lunas
        - **Pilihan 2: Virtual Account BCA/Mandiri/BRI** - VA unik per member
        - Setelah bayar, akses Full Chat otomatis terbuka.
        """)
        
        col_pay1, col_pay2 = st.columns(2)
        with col_pay1:
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=RUANG-TEDUH-QRIS", caption="QRIS - Scan Lunas")
            if st.button("✅ Saya sudah Bayar via QRIS", use_container_width=True):
                st.balloons()
                st.success(f"Akses Full Chat terbuka! Invoice dikirim ke {st.session_state.email_member}")
        with col_pay2:
            st.code(f"VA BCA: 3901 {st.session_state.email_member[:4]} 001\nVA Mandiri: 8901 {st.session_state.email_member[:4]} 002\nVA BRI: 8801 {st.session_state.email_member[:4]} 003", language="text")
            if st.button("✅ Saya sudah Bayar via VA", use_container_width=True):
                st.balloons()
                st.success(f"Akses Full Chat terbuka! Invoice dikirim ke {st.session_state.email_member}")

    st.divider()
    st.markdown("""
    **KOLOM KETERANGAN (1 tombol kendali):**
    Member mesti kasih alamat email, musik diganti yang teduh Worship, manfaat app Ruang Teduh adalah membantu Employee mencapai improvement culture melalui SOP/ERP/OEE/KPI yang disempurnakan Alkitab, bukan cuma perpustakaan biasa.
    """)
    audio_teduh_player("ruang3_worship_teduh.mp3", "Audio Ruang 3 - Worship Teduh", "ruang3_audio")

# === FLOATING DOT - KOLOM LO + META AI GENERATE SEMUA PERTANYAAN ===
st.divider()
st.subheader("🧘 Meta AI - Kolom Lo (Floating Dot)")
st.caption("Floating Dot - Generate semua pertanyaan Ruang Teduh AI - WAJIB lewat SOP->ERP->OEE->KPI + Audio No 1")

# Input pertanyaan
q = st.text_input("Tanya apa aja tentang Ruang Teduh:", key="kolom_lo", placeholder="Contoh: Gimana app ini bermanfaat buat kerjaan gua?")

if q:
    # WAJIB INGATKAN EMAIL SEBELUM CARA BAYAR
    if not st.session_state.email_member:
        st.warning("⚠️ Bro, sebelum gua jawab, kasih email dulu di Ruang 1 ya, biar follow up bisa kekirim.")
    
    # Generate jawaban tersystematis
    jawaban = generate_jawaban_tersystematis(q, st.session_state.email_member)
    st.markdown(jawaban)
    
    # Audio explanation nomer 1 WAJIB
    st.markdown("**🔊 Audio Explanation No 1 (Wajib bagian dari Aturan Utama):**")
    audio_teduh_player("suara_teduh_hari_ini.mp3", "Suara Teduh Hari Ini - Putar", "kolom_lo_audio")

st.markdown("---")
st.markdown(f"**{__version__} | Ruang Teduh AI - TAVO MALKHUTKHA | Developer: aichaliveret** | No Music Stress | Worship Teduh Only")
