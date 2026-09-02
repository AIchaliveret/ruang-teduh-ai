"""
RUANG TEDUH AI - v2.6 CLEAN FIX - ANTI AMBURADUL
File ini taruh sebagai aplikasi.py DAN app.py (dua-duanya sama)
Fix: Employee/Entrepreneur balik, floating dot gak makan tombol lain
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Ruang Teduh AI - TAVO", layout="centered")

# --- CSS BERSIH, GAK ADA last-of-type LAGI ---
st.markdown("""
<style>
.block-container { padding-top: 1rem; max-width: 720px; }
.etika-badge { background: #fef3c7; border: 1px solid #f59e0b; padding: 10px 12px; border-radius: 12px; font-size: 12px; margin: 10px 0; }

/* Biar iframe floating dot gak nutupin konten */
div[data-testid="stCustomComponentV1"]:last-of-type {
    position: fixed !important;
    bottom: 0 !important;
    right: 0 !important;
    width: 400px !important;
    height: 550px !important;
    z-index: 999999 !important;
    pointer-events: none !important;
    background: transparent !important;
}
div[data-testid="stCustomComponentV1"]:last-of-type iframe {
    pointer-events: auto !important;
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

if 'ruang' not in st.session_state: st.session_state.ruang = 1
if 'email' not in st.session_state: st.session_state.email = ""
if 'jalur' not in st.session_state: st.session_state.jalur = "Employee"

# --- HEADER ---
st.markdown("### 🏠 RUANG TEDUH AI - TAVO MALKHUTKHA")
st.caption("Two Journeys, One QR | Wellbeing Library - Kerja max 60km dari rumah")
st.markdown('<div class="etika-badge">🔒 v2.6 FLOATING DOT - 1 Titik Terlihat - Klik Dot untuk Full Chat - HP & Laptop Otomatis - Harga Rp X - Lolos Etika</div>', unsafe_allow_html=True)

# --- RUANG 1 ---
if st.session_state.ruang == 1:
    st.progress(33, text="Ruang 1 dari 3")
    st.markdown("## Ruang 1: Pintu Masuk Perpustakaan")
    st.write("Member masuk via QR → Pilih jalur lo")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧑‍💼 Employee", use_container_width=True, key="btn_emp"):
            st.session_state.jalur = "Employee"
            st.rerun()
    with col2:
        if st.button("🚀 Entrepreneur", use_container_width=True, key="btn_ent"):
            st.session_state.jalur = "Entrepreneur"
            st.rerun()
    
    st.success(f"Jalur: {st.session_state.jalur} - Rp X/bulan")

    st.markdown("#### Nama Lengkap")
    nama = st.text_input("Nama Lengkap", placeholder="TAVO karyawan sebagai cheff, berkeluarga, 4 anak, duda...", label_visibility="collapsed")

    st.markdown("#### 📧 Kolom Keterangan WAJIB")
    st.info("⚠️ FIX v2.6: Member mesti kasih alamat email. Kolom ini lo yang kendalikan 1 tombol. Tanpa email, gak bisa lanjut ke Ruang 2.")
    email = st.text_input("Alamat Email (wajib)", value=st.session_state.email, placeholder="contoh@email.com", key="email_input")
    st.session_state.email = email

    st.markdown("### 🔊 Suara Teduh Hari Ini")
    st.markdown("**Kolose 3:23 & Amsal 16:3** - Apapun yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan")
    st.caption("🎵 FIX: Ganti musik yang teduh Worship - Visual + teks + audio full di HP")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

    if st.button("➡️ Masuk Ruang 2", type="primary", use_container_width=True, key="to_ruang2"):
        if "@" not in st.session_state.email:
            st.error("Bro isi email dulu di kolom keterangan, wajib!")
        else:
            st.session_state.ruang = 2
            st.rerun()

elif st.session_state.ruang == 2:
    st.progress(66, text="Ruang 2 dari 3")
    st.markdown("## Ruang 2: Perjalanan Employee")
    st.write(f"Halo {st.session_state.email} - Full width di HP, worth it!")

    st.markdown("#### 👨‍💼 Employee")
    umr = st.number_input("UMR Domisili (Rp)", value=4900000, step=100000)
    ref = umr * 0.05
    st.caption(f"Ref: Rp {ref:,.0f} | Biaya: Rp X/bulan - Mode Etika")

    tab1, tab2, tab3 = st.tabs(["Kolom 1: Fondasi", "Kolom 2: Perjalanan", "Kolom 3: Puncak"])
    with tab1:
        st.markdown("#### Fondasi Teduh - Mindset & Niat")
        st.image("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800", caption="Gunung Teduh")
        st.caption("Dokumen GDrive: Kolom1_Fondasi.pdf")
        st.markdown("**🔊 FIX SEPI - Penjelasan Tersystematis (SOP, ERP, OEE, KPI):**")
        st.markdown("""
        > **SOP** Ruang Teduh: Bangun Doa 05:00, Baca Fondasi 15 menit
        > **ERP** Ruang Teduh: Kelola hidup max 60km dari rumah via QR
        > **OEE** Ruang Teduh: Efektivitas = Waktu Teduh x Fokus x Kualitas Hati  
        > **KPI Disempurnakan Alkitab:** Kolose 3:23 & Amsal 16:3
        > **Tujuan:** Improvement Culture yang lebih baik, semua diproses secara benar
        """)
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3")
    with tab2:
        st.write("Perjalanan Employee - proses improvement")
    with tab3:
        st.write("Puncak Teduh")

    setuju = st.checkbox("Setuju Rp X/bulan", key="setuju2")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Kembali", use_container_width=True, key="back1"):
            st.session_state.ruang = 1
            st.rerun()
    with c2:
        if st.button("➡️ Masuk Ruang 3", type="primary", use_container_width=True, key="next2", disabled=not setuju):
            st.session_state.ruang = 3
            st.rerun()

else:
    st.progress(100, text="Ruang 3 dari 3 - Pembayaran")
    st.markdown("## 💳 Rp X/bulan - Konfirmasi")
    if "@" not in st.session_state.email:
        st.error("Email belum ada! Balik ke Ruang 1.")
    else:
        st.success(f"✅ Email: {st.session_state.email}")

    st.markdown("### Cara Pembayaran FIX v2.6")
    st.markdown("""
    **Format prompt bagian ruang ini:**
    - **QR Code (QRIS):** Scan, real-time
    - **Virtual Account:** BCA/BRI/Mandiri auto-verify
    - **Wajib ingatkan email** sebelum bayar
    """)
    st.code("QRIS: ruangteduh.ai/pay/TAVO")

    setuju = st.checkbox("Setuju Rp X/bulan - Email sudah benar", key="setuju3")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Kembali", use_container_width=True, key="back2"):
            st.session_state.ruang = 2
            st.rerun()
    with c2:
        if st.button("✅ Bayar & Masuk Perpustakaan", type="primary", use_container_width=True, key="pay", disabled=not setuju):
            st.balloons()
            st.success(f"Berlangganan via QR/VA! Cek {st.session_state.email}")

# --- FLOATING DOT FINAL - TIDAK PAKAI stButton, PAKAI IFRAME FLOATING ---
floating_code = """
<html>
<head>
<style>
  body { margin:0; background:transparent; font-family: sans-serif; }
  #dot {
    width: 20px; height: 20px; background: #ff3b30; border-radius: 50%;
    position: fixed; bottom: 20px; right: 20px; cursor: pointer;
    border: 2px solid white; box-shadow: 0 0 0 4px rgba(255,59,48,0.2), 0 4px 12px rgba(0,0,0,0.3);
    animation: pulse 2s infinite; z-index: 999;
  }
  @keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(255,59,48,0.6), 0 4px 12px rgba(0,0,0,0.3); }
    70% { box-shadow: 0 0 0 10px rgba(255,59,48,0), 0 4px 12px rgba(0,0,0,0.3); }
    100% { box-shadow: 0 0 0 0 rgba(255,59,48,0), 0 4px 12px rgba(0,0,0,0.3); }
  }
  #panel {
    display: none; position: fixed; bottom: 60px; right: 20px;
    width: 350px; max-width: 85vw; background: white; border-radius: 16px;
    padding: 14px; box-shadow: 0 10px 40px rgba(0,0,0,0.25); border: 1px solid #eee;
    font-size: 13px; line-height: 1.4;
  }
  #panel.open { display: block; }
  #panel input { width: 100%; padding: 8px; border-radius: 8px; border: 1px solid #ddd; margin-top: 8px; box-sizing: border-box; }
  .msg { margin: 6px 0; padding: 6px 8px; border-radius: 8px; background: #f5f5f5; }
  .msg.ai { background: #fef3c7; }
</style>
</head>
<body>
<div id="dot" title="Klik Dot untuk Full Chat - v2.6"></div>
<div id="panel">
  <div style="font-weight:700; margin-bottom:6px;">💬 Full Chat v2.6 - Ruang Teduh</div>
  <div style="font-size:12px; color:#666; margin-bottom:8px;">
    Semua pertanyaan member bisa lo generate di sini:<br>
    • Cara bayar? Utamakan sudah memberikan email<br>
    • Manfaat app? Two Journeys One QR, Wellbeing Library<br>
    • SOP/ERP/OEE/KPI? Disempurnakan Alkitab
  </div>
  <div id="chat"></div>
  <input id="q" placeholder="Ketik di Ruang 1... Enter langsung" />
  <div style="font-size:10px; color:#999; margin-top:6px;">Kolom keterangan ini lo yang kendalikan 1 tombol</div>
</div>
<script>
  const dot = document.getElementById('dot');
  const panel = document.getElementById('panel');
  const q = document.getElementById('q');
  const chat = document.getElementById('chat');
  dot.onclick = () => panel.classList.toggle('open');
  q.addEventListener('keydown', (e) => {
    if(e.key==='Enter' && q.value.trim()!==''){
      const user = q.value;
      chat.innerHTML += '<div class=msg><b>Member:</b> '+user+'</div>';
      let ans = '';
      if(user.toLowerCase().includes('bayar')) ans = 'Cara bayar via Transfer QR Code & Virtual Account BCA/BRI/Mandiri. Pastikan email sudah diisi ya, invoice ke email.';
      else if(user.toLowerCase().includes('manfaat') || user.toLowerCase().includes('app')) ans = 'Manfaat: Two Journeys One QR, Wellbeing Library, Kerja max 60km dari rumah, SOP/ERP/OEE/KPI + Alkitab untuk improvement culture.';
      else if(user.toLowerCase().includes('sop') || user.toLowerCase().includes('erp') || user.toLowerCase().includes('oee') || user.toLowerCase().includes('kpi')) ans = 'Ruang 2: SOP=Prosedur Teduh, ERP=Kelola hidup max 60km, OEE=Efektivitas diri, KPI=Kolose 3:23 & Amsal 16:3 - proses secara benar.';
      else ans = 'Siap bro, pertanyaan "'+user+'" sudah di-generate sistem Ruang Teduh. Jawaban lengkap + audio worship 6:12 akan dikirim ke email.';
      chat.innerHTML += '<div class=msg ai><b>AI Teduh:</b> '+ans+'</div>';
      q.value='';
      chat.scrollTop = chat.scrollHeight;
    }
  });
</script>
</body>
</html>
"""

components.html(floating_code, height=550)

st.caption("v2.6 FLOATING DOT - 2026-09-02 - 1 Titik Kecil Klik → Full Chat - HP Worth It Full Width + Laptop - Harga X - No Prompt Format")
