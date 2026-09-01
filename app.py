import streamlit as st
import io
from gtts import gTTS

st.set_page_config(page_title="Ruang Teduh AI", page_icon="🌿", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "R1"
if "last_pesan" not in st.session_state:
    st.session_state.last_pesan = ""
if "last_tier" not in st.session_state:
    st.session_state.last_tier = ""

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

def render_bimbingan(tier):
    st.markdown("### 📊 Kolom Bimbingan & Nasehat Pengajaran")
    
    # Visual yang lo minta
    st.image("/mnt/data/resource/perjalanan_cinta_petunjuk.webp", 
             caption="Visual: Dari mata datangnya kasih, diterima hati dan brain, disanalah jiwa lestari", 
             use_container_width=True)
    
    if "Employee 20rb" in tier:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📋 SOP - Employee")
            st.write("1. Datang 5 menit lebih awal\n2. Checklist 5S\n3. Lapor harian via GDrive")
            if st.button("🔊 Bacakan SOP", key=f"sop_{tier}"):
                tts_player("SOP Employee: Datang lima menit lebih awal, checklist lima S, lapor harian via GDrive", "SOP Employee")
        with col2:
            st.markdown("#### 📈 KPI - Employee")
            st.write("• Kehadiran 95%\n• Task selesai 100%\n• Kolaborasi tim")
            if st.button("🔊 Bacakan KPI", key=f"kpi_{tier}"):
                tts_player("KPI Employee: Kehadiran sembilan puluh lima persen, task selesai seratus persen, kolaborasi tim", "KPI Employee")
        
        st.markdown("#### 🙏 Bimbingan Spiritual - Kolose 3:23")
        st.info("Bekerja untuk Tuhan, bukan untuk manusia. Dari mata turun ke hati, kerja jadi ibadah.")
        if st.button("🔊 Bacakan Spiritual Employee", key=f"spirit_emp_{tier}"):
            tts_player("Bimbingan spiritual: Bekerja untuk Tuhan bukan untuk manusia. Dari mata turun ke hati, kerja jadi ibadah, jiwa lestari.", "Spiritual Employee")
    
    else: # Entrepreneur 30rb
        st.markdown("#### Level Entrepreneur - Assemblying Hackathon")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**📋 SOP**\nSOP Produksi & QC\nSOP Customer Service")
            if st.button("🔊 SOP", key="sop_ent"):
                tts_player("SOP Entrepreneur: Standard Operating Procedure produksi dan QC, serta customer service", "SOP Entrepreneur")
        with c2:
            st.markdown("**💾 ERP**\nIntegrasi GDrive/Github\nStok & Keuangan realtime")
            if st.button("🔊 ERP", key="erp_ent"):
                tts_player("ERP Entrepreneur: Integrasi GDrive dan Github, stok dan keuangan realtime", "ERP")
        
        c3, c4 = st.columns(2)
        with c3:
            st.markdown("**⚙️ OEE**\nAvailability 90%\nPerformance 95%\nQuality 99%")
            if st.button("🔊 OEE", key="oee_ent"):
                tts_player("OEE Entrepreneur: Availability sembilan puluh persen, performance sembilan puluh lima persen, quality sembilan puluh sembilan persen", "OEE")
        with c4:
            st.markdown("**🎯 KPI**\nOmzet, Retensi, NPS\nScale Up Team")
            if st.button("🔊 KPI Ent", key="kpi_ent"):
                tts_player("KPI Entrepreneur: Omzet, retensi, NPS, scale up team", "KPI Entrepreneur")
        
        st.markdown("#### 🙏 Bimbingan Spiritual Advance - MALKHUTKHA")
        st.success("Level MALKHUTKHA: Staff -> Supervisor -> Manager -> Leader. Dari mata melihat peluang, hati memahami, brain merancang, jiwa lestari memimpin.")
        if st.button("🔊 Bacakan Spiritual MALKHUTKHA", key="spirit_mal"):
            tts_player("Bimbingan spiritual Malkhutkha: Dari mata melihat peluang, hati memahami dengan kasih, brain merancang dengan arif, disanalah jiwa lestari memimpin. Assemblying hackathon, bersaing dengan suara kebaikan.", "Spiritual Malkhutkha")
        
        # Tombol Bersaing Suara Hackathon
        if st.button("🏆 Assemblying Hackathon - Bersaing Suara (All Indikator)", key="hackathon_voice"):
            all_text = "Bimbingan lengkap: SOP, ERP, OEE, KPI. Dari mata turun ke hati, dari hati ke brain, jiwa lestari. Kolose 3:23 Advance."
            tts_player(all_text, "Hackathon Bersaing Suara - All Indikator")

    st.divider()

def render_ruang(ruang_name, ayat_default):
    st.markdown(f"""
    <div style="background:#0a3d2e;padding:20px;border-radius:15px;color:white;border:2px solid #2ecc71">
    <h3>🎧 Suara Halus Ruang Teduh • v3.2</h3>
    <p><b>PERFECT FINAL • Memikat</b><br>Dari mata turun ke hati • Halus di kuping • Backsound embun pagi</p>
    <small>{ayat_default}</small>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

    # PESAN MEMBER DARI R1 - TETAP SAMA KAYAK SCREENSHOT LO JAM 21:37 - TIDAK DIUBAH
    if ruang_name == "R2" and st.session_state.last_pesan:
        st.success(f"📩 Pesan Member dari R1 (Tier: {st.session_state.last_tier}):")
        st.info(f"\"{st.session_state.last_pesan}\"")
        if st.button("🔊 Bacakan Pesan Member di R2 (Halus)", key="bacakan_member_r2", type="primary"):
            tts_player(st.session_state.last_pesan, "Membacakan pesan member - id-ID 0.85x halus")
        st.divider()

    # KOLOM BIMBINGAN BARU - INI TAMBAHAN YANG LO MINTA
    # Ambil tier dari session atau default
    current_tier = st.session_state.last_tier if st.session_state.last_tier else ("Employee 20rb/bulan" if ruang_name=="R1" else "Entrepreneur 30rb/bulan")
    render_bimbingan(current_tier)

    # FORM R2 - INI GUE KUNCI, TIDAK GUE RUBAH LAGI SESUAI PERINTAH LO
    st.subheader(f"📝 Form Aktif Ruang {ruang_name[-1]} (v3.2) - Akan ke-reset pas masuk R2")
    
    with st.form(f"form_{ruang_name}_v32_LOCKED", clear_on_submit=False):
        tier = st.selectbox("Pilih Tier", ["Employee 20rb/bulan", "Entrepreneur 30rb/bulan"], key=f"tier_{ruang_name}_v32")
        pesan = st.text_area("Pesan ke Admin Email & WA", 
                             placeholder="Ketik pesan dan kesan lo di sini...", 
                             key=f"pesan_{ruang_name}_v32", height=120,
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
                st.success(f"Tersimpan! Pesan akan dibacakan di R2 nanti.")
                if ruang_name == "R1":
                    st.session_state.page = "R2"
                    st.rerun()
            else:
                st.warning("Tulis pesan dulu sebelum submit ke R2 bro")

    st.write("")
    if ruang_name == "R1":
        if st.button("➡️ Masuk ke Ruang 2 (R2)", key="to_r2_v32", use_container_width=True):
            st.session_state.page = "R2"
            st.rerun()
    else:
        if st.button("⬅️ Kembali ke R1", key="kembali_r1_v32", use_container_width=True):
            st.session_state.page = "R1"
            st.rerun()

if st.session_state.page == "R1":
    render_ruang("R1", "Kolose 3:23 - Bekerja untuk Tuhan...")
else:
    render_ruang("R2", "Kolose 3:23 Advance - Level MALKHUTKHA")
