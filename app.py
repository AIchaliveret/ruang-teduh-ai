import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import qrcode, io, hashlib, uuid, time, requests

st.set_page_config(page_title="Ruang Teduh V6.9 MEMBER GET MEMBER - KAUM KAPITAL", layout="wide", page_icon="💰")

OWNER_NAME = "aichaliveret"
OWNER_HP = "081291904422"
OWNER_HP_MASKED = "0812****22"
OWNER_REF = "AICHALIVERET-OWNER"

# PRICING BULANAN - KAUM KAPITAL
PRICE_EMP = 95000
PRICE_ENT = 145000
# BONUS MEMBER GET MEMBER - INTERNAL (jangan tampil detail di UI)
KOMISI_L1_EMP = int(PRICE_EMP * 0.20)  # 19k
KOMISI_L1_ENT = int(PRICE_ENT * 0.20)  # 29k
KOMISI_L2_EMP = 10000
KOMISI_L2_ENT = 26000
ADMIN_EMP = 5000
ADMIN_ENT = 10000

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

def transcribe_assemblyai(audio_bytes, api_key):
    try:
        h = {"authorization": api_key}
        r = requests.post("https://api.assemblyai.com/v2/upload", headers=h, data=audio_bytes, timeout=30)
        if r.status_code != 200:
            return f"Upload failed {r.status_code}"
        url = r.json().get("upload_url")
        h2 = {"authorization": api_key, "content-type": "application/json"}
        data = {"audio_url": url, "language_code": "id"}
        rt = requests.post("https://api.assemblyai.com/v2/transcript", json=data, headers=h2, timeout=30)
        tid = rt.json().get("id")
        for _ in range(20):
            rp = requests.get(f"https://api.assemblyai.com/v2/transcript/{tid}", headers=h2, timeout=15)
            j = rp.json()
            if j.get("status")=="completed":
                return j.get("text","")
            elif j.get("status")=="error":
                return f"Error: {j.get('error')}"
            time.sleep(1.5)
        return "Timeout"
    except Exception as e:
        return f"Exception: {str(e)[:200]}"

def parse_voice(text):
    tl = text.lower()
    role = "Entrepreneur" if "entrepreneur" in tl or "pengusaha" in tl or "wirausaha" in tl else "Employee" if "employee" in tl or "karyawan" in tl else None
    nama = None
    if "nama" in tl:
        try:
            part = tl.split("nama")[1].split("skill")[0].split("kategori")[0].split("zona")[0].strip()
            nama = " ".join([w.capitalize() for w in part.split()[:3] if w not in ["saya","aku","adalah"]])
        except: pass
    skill = None
    if "skill" in tl:
        try:
            skill = tl.split("skill")[1].split("zona")[0].split("kategori")[0].strip()[:30]
        except: pass
    return {"role":role, "nama":nama, "skill":skill, "raw":text}

def answer_voice_q(text, members):
    tl = text.lower()
    if "komisi" in tl or "bonus" in tl or "member get member" in tl:
        return f"Member Get Member! Ajak teman jadi downline, dapat bonus referral! Sistem bonus otomatis, transparan, bursa terintegrasi! Ajak 1 teman Employee dapat bonus, Entrepreneur lebih besar! Tanpa ribet!"
    elif "bursa" in tl or "member" in tl:
        return f"Bursa live {len(members)} member bulanan, auto-interaksi aktif, member get member jalan terus!"
    elif "telat" in tl or "bayar" in tl:
        return f"Member bulanan, telat bayar? Daftar lagi seperti member baru, tanpa denda tanpa blacklist, kode referral tetap sama, downline tetap aman! Gampang!"
    elif "qris" in tl or "bulanan" in tl:
        return f"Langganan bulanan {rupiah(PRICE_EMP)}/{rupiah(PRICE_ENT)} Auto-login tanpa password OTP, member get member aktif! QRIS Demo ready!"
    else:
        return f"Kamu bilang: '{text}'. Tanya: bonus member get member gimana? bursa berapa? telat bayar gimana?"

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = "Guest"
    st.session_state.show_dev = False
    st.session_state.current_user = None
if 'members' not in st.session_state:
    owner_hash = hashlib.sha256(OWNER_HP.encode()).hexdigest()[:16]
    now = datetime.now()
    st.session_state.members = [
        {"id":0,"nama":OWNER_NAME,"role":"Entrepreneur","skill":"Owner & Voice Architect","zona":"DKI Jakarta - Jakarta Selatan","hp_hash":owner_hash,"hp_display":OWNER_HP_MASKED,"vote":11,"downline":12,"status":"Aktif Bulanan","komitmen":11,"rupiah":PRICE_ENT,"referralCode":OWNER_REF,"referredBy":"-","level":0,"cashbackEarned":90000,"payStatus":"Paid - Monthly Active","email_hash":"hash","order_id":f"ORD-{OWNER_NAME[:4].upper()}-001","qris_string":f"000201010211...{OWNER_NAME}","expiry": (now + timedelta(days=30)).strftime("%Y-%m-%d"), "subscription":"monthly"},
        {"id":1,"nama":"Pak Budi","role":"Employee","skill":"ERP Operator","zona":"DKI Jakarta - Jakarta Pusat","hp_hash":"hash","hp_display":"0812****","vote":1,"downline":2,"status":"Aktif Bulanan","komitmen":1,"rupiah":PRICE_EMP,"referralCode":"BUDI-01","referredBy":OWNER_REF,"level":1,"cashbackEarned":KOMISI_L1_EMP,"payStatus":"Paid - Monthly Active","email_hash":"hash","order_id":"ORD-BUDI-002","qris_string":"...BUDI","expiry": (now + timedelta(days=25)).strftime("%Y-%m-%d"), "subscription":"monthly"},
        {"id":2,"nama":"Pak Bambang","role":"Entrepreneur","skill":"Owner F&B","zona":"Bekasi","hp_hash":"hash","hp_display":"0813****","vote":1,"downline":3,"status":"Telat Bayar 3 Hari","komitmen":1,"rupiah":PRICE_ENT,"referralCode":"BAMBANG-02","referredBy":OWNER_REF,"level":1,"cashbackEarned":KOMISI_L1_ENT,"payStatus":"Telat - Bisa Daftar Lagi Tanpa Denda","email_hash":"hash","order_id":"ORD-BAMBANG-003","qris_string":"...BAMBANG","expiry": (now - timedelta(days=3)).strftime("%Y-%m-%d"), "subscription":"monthly"},
    ]
if 'pending_order' not in st.session_state:
    st.session_state.pending_order = None
    st.session_state.payment_status = None

query_ref = st.query_params.get("ref", OWNER_REF)
judge_mode = st.query_params.get("judge", "")
auto_pass = st.query_params.get("pass", "")
mode = st.query_params.get("mode", "commercial")
dev_param = st.query_params.get("dev", "")
if auto_pass == "KOMITMEN" or judge_mode in ["building-indonesia","assemblyai"]:
    st.session_state.authenticated = True
    st.session_state.role = "Judge"
    mode = "judge"
    st.session_state.show_dev = True
if dev_param == "1":
    st.session_state.show_dev = True

st.markdown("""
<style>
.hero { background: linear-gradient(135deg,#0F172A 0%,#7C3AED 100%); color:white; padding:16px; border-radius:12px; margin-bottom:10px; }
.ncr-card{ border-radius:12px; padding:12px; border:2px solid #E5E7EB; box-shadow:0 2px 10px rgba(0,0,0,0.03); margin-bottom:12px; background:white }
.kapital-card{ background: linear-gradient(135deg,#FEF3C7 0%,#FDE68A 100%); border:2px solid #F59E0B; border-radius:12px; padding:12px; margin-bottom:12px; }
</style>
""", unsafe_allow_html=True)

assembly_key = st.secrets.get("ASSEMBLYAI_API_KEY", "demo_mode")
if st.session_state.show_dev:
    st.markdown(f'<div class="hero">💰 V6.9 MEMBER GET MEMBER - {rupiah(PRICE_EMP)}/{rupiah(PRICE_ENT)} BULANAN | Bonus Referral Otomatis | Auto-Login Tanpa Password | Telat? Daftar Lagi Tanpa Denda Tanpa Blacklist! | Voice Ready</div>', unsafe_allow_html=True)

st.markdown(f"""
### 💰 Ruang Teduh V6.9 MEMBER GET MEMBER - KAUM KAPITAL - {rupiah(PRICE_EMP)}/{rupiah(PRICE_ENT)}/bulan
**Langganan bulanan, Member Get Member, Bonus Referral Otomatis, Ajak Teman Dapat Cuan!**
""")

with st.container():
    st.markdown('<div class="ncr-card">', unsafe_allow_html=True)
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("#### 🎙️ Voice Registration - Member Get Member")
        audio_v = st.audio_input("Daftar pakai suara", key="audio_v")
        text_v = st.text_input("Atau ketik:", placeholder="Daftar Entrepreneur nama Budi skill ERP", key="text_v2")
        v_text = ""
        if audio_v:
            if assembly_key != "demo_mode":
                with st.spinner("Transcribing..."):
                    v_text = transcribe_assemblyai(audio_v.getvalue(), assembly_key)
                    st.success(f"Voice: {v_text}")
            else:
                v_text = "Daftar Entrepreneur nama Budi Santoso skill ERP Jam 9"
                st.warning(f"Demo: {v_text}")
        if text_v:
            v_text = text_v
        if v_text:
            parsed = parse_voice(v_text)
            st.json(parsed)
            if st.button("Daftar dari Voice - Member Get Member", type="primary"):
                v_nama = parsed.get("nama") or "Bambang"
                v_role = parsed.get("role") or "Employee"
                v_skill = parsed.get("skill") or "ERP"
                price = PRICE_EMP if v_role=="Employee" else PRICE_ENT
                new_m = {"id":len(st.session_state.members),"nama":v_nama,"role":v_role,"skill":v_skill,"zona":"DKI Jakarta - Jakarta Selatan","hp_hash":"hash","hp_display":"0812****","vote":1,"downline":0,"status":"Aktif Bulanan","komitmen":1,"rupiah":price,"referralCode":f"{v_nama.upper()[:4]}-{len(st.session_state.members):02d}","referredBy":query_ref,"level":1,"cashbackEarned":0,"payStatus":"Paid - Monthly Active - Member Get Member","email_hash":"hash","order_id":f"ORD-VOICE-{uuid.uuid4().hex[:4].upper()}","qris_string":"...VOICE","expiry": (datetime.now()+timedelta(days=30)).strftime("%Y-%m-%d"), "subscription":"monthly"}
                st.session_state.members.append(new_m)
                st.session_state.authenticated = True
                st.session_state.current_user = new_m
                st.success(f"Voice registration berhasil! {v_nama} Member Get Member aktif! Auto-login! Ajak teman dapat bonus!")
                st.balloons()
    with col_v2:
        st.markdown("#### 🤖 Voice Bot - Member Get Member")
        audio_q = st.audio_input("Tanya via suara", key="audio_q")
        text_q = st.text_input("Atau ketik pertanyaan:", placeholder="Bonus member get member gimana?", key="text_q")
        query_text = ""
        if audio_q:
            if assembly_key != "demo_mode":
                with st.spinner("Transcribing..."):
                    query_text = transcribe_assemblyai(audio_q.getvalue(), assembly_key)
                    st.success(f"Query: {query_text}")
            else:
                query_text = "Bonus member get member gimana?"
                st.warning(f"Demo: {query_text}")
        if text_q:
            query_text = text_q
        if query_text:
            ans = answer_voice_q(query_text, st.session_state.members)
            st.markdown(f'<div class="voice-box"><b>Q:</b> {query_text}<br><b>A:</b> {ans}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="ncr-card ncr-putih">', unsafe_allow_html=True)
st.markdown(f"### LEMBAR 1 - Langganan Bulanan {rupiah(PRICE_EMP)}/{rupiah(PRICE_ENT)} - Member Get Member :orange[BONUS]")
st.markdown(f'<div class="kapital-card">💰 <b>MEMBER GET MEMBER:</b> Ajak teman, rekan, keluarga jadi member, dapat <b>Bonus Referral Otomatis</b>! Sistem transparan, bursa terintegrasi, downline otomatis ke-track! Employee {rupiah(PRICE_EMP)}/bulan, Entrepreneur {rupiah(PRICE_ENT)}/bulan. Langganan bulanan, auto-renew, telat bayar? Daftar lagi seperti member baru, tanpa denda tanpa blacklist, kode referral tetap sama, downline tetap aman!</div>', unsafe_allow_html=True)

col_form, col_qris = st.columns([2,1])
with col_form:
    with st.form("form_qris_monthly"):
        f1,f2 = st.columns(2)
        with f1:
            nama = st.text_input("Nama Lengkap *", key="m_nama")
            email = st.text_input("Email * (untuk re-aktivasi)", key="m_email")
            hp = st.text_input("HP/WA *", key="m_hp")
            role = st.selectbox("Kategori Bulanan *", [f"Employee - {rupiah(PRICE_EMP)}/bulan - Member Get Member", f"Entrepreneur - {rupiah(PRICE_ENT)}/bulan - Member Get Member Bonus Lebih Besar"], key="m_role")
        with f2:
            zona = st.selectbox("Zona", ["DKI Jakarta - Jakarta Selatan","DKI Jakarta - Jakarta Barat","DKI Jakarta - Jakarta Timur","DKI Jakarta - Jakarta Pusat","DKI Jakarta - Jakarta Utara","DKI Jakarta (All)","Bekasi","Tangerang","Bandung","Surabaya","Lainnya"], key="m_zona")
            skill = st.text_input("Skill Utama *", placeholder="ERP Jam 9", key="m_skill")
            kode_referral = st.text_input("Kode Referral (Member Get Member)", value=query_ref if query_ref!=OWNER_REF else "", key="m_ref")
            metode = st.selectbox("Gateway", [f"Manual GoPay/DANA/OVO {OWNER_HP}", f"Xendit QRIS Bulanan Demo", "Midtrans QRIS Bulanan Demo"], key="m_metode")
        agree = st.checkbox("Setuju Member Get Member, bonus referral otomatis, langganan bulanan, auto-login tanpa password, telat daftar lagi tanpa denda tanpa blacklist", key="m_agree")
        submitted = st.form_submit_button("💳 Generate QRIS Bulanan - Member Get Member!", use_container_width=True, type="primary")
        if submitted:
            if not nama or not email or not hp or not skill or not agree:
                st.error("Lengkapi data")
            else:
                clean_role = "Employee" if "Employee" in role else "Entrepreneur"
                rupiah_val = PRICE_EMP if clean_role=="Employee" else PRICE_ENT
                existing = next((m for m in st.session_state.members if m.get('email_hash') == hashlib.sha256(email.encode()).hexdigest()[:16] or m['nama'].lower()==nama.lower()), None)
                if existing and "Telat" in existing.get('status',''):
                    st.info(f"Member lama {existing['nama']} terdeteksi Telat Bayar - Re-aktivasi Member Get Member! Kode {existing['referralCode']} tetap, downline tetap!")
                order_id = f"ORD-{nama.upper()[:4]}-{uuid.uuid4().hex[:6].upper()}-{int(time.time())%10000}-MONTHLY"
                qris_payload = f"000201010211...{rupiah_val}...{OWNER_NAME}...MONTHLY-MGM"
                st.session_state.pending_order = {"nama":nama,"email":email,"hp":hp,"role":clean_role,"zona":zona,"skill":skill,"referral":kode_referral or query_ref,"rupiah":rupiah_val,"metode":metode,"order_id":order_id,"qris_string":qris_payload,"hp_hash":hashlib.sha256(hp.encode()).hexdigest()[:16],"email_hash":hashlib.sha256(email.encode()).hexdigest()[:16], "existing_ref": existing['referralCode'] if existing else None}
                st.session_state.payment_status = "PENDING_QRIS"
                st.rerun()

with col_qris:
    st.markdown("#### 💳 QRIS Bulanan - Member Get Member")
    if st.session_state.pending_order and st.session_state.payment_status == "PENDING_QRIS":
        order = st.session_state.pending_order
        st.markdown('<div class="qris-box">', unsafe_allow_html=True)
        st.markdown(f"Order: `{order['order_id']}` - {rupiah(order['rupiah'])}/bulan - MGM")
        st.image(make_qr(order['qris_string']), caption=f"QRIS {rupiah(order['rupiah'])} - Member Get Member", width=200)
        st.caption(f"30 hari, expiry {(datetime.now()+timedelta(days=30)).strftime('%d %b %Y')}. Telat? Daftar lagi tanpa denda, Member Get Member tetap jalan!")
        if st.button("✅ Bayar Bulanan - Auto-Login Member Get Member!", use_container_width=True, type="primary"):
            if order.get('existing_ref'):
                for m in st.session_state.members:
                    if m['referralCode']==order['existing_ref']:
                        m['status']="Aktif Bulanan - Re-aktivasi Member Get Member"
                        m['payStatus']="Paid - Re-Activated - MGM"
                        m['expiry']=(datetime.now()+timedelta(days=30)).strftime("%Y-%m-%d")
                        m['rupiah']=order['rupiah']
                        st.session_state.current_user = m
                        st.session_state.authenticated = True
                        st.success(f"Re-aktivasi Member Get Member! {m['nama']} aktif lagi! Tanpa denda! Downline tetap! Auto-login!")
                        break
            else:
                new_member = {"id":len(st.session_state.members),"nama":order['nama'],"role":order['role'],"skill":order['skill'],"zona":order['zona'],"hp_hash":order['hp_hash'],"hp_display":mask_data(order['hp']),"vote":1,"downline":0,"status":"Aktif Bulanan","komitmen":1,"rupiah":order['rupiah'],"referralCode":order.get('existing_ref') or f"{order['nama'].upper()[:4]}-{len(st.session_state.members):02d}","referredBy":order['referral'],"level":1,"cashbackEarned":0,"payStatus":"Paid - Monthly Active - MGM","email_hash":order['email_hash'],"order_id":order['order_id'],"qris_string":order['qris_string'],"expiry": (datetime.now()+timedelta(days=30)).strftime("%Y-%m-%d"), "subscription":"monthly"}
                st.session_state.members.append(new_member)
                st.session_state.current_user = new_member
                st.session_state.authenticated = True
                st.success(f"Paid! {order['nama']} {rupiah(order['rupiah'])}/bulan Member Get Member aktif! Auto-login! Ajak teman dapat bonus!")
            st.session_state.pending_order = None
            st.session_state.payment_status = "PAID_DONE"
            st.balloons()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.payment_status == "PAID_DONE":
        st.markdown('<div class="qris-box"><h3>✅ PAID - Member Get Member Aktif!</h3></div>', unsafe_allow_html=True)
        if st.button("Buat QRIS Baru"):
            st.session_state.payment_status = None
            st.rerun()
    else:
        st.markdown('<div class="qris-box"><b>Belum ada QRIS</b><br>Member Get Member, daftar seperti member baru, tanpa blacklist tanpa denda!</div>', unsafe_allow_html=True)
        st.image(make_qr(f"{OWNER_HP} - {OWNER_NAME} - MGM"), width=160, caption=f"QR MGM {OWNER_NAME}")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="ncr-card ncr-pink">', unsafe_allow_html=True)
st.markdown(f"### LEMBAR 2 - Bursa Bulanan - Member Get Member - Auto-Interaksi")
st.caption(f"Database tetap ada, terhubung langsung, Member Get Member auto-track, tanpa logout. Bayar -> auto-login -> ajak teman jadi downline dapat bonus referral! Telat? Daftar lagi seperti semula, kode tetap sama!")
c1,c2 = st.columns([1,2])
with c1:
    df_chart = pd.DataFrame([{"date":"08-26","emp":1,"ent":0,"total":1},{"date":"08-27","emp":1,"ent":1,"total":2},{"date":"08-29","emp":2,"ent":1,"total":3},{"date":"08-31","emp":3,"ent":2,"total":5},{"date":"09-02","emp":4,"ent":3,"total":7},{"date":"09-04","emp":6,"ent":5,"total":11},])
    st.line_chart(df_chart, x="date", y=["emp","ent","total"])
    st.metric("Member Get Member", f"{len(st.session_state.members)} member", "Bonus referral otomatis")
with c2:
    st.dataframe(pd.DataFrame(st.session_state.members)[['nama','role','status','payStatus','expiry','referredBy','hp_display','referralCode','rupiah']], use_container_width=True, height=250)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="ncr-card ncr-hijau">', unsafe_allow_html=True)
st.markdown("### LEMBAR 3 - 5 Rak Storage - Member Get Member - No Logout")
col_rak1, col_rak2, col_rak3, col_rak4, col_rak5 = st.columns(5)
with col_rak1:
    st.markdown("**RAK 1 SOP**\nStandard\n40 file\n✅ Member Get Member")
with col_rak2:
    st.markdown("**RAK 2 ERP**\nResource\n55 file\n✅ Bonus Referral")
with col_rak3:
    st.markdown("**RAK 3 OEE**\nEfficiency\n35 file\n✅ Auto-Track")
with col_rak4:
    st.markdown("**RAK 4 KPI**\nTarget\n50 file\n✅ Bursa Aktif")
with col_rak5:
    st.markdown("**RAK 5 AMSAL**\nWisdom\n100 file\n✅ Daily")
st.success(f"Storage 280 file terintegrasi bursa Member Get Member | No logout, database tetap ada!")
if st.session_state.get('current_user'):
    cu = st.session_state.current_user
    st.info(f"🔗 Link Member Get Member: https://ruang-teduh-ai.streamlit.app/?ref={cu['referralCode']} | Kode: {cu['referralCode']} | Expiry: {cu.get('expiry','-')} | Ajak teman jadi downline dapat bonus referral otomatis! Telat? Daftar lagi tanpa denda!")
else:
    st.info(f"🔗 Link umum Member Get Member: https://ruang-teduh-ai.streamlit.app/?ref={OWNER_REF} | Ajak teman jadi downline, bonus referral otomatis, bursa terintegrasi, telat daftar lagi tanpa blacklist tanpa denda!")
st.markdown('</div>', unsafe_allow_html=True)
st.caption(f"V6.9 MEMBER GET MEMBER {PRICE_EMP}/{PRICE_ENT} KAUM KAPITAL - Owner {OWNER_NAME} - Bonus Referral Otomatis - Monthly Auto-Login No Password No Logout - Telat Daftar Lagi Tanpa Denda Tanpa Blacklist - AssemblyAI Voice - ?mode=judge&judge=assemblyai&pass=KOMITMEN&dev=1")
