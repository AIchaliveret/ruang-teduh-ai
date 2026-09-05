import streamlit as st
import pandas as pd
from datetime import datetime
import qrcode, io, hashlib, uuid, time

st.set_page_config(page_title="Ruang Teduh - Gampang Ganti Nama - QRIS", layout="wide", page_icon="💳")

# ======= EDIT DISINI AJA BRO - GAMPANG GANTI NAMA & HP =======
OWNER_NAME = "aichaliveret"  # ganti nama lu disini
OWNER_HP = "081291904422"    # ganti HP lu disini, contoh "081234567890"
OWNER_HP_MASKED = "0812****22"  # tampilan mask, contoh "0812****90"
OWNER_REF = "AICHALIVERET-OWNER"
# ==============================================================

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
        return s[:4] + "****" + s[-2:] if len(s)>=6 else s[:2]+"****"

def rupiah(n): return f"Rp{n:,.0f}".replace(",", ".")

# SESSION
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = "Guest"
if 'members' not in st.session_state:
    # AUTO generate hash dari OWNER_HP di atas - gak perlu edit manual hash!
    owner_hp_hash = hashlib.sha256(OWNER_HP.encode()).hexdigest()[:16]
    st.session_state.members = [
        {"id":0,"nama":OWNER_NAME,"role":"Entrepreneur","skill":"Owner & System Architect","zona":"Jakarta Selatan","hp_hash":owner_hp_hash,"hp_display":OWNER_HP_MASKED,"vote":11,"downline":12,"status":"Lunas Tahunan","komitmen":11,"rupiah":3465000,"referralCode":OWNER_REF,"referredBy":"-","level":0,"cashbackEarned":90000,"payStatus":"Paid - QRIS","email_hash":"hash","order_id":f"ORD-{OWNER_NAME[:4].upper()}-001","qris_string":f"000201010211...{OWNER_NAME}"},
        {"id":1,"nama":"Pak Budi","role":"Employee","skill":"ERP Operator","zona":"Jakarta Pusat","hp_hash":"hash","hp_display":"0812****","vote":1,"downline":2,"status":"Aktif","komitmen":1,"rupiah":55000,"referralCode":"BUDI-01","referredBy":OWNER_REF,"level":1,"cashbackEarned":11000,"payStatus":"Paid - QRIS","email_hash":"hash","order_id":"ORD-BUDI-002","qris_string":"000201010211...BUDI"},
        {"id":2,"nama":"Pak Bambang","role":"Entrepreneur","skill":"Owner F&B","zona":"Bekasi","hp_hash":"hash","hp_display":"0813****","vote":1,"downline":3,"status":"Aktif","komitmen":1,"rupiah":75000,"referralCode":"BAMBANG-02","referredBy":OWNER_REF,"level":1,"cashbackEarned":15000,"payStatus":"Approved","email_hash":"hash","order_id":"ORD-BAMBANG-003","qris_string":"000201010211...BAMBANG"},
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

query_ref = st.query_params.get("ref", OWNER_REF)
judge_mode = st.query_params.get("judge", "")
auto_pass = st.query_params.get("pass", "")
mode = st.query_params.get("mode", "commercial")
if auto_pass == "KOMITMEN" or judge_mode == "building-indonesia":
    st.session_state.authenticated = True
    st.session_state.role = "Judge"
    mode = "judge"

st.markdown("""
<style>
.hero { background: linear-gradient(135deg,#0F172A 0%,#1E293B 60%,#0F766E 100%); color:white; padding:36px; border-radius:20px; }
.value-card{ background:white; border:1px solid #E5E7EB; border-radius:16px; padding:20px; }
.ncr-card{ border-radius:16px; padding:24px; border:2px solid #E5E7EB; box-shadow:0 4px 20px rgba(0,0,0,0.05); margin-bottom:24px; background:white }
.ncr-putih{ border-left:8px solid #111827 } .ncr-pink{ border-left:8px solid #BE123C; background:#FFF1F2 } .ncr-hijau{ border-left:8px solid #059669; background:#ECFDF5 }
.billboard{ background:#111827; color:#10B981; font-family:monospace; padding:12px; border-radius:8px; overflow:hidden; white-space:nowrap; font-size:13px }
.ticker{ display:inline-block; animation:ticker 40s linear infinite } @keyframes ticker{0%{transform:translateX(10%)}100%{transform:translateX(-100%)}}
.badge{ display:inline-block; background:#0F766E; color:white; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:600; margin-right:6px }
.qris-box{ background:#FFFFFF; border:3px solid #0F766E; border-radius:16px; padding:20px; text-align:center }
.qris-paid{ background:#ECFDF5; border:3px solid #059669; border-radius:16px; padding:20px; text-align:center }
.edit-box{ background:#FEF3C7; border:2px dashed #F59E0B; border-radius:12px; padding:16px; margin-bottom:16px }
</style>
""", unsafe_allow_html=True)

# EDIT BOX - GAMPANG GANTI
st.markdown(f"""
<div class="edit-box">
<b>🔧 CARA GANTI NAMA & HP - EDIT 2 BARIS DI ATAS FILE app.py:</b><br>
Baris 10: OWNER_NAME = "{OWNER_NAME}" → ganti jadi nama lu, contoh "Budi Santoso"<br>
Baris 11: OWNER_HP = "{OWNER_HP}" → ganti jadi HP lu, contoh "081234567890"<br>
Baris 12: OWNER_HP_MASKED = "{OWNER_HP_MASKED}" → ganti mask, contoh "0812****90"<br>
Hash otomatis ke-generate dari OWNER_HP, gak perlu edit hash manual! 
</div>
""", unsafe_allow_html=True)

if mode == "commercial":
    st.markdown(f"""
    <div class="hero">
      <h1>📘 Ruang Teduh - 1x Tulis Tembus 3 Lembar + QRIS Otomatis</h1>
      <p>Owner: <b>{OWNER_NAME}</b> | HP: {OWNER_HP_MASKED} | Bayar <b>QRIS GoPay DANA OVO BCA</b> → Auto Aktif! <b>Rp55k→40k</b> & <b>Rp75k→55k TITIK!</b> | 69k/90k + Gratis</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    c1,c2,c3 = st.columns(3)
    with c1: st.markdown('<div class="value-card"><span class="badge">55k → 40k</span><h3>Employee</h3>Netto 40k TITIK! L1 11k L2 4k - 27% bonus sehat transparan!</div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="value-card"><span class="badge">75k → 55k</span><h3>Entrepreneur</h3>Netto 55k TITIK! L1 15k L2 5k - 26.6% bonus!</div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="value-card"><span class="badge">QRIS AUTO</span><h3>Midtrans/Xendit</h3>QRIS unik + webhook auto Paid. Minggu depan real setelah NIB jadi!</div>', unsafe_allow_html=True)
    st.write("")
else:
    st.markdown(f"## Ruang Teduh V6 QRIS - Owner {OWNER_NAME} - Mode Juri")
    st.caption(f"Mode: {mode} | Role: {st.session_state.role}")

top1, top2, top3 = st.columns([3,1,1])
with top1:
    st.markdown(f"<b>Bursa:</b> {len(st.session_state.members)} member | Owner {OWNER_NAME} | <a href='?mode=judge&judge=building-indonesia&pass=KOMITMEN'>Mode Juri</a> | QRIS Ready", unsafe_allow_html=True)
with top2: st.metric("Bursa", f"{len(st.session_state.members)} vote")
with top3:
    with st.popover("🔑 Login"):
        pwd = st.text_input("Password", type="password")
        if st.button("Login Owner"):
            if pwd in ["aichaliveret2024","aichaliveret",OWNER_HP]:
                st.session_state.authenticated=True; st.session_state.role="Owner"; st.rerun()
        if st.button("Login Member"):
            if pwd in ["KOMITMEN","komitmen"]:
                st.session_state.authenticated=True; st.session_state.role="Member"; st.rerun()

members_names = " | ".join([f"{m['nama'].upper()} [{m['role']}]" for m in st.session_state.members])
st.markdown(f'<div class="billboard"><div class="ticker">💳 Owner {OWNER_NAME} - QRIS READY — {len(st.session_state.members)} ARSIP = {len(st.session_state.members)} VOTE — {members_names} — 55k→40k 75k→55k — NIB minggu depan jadi, sekarang simulasi auto Paid! — </div></div>', unsafe_allow_html=True)
st.write("")

# LEMBAR 1
st.markdown('<div class="ncr-card ncr-putih">', unsafe_allow_html=True)
st.markdown("### LEMBAR 1 - Pendaftaran + QRIS (Simulasi dulu, minggu depan real setelah NIB jadi)")

col_form, col_qris = st.columns([2,1])
with col_form:
    st.markdown("**Alur:** [Form] → [QRIS Unik] → [Scan] → [Webhook Auto Paid] → Tembus 3 Lembar")
    with st.form("form_qris_easy"):
        f1,f2 = st.columns(2)
        with f1:
            nama = st.text_input("Nama Lengkap *")
            email = st.text_input("Email *")
            hp = st.text_input("HP/WA *")
            role = st.selectbox("Kategori *", ["Employee - Rp55.000 (Netto 40k)", "Entrepreneur - Rp75.000 (Netto 55k)"])
        with f2:
            zona = st.selectbox("Zona", ["Jakarta Selatan","Bekasi","Tangerang","Bandung","Surabaya","Lainnya"])
            skill = st.text_input("Skill Utama *", placeholder="ERP Jam 9 / OEE 95%")
            kode_referral = st.text_input("Kode Referral", value=query_ref if query_ref!=OWNER_REF else "")
            metode = st.selectbox("Gateway", [f"Xendit QRIS (Rekomendasi - tunggu NIB {OWNER_NAME})", "Midtrans QRIS", f"Manual GoPay/DANA/OVO {OWNER_HP} (jalan sekarang!)"])
        agree = st.checkbox("Setuju data di-hash & bonus transparan")
        submitted = st.form_submit_button("💳 Generate QRIS & Bayar Otomatis", use_container_width=True, type="primary")
        if submitted:
            if not nama or not email or not hp or not skill or not agree:
                st.error("Lengkapi data + centang")
            else:
                clean_role = "Employee" if "Employee" in role else "Entrepreneur"
                rupiah_val = 55000 if clean_role=="Employee" else 75000
                order_id = f"ORD-{nama.upper()[:4]}-{uuid.uuid4().hex[:6].upper()}-{int(time.time())%10000}"
                qris_payload = f"00020101021126610014ID.CO.QRIS.WWW01109360000000000000002{rupiah_val}5204000053033605802ID5914{OWNER_NAME[:14]}6007Jakarta6105123406207{order_id}6304"
                st.session_state.pending_order = {
                    "nama":nama,"email":email,"hp":hp,"role":clean_role,"zona":zona,"skill":skill,"referral":kode_referral or query_ref,
                    "rupiah":rupiah_val,"metode":metode,"order_id":order_id,"qris_string":qris_payload,
                    "hp_hash":hashlib.sha256(hp.encode()).hexdigest()[:16],"email_hash":hashlib.sha256(email.encode()).hexdigest()[:16]
                }
                st.session_state.payment_status = "PENDING_QRIS"
                st.rerun()

with col_qris:
    st.markdown("#### 💳 QRIS Payment")
    if st.session_state.pending_order and st.session_state.payment_status == "PENDING_QRIS":
        order = st.session_state.pending_order
        st.markdown('<div class="qris-box">', unsafe_allow_html=True)
        st.markdown(f"**Order:** `{order['order_id']}`")
        st.markdown(f"**{order['role']} - {rupiah(order['rupiah'])}**")
        st.image(make_qr(order['qris_string']), caption=f"QRIS {rupiah(order['rupiah'])} - Scan", width=220)
        st.caption("Simulasi QRIS - minggu depan jadi real Xendit setelah NIB beres!")
        c1,c2 = st.columns(2)
        with c1:
            if st.button("✅ Simulasi Webhook Paid", use_container_width=True, type="primary"):
                new_member = {
                    "id":len(st.session_state.members),"nama":order['nama'],"role":order['role'],"skill":order['skill'],"zona":order['zona'],
                    "hp_hash":order['hp_hash'],"hp_display":mask_data(order['hp']),"vote":1,"downline":0,"status":"Aktif - QRIS Paid","komitmen":1,"rupiah":order['rupiah'],
                    "referralCode":f"{order['nama'].upper()[:4]}-{len(st.session_state.members):02d}","referredBy":order['referral'],"level":1,"cashbackEarned":0,"payStatus":"Paid - QRIS Auto","email_hash":order['email_hash'],
                    "order_id":order['order_id'],"qris_string":order['qris_string']
                }
                l1 = 11000 if order['role']=="Employee" else 15000
                l2 = 4000 if order['role']=="Employee" else 5000
                st.session_state.members.append(new_member)
                st.success(f"Paid! Netto {rupiah(order['rupiah']-l1-l2)} TITIK!")
                st.info(f"L1 {rupiah(l1)} ke {order['referral']}, L2 {rupiah(l2)}, Netto {rupiah(order['rupiah']-l1-l2)}")
                st.session_state.pending_order = None
                st.session_state.payment_status = "PAID_DONE"
                st.balloons()
                time.sleep(1)
                st.rerun()
        with c2:
            if st.button("❌ Batal", use_container_width=True):
                st.session_state.pending_order = None
                st.session_state.payment_status = None
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.payment_status == "PAID_DONE":
        st.markdown('<div class="qris-paid"><h3>✅ PAID!</h3>Auto Aktif!</div>', unsafe_allow_html=True)
        if st.button("Buat QRIS Baru"):
            st.session_state.payment_status = None
            st.rerun()
    else:
        st.markdown('<div class="qris-box">', unsafe_allow_html=True)
        st.markdown("**Belum ada QRIS**")
        st.image(make_qr(f"{OWNER_HP} - {OWNER_NAME} - QRIS Ready"), width=180, caption=f"QR Owner {OWNER_NAME}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.info(f"**Sementara pakai Manual dulu:** Transfer ke GoPay/DANA/OVO {OWNER_HP} → WA bukti → Auto Paid (simulasi). Minggu depan NIB jadi, ganti ke Xendit QRIS real!")

    st.write("")
    st.markdown("#### 📊 Bonus Transparan")
    st.markdown("- Emp 55k = L1 11k + L2 4k + Netto 40k\n- Ent 75k = L1 15k + L2 5k + Netto 55k")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="ncr-card ncr-pink">', unsafe_allow_html=True)
st.markdown("### LEMBAR 2 - Bursa + Akuntan")
st.markdown(f"**Founder {OWNER_NAME}:** 55k-(11k+4k)=40k | 75k-(15k+5k)=55k TITIK!")
st.line_chart(pd.DataFrame([
    {"date":"08-26","emp":1,"ent":0,"total":1,"rupiah":315000},
    {"date":"08-27","emp":1,"ent":1,"total":2,"rupiah":630000},
    {"date":"08-29","emp":2,"ent":1,"total":3,"rupiah":945000},
    {"date":"08-31","emp":3,"ent":2,"total":5,"rupiah":1575000},
    {"date":"09-02","emp":4,"ent":3,"total":7,"rupiah":2205000},
    {"date":"09-04","emp":6,"ent":5,"total":11,"rupiah":3465000},
]), x="date", y=["emp","ent","total","rupiah"])
st.dataframe(pd.DataFrame(st.session_state.members)[['nama','role','vote','payStatus','referredBy','hp_display','order_id']], use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="ncr-card ncr-hijau">', unsafe_allow_html=True)
st.markdown("### LEMBAR 3 - 5 Rak System")
st.success(f"Auto Nasehat {datetime.now().strftime('%A')}: SOP | ERP | OEE | KPI | Amsal 16:3")
st.markdown('</div>', unsafe_allow_html=True)

st.caption(f"V6.3 Easy Edit - Owner {OWNER_NAME} HP {OWNER_HP_MASKED} | Edit 2 baris di atas file! | QRIS simulasi dulu, NIB minggu depan jadi real Xendit | Link ?mode=commercial | Judge ?judge=building-indonesia&pass=KOMITMEN")
