import streamlit as st
from pathlib import Path
from core import auto_generate_all, get_suara_teduh_lengkap, get_audio_aturan_utama

st.set_page_config(page_title="Ruang Teduh AI - TAVO MALKHUTKHA", layout="wide")
data = auto_generate_all()

st.title("🧘 Ruang Teduh AI - TAVO MALKHUTKHA")
st.caption("V28.1 AUDIO FIX + V2.7 Wellbeing Library | Kerja max 60km dari rumah")

# AUTO PLAY - langsung jalan kayak v2.7
audio_file = data["audio"]
if Path(audio_file).exists():
    st.audio(audio_file, autoplay=True)
    st.success(f"✅ PUTAR: Penjelasan SOP, ERP, OEE, KPI + Worship Teduh - Voice Only, Tanpa Musik Stress")
else:
    st.warning(f"File audio {audio_file} belum ada di repo, upload dulu ya bro")

# AUTO TAMPIL SOP->ERP->OEE->KPI + SUARA+TEKS biar gak sepi
st.warning("Jangan sepi. Jelaskan dengan SUARA + TEKS (ATURAN UTAMA TERSYSTEMATIS)")

st.subheader("1. SOP disempurnakan Kolose 3:23")
st.write(f"- {data['sop']['flow']}")
st.subheader("2. ERP versi Hati")
st.write(f"- M = Manusia ({data['erp']['Manusia']})")
st.write(f"- M = Material ({data['erp']['Material']})")
st.write(f"- M = Money ({data['erp']['Money']})")
st.subheader("3. OEE versi Rohani")
st.write(f"- Availability: {data['oee']['Availability']}")
st.write(f"- Performance: {data['oee']['Performance']}")
st.write(f"- Quality: {data['oee']['Quality']}")
st.subheader("4. KPI disempurnakan Amsal 16:3")
st.write(f"- {data['kpi']['ayat']}")
st.write(f"- Indikator: {', '.join(data['kpi']['indikator'])}")

st.divider()
st.subheader("🔊 Suara Teduh Hari Ini - Visual + Teks + Audio - Full di HP")
st.info(get_suara_teduh_lengkap())
