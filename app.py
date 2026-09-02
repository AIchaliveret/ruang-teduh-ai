"""
Ruang Teduh AI - FINAL v2.8.1 - NO MUSIC STRESS
Ruang 1,2,3 = HENING TOTAL, hanya voice SOP
"""
import streamlit as st

st.set_page_config(page_title="Ruang Teduh - Tanpa Musik Stress", page_icon="🧘", layout="centered")

# === KUNCI MATI MUSIK ===
USE_MUSIC = False
BACKGROUND_MUSIC = None

st.title("Ruang Teduh AI - Hening Total")
st.markdown("### ✅ Semua Musik Stress Sudah Dihapus di Ruang 1,2,3")
st.caption("v2.8.1 AUDIO FIX | Klik untuk bunyi, tanpa autoplay, tanpa backsound")
st.divider()

def audio_hening(path, ruang_name):
    """Ruang 1,2,3 - hanya voice, no music"""
    col1, col2 = st.columns([1, 3])
    with col1:
        play = st.button(f"🔊 Putar {ruang_name}", key=f"play_{ruang_name}", use_container_width=True)
    with col2:
        st.write(f"**{ruang_name} - Voice Only** | Tanpa musik stress")
    
    if play:
        st.session_state[f"show_{ruang_name}"] = True

    if st.session_state.get(f"show_{ruang_name}", False):
        try:
            st.audio(path, format="audio/mp3", autoplay=False)
            st.success(f"{ruang_name} diputar - Hening, tanpa musik")
        except:
            st.info(f"Upload file: {path} (versi voice only, tanpa musik)")
            st.write("""
            Shalom. Ini penjelasan Ruang Teduh. 
            SOP: Datang, Doa, Kerja seperti untuk Tuhan, Kolose 3:23.
            ERP Hati: Manusia, Material, Money UMR.
            OEE Rohani: Availability 100%, Performance +1% tiap hari, Quality memuliakan Tuhan.
            """)

# === RUANG 1 ===
st.subheader("Ruang 1 - Gratis")
audio_hening("ruang1_sop_only.mp3", "Ruang 1")

st.divider()

# === RUANG 2 ===
st.subheader("Ruang 2 - Gratis")
audio_hening("ruang2_sop_only.mp3", "Ruang 2")

st.divider()

# === RUANG 3 ===
st.subheader("Ruang 3 - Bayar")
audio_hening("ruang3_sop_only.mp3", "Ruang 3")
st.link_button("Masuk Ruang 3 - Bayar", "https://ruang-teduh-ai.streamlit.app", use_container_width=True)

st.divider()
st.markdown("""
**Yang sudah dihapus:**
- ❌ background_music = AudioSegment.from_file("musik_teduh.mp3")
- ❌ combined = voice.overlay(background_music - 15)
- ❌ st.audio(..., autoplay=True)
- ❌ Semua backsound stress di Ruang 1,2,3

**Yang sekarang:**
- ✅ USE_MUSIC = False
- ✅ st.audio(..., autoplay=False) + Tombol Klik
- ✅ Voice Only, Hening, Teduh
""")
