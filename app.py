"""
RUANG TEDUH AI - v2.61 - PATCH WORSHIP ASLI
Changelog v2.6 -> v2.61:
- FIX: st.audio("assets/worship_teduh.mp3") - musik teduh worship asli
- Folder assets/ ditambahkan (bukan code, cuma storage)
- Badge version update v2.61
- Floating dot, email gate, SOP/ERP/OEE/KPI tetap sama
"""

import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="Ruang Teduh AI - TAVO v2.61", layout="centered")

st.markdown("""
<style>
.block-container { padding-top: 1rem; max-width: 720px; }
.badge-v261 { background: #dcfce7; border: 1px solid #22c55e; padding: 10px 12px; border-radius: 12px; font-size: 12px; margin: 10px 0; font-weight: 600; }
div[data-testid="stCustomComponentV1"]:last-of-type {
    position: fixed !important; bottom: 0 !important; right: 0 !important;
    width: 400px !important; height: 550px !important;
    z-index: 999999 !important; pointer-events: none !important; background: transparent !important;
}
div[data-testid="stCustomComponentV1"]:last-of-type iframe {
    pointer-events: auto !important; background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

if 'ruang' not in st.session_state: st.session_state.ruang = 1
if 'email' not in st.session_state: st.session_state.email = ""
if 'jalur' not in st.session_state: st.session_state.jalur = "Employee"

# --- HEADER v2.61 ---
st.markdown("### 🏠 RUANG TEDUH AI - TAVO MALKHUTKHA")
st.caption("Two Journeys, One QR | Wellbeing Library - Kerja max 60km dari rumah")
st.markdown('<div class="badge-v261">✅ v2.61 FLOATING DOT - Worship Asli assets/worship_teduh.mp3 - 1 Titik Terlihat - Klik Dot untuk Full Chat - Lolos Etika</div>', unsafe_allow_html=True)

# Fungsi worship v2.61 - FORMAT BARU
def play_worship_v261(context="Ruang 1"):
    """
    FORMAT BARU v2.61 - 1 baris aja, gak perlu prompt baru
    Taruh file di: assets/worship_teduh.mp3
    """
    st.markdown(f"*🎵 Musik Teduh Worship - {context} (v2.61)*")
    path = "assets/worship_teduh.mp3"
    if os.path.exists(path):
        st.audio(path)  # <-- FORMAT BARU v2.61
        st.caption(f"✅ v2.61 Playing: {path}")
    else:
        st.error(f"❌ File {path} belum ada. Upload ke folder assets/ dulu bro")
        st.info("Cara: GitHub -> Add file -> Upload -> tulis path assets/worship_teduh.mp3")

if st.session_state.ruang == 1:
    st.progress(33, text="Ruang 1 dari 3 - v2.61")
    st.markdown("## Ruang 1: Pintu Masuk Perpustakaan [v2.61]")
    st.write("Member masuk via QR → Pilih jalur lo")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🧑‍💼 Employee", use_container_width=True, key="emp261"):
            st.session_state.jalur = "Employee"
            st.rerun()
    with c2:
        if st.button("🚀 Entrepreneur", use_container_width=True, key="ent261"):
            st.session_state.jalur = "Entrepreneur"
            st.rerun()
    st.success(f"Jalur: {st.session_state.jalur} - Rp X/bulan")
    
    st.markdown("#### Nama Lengkap")
    st.text_input("Nama Lengkap", placeholder="TAVO karyawan sebagai cheff, berkeluarga, 4 anak, duda...", label_visibility="collapsed", key="nama261")
    
    st.markdown("#### 📧 Kolom Keterangan WAJIB")
    st.info("FIX v2.61: Member mesti kasih email. 1 tombol kendalikan kolom ini.")
    st.session_state.email = st.text_input("Alamat Email (wajib)", value=st.session_state.email, placeholder="contoh@email.com", key="email261")
    
    st.markdown("### 🔊 Suara Teduh Hari Ini")
    st.markdown("**Kolose 3:23 & Amsal 16:3**")
    play_worship_v261("Ruang 1 - Pintu Masuk")
    st.caption("Visual + teks + audio worship asli - full di HP")

    if st.button("➡️ Masuk Ruang 2", type="primary", use_container_width=True, key="to2_261"):
        if "@" not in st.session_state.email:
            st.error("Isi email dulu bro!")
        else:
            st.session_state.ruang = 2
            st.rerun()

elif st.session_state.ruang == 2:
    st.progress(66, text="Ruang 2 dari 3 - v2.61")
    st.markdown("## Ruang 2: Perjalanan Employee [v2.61]")
    st.write(f"Halo {st.session_state.email} - Fix Sepi v2.61")
    
    umr = st.number_input("UMR Domisili (Rp)", value=4900000, step=100000, key="umr261")
    st.caption(f"Ref: Rp {umr*0.05:,.0f} | Biaya: Rp X/bulan - Mode Etika")

    tab1, tab2, tab3 = st.tabs(["Kolom 1: Fondasi", "Kolom 2: Perjalanan", "Kolom 3: Puncak"])
    with tab1:
        st.markdown("#### Fondasi Teduh - Mindset & Niat")
        st.image("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800")
        st.markdown("**FIX SEPI v2.61 - SOP, ERP, OEE, KPI Disempurnakan Alkitab:**")
        st.markdown("> SOP, ERP, OEE, KPI - Improvement Culture, proses secara benar")
        play_worship_v261("Ruang 2 - SOP/ERP/OEE/KPI")
    with tab2:
        st.write("Perjalanan Employee v2.61")
    with tab3:
        st.write("Puncak Teduh v2.61")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Kembali", use_container_width=True, key="b1_261"):
            st.session_state.ruang=1
            st.rerun()
    with c2:
        if st.button("➡️ Masuk Ruang 3", type="primary", use_container_width=True, key="n2_261"):
            st.session_state.ruang=3
            st.rerun()
else:
    st.progress(100, text="Ruang 3 dari 3 - v2.61")
    st.markdown("## 💳 Rp X/bulan - v2.61")
    st.success(f"Email: {st.session_state.email}")
    st.markdown("### Cara Pembayaran QR + Virtual Account")
    st.code("QRIS: ruangteduh.ai/pay/TAVO-v261")
    play_worship_v261("Ruang 3 - Konfirmasi")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Kembali", use_container_width=True, key="b2_261"):
            st.session_state.ruang=2
            st.rerun()
    with c2:
        if st.button("✅ Bayar v2.61", type="primary", use_container_width=True, key="pay261"):
            st.balloons()
            st.success(f"v2.61 Berlangganan via QR/VA! Cek {st.session_state.email}")

# Floating Dot v2.61
floating_code = """
<html><head><style>
body{margin:0;background:transparent;font-family:sans-serif}
#dot{width:20px;height:20px;background:#22c55e;border-radius:50%;position:fixed;bottom:20px;right:20px;cursor:pointer;border:2px solid white;box-shadow:0 0 0 4px rgba(34,197,94,0.2),0 4px 12px rgba(0,0,0,0.3);animation:pulse 2s infinite;z-index:999}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(34,197,94,0.6),0 4px 12px rgba(0,0,0,0.3)}70%{box-shadow:0 0 0 10px rgba(34,197,94,0),0 4px 12px rgba(0,0,0,0.3)}100%{box-shadow:0 0 0 0 rgba(34,197,94,0),0 4px 12px rgba(0,0,0,0.3)}}
#panel{display:none;position:fixed;bottom:60px;right:20px;width:350px;max-width:85vw;background:white;border-radius:16px;padding:14px;box-shadow:0 10px 40px rgba(0,0,0,0.25);border:1px solid #eee;font-size:13px}
#panel.open{display:block}
#panel input{width:100%;padding:8px;border-radius:8px;border:1px solid #ddd;margin-top:8px;box-sizing:border-box}
.msg{margin:6px 0;padding:6px 8px;border-radius:8px;background:#f5f5f5}
.msg.ai{background:#dcfce7}
</style></head><body>
<div id="dot" title="v2.61 Worship Asli"></div>
<div id="panel"><div style="font-weight:700">💬 Full Chat v2.61 - Worship Asli</div><div style="font-size:12px;color:#666">Format baru: st.audio("assets/worship_teduh.mp3") - 1 baris doang!</div><div id="chat"></div><input id="q" placeholder="Ketik di Ruang 1..." /><div style="font-size:10px;color:#999;margin-top:6px">v2.6 -> v2.61 - assets/worship_teduh.mp3</div></div>
<script>
const dot=document.getElementById('dot'),panel=document.getElementById('panel'),q=document.getElementById('q'),chat=document.getElementById('chat');
dot.onclick=()=>panel.classList.toggle('open');
q.addEventListener('keydown',e=>{if(e.key==='Enter'&&q.value.trim()!==''){const u=q.value;chat.innerHTML+='<div class=msg><b>Member:</b> '+u+'</div>';let a='';if(u.toLowerCase().includes('bayar'))a='Via QR & VA - Email wajib assets/worship_teduh.mp3';else a='v2.61 - Worship asli sudah aktif!';chat.innerHTML+='<div class=msg ai><b>AI Teduh v2.61:</b> '+a+'</div>';q.value=''}});
</script></body></html>
"""
components.html(floating_code, height=550)

st.caption("v2.61 - PATCH WORSHIP - st.audio(assets/worship_teduh.mp3) - Format baru 1 baris, gak perlu 5 jadi 6 file")
