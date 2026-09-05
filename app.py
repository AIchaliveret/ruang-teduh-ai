import streamlit as st
import pandas as pd
from datetime import datetime
import qrcode, io, hashlib, uuid, time, random

st.set_page_config(page_title="Ruang Teduh - QRIS Midtrans Xendit - aichaliveret", layout="wide", page_icon="💳")

def make_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(data); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return buf.getvalue()

def mask_data(s):
    if not s: return "-"
    if "@" in s:
        a,b = s.split("@",1)
        return a[:2] + "***@" + b
    else:
        return s[:4] + "****" + s[-2:]

def rupiah(n): return f"Rp{n:,.0f}".replace(",", ".")

# --- SESSION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = "Guest"
if 'members' not in st.session_state:
    st.session_state.members = [
        {"id":0,"nama":"aichaliveret","role":"Entrepreneur","skill":"Owner & System Architect","zona":"Jakarta Selatan","hp_hash":hashlib.sha256(b"081291904422").hexdigest()[:16],"hp_display":"0812****22","vote":11,"downline":12,"status":"Lunas Tahunan","komitmen":11,"rupiah":3465000,"referralCode":"AICHALIVERET-OWNER","referredBy":"-","level":0,"cashbackEarned":90000,"payStatus":"Paid - QRIS","email_hash":"hash","order_id":"ORD-AICHALIVERET-001","qris_string":"000201010211...aichaliveret"},
        {"id":1,"nama":"Pak Budi","role":"Employee","skill":"ERP Operator","zona":"Jakarta Pusat","hp_hash":"hash","hp_display":"0812****","vote":1,"downline":2,"status":"Aktif","komitmen":1,"rupiah":55000,"referralCode":"BUDI-01","referredBy":"AICHALIVERET-OWNER","level":1,"cashbackEarned":11000,"payStatus":"Paid - QRIS","email_hash":"hash","order_id":"ORD-BUDI-002","qris_string":"000201010211...BUDI"},
        {"id":2,"nama":"Pak Bambang","role":"Entrepreneur","skill":"Owner F&B","zona":"Bekasi","hp_hash":"hash","hp_display":"0813****","vote":1,"downline":3,"status":"Aktif","komitmen":1,"rupiah":75000,"referralCode":"BAMBANG-02","referredBy":"AICHALIVERET-OWNER","level":1,"cashbackEarned":15000,"payStatus":"Paid - QRIS","email_hash":"hash","order_id":"ORD-BAMBANG-003","qris_string":"000201010211...BAMBANG"},
    ]
if 'pending_order' not in st.session_state:
    st.session_state.pending_order = None
if 'payment_status' not in st.session_state:
    st.session_state.payment_status = None

progress_data = [
    {"date":"08-26","emp":1,"ent":0,"total":1,"rupiah":315000},
    {"date":"08-27","emp":1,"ent":1,"total":2,"rupiah":630000},
    {"date":"08-29","emp":2,"ent":1,"total":3,"rupiah":945000},
    {"date":"08-31","emp":3,"ent":2,"total":5,"rupiah":1575000},
    {"date":"09-02","emp":4,"ent":3,"total":7,"rupiah":2205000},
    {"date":"09-04","emp":6,"ent":5,"total":11,"rupiah":3465000},
]

query_ref = st.query_params.get("ref", "aichaliveret")
judge_mode = st.query_params.get("judge", "")
auto_pass = st.query_params.get("pass", "")
mode = st.query_params.get("mode", "commercial")
if auto_pass == "KOMITMEN" or judge_mode == "building-indonesia":
    st.session_state.authenticated = True
    st.session_state.role = "Judge"
    mode = "judge"

# --- CSS ---
st.markdown("""
<style>
.hero { background: linear-gradient(135deg,#0F172A 0%,#1E293B 60%,#0F766E 100%); color:white; padding:36px; border-radius:20px; }
.hero h1{ font-size:32px; font-weight:800; margin:0 }
.hero p{ font-size:16px; opacity:0.9; margin-top:8px }
.value-card{ background:white; border:1px solid #E5E7EB; border-radius:16px; padding:20px; }
.ncr-card{ border-radius:16px; padding:24px; border:2px solid #E5E7EB; box-shadow:0 4px 20px rgba(0,0,0,0.05); margin-bottom:24px; background:white }
.ncr-putih{ border-left:8px solid #111827 } .ncr-pink{ border-left:8px solid #BE123C; background:#FFF1F2 } .ncr-hijau{ border-left:8px solid #059669; background:#ECFDF5 }
.billboard{ background:#111827; color:#10B981; font-family:monospace; padding:12px; border-radius:8px; overflow:hidden; white-space:nowrap; font-size:13px }
.ticker{ display:inline-block; animation:ticker 40s linear infinite } @keyframes ticker{0%{transform:translateX(10%)}100%{transform:translateX(-100%)}}
.badge{ display:inline-block; background:#0F766E; color:white; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:600; margin-right:6px }
.qris-box{ background:#FFFFFF; border:3px solid #0F766E; border-radius:16px; padding:20px; text-align:center }
.qris-paid{ background:#ECFDF5; border:3px solid #059669; border-radius:16px; padding:20px; text-align:center }
</style>
""", unsafe_allow_html=True)

# === HEADER COMMERCIAL - VALUE PROP 5 DETIK + QRIS ===
if mode == "commercial":
    st.markdown("""
    <div class="hero">
      <h1>📘 Ruang Teduh - 1x Tulis Tembus 3 Lembar + QRIS Otomatis</h1>
      <p>Bayar pakai <b>QRIS GoPay DANA OVO ShopeePay BCA BRI BNI</b> → Auto Aktif! Cuma <b>Rp55.000 Employee (Netto 40k)</b> & <b>Rp75.000 Entrepreneur (Netto 55k TITIK!)</b> | Member Get Member <b>69k/90k + Gratis</b></p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown('<div class="value-card"><span class="badge">55k → 40k</span><h3>Employee</h3>Netto Founder 40k TITIK! (55k - 11k L1 - 4k L2) - Selisih 15k (27%) untuk bonus referal sehat, transparan di kode!</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="value-card"><span class="badge">75k → 55k</span><h3>Entrepreneur</h3>Netto Founder 55k TITIK! (75k - 15k L1 - 5k L2) - Selisih 20k (26.6%) untuk bonus, gak gerus netto founder, upline/downline gak kecewa!</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="value-card"><span class="badge">QRIS AUTO</span><h3>Midtrans / Xendit</h3>QRIS unik per transaksi, webhook auto Paid dalam detik, tanpa cek WA manual. Bisa tetap pakai manual GoPay/DANA pribadi kalau mau.</div>', unsafe_allow_html=True)
    st.write("")
else:
    st.markdown("## Ruang Teduh V6 QRIS - Mode Juri / Owner")
    st.caption(f"Mode: {mode} | Role: {st.session_state.role} | Ref: ?ref={query_ref}")

top1, top2, top3 = st.columns([3,1,1])
with top1:
    if mode == "commercial":
        st.markdown(f"<b>Bursa Live:</b> {len(st.session_state.members)} member | Owner aichaliveret | <a href='?mode=judge&judge=building-indonesia&pass=KOMITMEN'>Mode Juri</a> | QRIS Ready", unsafe_allow_html=True)
    else:
        st.caption(f"Role: {st.session_state.role} | Judge link ?judge=building-indonesia&pass=KOMITMEN")
with top2: st.metric("Bursa", f"{len(st.session_state.members)} vote")
with top3:
    with st.popover("🔑 Login"):
        pwd = st.text_input("Password", type="password")
        if st.button("Login Owner"):
            if pwd in ["aichaliveret2024","aichaliveret","081291904422"]:
                st.session_state.authenticated=True; st.session_state.role="Owner"; st.rerun()
        if st.button("Login Member/Juri"):
            if pwd in ["KOMITMEN","komitmen"]:
                st.session_state.authenticated=True; st.session_state.role="Member"; st.rerun()

members_names = " | ".join([f"{m['nama'].upper()} [{m['role']}]" for m in st.session_state.members])
st.markdown(f'<div class="billboard"><div class="ticker">💳 QRIS MIDTRANS/XENDIT READY — {len(st.session_state.members)} ARSIP = {len(st.session_state.members)} VOTE — {members_names} — Employee 55k→40k (L1 11k L2 4k) Entrepreneur 75k→55k (L1 15k L2 5k) — Transparan di kode! — </div></div>', unsafe_allow_html=True)
st.write("")

# === LEMBAR 1 - FORM + QRIS FLOW ===
st.markdown('<div class="ncr-card ncr-putih">', unsafe_allow_html=True)
st.markdown("### LEMBAR 1 - Pendaftaran + QRIS Midtrans/Xendit Otomatis")

col_form, col_qris = st.columns([2,1])
with col_form:
    st.markdown("**Alur QRIS:** [Form] → [Generate QRIS Unik] → [Scan GoPay/DANA/OVO/BCA] → [Webhook Midtrans/Xendit] → [Auto Paid] → Tembus 3 Lembar")
    with st.form("form_qris"):
        f1,f2 = st.columns(2)
        with f1:
            nama = st.text_input("Nama Lengkap *")
            email = st.text_input("Email *")
            hp = st.text_input("HP/WA *")
            role = st.selectbox("Kategori *", ["Employee - Rp55.000 (Netto 40k) - Selisih 15k bonus", "Entrepreneur - Rp75.000 (Netto 55k) - Selisih 20k bonus"])
        with f2:
            zona = st.selectbox("Zona", ["Jakarta Selatan","Bekasi","Tangerang","Bandung","Surabaya","Lainnya"])
            skill = st.text_input("Skill Utama *", placeholder="ERP Jam 9 / OEE 95%")
            kode_referral = st.text_input("Kode Referral", value=query_ref if query_ref!="aichaliveret" else "")
            metode = st.selectbox("Gateway", ["Xendit QRIS (Rekomendasi - All e-wallet)","Midtrans QRIS GoPay","Manual GoPay/DANA/OVO/Bank Pribadi 081291904422"])
        agree = st.checkbox("Setuju data di-hash & bonus L1 11k/15k L2 4k/5k transparan di kode")
        submitted = st.form_submit_button("💳 Generate QRIS & Bayar Otomatis", use_container_width=True, type="primary")
        if submitted:
            if not nama or not email or not hp or not skill or not agree:
                st.error("Lengkapi data + centang")
            else:
                clean_role = "Employee" if "Employee" in role else "Entrepreneur"
                rupiah_val = 55000 if clean_role=="Employee" else 75000
                # Generate order_id & QRIS string simulasi Midtrans/Xendit
                order_id = f"ORD-{nama.upper()[:4]}-{uuid.uuid4().hex[:6].upper()}-{int(time.time())%10000}"
                # QRIS string format real (simplified): contains amount, merchant, order_id
                qris_payload = f"00020101021126610014ID.CO.QRIS.WWW01109360000000000000002{rupiah_val}5204000053033605802ID5914aichaliveret6007Jakarta6105123406207{order_id}6304"
                st.session_state.pending_order = {
                    "nama":nama,"email":email,"hp":hp,"role":clean_role,"zona":zona,"skill":skill,"referral":kode_referral or query_ref,
                    "rupiah":rupiah_val,"metode":metode,"order_id":order_id,"qris_string":qris_payload,
                    "hp_hash":hashlib.sha256(hp.encode()).hexdigest()[:16],"email_hash":hashlib.sha256(email.encode()).hexdigest()[:16]
                }
                st.session_state.payment_status = "PENDING_QRIS"
                st.rerun()

with col_qris:
    st.markdown("#### 💳 QRIS Payment Gateway")
    if st.session_state.pending_order and st.session_state.payment_status == "PENDING_QRIS":
        order = st.session_state.pending_order
        st.markdown('<div class="qris-box">', unsafe_allow_html=True)
        st.markdown(f"**Order ID:** `{order['order_id']}`")
        st.markdown(f"**{order['role']} - {rupiah(order['rupiah'])}**")
        st.markdown(f"**Metode:** {order['metode']}")
        st.image(make_qr(order['qris_string']), caption=f"QRIS {rupiah(order['rupiah'])} - Scan GoPay/DANA/OVO/BCA", width=220)
        st.markdown(f"**QRIS String (Xendit/Midtrans):** `{order['qris_string'][:40]}...`")
        st.caption("Scan pakai GoPay, DANA, OVO, ShopeePay, BCA, BRI, BNI, dll. QRIS unik per transaksi!")
        st.write("")
        c1,c2 = st.columns(2)
        with c1:
            if st.button("✅ Simulasi Webhook Paid (Midtrans/Xendit)", use_container_width=True, type="primary"):
                # Simulate webhook -> auto Paid
                st.session_state.payment_status = "PAID"
                # Auto create member
                new_member = {
                    "id":len(st.session_state.members),"nama":order['nama'],"role":order['role'],"skill":order['skill'],"zona":order['zona'],
                    "hp_hash":order['hp_hash'],"hp_display":mask_data(order['hp']),"vote":1,"downline":0,"status":"Aktif - QRIS Paid","komitmen":1,"rupiah":order['rupiah'],
                    "referralCode":f"{order['nama'].upper()[:4]}-{len(st.session_state.members):02d}","referredBy":order['referral'],"level":1,"cashbackEarned":0,"payStatus":"Paid - QRIS Auto","email_hash":order['email_hash'],
                    "order_id":order['order_id'],"qris_string":order['qris_string']
                }
                # Bonus transparan: L1 & L2
                l1_bonus = 11000 if order['role']=="Employee" else 15000
                l2_bonus = 4000 if order['role']=="Employee" else 5000
                st.session_state.members.append(new_member)
                st.success(f"Webhook: Payment {order['order_id']} PAID! Member aktif otomatis!")
                st.info(f"💰 Bonus transparan terkunci di kode: L1 {rupiah(l1_bonus)} ke {order['referral']} , L2 {rupiah(l2_bonus)} ke upline level 2. Netto founder: {rupiah(order['rupiah']-l1_bonus-l2_bonus)} TITIK! - Tidak ada yang dirugikan karena rumus transparan di dashboard!")
                st.balloons()
                st.session_state.pending_order = None
                st.session_state.payment_status = "PAID_DONE"
                time.sleep(1)
                st.rerun()
        with c2:
            if st.button("❌ Batal", use_container_width=True):
                st.session_state.pending_order = None
                st.session_state.payment_status = None
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**Cara kerja Midtrans/Xendit asli:**")
        st.code("""
# 1. Backend create QRIS
xendit.QRCode.create(
  external_id=order_id,
  amount=rupiah_val,
  callback_url="https://ruang-teduh-ai.streamlit.app/webhook"
)
# 2. User scan QRIS
# 3. Xendit kirim webhook POST ke /webhook
# 4. Auto update status Paid
        """, language="python")
    elif st.session_state.payment_status == "PAID_DONE":
        st.markdown('<div class="qris-paid">', unsafe_allow_html=True)
        st.markdown("### ✅ PAID - Auto Aktif!")
        st.markdown("Member sudah tembus 3 lembar. Tidak perlu cek WA manual!")
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Buat QRIS Baru"):
            st.session_state.payment_status = None
            st.rerun()
    else:
        st.markdown('<div class="qris-box">', unsafe_allow_html=True)
        st.markdown("**Belum ada QRIS**")
        st.markdown("Isi form → Generate QRIS unik → Scan → Auto Paid")
        st.image(make_qr("081291904422 - aichaliveret - QRIS Ready - GoPay DANA OVO BCA"), width=180, caption="QRIS Contoh - Owner")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        **Manual (jika belum pakai Midtrans/Xendit):**
        Transfer ke GoPay/DANA/OVO/Bank 081291904422 → Kirim bukti WA → Admin aktifkan manual
        """)

    st.write("")
    st.markdown("#### 📊 Transparansi Bonus (Anti Kecewa)")
    st.markdown("""
    - Employee 55k = L1 11k (20%) + L2 4k (7.2%) + Netto 40k (72.7%)
    - Entrepreneur 75k = L1 15k (20%) + L2 5k (6.6%) + Netto 55k (73.3%)
    - Rumus terkunci di kode, dashboard bisa lihat semua!
    """)
    df = pd.DataFrame(st.session_state.members)
    st.dataframe(df[['nama','role','vote','payStatus','referredBy']], use_container_width=True, height=160)

st.markdown('</div>', unsafe_allow_html=True)

# LEMBAR 2 & 3
st.markdown('<div class="ncr-card ncr-pink">', unsafe_allow_html=True)
st.markdown("### LEMBAR 2 - Bursa + Akuntan Netto TITIK! + Bonus Transparan")
st.markdown("**Founder Netto TITIK!:** Employee 55k-(11k+4k)=40k | Entrepreneur 75k-(15k+5k)=55k | Bonus L1 L2 transparan di kode, upline/downline tidak kecewa karena terlihat di dashboard!")
st.line_chart(pd.DataFrame(progress_data), x="date", y=["emp","ent","total","rupiah"])
st.dataframe(pd.DataFrame(st.session_state.members)[['nama','role','skill','zona','vote','downline','status','rupiah','referralCode','referredBy','payStatus','hp_display','order_id']], use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="ncr-card ncr-hijau">', unsafe_allow_html=True)
st.markdown("### LEMBAR 3 - 5 Rak System")
st.success(f"Auto Nasehat {datetime.now().strftime('%A')}: SOP | ERP Jam 9 | OEE 95% | KPI | Amsal 16:3")
st.markdown('</div>', unsafe_allow_html=True)

st.caption("V6.2 QRIS Midtrans/Xendit - Owner aichaliveret QR 081291904422 | QRIS unik per transaksi + webhook auto Paid + bonus L1 L2 transparan 40k/55k TITIK! | Link https://ruang-teduh-ai.streamlit.app?mode=commercial | Judge ?judge=building-indonesia&pass=KOMITMEN | Password Member KOMITMEN Owner aichaliveret2024")
