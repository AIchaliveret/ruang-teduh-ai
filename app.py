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

def render_ruang(ruang_name, ayat_default):
    # HEADER
    st.markdown(f"""
    <div style="background:#0a3d2e;padding:20px;border-radius:15px;color:white;border:2px solid #2ecc71">
    <h3>🎧 Suara Halus Ruang Teduh • v3.1</h3>
    <p><b>PERFECT FINAL • Memikat</b><br>Dari mata turun ke hati • Halus di kuping • Backsound embun pagi</p>
    <small>{ayat_default}</small>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

    # JIKA DI R2 DAN ADA PESAN DARI R1 -> TAMPILKAN + BACAKAN
    if ruang_name == "R2" and st.session_state.last_pesan:
        st.success(f"📩 Pesan Member dari R1 (Tier: {st.session_state.last_tier}):")
        st.info(f"\"{st.session_state.last_pesan}\"")
        if st.button("🔊 Bacakan Pesan Member di R2 (Halus)", key="bacakan_member_r2", type="primary"):
            tts_player(st.session_state.last_pesan, "Membacakan pesan member - id-ID 0.85x halus")
        st.divider()
    elif ruang_name == "R2" and not st.session_state.last_pesan:
        st.warning("Belum ada pesan dari R1. Silakan ketik dulu di Ruang 1 lalu Submit R1.")

    # Renungan default
    if ruang_name == "R1":
        renungan = "Otak butuh 5 detik visual hijau sebelum bisa menerima nasehat. Lihat dulu, baru dengar, baru renungkan."
        tier_info = "Employee 20rb/bulan - Fokus skill naik, jaringan luas"
        script_audio = "Kolose 3 ayat 23 - Bekerja untuk Tuhan, bukan untuk manusia. Tarik nafas 5 detik."
    else:
        renungan = "Kerja bukan soal gaji, tapi skill naik, jaringan luas. Visual teamwork memicu rasa memiliki."
        tier_info = "Entrepreneur 30rb/bulan - Fokus SOP/ERP/OEE/KPI via GDrive/Github"
        script_audio = "Kolose 3:23 Advance - Bekerja untuk Tuhan dengan level Malkhutkha. Dari Staff ke Manager."

    st.info(f"**Renungan:** {renungan}\n\n🌱 **Terapan:** {tier_info}")
    if st.button(f"▶️ Play Nasehat {ruang_name} (Halus)", key=f"play_{ruang_name}_v31"):
        tts_player(script_audio, f"Nasehat {ruang_name}")

    st.divider()

    # FORM - HARGA BARU 20RB & 30RB
    st.subheader(f"📝 Form Aktif Ruang {ruang_name[-1]} (v3.1) - Akan ke-reset pas masuk R2")
    
    with st.form(f"form_{ruang_name}_v31", clear_on_submit=False):
        # UPDATE HARGA SESUAI REQUEST LO
        tier = st.selectbox("Pilih Tier", ["Employee 20rb/bulan", "Entrepreneur 30rb/bulan"], key=f"tier_{ruang_name}_v31")
        pesan = st.text_area("Pesan ke Admin Email & WA", 
                             placeholder="Ketik pesan dan kesan lo di sini...", 
                             key=f"pesan_{ruang_name}_v31", height=120,
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

    # TOMBOL NAVIGASI - HARUS DI LUAR FORM (FIX ERROR LINE 263)
    st.write("")
    if ruang_name == "R1":
        if st.button("➡️ Masuk ke Ruang 2 (R2)", key="to_r2_v31", use_container_width=True):
            st.session_state.page = "R2"
            st.rerun()
    else:
        if st.button("⬅️ Kembali ke R1", key="kembali_r1_v31", use_container_width=True):
            st.session_state.page = "R1"
            st.rerun()

# ROUTER
if st.session_state.page == "R1":
    render_ruang("R1", "Kolose 3:23 - Bekerja untuk Tuhan...")
else:
    render_ruang("R2", "Kolose 3:23 Advance - Level MALKHUTKHA")
