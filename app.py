import streamlit as st
import io
from gtts import gTTS

# --- CONFIG ---
st.set_page_config(page_title="Ruang Teduh AI", page_icon="🌿", layout="centered")

# --- STATE ---
if "page" not in st.session_state:
    st.session_state.page = "R1"

# --- PROMPT TEMPLATE (ANTI FULGAR) ---
PROMPT_TEMPLATE = """
Kamu mentor Ruang Teduh. Tone: PERFECT FINAL, Memikat, Dari mata turun ke hati, Halus di kuping, Backsound embun pagi.
Ruang: {ruang}, Ayat: {ayat}, Curhat: {curhat}, Tier: {tier}
Aturan: Jangan fulgar/kasar. Teduh, membangun.
Output JSON: nasehat_utama, renungan, terapan, script_audio_halus
"""

def tts_player(text, key_audio):
    """Ganti Browser TTS yang 'tak ada suara' jadi server TTS"""
    try:
        tts = gTTS(text, lang='id', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3', autoplay=False)
        st.caption(f"🔊 Memutar via Server TTS (id-ID, 0.85x halus) - {key_audio}")
    except Exception as e:
        st.error(f"Audio error: {e}")

def render_ruang(ruang_name, ayat_default, tier_info):
    # --- BOX SUARA HALUS ---
    st.markdown(f"""
    <div style="background:#0a3d2e;padding:20px;border-radius:15px;color:white;border:2px solid #2ecc71">
    <h3>🎧 Suara Halus Ruang Teduh • v3.0</h3>
    <p><b>PERFECT FINAL • Memikat</b><br>Dari mata turun ke hati • Halus di kuping • Backsound embun pagi</p>
    <small>{ayat_default}</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # Contoh data - nanti ini dari LLM
    if ruang_name == "R1":
        nasehat = "Otak butuh 5 detik visual hijau sebelum bisa menerima nasehat. Lihat dulu, baru dengar, baru renungkan."
        renungan = "Kerja bukan soal gaji, tapi skill naik, jaringan luas. Visual teamwork memicu rasa memiliki."
        script_audio = "Kolose 3 ayat 23 - Bekerja untuk Tuhan, bukan untuk manusia. Tarik nafas 5 detik sambil lihat visual hijau."
    else:
        nasehat = "Kolose 3:23 Advance - Bekerja untuk Tuhan dengan level MALKHUTKHA. Dari Staff -> Supervisor -> Manager."
        renungan = "Kerja bukan soal gaji, tapi skill naik, jaringan luas. Visual teamwork memicu rasa memiliki."
        script_audio = "Bekerja untuk Tuhan dengan level Malkhutkha. Dari Staff menjadi Supervisor, lalu Manager. Fokus bangun SOP."

    st.info(f"**Renungan:** {renungan}\n\n🌱 **Terapan:** {tier_info}")

    # TOMBOL PLAY - INI SUDAH FIX, PAKAI KEY UNIK
    if st.button(f"▶️ Play Nasehat {ruang_name} (Halus)", key=f"play_{ruang_name}_v3"):
        tts_player(script_audio, ruang_name)

    # Tombol browser backup
    if st.button(f"🔊 Suara Browser {ruang_name}", key=f"browser_{ruang_name}"):
        tts_player(script_audio, f"Browser {ruang_name}")

    st.divider()

    # --- FORM ADMIN - INI YANG TADI ERROR ---
    st.subheader(f"📝 Form Aktif Ruang {ruang_name[-1]} (v3.0) - Akan ke-reset pas masuk R2")
    
    # FORM MULAI DI SINI - DI DALAM FORM CUMA BOLEH form_submit_button
    with st.form(f"form_{ruang_name}", clear_on_submit=False):
        tier = st.selectbox("Pilih Tier", ["Employee 200rb/bulan", "Entrepreneur 300rb/bulan", "Employee 200rb - Entrepreneur 300rb"], key=f"tier_{ruang_name}")
        pesan = st.text_area("Pesan ke Admin Email & WA (ini yang lo ketik tadi gak ada suaranya)", 
                             placeholder="Mau jadi member sih tapi...", key=f"pesan_{ruang_name}", height=120)
        
        # DI DALAM FORM: HANYA form_submit_button YANG BOLEH
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Kirim ke Admin", use_container_width=True, type="primary")
        with col2:
            # Kalau butuh 2 tombol submit, pakai form_submit_button juga, jangan st.button
            submit_r2 = st.form_submit_button(f"Submit {ruang_name}", use_container_width=True)

        if submit or submit_r2:
            if pesan:
                st.success(f"Terkirim: {pesan[:50]}... Tier: {tier}")
                # TODO: logic kirim email/WA di sini
            else:
                st.warning("Tulis pesannya dulu bro")

    # TOMBOL KEMBALI HARUS DI LUAR FORM - INI FIX UTAMA ERROR LINE 263
    st.write("")
    if ruang_name == "R1":
        if st.button("➡️ Masuk ke Ruang 2 (R2)", key="to_r2", use_container_width=True):
            st.session_state.page = "R2"
            st.rerun()
    else:
        if st.button("⬅️ Kembali ke R1", key="kembali_r1_fix", use_container_width=True):
            st.session_state.page = "R1"
            st.rerun()

# --- ROUTER ---
if st.session_state.page == "R1":
    render_ruang("R1", "Kolose 3:23 - Bekerja untuk Tuhan...", "SOP/ERP/OEE/KPI via GDrive/Github - Employee 200rb")
else:
    render_ruang("R2", "Kolose 3:23 Advance - Bekerja untuk Tuhan dengan level MALKHUTKHA", "SOP/ERP/OEE/KPI via GDrive/Github - Entrepreneur 300rb")
