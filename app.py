import streamlit as st
import os, json, hashlib, time
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Ruang Teduh v2.9 PERFECT", layout="wide", initial_sidebar_state="expanded")

# ================= STATE =================
if 'current_ruang' not in st.session_state:
    st.session_state.current_ruang = 'R1'
if 'is_subscribed' not in st.session_state:
    st.session_state.is_subscribed = False
if 'member_email' not in st.session_state:
    st.session_state.member_email = "asuveleikha@gmail.com"
if 'riwayat' not in st.session_state:
    st.session_state.riwayat = []
if 'config' not in st.session_state:
    st.session_state.config = {
        "bca_rek": "1234567890",
        "bca_an": "Ruang Teduh Yayasan",
        "hp_wa": "085692162564",
        "hp_gopay": "085692162564"
    }

# ================= BUANG SAMPAH CACHE - SESUAI REQUEST LO =================
def buang_sampah_cache(ruang_id):
    prefix = ruang_id.lower() + "_"
    to_del = [k for k in list(st.session_state.keys()) if k.startswith(prefix) and not k.endswith('_blank') and k != f"{prefix}progress"]
    for k in to_del:
        try:
            del st.session_state[k]
        except:
            pass
    # Jangan clear semua cache, cuma audio
    try:
        st.cache_data.clear()
    except:
        pass

def pindah_ruang(tujuan):
    asal = st.session_state.current_ruang
    # LOGIC PERFECT: R1 tetap ada bila belum R2, R2 tetap ada bila belum R3
    if asal == 'R1' and tujuan == 'R2':
        buang_sampah_cache('R1')
        if 'R1→R2' not in st.session_state.riwayat:
            st.session_state.riwayat.append('R1→R2')
    elif asal == 'R2' and tujuan == 'R3':
        if not st.session_state.is_subscribed:
            st.session_state.current_ruang = 'PAYMENT'
            return
        buang_sampah_cache('R2')
        if 'R2→R3' not in st.session_state.riwayat:
            st.session_state.riwayat.append('R2→R3')
    elif tujuan == 'PAYMENT':
        st.session_state.current_ruang = 'PAYMENT'
        return
    st.session_state.current_ruang = tujuan

# ================= SUARA HALUS - BALIKIN v2.4/v2.5 YANG MEMIKAT =================
@st.cache_data(show_spinner=False)
def buat_audio_halus(teks, ruang_id):
    """v2.4/v2.5 style - gTTS slow=True + cache biar hemat"""
    try:
        from gtts import gTTS
        safe_teks = teks[:800]  # limit biar gak berat
        hash_id = hashlib.md5(safe_teks.encode()).hexdigest()[:8]
        tmp_path = f"/tmp/suara_{ruang_id}_{hash_id}.mp3"
        if not Path(tmp_path).exists():
            tts = gTTS(text=safe_teks, lang='id', slow=True)  # slow=True = halus
            tts.save(tmp_path)
        return tmp_path
    except Exception as e:
        # Fallback kalau gtts gagal
        print(f"gTTS error: {e}")
        return None

def player_suara_v24(quote, ruang_id):
    # Visual player cantik v2.4/v2.5
    st.markdown(f"""
    <div style="background:#1a3c34; padding:14px 18px; border-radius:16px; color:white; display:flex; align-items:center; gap:14px; margin:12px 0;">
        <div style="background:#2d5a4a; width:44px; height:44px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:20px; animation: pulse 2s infinite;">🎧</div>
        <div>
            <div style="font-weight:700; font-size:14px;">Suara Halus Ruang Teduh • v2.4/v2.5 Memikat</div>
            <div style="font-size:11px; opacity:0.8;">Dari mata turun ke hati • Halus di kuping • Backsound embun pagi</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2 tombol: Play gTTS + Play Browser TTS (fallback kalau gTTS hilang)
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"▶️ Play Nasehat {ruang_id} (Halus)", key=f"btn_play_{ruang_id}", use_container_width=True):
            path = buat_audio_halus(quote, ruang_id)
            if path and Path(path).exists():
                st.audio(path, format='audio/mp3', autoplay=True)
                st.success(f"🔊 Memutar suara halus {ruang_id}...")
            else:
                st.warning("gTTS lagi gangguan, pakai suara browser di sebelah →")
                st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", autoplay=True)
    with col2:
        # Fallback browser SpeechSynthesis API - langsung bunyi tanpa file
        if st.button(f"🔊 Suara Browser {ruang_id}", key=f"btn_browser_{ruang_id}", use_container_width=True):
            # HTML + JS untuk speech synthesis
            html_code = f"""
            <script>
            const teks = `{quote.replace('`','').replace(chr(34),"'")}`;
            const utter = new SpeechSynthesisUtterance(teks);
            utter.lang = 'id-ID';
            utter.rate = 0.85;
            utter.pitch = 0.9;
            utter.volume = 1;
            speechSynthesis.speak(utter);
            </script>
            <div style="background:#e8f5e9; padding:8px; border-radius:8px; font-size:12px;">🔊 Memutar via Browser TTS (id-ID, 0.85x halus)...</div>
            """
            st.components.v1.html(html_code, height=80)

# ================= VISUAL MEMIKAT v2.5 =================
def kartu_visual(emoji, visual_desc, judul, quote, renungan, terapan, warna="#fdf6e3"):
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a3c34 0%, #2d5a4a 100%); padding:26px; border-radius:24px; color:white; text-align:center; box-shadow: 0 8px 24px rgba(0,0,0,0.2);">
        <div style="font-size:54px;">{emoji}</div>
        <div style="font-size:10px; letter-spacing:2px; opacity:0.7; margin-top:4px;">{visual_desc}</div>
        <div style="font-size:24px; font-weight:800; margin-top:8px; font-family:serif;">{judul}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:{warna}; padding:20px; border-radius:18px; border-left:6px solid #1a3c34; margin:12px 0;">
        <div style="font-size:19px; font-family:serif; font-style:italic; color:#1a3c34; line-height:1.6;">"{quote}"</div>
        <div style="margin-top:10px; font-size:12px; color:#555;"><b>Renungan:</b> {renungan}</div>
        <div style="margin-top:8px; font-size:12px; color:#1a3c34; font-weight:700;">🌱 {terapan}</div>
    </div>
    """, unsafe_allow_html=True)

# ================= FORM BLANK (BENTUK SEMULA) =================
def form_blank(r_name):
    st.markdown(f"""
    <div style="border:2px dashed #bbb; padding:14px; border-radius:12px; background:#fafafa; text-align:center; font-size:12px;">
    <b>{r_name} - Bentuk Semula (Cache Dibuang)</b><br>Form kosong, sampah ketikan sudah dibuang. Member tetap di ruang terbaru.
    </div>
    """, unsafe_allow_html=True)

# ================= RUANG 1 PERFECT =================
def ruang1():
    st.caption("Ruang 1 tetap ada bila belum masuk ke Ruang 2")
    kartu_visual("🌿", "VISUAL: Sawah Embun Pagi • Matahari Terbit • Tenang", 
                 "Ruang 1 - Pustaka Teduh - Santapan Rohani",
                 "Embun pagi tidak pernah terburu-buru, tapi ia membasahi seluruh ladang. Begitu juga kasih, dari mata turun ke hati.",
                 "Otak butuh 5 detik visual hijau sebelum bisa menerima nasehat. Lihat dulu, baru dengar, baru renungkan.",
                 "Terapan: Tarik nafas 5 detik sambil lihat visual hijau", "#fdf6e3")
    player_suara_v24("Embun pagi tidak pernah terburu-buru, tapi ia membasahi seluruh ladang. Begitu juga kasih, dari mata turun ke hati. Shalom.", "R1")
    
    st.markdown("---")
    st.markdown("**📝 Form Aktif Ruang 1 (v2.4/v2.5) - Akan ke-reset pas masuk R2**")
    st.text_input("Nama Member", key="r1_nama", placeholder="Tulis nama")
    st.text_area("Nasehat hari ini", key="r1_nasehat", height=90, placeholder="Tulis renungan...")
    st.slider("Progress Pustaka", 0, 1000, 2, key="r1_progress")
    if st.button("➡️ Masuk Ruang 2 - Pustaka Layanan", type="primary", use_container_width=True, key="to_r2"):
        pindah_ruang('R2')
        st.rerun()

# ================= RUANG 2 PERFECT =================
def ruang2():
    st.caption("Ruang 2 tetap ada bila belum masuk ke Ruang 3 • Member berasa di Ruang 2")
    with st.expander("📖 Lihat Ruang 1 - Sudah di-reset ke bentuk semula", expanded=False):
        form_blank("Ruang 1 - Pustaka Teduh")
    
    kartu_visual("🏢", "VISUAL: Teamwork Hangat • Chef Ajari Junior • Kerja Ibadah",
                 "Ruang 2 - Pustaka Layanan Member - TAVO - Rp200rb/300rb",
                 "Kolose 3:23 Advance - Bekerja untuk Tuhan dengan level MALKHUTKHA. Dari Staff → Supervisor → Manager.",
                 "Kerja bukan soal gaji, tapi skill naik, jaringan luas. Visual teamwork memicu rasa memiliki.",
                 "SOP/ERP/OEE/KPI via GDrive/Github - Corporation Access Dasar", "#fff8e1")
    player_suara_v24("Bekerja untuk Tuhan dengan level Malkhutkha. Dari Staff menjadi Supervisor menjadi Manager. Dapat bimbingan advance dan motivasi lebih besar.", "R2")
    
    st.markdown("---")
    st.markdown("**📝 Form Aktif Ruang 2 (v2.4/v2.5) - Akan ke-reset pas masuk R3**")
    st.text_input("Email Member (terkoneksi ke asuveleikha@gmail.com)", key="r2_email", value=st.session_state.member_email)
    st.text_input("WA", key="r2_wa", value=st.session_state.config["hp_wa"])
    st.selectbox("Paket", ["Employee 200rb/bulan", "Entrepreneur 300rb/bulan"], key="r2_paket")
    st.text_area("Pesan ke Admin Email & WA (ini yang lo ketik tadi gak ada suaranya)", key="r2_pesan", placeholder="Tulis pesan ke asuveleikha@gmail.com", height=100)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Kembali ke R1", use_container_width=True, key="back_r1"):
            pindah_ruang('R1')
            st.rerun()
    with c2:
        if st.button("🌟 Masuk Ruang 3 - MALKHUTKHA", type="primary", use_container_width=True, key="to_r3"):
            if not st.session_state.is_subscribed:
                pindah_ruang('PAYMENT')
                st.rerun()
            else:
                pindah_ruang('R3')
                st.rerun()

# ================= RUANG 3 PERFECT =================
def ruang3():
    st.success("✅ Member di Ruang 3 - Sudah Berlangganan - Member tetap di Ruang 3 saja")
    st.caption("Ruang 2 masih bentuk form semula tanpa sisa cache ketikan")
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("📖 R1 Blank (sampah dibuang)", expanded=False):
            form_blank("Ruang 1")
    with col2:
        with st.expander("🏢 R2 Blank (sampah dibuang)", expanded=False):
            form_blank("Ruang 2 - Pustaka Layanan")
    
    kartu_visual("🌟", "VISUAL: Corporation Megah • Cabang Banyak • Member Saling Access",
                 "Ruang 3 • TAVO MALKHUTKHA - Two Journey Advance",
                 "Tabur Tuai - Corporation Access - Member Saling Access! Employee butuh kerja, Entrepreneur butuh staff - Match di Ruang 3!",
                 "Motivasi lebih besar sudah ditempa. Visual corporation memicu visualisasi masa depan. Dari mata turun ke hati, dari hati jadi omzet.",
                 "Full Binding + Bimbingan Advance + Motivasi Besar + Corporation Access Full + Omzet Naik", "#e0f2f1")
    player_suara_v24("Tabur Tuai, Corporation Access, Member Saling Access. Member di Ruang tiga bisa access ke semua bidang dan skill bahkan corporation. Entrepreneur butuh staff, employee butuh kerja, match di Ruang tiga.", "R3")
    
    st.info(f"Member: {st.session_state.member_email} - Employee - Sudah magang 3 bulan di garment - Bisa access corporation")
    if st.button("⬅️ Kembali ke R2 (R2 tetap blank)", use_container_width=True, key="back_r2_from_r3"):
        st.session_state.current_ruang = 'R2'
        st.rerun()

# ================= PAYMENT =================
def payment():
    st.markdown("## 💳 Pembayaran Langganan - Target: R3")
    cfg = st.session_state.config
    st.markdown(f"""
    <div style="background:#fff3e0; padding:10px; border-radius:10px; border-left:4px solid #ff9800; font-size:13px;">
    <b>BCA:</b> {cfg['bca_rek']} a/n {cfg['bca_an']} | <b>WA:</b> {cfg['hp_wa']} | <b>GoPay:</b> {cfg['hp_gopay']}<br>
    <b>Rate:</b> Employee 200rb | Entrepreneur 300rb | MALKHUTKHA Full
    </div>
    """, unsafe_allow_html=True)
    
    tab_va, tab_qris, tab_wallet = st.tabs(["🏦 VA Bank", "📱 QRIS", "💚 GoPay/OVO/DANA"])
    with tab_va:
        st.write(f"VA auto-forward ke BCA {cfg['bca_rek']} - Aman masuk rekening kita")
        st.code(f"BCA VA: 12345 {cfg['hp_wa'][-4:]} | BRI VA: 88810 {cfg['hp_wa']} | BNI VA: 8810 {cfg['hp_wa']}", language="text")
        if st.button("✅ Simulasi VA Lunas → Masuk R3", key="va_lunas"):
            st.session_state.is_subscribed = True
            pindah_ruang('R3')
            st.rerun()
    with tab_qris:
        st.markdown(f"""<div style="background:white; border:2px solid #1a3c34; width:200px; height:200px; margin:auto; border-radius:14px; display:flex; align-items:center; justify-content:center; flex-direction:column;"><div style="font-size:50px;">🔳</div><div style="font-size:10px;">QRIS {cfg['hp_gopay']}</div><div style="font-size:9px; background:#1a3c34; color:white; padding:2px 8px; border-radius:6px; margin-top:4px;">Rp200rb</div></div>""", unsafe_allow_html=True)
        if st.button("✅ Simulasi QRIS Lunas → Masuk R3", key="qris_lunas", type="primary"):
            st.session_state.is_subscribed = True
            pindah_ruang('R3')
            st.rerun()
    with tab_wallet:
        st.write(f"GoPay/OVO/DANA {cfg['hp_gopay']} - Butuh 2x24 jam kalau baru daftar SIM baru")
        if st.button(f"Kirim Tagihan GoPay {cfg['hp_gopay']}", key="wallet_lunas"):
            st.session_state.is_subscribed = True
            pindah_ruang('R3')
            st.rerun()
    
    if st.button("⬅️ Kembali ke R2", key="back_from_pay"):
        pindah_ruang('R2')
        st.rerun()

# ================= SIDEBAR PERFECT - FIX RERUN BUG =================
with st.sidebar:
    st.markdown("### 🌿 Ruang Teduh v2.9 PERFECT")
    st.caption(f"Posisi: {st.session_state.current_ruang} | Langganan: {'✅ Aktif' if st.session_state.is_subscribed else '❌ Belum'}")
    st.caption(f"Riwayat: {' > '.join(st.session_state.riwayat) if st.session_state.riwayat else 'Baru'}")
    
    if st.session_state.current_ruang == 'R1':
        st.markdown('<div style="background:#1a3c34; color:white; padding:10px; border-radius:10px; text-align:center;">📚 2/1000<br>Pustaka Teduh<br><span style="font-size:10px;">Ruang 1 Aktif</span></div>', unsafe_allow_html=True)
    else:
        st.info(f"R1 standby 2/1000 • Sekarang di {st.session_state.current_ruang}")
    
    st.markdown("---")
    # FIX: Jangan pakai on_click + rerun, pakai if button
    if st.button("📖 Ruang 1", use_container_width=True, key="sb_r1"):
        pindah_ruang('R1')
        st.rerun()
    if st.button("🏢 Ruang 2", use_container_width=True, key="sb_r2"):
        pindah_ruang('R2')
        st.rerun()
    if st.button("🌟 Ruang 3 (Perlu Langganan)" if not st.session_state.is_subscribed else "🌟 Ruang 3", use_container_width=True, key="sb_r3"):
        if not st.session_state.is_subscribed:
            pindah_ruang('PAYMENT')
        else:
            pindah_ruang('R3')
        st.rerun()
    
    st.markdown("---")
    # Checkbox simulasi - FIX agar langsung aktifkan R3
    cek = st.checkbox("✅ Simulasi Sudah Bayar (biar bisa masuk R3)", value=st.session_state.is_subscribed, key="chk_bayar")
    if cek != st.session_state.is_subscribed:
        st.session_state.is_subscribed = cek
        if cek:
            st.success("Aktif! Sekarang bisa masuk R3")
        st.rerun()
    
    st.markdown(f"📧 Admin: {st.session_state.member_email}")
    st.caption("R1 tetap ada bila belum R2 • R2 tetap ada bila belum R3 • Masuk R2=R1 reset • Masuk R3=R2 reset")

# ================= MAIN - FIX ANTI BOROS TAPI JANGAN EMPTY SEMBARANGAN =================
if st.session_state.current_ruang == 'R1':
    ruang1()
elif st.session_state.current_ruang == 'R2':
    ruang2()
elif st.session_state.current_ruang == 'R3':
    if not st.session_state.is_subscribed:
        st.warning("🔒 R3 butuh langganan, centang Simulasi Sudah Bayar di sidebar atau bayar via QRIS/VA")
        payment()
    else:
        ruang3()
elif st.session_state.current_ruang == 'PAYMENT':
    payment()
