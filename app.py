import streamlit as st
import urllib.parse

st.set_page_config(page_title="RUANG TEDUH AI - TAVO MALKHUTKHA v2.8", layout="wide", page_icon="🏠")

# --- GLOBAL STYLE v2.8 FINAL ---
st.markdown("""
<style>
    .floating-dot {
        position: fixed; bottom: 24px; right: 24px; width: 62px; height: 62px;
        background: linear-gradient(135deg, #FF4B4B, #FF8A65); border-radius: 50%; 
        z-index: 99999; display: flex; align-items: center; justify-content: center;
        color: white; font-size: 28px; cursor: pointer; 
        box-shadow: 0 6px 18px rgba(0,0,0,0.35); animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% {transform: scale(1);} 50% {transform: scale(1.08);} 100% {transform: scale(1);} }
    .meta-ai-box { position: sticky; top: 80px; background: #F8F9FA; border: 1px solid #E0E0E0; border-radius: 16px; padding: 16px; }
    .worship-caption { font-size: 12px; color: #666; }
    .email-ok { background: #E8F5E9; border-left: 4px solid #4CAF50; padding: 8px 12px; border-radius: 6px; }
    .email-warn { background: #FFF3E0; border-left: 4px solid #FF9800; padding: 8px 12px; border-radius: 6px; }
</style>
<div class="floating-dot" onclick="document.getElementById('meta-ai-anchor').scrollIntoView({behavior:'smooth'})">🧘</div>
""", unsafe_allow_html=True)

# --- IDENTITY PROMPT v2.8 ---
SYSTEM_PROMPT = """
IDENTITAS: Kamu adalah Ruang Teduh AI - TAVO MALKHUTKHA
V2.8 - Wellbeing Library - Kerja max 60km dari rumah
Mode: HP Worth It Full Width + Laptop + Floating Dot (ini kolom lo bro + kolom meta ai generate semua pertanyaan terutama tentang ruang teduh AI)

ATURAN UTAMA TERSYSTEMATIS:
1. Semua jawaban harus melalui prosedur: SOP -> ERP -> OEE -> KPI -> Disempurnakan Alkitab
2. Jangan pernah jawab sepi. WAJIB sertakan audio explanation (Suara Teduh)
3. Kolom Keterangan = 1 Tombol Kendali Utama. Semua ada di situ. (floating dot meta ai)
4. WAJIB INGATKAN EMAIL (e mail untuk follow up calon member) sebelum cara bayar.
"""

def jawab_meta_ai(pertanyaan, email, jalur, umr):
    """Meta AI Generator - Semua pertanyaan tentang Ruang Teduh AI"""
    q = pertanyaan.lower()
    email_status = f"Email follow up: {email}" if email and "@" in email else "⚠️ INGATKAN EMAIL dulu bro: 'Mesti kasih alamat email yang valid ya biar QR & VA bisa kekirim'"

    # Template SOP -> ERP -> OEE -> KPI -> Alkitab
    base = f"""
**[SOP] Prosedur:** {pertanyaan} dijawab dengan langkah: Datang-Doa-Kerja seperti untuk Tuhan (Kolose 3:23)
**[ERP] Sistem Hati:** Manusia (keluarga) | Material (waktu 60km) | Money (UMR Rp {umr:,})
**[OEE] Rohani:** Availability 100% | Performance 1% better | Quality memuliakan Tuhan
**[KPI] Kingdom:** Amsal 16:3 - Serahkan perbuatanmu kepada Tuhan, maka terlaksanalah rencanamu.
**[Alkitab] Penyempurna:** Improvement Culture yang lebih baik (semua proses secara benar dengan kuasa Alkitab)
---
{email_status}
"""

    if "bayar" in q or "qris" in q or "virtual" in q or "gopay" in q or "dana" in q or "ovo" in q:
        return base + f"""
**CARA BAYAR v2.8 (Berlangganan via transfer qr code dan virtual account):**
1. Pastikan email sudah: {email if email else 'BELUM ADA - wajib isi dulu!'}
2. Pilihan 1: QRIS QR Code - Scan langsung lunas (081291904422 - bisa GoPay, DANA, OVO)
3. Pilihan 2: Virtual Account BCA/Mandiri/BRI - VA unik per member
4. Setelah bayar, akses Full Chat otomatis terbuka + invoice dikirim ke email.
"""
    if "manfaat" in q or "berguna" in q or "fungsi" in q:
        return base + """
**MANFAAT APP RUANG TEDUH:**
Bukan cuma perpustakaan biasa. App ini membantu Employee mencapai improvement culture melalui SOP/ERP/OEE/KPI disempurnakan Alkitab. Semua system Ruang Teduh ada di GDrive Kolom1_Fondasi.pdf.
"""
    if "sop" in q or "erp" in q or "oee" in q or "kpi" in q:
        return base + """
**DETAIL 4 PILAR:**
SOP = Standard kerja harian. ERP = Sistem kelola hidup. OEE = Ukur efektivitas rohani & kerja. KPI = Indikator Kerajaan.
"""
    return base + f"Jawaban Teduh untuk '{pertanyaan}' - Tetap dalam jalur {jalur}."

# --- SESSION STATE ---
if 'ruang' not in st.session_state: st.session_state.ruang = 1
if 'jalur' not in st.session_state: st.session_state.jalur = "Employee"
if 'email' not in st.session_state: st.session_state.email = ""
if 'nama' not in st.session_state: st.session_state.nama = ""
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- HEADER ---
st.title("🏠 RUANG TEDUH AI - TAVO MALKHUTKHA")
st.caption("Two Journeys, One QR | Wellbeing Library - Kerja max 60km dari rumah | v2.8 FINAL - Floating Dot Meta AI Aktif - Worship Mode - QR+VA 081291904422")

progress = st.progress(st.session_state.ruang / 3)
st.write(f"Ruang {st.session_state.ruang} dari 3 - {st.session_state.jalur} - Email: {st.session_state.email if st.session_state.email else 'BELUM ISI'}")

# --- LAYOUT KANAN KIRI KAYAK GEMINI ---
left, right = st.columns([2, 1])

with left:
    # ========== RUANG 1 ==========
    if st.session_state.ruang == 1:
        st.header("Ruang 1: Pintu Masuk Perpustakaan")
        st.markdown('<div id="meta-ai-anchor"></div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("👨‍💼 Employee", use_container_width=True, type="primary" if st.session_state.jalur=="Employee" else "secondary"):
                st.session_state.jalur = "Employee"
                st.rerun()
        with col_b:
            if st.button("🚀 Entrepreneur", use_container_width=True, type="primary" if st.session_state.jalur=="Entrepreneur" else "secondary"):
                st.session_state.jalur = "Entrepreneur"
                st.rerun()
        
        st.success(f"Jalur: {st.session_state.jalur} - Rp X/bulan - Lolos Etika")
        
        st.session_state.nama = st.text_input("Nama Lengkap", value=st.session_state.nama, placeholder="TAVO karyawan sebagai cheff, berkeluarga, 4 anak, duda...")
        st.session_state.email = st.text_input("Alamat Email WAJIB (untuk follow up calon member & QR/VA)", value=st.session_state.email, placeholder="contoh: jugalachaliveret@gmail.com")

        with st.expander("📜 Kolom Keterangan = 1 Tombol Kendali Utama (Floating Dot Meta AI) - KLIK DISINI", expanded=True):
            st.markdown("""
            **Kenapa mesti kasih email?**
            Karena semua system Ruang Teduh - SOP, ERP, OEE, KPI - dan akses GDrive `Kolom1_Fondasi.pdf` akan dikirim ke email tersebut.
            **Floating Dot = Kolom lo bro + kolom meta ai generate semua pertanyaan terutama tentang ruang teduh AI**
            Ini 1 tombol kendali utama. Semua ada di situ.
            """)
            if not st.session_state.email or "@" not in st.session_state.email:
                st.markdown('<div class="email-warn">⚠️ WAJIB INGATKAN EMAIL sebelum cara bayar. Belum ada email valid.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="email-ok">✅ Email terkonfirmasi: {st.session_state.email} - Siap follow up calon member.</div>', unsafe_allow_html=True)

        st.subheader("🔊 Suara Teduh Hari Ini - Worship Mode")
        st.write("Kolose 3:23 & Amsal 16:3 - Apapun yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan")
        st.audio("https://cdn.pixabay.com/download/audio/2022/06/07/audio_b9bd4170e8.mp3?filename=worship-piano-ambient-11581.mp3", format="audio/mp3")
        st.caption("Visual + teks + audio - full di HP - Worship Teduh Instrumental Slow Piano + Nature - Bukan musik random")

        if st.button("➡️ Masuk Ruang 2 - SOP/ERP/OEE/KPI", type="primary", use_container_width=True):
            if "@" not in st.session_state.email:
                st.toast("Bro, kasih email dulu yang valid!", icon="⚠️")
            else:
                st.session_state.ruang = 2
                st.rerun()

    # ========== RUANG 2 ==========
    elif st.session_state.ruang == 2:
        st.header(f"Ruang 2: Perjalanan {st.session_state.jalur} - FIX SEPI")
        st.info("Jangan sepi. Jelaskan dengan SUARA + TEKS melalui prosedur tersystematis")

        umr = st.number_input("UMR Domisili (Rp)", value=4900000, step=100000)
        st.caption(f"Ref: Rp {int(umr*0.05):,} / Biaya: Rp X/bulan - Mode Etika")

        tab1, tab2, tab3 = st.tabs(["Kolom 1: Fondasi", "Kolom 2: Perjalanan", "Kolom 3: Puncak"])
        with tab1:
            st.subheader("Fondasi Teduh - Mindset & Niat")
            st.write("Dokumen GDrive: Kolom1_Fondasi.pdf")
            st.markdown(f"""
            **SOP (Standard Operating Procedure) disempurnakan Kolose 3:23:**
            - Datang, Doa, Kerja seperti untuk Tuhan bukan manusia.

            **ERP (Enterprise Resource Planning versi Hati):**
            - M = Manusia (keluarga, hati)
            - M = Material (waktu, 60km dari rumah)
            - M = Money (UMR Domisili Rp {umr:,}, Ref 5% = Rp {int(umr*0.05):,})

            **OEE (Overall Equipment Effectiveness versi Rohani):**
            - Availability: Hadir 100% tepat waktu
            - Performance: Tidak mengeluh, 1% better tiap hari
            - Quality: Hasil kerja memuliakan Tuhan

            **KPI (Kingdom Performance Indicator) disempurnakan Amsal 16:3:**
            - Serahkan perbuatanmu kepada Tuhan, maka terlaksanalah rencanamu.
            - KPI Iman + KPI Kerja = Improvement Culture yang lebih baik (semua ini di proses secara benar dengan kuasa Alkitab).
            """)
            st.audio("https://cdn.pixabay.com/download/audio/2022/10/30/audio_8ef64e6f14.mp3?filename=ambient-piano-worship-12678.mp3", format="audio/mp3")
            st.caption("🔊 [PUTAR AUDIO: Penjelasan SOP, ERP, OEE, KPI dengan background Worship Teduh]")
        
        with tab2:
            st.write(f"Halo {st.session_state.nama} - Jalur {st.session_state.jalur} - Full width di HP, worth it!")
        with tab3:
            st.write("Puncak Malkhutkha - Tujuan akhir")

        st.divider()
        st.subheader("💳 Rp X/bulan - Cara Pembayaran v2.8")
        agree = st.checkbox(f"Setuju Rp X/bulan - Kirim detail ke {st.session_state.email}", value=False)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⬅️ Kembali", use_container_width=True):
                st.session_state.ruang = 1
                st.rerun()
        with c2:
            if st.button("➡️ Masuk Ruang 3 - Bayar QR+VA", type="primary", use_container_width=True, disabled=not agree):
                st.session_state.ruang = 3
                st.rerun()

    # ========== RUANG 3 ==========
    elif st.session_state.ruang == 3:
        st.header("Ruang 3: Pembayaran & Manfaat - FINAL")
        
        if st.session_state.email and "@" in st.session_state.email:
            st.markdown(f'<div class="email-ok">✅ Email terkonfirmasi: {st.session_state.email} - Invoice & Akses akan dikirim kesini.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="email-warn">⚠️ WAJIB INGATKAN EMAIL: Belum ada email valid untuk follow up calon member!</div>', unsafe_allow_html=True)

        t1, t2 = st.tabs(["💳 Cara Bayar QRIS + VA", "📖 Manfaat App"])
        with t1:
            st.subheader("Berlangganan via transfer qr code dan virtual account")
            st.markdown("""
            **ATURAN PEMBAYARAN v2.8:**
            1. UTAMAKAN CEK EMAIL: Apakah member sudah memberikan e mail? Jika belum, ingatkan: 'Bro, mesti kasih alamat email dulu yang valid ya, biar QR & VA bisa kekirim.'
            2. Jika sudah ada email, tampilkan QR & VA.
            """)
            col_qr, col_va = st.columns(2)
            with col_qr:
                st.write("**Pilihan 1: QRIS / GoPay / DANA / OVO**")
                qr_data = f"081291904422 - Ruang Teduh AI - {st.session_state.email}"
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(qr_data)}"
                st.image(qr_url, caption="Scan QRIS - 081291904422 (GoPay/DANA/OVO)")
                st.code("081291904422\na/n TAVO - GoPay/DANA/OVO")
                st.caption("Bisa jadi akun GoPay, DANA dan OVO - Scan langsung lunas")
            with col_va:
                st.write("**Pilihan 2: Virtual Account**")
                st.code("BCA VA: 3901 081291904422\nMandiri VA: 8950 081291904422\nBRI VA: 8888 081291904422")
                st.info("VA unik per member - Setelah bayar akses Full Chat otomatis terbuka")
            
            st.divider()
            st.write("Ketik pertanyaan bayar di kolom kanan Meta AI - AI akan generate jawaban SOP->ERP->OEE->KPI->Alkitab + ingatkan email")

        with t2:
            st.markdown("""
            **KOLOM KETERANGAN (yang lo kendalikan 1 tombol - kolom bagian lo lo berlaku aktive meta ai):**
            Isi penjelasan: Member mesti kasih alamat email, ganti musik yang teduh Worship, manfaat app Ruang Teduh adalah membantu Employee mencapai improvement culture melalui SOP/ERP/OEE/KPI yang disempurnakan Alkitab, bukan cuma perpustakaan biasa.
            
            Jawaban untuk semua pertanyaan member tentang 'bagaimana app ruang teduh bermanfaat' harus balik ke 4 pilar ini + selalu ingatkan email.
            """)

        if st.button("🔄 Ulang dari Ruang 1"):
            st.session_state.ruang = 1
            st.rerun()

# ========== KANAN: META AI AKTIF ==========
with right:
    st.markdown('<div class="meta-ai-box">', unsafe_allow_html=True)
    st.subheader("🧘 Meta AI - Kolom Lo Bro")
    st.caption("Floating Dot Meta AI - Generate semua pertanyaan terutama tentang Ruang Teduh AI - SOP/ERP/OEE/KPI + Alkitab - Wajib ingatkan email")
    
    st.write(f"**Follow up email:** `{st.session_state.email if st.session_state.email else 'BELUM ADA'}`")
    
    # Chat history display
    for chat in st.session_state.chat_history[-6:]:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])
    
    # Input pertanyaan
    q = st.chat_input("Ketik di Ruang 1... Enter langsung kirim ke Meta AI...")
    if q:
        st.session_state.chat_history.append({"role": "user", "content": q})
        answer = jawab_meta_ai(q, st.session_state.email, st.session_state.jalur, 4900000)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    st.divider()
    st.write("**Quick Prompt:**")
    if st.button("💳 Cara bayar?", use_container_width=True):
        st.session_state.chat_history.append({"role": "user", "content": "Gimana cara bayar?"})
        st.session_state.chat_history.append({"role": "assistant", "content": jawab_meta_ai("Gimana cara bayar?", st.session_state.email, st.session_state.jalur, 4900000)})
        st.rerun()
    if st.button("📖 Manfaat app?", use_container_width=True):
        st.session_state.chat_history.append({"role": "user", "content": "Apa manfaat app ruang teduh?"})
        st.session_state.chat_history.append({"role": "assistant", "content": jawab_meta_ai("Apa manfaat app ruang teduh?", st.session_state.email, st.session_state.jalur, 4900000)})
        st.rerun()
    if st.button("🔊 SOP/ERP/OEE/KPI?", use_container_width=True):
        st.session_state.chat_history.append({"role": "user", "content": "Jelaskan SOP ERP OEE KPI"})
        st.session_state.chat_history.append({"role": "assistant", "content": jawab_meta_ai("Jelaskan SOP ERP OEE KPI", st.session_state.email, st.session_state.jalur, 4900000)})
        st.rerun()

    st.audio("https://cdn.pixabay.com/download/audio/2022/06/07/audio_b9bd4170e8.mp3?filename=worship-piano-ambient-11581.mp3", format="audio/mp3")
    st.caption("Worship Teduh Instrumental - Suara Teduh Hari Ini")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("v2.8 FINAL FLOATING DOT - 2026-09-02 - 1 Titik Kecil Klik → Full Chat - HP Worth It Full Width + Laptop - Harga X - QR 081291904422 GoPay/DANA/OVO + VA - Email Wajib Follow Up - SOP/ERP/OEE/KPI + Alkitab")
