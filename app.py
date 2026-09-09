"""
RUANG TEDUH - BUKU 3 LEMBAR V29 - Three Way Function
1 Ruang = 1 Buku | 3 Tembusan Otomatis

LEMBAR 1 PUTIH: RUANG TEDUH - Entry Member
LEMBAR 2 MERAH: RUANG INTERAKSI - Manage Member Terikat  
LEMBAR 3 HIJAU: RUANG BOARDING - Storage SOP ERP OEE KPI ALKITAB

Flowchart konsep sama, tampilan floorplan jadi buku nota NCR
"""

import streamlit as st
import os

# ========== CONFIG ==========
st.set_page_config(
    page_title="Ruang Teduh - Buku 3 Lembar V29",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== FLAGS ANTI MUSIK STRESS ==========
USE_MUSIC = False
AUTOPLAY = False

# ========== STATE ==========
if "email_member" not in st.session_state:
    st.session_state.email_member = ""
if "lembar_active" not in st.session_state:
    st.session_state.lembar_active = 1
if "member_terikat" not in st.session_state:
    st.session_state.member_terikat = False
if "audio_played" not in st.session_state:
    st.session_state.audio_played = False
if "payment_done" not in st.session_state:
    st.session_state.payment_done = False

# ========== CSS BUKU 3 LEMBAR ==========
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');

* { font-family: 'Inter', sans-serif; }
.mono { font-family: 'JetBrains Mono', monospace; }

/* Book Container */
.book-wrapper {
    background: #F5F5F0;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
}

/* Perforation effect */
.perforasi {
    position: absolute;
    left: -12px;
    top: 0;
    bottom: 0;
    width: 20px;
    background-image: radial-gradient(circle, #ccc 3px, transparent 4px);
    background-size: 20px 20px;
    background-repeat: repeat-y;
}

/* Lembar Styles */
.lembar {
    border-radius: 12px;
    padding: 24px 24px 24px 32px;
    margin-bottom: 20px;
    position: relative;
    border-left: 3px dashed #bbb;
    box-shadow: 4px 4px 0px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
}
.lembar-putih {
    background: #FFFFFF;
    border-top: 4px solid #9E9E9E;
}
.lembar-merah {
    background: #FFEBEE;
    border-top: 4px solid #FF5252;
}
.lembar-hijau {
    background: #E8F5E9;
    border-top: 4px solid #4CAF50;
}

.lembar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 2px dashed rgba(0,0,0,0.1);
}
.lembar-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 4px 10px;
    border-radius: 4px;
}
.label-putih { background: #424242; color: white; }
.label-merah { background: #FF5252; color: white; }
.label-hijau { background: #4CAF50; color: white; }

.flow-box {
    background: rgba(255,255,255,0.8);
    border: 2px solid rgba(0,0,0,0.1);
    border-radius: 8px;
    padding: 12px;
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 600;
}

/* Floating Dot */
.floating-dot {
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 56px;
    height: 56px;
    background: linear-gradient(135deg, #FF8A65, #FF5722);
    border-radius: 50%;
    box-shadow: 0 4px 20px rgba(255,87,34,0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 24px;
    z-index: 999;
    cursor: pointer;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(255,87,34,0.7); }
    70% { box-shadow: 0 0 0 12px rgba(255,87,34,0); }
    100% { box-shadow: 0 0 0 0 rgba(255,87,34,0); }
}

/* Carbon copy text */
.carbon-copy {
    opacity: 0.6;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    background: rgba(255,255,0,0.2);
    padding: 2px 6px;
    border-radius: 3px;
}

/* Storage Rak */
.rak {
    background: white;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 14px;
    text-align: center;
    height: 110px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.rak-icon { font-size: 28px; margin-bottom: 6px; }
.rak-title { font-weight: 800; font-size: 13px; letter-spacing: 0.5px; }
.rak-desc { font-size: 11px; color: #666; margin-top: 4px; font-family: 'JetBrains Mono', monospace; }

/* Three way line */
.three-way-connector {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    margin: 16px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #888;
}
</style>
""", unsafe_allow_html=True)

# ========== HELPER ==========
def load_nasehat():
    try:
        if os.path.exists("nasehat_mingguan.txt"):
            with open("nasehat_mingguan.txt", "r", encoding="utf-8") as f:
                return f.read()
        return "Senin: SOP Cek Kebersihan\nSelasa: ERP Jam 9 Tepat\nRabu: OEE 95%\nKamis: KPI Review\nJumat: Alkitab Fondasi"
    except:
        return "Nasehat mingguan tidak tersedia"

def load_core_info():
    try:
        import core
        return True
    except:
        return False

core_available = load_core_info()

# ========== HEADER BUKU ==========
st.markdown("""
<div style="text-align:center; padding: 10px 0 20px 0;">
    <div style="font-family:'JetBrains Mono'; font-size:11px; letter-spacing:3px; color:#888;">TAVO MALKHUTKHA • V29</div>
    <div style="font-size:28px; font-weight:800; margin:6px 0;">📖 BUKU 1 RUANG - 3 LEMBAR TEMBUSAN</div>
    <div style="font-family:'JetBrains Mono'; font-size:12px; color:#666; background:#FFF9C4; display:inline-block; padding:4px 12px; border-radius:20px;">
        Three Way Function • 1x Input = 3x Tembus Otomatis
    </div>
</div>
""", unsafe_allow_html=True)

# ========== TAB NAVIGASI BUKU ==========
tab1, tab2, tab3 = st.tabs(["📄 LEMBAR 1 PUTIH - RUANG TEDUH", "🔴 LEMBAR 2 MERAH - RUANG INTERAKSI", "🟢 LEMBAR 3 HIJAU - RUANG BOARDING"])

# ==================== LEMBAR 1 PUTIH ====================
with tab1:
    st.markdown("""
    <div class="lembar lembar-putih">
        <div class="perforasi"></div>
        <div class="lembar-header">
            <div><b>LEMBAR 1 - RUANG TEDUH</b> <span style="font-size:12px; color:#666;">(Entry Gate)</span></div>
            <div class="lembar-label label-putih">ASLI - UNTUK MEMBER</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_qr, col_form = st.columns([1, 2])
    
    with col_qr:
        st.markdown("""
        <div class="flow-box" style="height:160px; display:flex; flex-direction:column; justify-content:center; background:white;">
            <div style="font-size:48px;">⬜</div>
            <div style="margin-top:8px;">QR GATE</div>
            <div style="font-size:10px; color:#888; margin-top:4px;">SCAN UNTUK MASUK</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='three-way-connector'>⬇ tembus ke merah & hijau</div>", unsafe_allow_html=True)
    
    with col_form:
        st.markdown("**📥 INPUT WAJIB - Three Way Source**")
        email_input = st.text_input(
            "Email Member (akan tercopy otomatis ke 2 lembar lain)",
            value=st.session_state.email_member,
            placeholder="nama@email.com",
            key="email_putih"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("✅ MASUK RUANG TEDUH", type="primary", use_container_width=True):
                if "@" in email_input and "." in email_input:
                    st.session_state.email_member = email_input
                    st.session_state.lembar_active = 2
                    st.success(f"Berhasil! Email {email_input} tercatat di 3 lembar")
                    st.balloons()
                else:
                    st.error("Email tidak valid bro")
        with col_b:
            st.markdown(f"<div class='carbon-copy'>📋 Tembusan: {email_input if email_input else 'belum input'}</div>", unsafe_allow_html=True)
        
        if st.session_state.email_member:
            st.info(f"✓ Member: **{st.session_state.email_member}** sudah masuk Ruang Teduh (Lembar Putih)")

    # Flow visualization
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown('<div class="flow-box">📱 SCAN QR</div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="flow-box">📧 INPUT EMAIL WAJIB</div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="flow-box">✔️ VALIDASI</div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="flow-box" style="background:#E8F5E9;">🌿 MASUK TEDUH</div>', unsafe_allow_html=True)
    
    st.caption("File terhubung: app.py (UI Full Width + Floating Dot) • requirements.txt")

# ==================== LEMBAR 2 MERAH ====================
with tab2:
    st.markdown("""
    <div class="lembar lembar-merah">
        <div class="perforasi"></div>
        <div class="lembar-header">
            <div><b>LEMBAR 2 - RUANG INTERAKSI</b> <span style="font-size:12px; color:#666;">(Management)</span></div>
            <div class="lembar-label label-merah">TEMBUSAN 1 - KELOLA IKATAN</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.email_member:
        st.warning("⚠️ Isi dulu Lembar Putih (Email) bro - baru bisa akses Ruang Interaksi")
        st.stop()
    
    st.markdown(f"<div class='carbon-copy'>📋 Carbon Copy dari Putih: {st.session_state.email_member} • Status: Mau Terikat</div>", unsafe_allow_html=True)
    st.markdown("")
    
    col_emp, col_audio = st.columns([2, 1])
    
    with col_emp:
        st.markdown("**👥 PILIH EMPLOYEE - Kelola Member Terikat**")
        employee = st.selectbox(
            "Employee yang handle",
            ["Pilih Employee", "Employee A - Sage", "Employee B - Beige", "Employee C - Orange"],
            label_visibility="collapsed"
        )
        
        st.markdown("**💬 Ruang Interaksi Chat**")
        if core_available:
            try:
                import core
                st.write("Core.py terhubung - SOP->ERP->OEE->KPI")
            except:
                st.text_area("Chat Interaksi", placeholder="Halo, selamat datang di Ruang Teduh...", height=120)
        else:
            chat_msg = st.text_area(
                "Chat Interaksi",
                placeholder=f"Halo {st.session_state.email_member}, selamat datang...",
                height=120,
                key="chat_merah"
            )
        
        if st.button("🔗 IKAT & LANJUT KE BOARDING (HIJAU)", use_container_width=True):
            st.session_state.member_terikat = True
            st.session_state.lembar_active = 3
            st.success("Member terikat! Lanjut ke Ruang Boarding (Hijau)")
    
    with col_audio:
        st.markdown("**🔊 AUDIO TEDUH**")
        st.markdown("""
        <div class="flow-box" style="background:white;">
            <div style="font-size:32px;">🎵</div>
            <div style="font-size:11px; margin-top:6px;">Worship Teduh<br/>Slow Piano + Nature</div>
            <div style="font-size:9px; color:#FF5252; margin-top:6px; background:#FFEBEE; padding:2px 6px; border-radius:4px;">NO AUTOPLAY<br/>KLIK UNTUK BUNYI</div>
        </div>
        """, unsafe_allow_html=True)
        
        audio_file = "ruang1_V28.1_NO_MUSIC.mp3"
        if os.path.exists(audio_file):
            if st.button("🔊 PUTAR", key="putar_merah"):
                st.session_state.audio_played = True
            if st.session_state.audio_played:
                st.audio(audio_file, format="audio/mp3")
                st.caption("✓ Audio SOP Only - No Musik Stress")
        else:
            st.caption("Audio file belum ada - pakai mode hening")
            if st.button("🔊 SIMULASI PUTAR", key="sim_putar"):
                st.toast("🔊 Bunyi: Worship Teduh Slow Piano (Hening, SOP Only)")
        
        st.markdown("---")
        st.markdown("**📅 Nasehat Mingguan**")
        st.code(load_nasehat(), language="text")

    # 4 Pilar
    st.markdown("---")
    p1, p2, p3, p4 = st.columns(4)
    with p1: st.markdown('<div class="rak" style="border-color:#FF5252;"><div class="rak-icon">🧹</div><div class="rak-title">SOP</div><div class="rak-desc">Kebersihan</div></div>', unsafe_allow_html=True)
    with p2: st.markdown('<div class="rak" style="border-color:#FF5252;"><div class="rak-icon">⏰</div><div class="rak-title">ERP</div><div class="rak-desc">Jam 9 Tepat</div></div>', unsafe_allow_html=True)
    with p3: st.markdown('<div class="rak" style="border-color:#FF5252;"><div class="rak-icon">⚙️</div><div class="rak-title">OEE</div><div class="rak-desc">Target 95%</div></div>', unsafe_allow_html=True)
    with p4: st.markdown('<div class="rak" style="border-color:#FF5252;"><div class="rak-icon">📊</div><div class="rak-title">KPI</div><div class="rak-desc">Performance</div></div>', unsafe_allow_html=True)
    
    st.caption("File terhubung: core.py (Otak SOP->ERP->OEE->KPI) • nasehat_mingguan.txt")

# ==================== LEMBAR 3 HIJAU ====================
with tab3:
    st.markdown("""
    <div class="lembar lembar-hijau">
        <div class="perforasi"></div>
        <div class="lembar-header">
            <div><b>LEMBAR 3 - RUANG BOARDING</b> <span style="font-size:12px; color:#666;">(Storage System)</span></div>
            <div class="lembar-label label-hijau">TEMBUSAN 2 - STORAGE ATURAN</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.email_member:
        st.warning("⚠️ Isi Lembar Putih dulu")
        st.stop()
    
    st.markdown(f"<div class='carbon-copy'>📋 Carbon Copy Final: {st.session_state.email_member} • Status: {'TERIKAT ✓' if st.session_state.member_terikat else 'Belum Terikat'} • Storage Permanen</div>", unsafe_allow_html=True)
    st.markdown("")
    
    st.markdown("### 🗄️ STORAGE SYSTEM - Full Aturan Tersystematis")
    st.caption("Lembar 3 ini full aturan yang tersystematis yaitu SOP, ERP, OEE, KPI dan Alkitab")
    
    s1, s2, s3, s4, s5 = st.columns(5)
    with s1:
        st.markdown("""
        <div class="rak" style="border-color:#4CAF50; background:#E8F5E9;">
            <div class="rak-icon">📜</div>
            <div class="rak-title">SOP</div>
            <div class="rak-desc">Standard Operating<br/>Cek kebersihan Senin<br/>Checklist harian</div>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown("""
        <div class="rak" style="border-color:#4CAF50; background:#E8F5E9;">
            <div class="rak-icon">🏢</div>
            <div class="rak-title">ERP</div>
            <div class="rak-desc">Enterprise System<br/>Jam 9 Tepat<br/>Integrasi data</div>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown("""
        <div class="rak" style="border-color:#4CAF50; background:#E8F5E9;">
            <div class="rak-icon">⚙️</div>
            <div class="rak-title">OEE</div>
            <div class="rak-desc">Overall Equipment<br/>Target 95%<br/>Efficiency</div>
        </div>
        """, unsafe_allow_html=True)
    with s4:
        st.markdown("""
        <div class="rak" style="border-color:#4CAF50; background:#E8F5E9;">
            <div class="rak-icon">📈</div>
            <div class="rak-title">KPI</div>
            <div class="rak-desc">Key Performance<br/>Review Mingguan<br/>Tracking</div>
        </div>
        """, unsafe_allow_html=True)
    with s5:
        st.markdown("""
        <div class="rak" style="border-color:#4CAF50; background:#E8F5E9;">
            <div class="rak-icon">📖</div>
            <div class="rak-title">ALKITAB</div>
            <div class="rak-desc">Fondasi Nilai<br/>Tavo Malkhutkha<br/>Spiritual Core</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    col_pay, col_inv = st.columns([1, 1])
    
    with col_pay:
        st.markdown("**💳 QRIS VA - Payment Gate**")
        st.markdown("""
        <div class="flow-box" style="height:140px; display:flex; flex-direction:column; justify-content:center;">
            <div style="font-size:40px;">💚</div>
            <div>QRIS VA PAYMENT</div>
            <div style="font-size:10px; color:#666;">Scan untuk Full Access</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✅ SIMULASI BAYAR QRIS", use_container_width=True):
            st.session_state.payment_done = True
            st.success("Pembayaran tercatat di Storage Hijau!")
    
    with col_inv:
        st.markdown("**🧾 INVOICE & FULL ACCESS**")
        if st.session_state.payment_done:
            st.success("INVOICE LUNAS - FULL ACCESS GRANTED")
            st.markdown(f"""
            ```
            INVOICE - RUANG TEDUH V29
            --------------------------
            Member: {st.session_state.email_member}
            Lembar: 3 Rangkap (Putih/Merah/Hijau)
            Storage: SOP/ERP/OEE/KPI/Alkitab
            Status: TERIKAT & LUNAS
            Access: FULL CHAT
            ```
            """)
            st.markdown("**💬 FULL ACCESS CHAT**")
            st.text_input("Chat Full Access", placeholder="Ketik disini setelah lunas...", key="full_chat")
        else:
            st.info("Belum bayar - Invoice pending di Storage")
    
    # Flow final
    st.markdown("---")
    f1, f2, f3, f4 = st.columns(4)
    with f1: st.markdown('<div class="flow-box">💳 QRIS VA</div>', unsafe_allow_html=True)
    with f2: st.markdown('<div class="flow-box">🧾 INVOICE</div>', unsafe_allow_html=True)
    with f3: st.markdown('<div class="flow-box" style="background:#C8E6C9;">🔓 FULL ACCESS</div>', unsafe_allow_html=True)
    with f4: st.markdown('<div class="flow-box" style="background:#A5D6A7;">🗄️ STORAGE RULES</div>', unsafe_allow_html=True)
    
    st.caption("File terhubung: README.md • SOP • ERP • OEE • KPI • ALKITAB = Storage Permanen")

# ========== FLOATING DOT ==========
st.markdown("""
<div class="floating-dot" title="Kontrol Utama - Kolom Lo + Meta AI">●</div>
""", unsafe_allow_html=True)

# ========== FOOTER THREE WAY FLOWCHART ==========
st.markdown("---")
st.markdown("### 🔄 FLOWCHART THREE WAY FUNCTION - Tetap Sama")
st.markdown("""
<div style="background:white; border-radius:12px; padding:20px; border:2px solid #eee; font-family:'JetBrains Mono', monospace; font-size:12px;">
<div style="text-align:center; margin-bottom:12px;">
<div style="background:#FFF9C4; display:inline-block; padding:6px 14px; border-radius:20px; font-weight:700;">INPUT: Email Member (Lembar Putih)</div>
<div style="margin:8px 0;">⬇</div>
<div style="color:#888;">CARBON COPY OTOMATIS - 1x tulis = 3x tembus</div>
<div style="margin:8px 0;">⬇ ⬇ ⬇</div>
</div>
<div style="display:flex; gap:12px; justify-content:center;">
<div style="flex:1; background:#FAFAFA; border:2px solid #9E9E9E; border-radius:8px; padding:12px; text-align:center;">
<b>PUTIH</b><br/>Ruang Teduh<br/>Entry Gate<br/>app.py
</div>
<div style="flex:1; background:#FFEBEE; border:2px solid #FF5252; border-radius:8px; padding:12px; text-align:center;">
<b>MERAH</b><br/>Ruang Interaksi<br/>Manage Terikat<br/>core.py
</div>
<div style="flex:1; background:#E8F5E9; border:2px solid #4CAF50; border-radius:8px; padding:12px; text-align:center;">
<b>HIJAU</b><br/>Ruang Boarding<br/>Storage System<br/>SOP ERP OEE KPI ALKITAB
</div>
</div>
<div style="text-align:center; margin-top:12px;">
<div>⬇ ⬇ ⬇</div>
<div style="background:#C8E6C9; display:inline-block; padding:6px 14px; border-radius:20px; font-weight:700; margin-top:8px;">FULL ACCESS CHAT - Semua Aturan Tersimpan</div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align:center; color:#999; font-family:JetBrains Mono; font-size:10px; margin-top:20px;'>Terstruktur • Tersystematis • Terinstallasi Benar • Sesuai Flow Chat • V29 Buku 3 Lembar</div>", unsafe_allow_html=True)
