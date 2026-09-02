import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Ruang Teduh AI - TAVO MALKHUTKHA", page_icon="🧘", layout="centered")

# --- DATA BUDI ---
teks_budi = "Budi status duda karyawan dengan 4 anak. Membutuhkan kerja. Pengalaman 15 tahun ngurus anak. Visi kawin lagi misi jadi milyuner."

aturan_utama = """
1. SOP disempurnakan Kolose 3:23 - Apapun yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan.
Datang -> Doa -> Kerja -> Evaluasi

2. ERP versi Hati - Manusia, keluarga dan hati. Material, waktu dan jarak kerja maksimal 60 kilometer dari rumah. Money, UMR domisili sepuluh juta.

3. OEE versi Rohani - Availability hadir 100 persen. Performance tidak mengeluh, 1 persen lebih baik setiap hari. Quality hasil kerja memuliakan Tuhan, target 95 persen.

4. KPI disempurnakan Amsal 16:3 - Serahkanlah perbuatanmu kepada Tuhan, maka terlaksanalah segala rencanamu.
"""

st.markdown("""
# 🧘 Ruang Teduh AI - TAVO MALKHUTKHA
### V28.1 AUDIO FIX + V2.7 Wellbeing Library | Kerja max 60km dari rumah
""")

st.warning("V28.1 VOICE ONLY - Tanpa upload mp3 26MB, langsung dari teks jadi suara. Gak ditolak GitHub lagi.")

# --- KARTU BUDI ---
st.markdown("### 👨‍👧‍👦 Profil - Budi")
st.info(teks_budi)

# Komponen TTS - pakai Web Speech API, tanpa file mp3
tts_html = f"""
<div style="font-family: sans-serif;">
  <div style="background:#f0fdf4; border:1px solid #bbf7d0; padding:16px; border-radius:12px; margin-bottom:12px;">
    <p style="margin:0; font-size:14px; color:#166534;">🔊 Mode: Voice Only - Teks jadi Suara (id-ID)</p>
    <p style="margin:4px 0 0; font-size:12px; color:#15803d;">Tanpa mp3, tanpa upload GitHub</p>
  </div>
  
  <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:16px;">
    <button id="playBtn" style="background:#16a34a; color:white; border:none; padding:14px 24px; border-radius:10px; font-size:16px; font-weight:bold; cursor:pointer; flex:1;">▶️ Putar Suara Budi</button>
    <button id="stopBtn" style="background:#dc2626; color:white; border:none; padding:14px 20px; border-radius:10px; font-size:16px; cursor:pointer;">⏹️ Stop</button>
  </div>

  <div style="display:flex; gap:10px; align-items:center; margin-bottom:12px;">
    <label style="font-size:13px;">Kecepatan:</label>
    <input type="range" id="rate" min="0.7" max="1.3" step="0.1" value="1.0" style="flex:1;">
    <span id="rateVal" style="font-size:13px;">1.0x</span>
  </div>

  <div style="display:flex; gap:10px; align-items:center;">
    <label style="font-size:13px;">Suara:</label>
    <select id="voiceSelect" style="flex:1; padding:6px; border-radius:6px; border:1px solid #ccc;"></select>
  </div>
</div>

<script>
let voices = [];
const voiceSelect = document.getElementById('voiceSelect');
const rateSlider = document.getElementById('rate');
const rateVal = document.getElementById('rateVal');

function loadVoices() {{
  voices = window.speechSynthesis.getVoices();
  voiceSelect.innerHTML = '';
  voices.forEach((voice, i) => {{
    if (voice.lang.includes('id') || voice.lang.includes('ID') || voice.name.toLowerCase().includes('indonesia')) {{
      const opt = document.createElement('option');
      opt.value = i;
      opt.textContent = voice.name + ' (' + voice.lang + ') - ID';
      opt.selected = true;
      voiceSelect.appendChild(opt);
    }}
  }});
  // kalau gak ada suara ID, tampilkan semua
  if (voiceSelect.options.length === 0) {{
    voices.forEach((voice, i) => {{
      const opt = document.createElement('option');
      opt.value = i;
      opt.textContent = voice.name + ' (' + voice.lang + ')';
      voiceSelect.appendChild(opt);
    }});
  }}
}}

if (speechSynthesis.onvoiceschanged !== undefined) {{
  speechSynthesis.onvoiceschanged = loadVoices;
}}
loadVoices();

rateSlider.addEventListener('input', () => {{
  rateVal.textContent = rateSlider.value + 'x';
}});

document.getElementById('playBtn').addEventListener('click', () => {{
  window.speechSynthesis.cancel();
  const text = `{teks_budi} . Aturan utama tersystematis. {aturan_utama.replace(chr(10), ' ')}`;
  const utter = new SpeechSynthesisUtterance(text);
  const selectedVoice = voices[voiceSelect.value];
  if (selectedVoice) utter.voice = selectedVoice;
  utter.lang = 'id-ID';
  utter.rate = parseFloat(rateSlider.value);
  utter.pitch = 1.0;
  window.speechSynthesis.speak(utter);
}});

document.getElementById('stopBtn').addEventListener('click', () => {{
  window.speechSynthesis.cancel();
}});
</script>
"""

components.html(tts_html, height=280)

st.markdown("---")
st.markdown("### 1. SOP disempurnakan Kolose 3:23")
st.markdown("- Datang → Doa → Kerja → Evaluasi")

st.markdown("### 2. ERP versi Hati")
st.markdown("- Manusia, keluarga dan hati. Material, waktu dan jarak max 60km dari rumah. Money, UMR domisili 10jt")

st.markdown("### 3. OEE versi Rohani")
st.markdown("- Availability 100%, Performance tidak mengeluh 1% lebih baik, Quality 95% memuliakan Tuhan")

st.markdown("### 4. KPI disempurnakan Amsal 16:3")
st.markdown("- Serahkanlah perbuatanmu kepada Tuhan, maka terlaksanalah segala rencanamu")

st.success("✅ Siap submit lablab.ai - Tanpa file mp3 besar, tanpa error GitHub. Kerja max 60km dari rumah.")
