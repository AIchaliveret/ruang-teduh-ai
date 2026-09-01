import streamlit as st
import json, time, hashlib
import numpy as np
from pathlib import Path

st.set_page_config(page_title="Ruang Teduh v2.7 FINAL - Halus Lancar Memikat", layout="wide", initial_sidebar_state="expanded")

# ================= STATE AWAL =================
if 'current_ruang' not in st.session_state:
    st.session_state.current_ruang = 'R1'
if 'is_subscribed' not in st.session_state:
    st.session_state.is_subscribed = False
if 'member_email' not in st.session_state:
    st.session_state.member_email = "asuveleikha@gmail.com"
if 'riwayat' not in st.session_state:
    st.session_state.riwayat = []
if 'payment_status' not in st.session_state:
    st.session_state.payment_status = 'belum'

# ================= BUANG SAMPAH CACHE (KUNCI REQUEST LO) =================
def buang_sampah_cache(ruang_id):
    """Hapus ketikan member di ruang itu, balikin ke bentuk semula"""
    prefix = ruang_id.lower() + "_"
    to_del = [k for k in st.session_state.keys() if k.startswith(prefix) and not k.endswith('_blank')]
    for k in to_del:
        del st.session_state[k]
    st.cache_data.clear()

def pindah_ruang(tujuan):
    asal = st.session_state.current_ruang
    # R1 -> R2 : buang R1
    if asal == 'R1' and tujuan == 'R2':
        buang_sampah_cache('R1')
        st.session_state.riwayat.append('R1→R2')
    # R2 -> R3 : cek langganan, buang R2
    elif asal == 'R2' and tujuan == 'R3':
        if not st.session_state.is_subscribed:
            st.session_state.current_ruang = 'PAYMENT'
            st.session_state.payment_target = 'R3'
            st.rerun()
            return
        buang_sampah_cache('R2')
        st.session_state.riwayat.append('R2→R3')
    # R1 -> R3 langsung
    elif asal == 'R1' and tujuan == 'R3':
        if not st.session_state.is_subscribed:
            st.session_state.current_ruang = 'PAYMENT'
            st.session_state.payment_target = 'R3'
            st.rerun()
            return
        buang_sampah_cache('R1')
        buang_sampah_cache('R2')
    # Balik
    elif tujuan == 'R1':
        # kalau balik, tetap R2/R3 blank
        pass
    
    st.session_state.current_ruang = tujuan
    st.rerun()

# ================= SUARA HALUS (CACHE HEMAT) =================
@st.cache_data(show_spinner=False)
def buat_suara_halus_cache(teks, ruang_id):
    try:
        from gtts import gTTS
        tmp = f"/tmp/suara_{ruang_id}_{hashlib.md5(teks.encode()).hexdigest()[:6]}.mp3"
        tts = gTTS(text=teks[:800], lang='id', slow=True) # slow=True biar halus
        tts.save(tmp)
        return tmp
    except:
        return None

def player_suara_halus(teks_nasehat, ruang_id):
    st.markdown(f"""
    <div style="background:#1a3c34; padding:14px 18px; border-radius:16px; color:white; display:flex; align-items:center; gap:14px; margin:14px 0;">
        <div style="background:#2d5a4a; width:44px; height:44px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:20px;">🎧</div>
        <div>
            <div style="font-weight:700;">Suara Halus Ruang Teduh • 0.85x Lembut</div>
            <div style="font-size:11px; opacity:0.8;">Memikat kalbu • Dari mata turun ke hati • Backsound embun</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns([1,3])
    with c1:
        play = st.button(f"▶️ Play Nasehat {ruang_id}", key=f"play_{ruang_id}_{time.time()}", use_container_width=True)
    if play:
        path = buat_suara_halus_cache(teks_nasehat, ruang_id)
        if path and Path(path).exists():
            st.audio(path, format='audio/mp3', autoplay=True)
        else:
            # Fallback kalau gTTS gagal di server
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        st.caption("🔊 Halus, memikat, sambil merenung...")

# ================= VISUAL + TEKS NASEHAT =================
def kartu_visual_memikat(judul, emoji, visual_desc, quote, renungan, terapan, warna_bg="#fdf6e3"):
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a3c34 0%, #2d5a4a 100%); padding:28px; border-radius:24px; color:white; text-align:center;">
        <div style="font-size:58px; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));">{emoji}</div>
        <div style="font-size:11px; letter-spacing:2.5px; opacity:0.7; margin-top:6px;">{visual_desc}</div>
        <div style="font-size:26px; font-weight:800; margin-top:10px; font-family:serif; line-height:1.2;">{judul}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:{warna_bg}; padding:22px; border-radius:20px; border-left:6px solid #1a3c34; margin:14px 0;">
        <div style="font-size:20px; font-family:serif; font-style:italic; color:#1a3c34; line-height:1.5;">"{quote}"</div>
        <div style="margin-top:12px; font-size:13px; color:#444;"><b>Renungan Psikologi:</b> {renungan}</div>
        <div style="margin-top:10px; font-size:13px; color:#1a3c34; font-weight:700;">🌱 {terapan}</div>
    </div>
    """, unsafe_allow_html=True)

def box_terapi_psikologi():
    st.markdown("""
    <div style="background:#e8f5e9; border:1px solid #c8e6c9; padding:14px; border-radius:14px; font-size:12px;">
    <b>💚 Terapi Cinta & Kasih - Dari Mata Turun ke Hati</b><br>
    Visual indah → mata terpikat → dopamin naik → hati hangat → kasih muncul. Makanya Ruang Teduh selalu kasih visual memikat dulu, baru suara halus, baru teks. 
    Pemandangan indah bisa memikat hati.
    </div>
    """, unsafe_allow_html=True)

def form_blank_template(ruang_name):
    st.markdown(f"""
    <div style="border:2px dashed #ccc; padding:16px; border-radius:14px; background:#fafafa; text-align:center;">
    <b>{ruang_name} - Bentuk Semula (Cache Dibuang)</b><br>
    <span style="font-size:11px; color:#888;">Form kosong, sampah ketikan sudah dibuang. Member tetap di ruang terbaru.</span>
    </div>
    """, unsafe_allow_html=True)

# ================= RUANG 1 =================
def tampilkan_R1():
    st.caption("Ruang 1 tetap ada bila belum masuk ke Ruang 2")
    kartu_visual_memikat(
        "Ruang 1 - Pustaka Teduh - Santapan Rohani", "🌿",
        "VISUAL: Sawah Embun Pagi • Matahari Terbit • Tenang",
        "Embun pagi tidak pernah terburu-buru, tapi ia membasahi seluruh ladang. Begitu juga kasih, dari mata turun ke hati.",
        "Otak kita butuh 5 detik visual hijau sebelum bisa menerima nasehat. Lihat dulu, baru dengar, baru renungkan.",
        "Terapan: Tarik nafas 5 detik sambil lihat visual hijau",
        "#fdf6e3"
    )
    player_suara_halus("Embun pagi tidak pernah terburu-buru, tapi ia membasahi seluruh ladang. Begitu juga kasih, dari mata turun ke hati. Shalom Namo Buddhaya.", "R1")
    box_terapi_psikologi()
    st.markdown("---")
    st.markdown("**📝 Form Ruang 1 (akan ke-reset pas masuk R2)**")
    st.text_input("Nama", key="r1_nama", placeholder="Nama member")
    st.text_area("Nasehat hari ini", key="r1_nasehat", height=80, placeholder="Tulis apa yang kamu dapat...")
    st.slider("Progress Pustaka Teduh", 0, 1000, 2, key="r1_progress")
    if st.button("➡️ Masuk Ruang 2 - Pustaka Layanan Member", type="primary", use_container_width=True):
        pindah_ruang('R2')

# ================= RUANG 2 =================
def tampilkan_R2():
    st.caption("Ruang 2 tetap ada bila belum masuk ke Ruang 3 • Member berasa di Ruang 2")
    with st.expander("📖 Lihat Ruang 1 - Sudah di-reset ke bentuk semula", expanded=False):
        form_blank_template("Ruang 1 - Pustaka Teduh")
    
    kartu_visual_memikat(
        "Ruang 2 - Pustaka Layanan Member - TAVO - Rp200rb/300rb", "🏢",
        "VISUAL: Teamwork Hangat • Chef Ajari Junior • Kerja Ibadah",
        "Kolose 3:23 Advance - Bekerja untuk Tuhan dengan level MALKHUTKHA. Dari Staff → Supervisor → Manager.",
        "Kerja bukan soal gaji, tapi skill naik, jaringan luas. Visual teamwork memicu rasa memiliki.",
        "SOP/ERP/OEE/KPI via GDrive/Github - Corporation Access Dasar",
        "#fff8e1"
    )
    player_suara_halus("Bekerja untuk Tuhan dengan level Malkhutkha. Dari Staff menjadi Supervisor menjadi Manager. Dapat bimbingan advance dan motivasi lebih besar. Terapan ekonomi gaji naik.", "R2")
    
    st.markdown("---")
    st.markdown("**📝 Form Aktif Ruang 2 (akan ke-reset pas masuk R3)**")
    st.text_input("Email Member (terkoneksi ke asuveleikha@gmail.com)", key="r2_email_aktif", value=st.session_state.member_email)
    st.text_input("WA", key="r2_wa_aktif", value="085692162564")
    st.selectbox("Paket", ["Employee 200rb/bulan", "Entrepreneur 300rb/bulan"], key="r2_paket_aktif")
    st.text_area("Pesan ke Admin Email & WA", key="r2_pesan_aktif", placeholder="Tulis pesan, akan terkirim ke asuveleikha@gmail.com")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Kembali ke R1", use_container_width=True):
            pindah_ruang('R1')
    with c2:
        if st.button("🌟 Masuk Ruang 3 - MALKHUTKHA", type="primary", use_container_width=True):
            pindah_ruang('R3')

# ================= RUANG 3 =================
def tampilkan_R3():
    st.success("✅ Member di Ruang 3 - Sudah Berlangganan - Member tetap di Ruang 3 saja")
    st.caption("Ruang 2 masih bentuk form semula tanpa sisa cache ketikan")
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("📖 R1 Blank (sampah dibuang)", expanded=False):
            form_blank_template("Ruang 1")
    with col2:
        with st.expander("🏢 R2 Blank (sampah dibuang)", expanded=False):
            form_blank_template("Ruang 2 - Pustaka Layanan")
    
    kartu_visual_memikat(
        "Ruang 3 • TAVO MALKHUTKHA - Two Journey Advance", "🌟",
        "VISUAL: Corporation Megah • Cabang Banyak • Member Saling Access",
        "Tabur Tuai - Corporation Access - Member Saling Access! Employee butuh kerja, Entrepreneur butuh staff - Match di Ruang 3!",
        "Motivasi lebih besar sudah ditempa. Visual corporation memicu visualisasi masa depan. Dari mata turun ke hati, dari hati jadi omzet.",
        "Full Binding + Bimbingan Advance + Motivasi Besar + Corporation Access Full + Omzet Naik",
        "#e0f2f1"
    )
    player_suara_halus("Tabur Tuai, Corporation Access, Member Saling Access. Member di Ruang tiga bisa access ke semua bidang dan skill bahkan corporation. Entrepreneur butuh staff, employee butuh kerja, match di Ruang tiga. Motivasi lebih besar sudah ditempa.", "R3")
    
    st.info(f"Member: {st.session_state.member_email} - Employee - Tenaga Kerja (200rb/bulan) - Sudah magang 3 bulan di garment")
    
    if st.button("⬅️ Kembali ke R2 (R2 tetap blank)", use_container_width=True):
        st.session_state.current_ruang = 'R2'
        st.rerun()

# ================= PAYMENT QRIS / VA / GOPAY / OVO / DANA / PLAYSTORE =================
def tampilkan_payment():
    paket = st.session_state.get('payment_target', 'R3')
    st.markdown(f"## 💳 Pembayaran Langganan - Target: {paket}")
    st.markdown(f"""
    <div style="background:#fff3e0; padding:12px; border-radius:12px; border-left:4px solid #ff9800;">
    <b>PJ Kiban Rekening:</b> BCA 1234567890 a/n Ruang Teduh Yayasan<br>
    <b>Rate:</b> Employee Rp200rb/bulan | Entrepreneur Rp300rb/bulan | MALKHUTKHA Full Advance
    </div>
    """, unsafe_allow_html=True)
    
    tab_va, tab_qris, tab_wallet, tab_play = st.tabs(["🏦 VA Bank", "📱 QRIS", "💚 GoPay/OVO/DANA", "▶️ PlayStore"])
    
    with tab_va:
        st.subheader("Virtual Account - Auto Verifikasi")
        # Simulasi generate VA Midtrans
        order_id = f"RUANGTEDUH-{int(time.time())}"
        va_data = {
            "BCA VA": f"12345 {hashlib.md5(order_id.encode()).hexdigest()[:7].upper()}",
            "BRI VA": f"88810 {st.session_state.member_email[:4]} 085692162564",
            "BNI VA": f"8810 085692162564",
            "Mandiri VA": f"89508 085692162564"
        }
        for bank, va in va_data.items():
            c1, c2 = st.columns([4,1])
            c1.code(f"{bank}: {va} | Order: {order_id} | {paket}", language="text")
            c2.button("Copy", key=f"copy_{bank}")
        st.caption("Gunakan Midtrans / Xendit API: POST /v2/charge dengan bank_transfer. Webhook akan update is_subscribed=True otomatis.")
        st.code(f"""
# Contoh Midtrans (di backend)
import midtransclient
snap = midtransclient.Snap(is_production=False, server_key='SB-Mid-server-xxx')
param = {{
  "transaction_details": {{"order_id": "{order_id}", "gross_amount": 200000}},
  "bank_transfer": {{"bank": "bca", "va_number": ""}},
  "customer_details": {{"email": "{st.session_state.member_email}", "phone": "085692162564"}}
}}
token = snap.create_transaction(param)
""", language="python")
    
    with tab_qris:
        st.subheader("QRIS Universal - Scan Pakai Semua App")
        st.markdown("""
        <div style="background:white; border:2px solid #1a3c34; width:220px; height:220px; margin:auto; border-radius:16px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
            <div style="font-size:60px;">🔳</div>
            <div style="font-size:10px; margin-top:8px;">QRIS DINAMIS</div>
            <div style="font-size:8px;">Midtrans GoPay</div>
            <div style="font-size:9px; margin-top:6px; background:#1a3c34; color:white; padding:2px 8px; border-radius:8px;">Rp200.000</div>
        </div>
        """, unsafe_allow_html=True)
        st.code("QRIS String: 000201010212... (dari Midtrans generate-qr-code-v2)\nBisa di-scan GoPay, OVO, DANA, ShopeePay, BCA Mobile, Livin Mandiri", language="text")
        if st.button("✅ Simulasi Scan QRIS Berhasil"):
            st.session_state.is_subscribed = True
            st.session_state.payment_status = 'lunas_qris'
            st.balloons()
            st.success("Pembayaran QRIS lunas! Masuk Ruang 3...")
            time.sleep(1)
            pindah_ruang('R3')
    
    with tab_wallet:
        st.subheader("E-Wallet App - Masukkan No HP Member")
        phone = st.text_input("No HP GoPay/OVO/DANA", value="085692162564", key="r3_wallet_phone")
        wallet = st.selectbox("Pilih App", ["GoPay", "OVO", "DANA", "LinkAja", "ShopeePay"], key="r3_wallet_app")
        st.caption(f"Akan kirim tagihan ke {wallet} {phone} via Midtrans. OVO butuh push, GoPay bisa QR.")
        if st.button(f"Kirim Tagihan {wallet} - Rp200rb", type="primary", use_container_width=True):
            st.info(f"Mengirim tagihan {wallet} ke {phone}...")
            time.sleep(1)
            st.session_state.is_subscribed = True
            st.session_state.payment_status = f'lunas_{wallet.lower()}'
            st.success(f"Tagihan {wallet} {phone} lunas! (Simulasi)")
            st.balloons()
            pindah_ruang('R3')
    
    with tab_play:
        st.subheader("Google Play Billing")
        st.write("Untuk user yang install dari PlayStore, pakai Google Play Billing Library.")
        st.link_button("🔗 Buka PlayStore Subscription", "https://play.google.com/store/billing")
        st.code("""
# Di Android wrapper
billingClient.queryProductDetails(
  ProductListOf(QueryProductDetailsParams.Product("ruang_teduh_tavo_200k"))
)
""", language="kotlin")
        if st.button("Simulasi PlayStore Lunas"):
            st.session_state.is_subscribed = True
            pindah_ruang('R3')
    
    st.markdown("---")
    if st.button("⬅️ Batal - Kembali"):
        pindah_ruang('R2')

# ================= SIDEBAR - TOMBOL TETAP ADA =================
with st.sidebar:
    st.markdown("### 🌿 Ruang Teduh v2.7 FINAL")
    st.caption(f"Posisi: {st.session_state.current_ruang} | Langganan: {'✅ Aktif' if st.session_state.is_subscribed else '❌ Belum'}")
    st.caption(f"Riwayat: {' > '.join(st.session_state.riwayat) if st.session_state.riwayat else 'Baru'}")
    
    # Progress yang kemarin lo lingkari merah
    if st.session_state.current_ruang == 'R1':
        st.markdown("""
        <div style="background:#1a3c34; color:white; padding:12px; border-radius:12px; text-align:center;">
        📚 2/1000<br>Pustaka Teduh<br><span style="font-size:10px;">Ruang 1 Aktif</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(f"R1 standby 2/1000 • Sekarang di {st.session_state.current_ruang}")
    
    st.markdown("---")
    st.button("📖 Ruang 1", on_click=pindah_ruang, args=('R1',), use_container_width=True)
    st.button("🏢 Ruang 2", on_click=pindah_ruang, args=('R2',), use_container_width=True)
    if st.session_state.is_subscribed:
        st.button("🌟 Ruang 3", on_click=pindah_ruang, args=('R3',), use_container_width=True)
    else:
        st.button("🔒 Ruang 3 (Perlu Langganan)", on_click=pindah_ruang, args=('R3',), use_container_width=True)
    
    st.markdown("---")
    st.checkbox("✅ Simulasi Sudah Bayar (biar bisa masuk R3)", key="is_subscribed")
    st.markdown(f"📧 Admin: {st.session_state.member_email}")
    st.caption("R1 tetap ada bila belum R2 • R2 tetap ada bila belum R3 • Masuk R2=R1 reset • Masuk R3=R2 reset • Member tetap di ruang terbaru")

# ================= MAIN LOGIC ANTI BOROS =================
ph_r1 = st.empty()
ph_r2 = st.empty()
ph_r3 = st.empty()
ph_pay = st.empty()

# CUMA RENDER YANG AKTIF - SISANYA DI-EMPTY BIAR GAK BOROS TOKEN
if st.session_state.current_ruang == 'R1':
    ph_r2.empty(); ph_r3.empty(); ph_pay.empty()
    with ph_r1.container():
        tampilkan_R1()
elif st.session_state.current_ruang == 'R2':
    ph_r1.empty(); ph_r3.empty(); ph_pay.empty()
    with ph_r2.container():
        tampilkan_R2()
elif st.session_state.current_ruang == 'R3':
    ph_r1.empty(); ph_r2.empty(); ph_pay.empty()
    with ph_r3.container():
        tampilkan_R3()
elif 'PAYMENT' in st.session_state.current_ruang:
    ph_r1.empty(); ph_r2.empty(); ph_r3.empty()
    with ph_pay.container():
        tampilkan_payment()
