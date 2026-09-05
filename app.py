import streamlit as st
import pandas as pd
from datetime import datetime
import qrcode
import io
import random

st.set_page_config(page_title="Ruang Teduh V6 - aichaliveret - Public Judge Friendly", layout="wide", page_icon="📄")

def make_qr(data):
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def rupiah(n):
    return f"Rp{n:,.0f}".replace(",", ".")

# --- AUTH STATE TAPI GAK BLOK FULL ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = "Guest"
if 'members' not in st.session_state:
    st.session_state.members = [
        {"id":0,"nama":"aichaliveret","role":"Entrepreneur","skill":"Owner & System Architect","zona":"Jakarta Selatan","hp":"081291904422","vote":11,"downline":12,"status":"Lunas Tahunan","komitmen":11,"rupiah":3465000,"referralCode":"AICHALIVERET-OWNER","referredBy":"-","level":0,"cashbackEarned":90000,"payStatus":"Paid","email":"aichaliveret@gmail.com"},
        {"id":1,"nama":"Pak Budi","role":"Employee","skill":"ERP Operator","zona":"Jakarta Pusat","hp":"0812xxxx","vote":1,"downline":2,"status":"Aktif","komitmen":1,"rupiah":55000,"referralCode":"BUDI-01","referredBy":"AICHALIVERET-OWNER","level":1,"cashbackEarned":11000,"payStatus":"Paid","email":"budi@test.com"},
        {"id":2,"nama":"Pak Bambang","role":"Entrepreneur","skill":"Owner F&B","zona":"Bekasi","hp":"0813xxxx","vote":1,"downline":3,"status":"Aktif","komitmen":1,"rupiah":75000,"referralCode":"BAMBANG-02","referredBy":"AICHALIVERET-OWNER","level":1,"cashbackEarned":15000,"payStatus":"Approved","email":"bambang@test.com"},
    ]

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

# Auto login for judge via link ?judge=building-indonesia&pass=KOMITMEN
if auto_pass == "KOMITMEN" or judge_mode == "building-indonesia":
    st.session_state.authenticated = True
    st.session_state.role = "Judge"

# --- CSS ---
st.markdown("""
<style>
.ncr-card { border-radius: 16px; padding: 24px; border: 2px solid #E5E7EB; box-shadow: 0 4px 20px rgba(0,0,0,0.05); margin-bottom: 24px; }
.ncr-putih { background: #FFFFFF; border-left: 8px solid #111827; }
.ncr-pink { background: #FFF1F2; border-left: 8px solid #BE123C; }
.ncr-hijau { background: #ECFDF5; border-left: 8px solid #059669; }
.billboard { background: #111827; color: #10B981; font-family: monospace; padding: 12px; border-radius: 8px; overflow: hidden; white-space: nowrap; font-size: 13px; }
.ticker { display: inline-block; animation: ticker 40s linear infinite; }
@keyframes ticker { 0% { transform: translateX(10%); } 100% { transform: translateX(-100%); } }
.nb-box { background: #FEF3C7; border: 2px solid #F59E0B; border-radius: 12px; padding: 16px; }
.metric-card { background: white; border-radius: 12px; padding: 16px; border: 1px solid #E5E7EB; text-align: center; }
</style>
""", unsafe_allow_html=True)

# Header - PUBLIC, NO PASSWORD NEEDED
c1, c2, c3 = st.columns([3,1,1])
with c1:
    st.markdown("## Ruang Teduh V6 FINAL - aichaliveret - PUBLIC JUDGE FRIENDLY")
    if st.session_state.role == "Judge":
        st.success("👨‍⚖️ Mode Judge Building Indonesia - Auto login via ?judge=building-indonesia - Full access!")
    elif st.session_state.authenticated:
        st.caption(f"Role: {st.session_state.role} | Ref: ?ref={query_ref} | Protected actions with password")
    else:
        st.caption(f"Public view - Bursa bisa dilihat tanpa password | Daftar butuh password Member KOMITMEN | Owner actions butuh aichaliveret2024 | Ref: ?ref={query_ref}")
with c2:
    st.metric("Total Bursa", f"{len(st.session_state.members)} vote")
with c3:
    with st.popover("🔑 Login"):
        pwd = st.text_input("Password", type="password", placeholder="KOMITMEN / aichaliveret2024")
        if st.button("Login Owner"):
            if pwd in ["aichaliveret2024","aichaliveret","081291904422"]:
                st.session_state.authenticated = True
                st.session_state.role = "Owner"
                st.success("Owner!")
                st.rerun()
        if st.button("Login Member/Judge"):
            if pwd in ["KOMITMEN","komitmen","Tamu","building"]:
                st.session_state.authenticated = True
                st.session_state.role = "Member"
                st.success("Member!")
                st.rerun()
        if st.session_state.authenticated:
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.session_state.role = "Guest"
                st.rerun()

members_names = " | ".join([f"{m['nama'].upper()} [{m['role'].upper()}] {m['vote']}" for m in st.session_state.members])
st.markdown(f'<div class="billboard"><div class="ticker">📢 BURSA LIVE PUBLIC — {len(st.session_state.members)} ARSIP = {len(st.session_state.members)} VOTE — {members_names} — Employee 55k->40k Entrepreneur 75k->55k — Member Get Member 69k/90k — ?ref=aichaliveret — Judge link ?judge=building-indonesia&pass=KOMITMEN — </div></div>', unsafe_allow_html=True)
st.write("")

# LEMBAR 1 - PUBLIC VIEW + PROTECTED ACTION
st.markdown('<div class="ncr-card ncr-putih">', unsafe_allow_html=True)
st.markdown("### LEMBAR 1 PUTIH - ASLI | Public View + Protected Daftar")
st.info("**Untuk Juri Building Indonesia / Emergent:** Link ini bisa dibuka tanpa password untuk lihat Bursa! Untuk coba daftar, pakai password **KOMITMEN**. Untuk owner actions, pakai **aichaliveret2024**. Atau buka link khusus juri: `?judge=building-indonesia&pass=KOMITMEN` auto-login!")

col_form, col_info = st.columns([2,1])
with col_form:
    st.markdown("**[QR GATE] -> [FORM ORG LENGKAP] -> [VALIDASI] -> 3 LEMBAR**")
    # Form - but submit requires password check inside
    with st.form("form_v6_public"):
        f1, f2 = st.columns(2)
        with f1:
            nama = st.text_input("Nama Lengkap *")
            email = st.text_input("Email *")
            hp = st.text_input("HP/WA *")
            role = st.selectbox("Kategori *", ["Employee","Entrepreneur"])
        with f2:
            zona = st.selectbox("Zona", ["Jakarta Selatan","Bekasi","Tangerang","Bandung","Surabaya","Lainnya"])
            skill = st.text_input("Skill Utama *", placeholder="ERP Jam 9 / OEE 95%")
            kode_referral = st.text_input("Kode Referral", value=query_ref if query_ref != "aichaliveret" else "")
            form_pwd = st.text_input("Password Daftar *", type="password", placeholder="KOMITMEN untuk member / judge")
        submitted = st.form_submit_button("✅ Berlangganan & Tembus 3 Lembar - Butuh Password KOMITMEN", use_container_width=True, type="primary")
        if submitted:
            # Check password untuk daftar - ini yang blok JS recokin
            if form_pwd not in ["KOMITMEN","komitmen","Tamu","building","aichaliveret2024","aichaliveret","081291904422"] and st.session_state.role not in ["Owner","Member","Judge"]:
                st.error("⛔ Password daftar salah! Untuk juri, pakai password **KOMITMEN** atau buka link `?judge=building-indonesia&pass=KOMITMEN` - Ini anti JS recokin!")
            elif not nama or not email or not hp or not skill:
                st.error("Wajib: Nama, Email, HP, Skill")
            else:
                new_member = {"id": len(st.session_state.members),"nama":nama,"role":role,"skill":skill,"zona":zona,"hp":hp,"vote":1,"downline":0,"status":"Aktif","komitmen":1,"rupiah":55000 if role=="Employee" else 75000,"referralCode":f"{nama.upper()[:4]}-{len(st.session_state.members):02d}","referredBy":kode_referral or query_ref,"level":1,"cashbackEarned":0,"payStatus":"Pending","email":email}
                st.session_state.members.append(new_member)
                st.success(f"Berhasil! {nama} ({role}) -> 1 arsip = 1 vote")
                st.balloons()

with col_info:
    st.markdown("#### Bursa - Public bisa lihat tanpa password")
    df = pd.DataFrame(st.session_state.members)
    st.dataframe(df[['nama','role','skill','vote','referredBy','payStatus']], use_container_width=True, height=200)
    chart_df = pd.DataFrame([{"nama": m['nama'][:8], "Employee": 1 if m['role']=="Employee" else 0, "Entrepreneur": 1 if m['role']=="Entrepreneur" else 0} for m in st.session_state.members])
    st.bar_chart(chart_df, x="nama", y=["Employee","Entrepreneur"])
    st.markdown('<div class="nb-box">', unsafe_allow_html=True)
    st.markdown("- Employee Rp55.000 = Netto **Rp40.000 TITIK!**")
    st.markdown("- Entrepreneur Rp75.000 = Netto **Rp55.000 TITIK!**")
    st.markdown("**QR 081291904422 aichaliveret**")
    st.image(make_qr("081291904422"), width=150)
    st.markdown('</div>', unsafe_allow_html=True)
    # Owner only delete
    if st.session_state.role == "Owner":
        st.markdown("---")
        st.warning("Owner Mode: Bisa hapus member recokin")
        if st.button("🗑️ Hapus Member Terakhir (Anti Recokin)"):
            if len(st.session_state.members) > 1:
                st.session_state.members.pop()
                st.rerun()
    else:
        st.caption("Login Owner aichaliveret2024 untuk hapus member recokin")

st.markdown('</div>', unsafe_allow_html=True)

# LEMBAR 2 & 3 - PUBLIC VIEW
st.markdown('<div class="ncr-card ncr-pink">', unsafe_allow_html=True)
st.markdown("### LEMBAR 2 MERAH - Bursa + Akuntan - Public View")
st.line_chart(pd.DataFrame(progress_data), x="date", y=["emp","ent","total","rupiah"])
st.success("Founder Netto: Employee 55k-(11k+4k)=40k | Entrepreneur 75k-(15k+5k)=55k TITIK!")
st.dataframe(pd.DataFrame(st.session_state.members)[['nama','role','skill','zona','vote','downline','status','rupiah','referralCode','referredBy','level','cashbackEarned','payStatus']], use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="ncr-card ncr-hijau">', unsafe_allow_html=True)
st.markdown("### LEMBAR 3 HIJAU - 5 Rak System - Public View")
st.success(f"Auto Nasehat: {datetime.now().strftime('%A')} - SOP/ERP/OEE/KPI/Alkitab Amsal 16:3")
st.markdown('</div>', unsafe_allow_html=True)

st.caption("V6 Public Judge Friendly - Bursa bisa dilihat tanpa password, daftar butuh KOMITMEN, owner actions butuh aichaliveret2024 - Anti JS recokin tapi gak repot juri - Link juri ?judge=building-indonesia&pass=KOMITMEN")
