import streamlit as st
import pandas as pd
from datetime import datetime
import qrcode, io, hashlib, uuid, time, requests

st.set_page_config(page_title="Ruang Teduh V6.5 Voice - AssemblyAI - aichaliveret", layout="wide", page_icon="🎙️")

OWNER_NAME = "aichaliveret"
OWNER_HP = "081291904422"
OWNER_HP_MASKED = "0812****22"
OWNER_REF = "AICHALIVERET-OWNER"

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
        headers_upload = {"authorization": api_key}
        r_upload = requests.post("https://api.assemblyai.com/v2/upload", headers=headers_upload, data=audio_bytes, timeout=30)
        if r_upload.status_code != 200:
            return f"Upload failed {r_upload.status_code}: {r_upload.text[:200]}"
        upload_url = r_upload.json().get("upload_url")
        if not upload_url:
            return f"No upload_url: {r_upload.text[:200]}"
        headers_trans = {"authorization": api_key, "content-type": "application/json"}
        data = {"audio_url": upload_url, "language_code": "id"}
        r_trans = requests.post("https://api.assemblyai.com/v2/transcript", json=data, headers=headers_trans, timeout=30)
        trans_id = r_trans.json().get("id")
        if not trans_id:
            return f"Transcribe failed: {r_trans.text[:200]}"
        for _ in range(20):
            r_poll = requests.get(f"https://api.assemblyai.com/v2/transcript/{trans_id}", headers=headers_trans, timeout=15)
            j = r_poll.json()
            status = j.get("status")
            if status == "completed":
                return j.get("text","")
            elif status == "error":
                return f"Error: {j.get('error')}"
            time.sleep(1.5)
        return "Timeout polling AssemblyAI"
    except Exception as e:
        return f"Exception: {str(e)[:300]}"

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
    if "komisi" in tl or "bonus" in tl or "l1" in tl:
        total_l1 = sum([11000 if m['role']=="Employee" else 15000 for m in members[1:]])
        return f"Total komisi L1 kamu {rupiah(total_l1)} dari {len(members)-1} member. L1 Employee 11 ribu, Entrepreneur 15 ribu. Netto founder 40 ribu dan 55 ribu TITIK!"
    elif "bursa" in tl or "member" in tl:
        return f"Bursa live {len(members)} member, total Rp3.465.000."
    elif "netto" in tl or "founder" in tl:
        return "Founder netto TITIK! Employee 55k-(11k+4k)=40k. Entrepreneur 75k-(15k+5k)=55k TITIK!"
    elif "qris" in tl or "bayar" in tl:
        return "QRIS versi demo, alur teknis ready AssemblyAI voice. Real Xendit minggu depan setelah NIB + NPWP jadi!"
    else:
        return f"Kamu bilang: '{text}'. Tanya: berapa komisi L1? bursa berapa? netto founder?"

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = "Guest"
    st.session_state.show_dev = False
    st.session_state.voice_text = ""
if 'members' not in st.session_state:
    owner_hash = hashlib.sha256(OWNER_HP.encode()).hexdigest()[:16]
    st.session_state.members = [
        {"id":0,"nama":OWNER_NAME,"role":"Entrepreneur","skill":"Owner & Voice Architect","zona":"Jakarta Selatan","hp_hash":owner_hash,"hp_display":OWNER_HP_MASKED,"vote":11,"downline":12,"status":"Lunas Tahunan","komitmen":11,"rupiah":3465000,"referralCode":OWNER_REF,"referredBy":"-","level":0,"cashbackEarned":90000,"payStatus":"Paid - Voice Ready","email_hash":"hash","order_id":f"ORD-{OWNER_NAME[:4].upper()}-001","qris_string":f"000201010211...{OWNER_NAME}"},
        {"id":1,"nama":"Pak Budi","role":"Employee","skill":"ERP Operator","zona":"Jakarta Pusat","hp_hash":"hash","hp_display":"0812****","vote":1,"downline":2,"status":"Aktif","komitmen":1,"rupiah":55000,"referralCode":"BUDI-01","referredBy":OWNER_REF,"level":1,"cashbackEarned":11000,"payStatus":"Paid - Voice Ready","email_hash":"hash","order_id":"ORD-BUDI-002","qris_string":"...BUDI"},
        {"id":2,"nama":"Pak Bambang","role":"Entrepreneur","skill":"Owner F&B","zona":"Bekasi","hp_hash":"hash","hp_display":"0813****","vote":1,"downline":3,"status":"Aktif","komitmen":1,"rupiah":75000,"referralCode":"BAMBANG-02","referredBy":OWNER_REF,"level":1,"cashbackEarned":15000,"payStatus":"Paid - Voice Ready","email_hash":"hash","order_id":"ORD-BAMBANG-003","qris_string":"...BAMBANG"},
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
.hero { background: linear-gradient(135deg,#0F172A 0%,#1E293B 60%,#7C3AED 100%); color:white; padding:32px; border-radius:20px; }
.value-card{ background:white; border:1px solid #E5E7EB; border-radius:16px; padding:16px; height:100% }
.ncr-card{ border-radius:16px; padding:20px; border:2px solid #E5E7EB; box-shadow:0 4px 20px rgba(0,0,0,0.05); margin-bottom:20px; background:white }
.ncr-putih{ border-left:8px solid #111827 } .ncr-pink{ border-left:8px solid #BE123C; background:#FFF1F2 } .ncr-hijau{ border-left:8px solid #059669; background:#ECFDF5 } .ncr-voice{ border-left:8px solid #7C3AED; background:#F5F3FF }
.billboard{ background:#111827; color:#10B981; font-family:monospace; padding:10px; border-radius:8px; overflow:hidden; white-space:nowrap; font-size:12px }
.ticker{ display:inline-block; animation:ticker 40s linear infinite } @keyframes ticker{0%{transform:translateX(10%)}100%{transform:translateX(-100%)}}
.badge{ display:inline-block; background:#0F766E; color:white; padding:4px 10px; border-radius:999px; font-size:11px; font-weight:600; margin-right:6px }
.badge-voice{ display:inline-block; background:#7C3AED; color:white; padding:4px 10px; border-radius:999px; font-size:11px; font-weight:800; margin-right:6px; animation:pulse 2s infinite }
.badge-demo{ display:inline-block; background:#F59E0B; color:black; padding:4px 10px; border-radius:999px; font-size:11px; font-weight:800; margin-right:6px }
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.7}}
.qris-box{ background:#FFFFFF; border:3px solid #0F766E; border-radius:16px; padding:18px; text-align:center }
.edit-box{ background:#FEF3C7; border:2px dashed #F59E0B; border-radius:12px; padding:12px; margin-bottom:12px }
.voice-box{ background:#EDE9FE; border:2px solid #7C3AED; border-radius:16px; padding:14px; margin-bottom:12px }
</style>
""", unsafe_allow_html=True)

top1, top2 = st.columns([4,1])
with top1:
    if st.session_state.role in ["Judge","Owner"] or st.session_state.show_dev:
        st.markdown(f"""<div class="edit-box"><b>🎙️ AssemblyAI Voice Agent Hackathon:</b> OWNER={OWNER_NAME} | Voice Ready | Secrets: ASSEMBLYAI_API_KEY | <a href="?mode=commercial">Hide Dev</a></div>""", unsafe_allow_html=True)
    else:
        st.caption(f"Owner {OWNER_NAME} | Voice Agent Ready | [Demo Voice + Demo QRIS] | <a href='?mode=commercial&dev=1'>Show Dev</a> | <a href='?mode=judge&judge=assemblyai&pass=KOMITMEN&dev=1'>Juri AssemblyAI</a>", unsafe_allow_html=True)
with top2:
    with st.popover("🔑 Login"):
        pwd = st.text_input("Password", type="password")
        if st.button("Login Owner"):
            if pwd in ["aichaliveret2024","aichaliveret",OWNER_HP]:
                st.session_state.authenticated=True; st.session_state.role="Owner"; st.session_state.show_dev=True; st.rerun()
        if st.button("Login Juri"):
            if pwd in ["KOMITMEN","komitmen","assemblyai"]:
                st.session_state.authenticated=True; st.session_state.role="Judge"; st.session_state.show_dev=True; st.rerun()

if mode == "commercial":
    st.markdown(f"""<div class="hero"><h1>🎙️ Ruang Teduh V6.5 Voice Agent + 3 Lembar + QRIS</h1><p><span class='badge-voice'>AssemblyAI $10k</span> Owner: <b>{OWNER_NAME}</b> | Daftar pakai suara! Tanya komisi pakai suara! <b>Rp55k→40k & Rp75k→55k TITIK!</b> | <span class='badge-demo'>DEMO VOICE + QRIS</span></p></div>""", unsafe_allow_html=True)
    st.write("")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown('<div class="value-card"><span class="badge-voice">VOICE REGIST</span><h3>Daftar Pakai Suara</h3>Bilang "Daftar Entrepreneur nama Budi" → AssemblyAI → auto isi!</div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="value-card"><span class="badge">55k → 40k</span><h3>Employee</h3>Netto 40k TITIK!</div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="value-card"><span class="badge">75k → 55k</span><h3>Entrepreneur</h3>Netto 55k TITIK!</div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="value-card"><span class="badge-voice">VOICE BOT</span><h3>Tanya Komisi</h3>"Berapa komisi L1 gua?" → Bot jawab!</div>', unsafe_allow_html=True)
    st.write("")
else:
    st.markdown(f"## 🎙️ Ruang Teduh V6.5 Voice - AssemblyAI - Owner {OWNER_NAME} - Mode Juri")
    st.success("🎙️ AssemblyAI Voice Agent - Voice Registration + Voice Bot Ready!")

members_names = " | ".join([f"{m['nama'].upper()} [{m['role']}]" for m in st.session_state.members])
st.markdown(f'<div class="billboard"><div class="ticker">🎙️ AssemblyAI VOICE READY — Owner {OWNER_NAME} — {len(st.session_state.members)} ARSIP — {members_names} — 55k→40k 75k→55k — Daftar pakai suara! — $10k Prize! — </div></div>', unsafe_allow_html=True)
st.write("")

st.markdown('<div class="ncr-card ncr-voice">', unsafe_allow_html=True)
st.markdown("### 🎙️ Voice Agent - AssemblyAI Integration - WAJIB HACKATHON $10k")
api_key_from_secrets = st.secrets.get("ASSEMBLYAI_API_KEY", "") if hasattr(st, 'secrets') else ""
assembly_key = api_key_from_secrets
if not assembly_key:
    st.warning("⚠️ Masukkan API Key di Streamlit Secrets: ASSEMBLYAI_API_KEY untuk real transcribe. Demo mode jalan tanpa key.")
    assembly_key = "demo_mode"
else:
    st.success(f"✅ API Key aktif dari Secrets: {assembly_key[:8]}...{assembly_key[-4:]}")

col_v1, col_v2 = st.columns(2)
with col_v1:
    st.markdown("#### 🎤 Voice Registration")
    st.code('"Daftar kategori Entrepreneur nama Budi Santoso skill ERP Jam 9"', language="text")
    audio_reg = st.audio_input("🎙️ Rekam suara pendaftaran", key="audio_reg")
    if audio_reg:
        if assembly_key != "demo_mode":
            with st.spinner("🎙️ Transcribing via AssemblyAI..."):
                text = transcribe_assemblyai(audio_reg.getvalue(), assembly_key)
                st.session_state.voice_text = text
                st.success(f"✅ Transcribed: {text}")
                st.json(parse_voice(text))
        else:
            demo_text = "Daftar kategori Entrepreneur nama Budi Santoso skill ERP Jam 9"
            st.session_state.voice_text = demo_text
            st.success(f"✅ Demo Transcribed: {demo_text}")
            st.json(parse_voice(demo_text))
    if st.session_state.voice_text:
        parsed = parse_voice(st.session_state.voice_text)
        with st.form("form_voice_auto"):
            v_nama = st.text_input("Nama (dari suara)", value=parsed.get('nama') or "")
            v_role = st.selectbox("Kategori (dari suara)", ["Employee - Rp55.000", "Entrepreneur - Rp75.000"], index=1 if parsed.get('role')=="Entrepreneur" else 0)
            v_skill = st.text_input("Skill (dari suara)", value=parsed.get('skill') or "")
            v_zona = st.selectbox("Zona", ["Jakarta Selatan","Bekasi","Tangerang","Bandung","Surabaya","Lainnya"])
            v_email = st.text_input("Email *")
            v_hp = st.text_input("HP/WA *")
            v_ref = st.text_input("Referral", value=query_ref)
            if st.form_submit_button("✅ Daftar via Voice + QRIS Demo", type="primary"):
                if v_nama and v_email and v_hp:
                    clean_role = "Entrepreneur" if "Entrepreneur" in v_role else "Employee"
                    rupiah_val = 75000 if clean_role=="Entrepreneur" else 55000
                    new_m = {"id":len(st.session_state.members),"nama":v_nama,"role":clean_role,"skill":v_skill or "Voice Registered","zona":v_zona,"hp_hash":hashlib.sha256(v_hp.encode()).hexdigest()[:16],"hp_display":mask_data(v_hp),"vote":1,"downline":0,"status":"Aktif - Voice Registered","komitmen":1,"rupiah":rupiah_val,"referralCode":f"{v_nama.upper()[:4]}-{len(st.session_state.members):02d}","referredBy":v_ref,"level":1,"cashbackEarned":0,"payStatus":"Paid - Voice + QRIS Demo","email_hash":hashlib.sha256(v_email.encode()).hexdigest()[:16],"order_id":f"ORD-VOICE-{uuid.uuid4().hex[:4].upper()}","qris_string":f"Voice {v_nama}"}
                    st.session_state.members.append(new_m)
                    st.success(f"Voice registration berhasil! {v_nama} via AssemblyAI!")
                    st.balloons()

with col_v2:
    st.markdown("#### 🤖 Voice Bot Keuangan")
    st.code('"Berapa total komisi L1 gua hari ini?"', language="text")
    audio_q = st.audio_input("🎙️ Tanya via suara", key="audio_q")
    text_q = st.text_input("Atau ketik pertanyaan:", placeholder="Berapa komisi L1 gua?", key="text_q")
    query_text = ""
    if audio_q:
        if assembly_key != "demo_mode":
            with st.spinner("🎙️ Transcribing query..."):
                query_text = transcribe_assemblyai(audio_q.getvalue(), assembly_key)
                st.success(f"Query: {query_text}")
        else:
            query_text = "Berapa total komisi L1 gua hari ini"
            st.warning(f"Demo query: {query_text}")
    if text_q:
        query_text = text_q
    if query_text:
        ans = answer_voice_q(query_text, st.session_state.members)
        st.markdown(f'<div class="voice-box"><b>Q:</b> {query_text}<br><b>A Voice Bot:</b> {ans}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="ncr-card ncr-putih">', unsafe_allow_html=True)
st.markdown(f"### LEMBAR 1 - Manual + Voice + QRIS <span class='badge-demo'>DEMO</span>")
col_form, col_qris = st.columns([2,1])
with col_form:
    with st.form("form_qris_voice"):
        f1,f2 = st.columns(2)
        with f1:
            nama = st.text_input("Nama Lengkap *", key="m_nama")
            email = st.text_input("Email *", key="m_email")
            hp = st.text_input("HP/WA *", key="m_hp")
            role = st.selectbox("Kategori *", ["Employee - Rp55.000 (Netto 40k)", "Entrepreneur - Rp75.000 (Netto 55k)"], key="m_role")
        with f2:
            zona = st.selectbox("Zona", ["Jakarta Selatan","Bekasi","Tangerang","Bandung","Surabaya","Lainnya"], key="m_zona")
            skill = st.text_input("Skill Utama *", placeholder="ERP Jam 9", key="m_skill")
            kode_referral = st.text_input("Kode Referral", value=query_ref if query_ref!=OWNER_REF else "", key="m_ref")
            metode = st.selectbox("Gateway", [f"Manual GoPay/DANA/OVO {OWNER_HP} (Demo jalan!)", f"Xendit QRIS Demo (Real minggu depan)", "Midtrans QRIS Demo"], key="m_metode")
        agree = st.checkbox("Setuju data hash & bonus transparan", key="m_agree")
        submitted = st.form_submit_button("💳 Generate QRIS Demo", use_container_width=True, type="primary")
        if submitted:
            if not nama or not email or not hp or not skill or not agree:
                st.error("Lengkapi data")
            else:
                clean_role = "Employee" if "Employee" in role else "Entrepreneur"
                rupiah_val = 55000 if clean_role=="Employee" else 75000
                order_id = f"ORD-{nama.upper()[:4]}-{uuid.uuid4().hex[:6].upper()}-{int(time.time())%10000}"
                qris_payload = f"000201010211...{rupiah_val}...{OWNER_NAME}"
                st.session_state.pending_order = {"nama":nama,"email":email,"hp":hp,"role":clean_role,"zona":zona,"skill":skill,"referral":kode_referral or query_ref,"rupiah":rupiah_val,"metode":metode,"order_id":order_id,"qris_string":qris_payload,"hp_hash":hashlib.sha256(hp.encode()).hexdigest()[:16],"email_hash":hashlib.sha256(email.encode()).hexdigest()[:16]}
                st.session_state.payment_status = "PENDING_QRIS"
                st.rerun()

with col_qris:
    st.markdown("#### 💳 QRIS <span class='badge-demo'>DEMO</span>")
    if st.session_state.pending_order and st.session_state.payment_status == "PENDING_QRIS":
        order = st.session_state.pending_order
        st.markdown('<div class="qris-box">', unsafe_allow_html=True)
        st.markdown(f"Order: `{order['order_id']}` - {rupiah(order['rupiah'])}")
        st.image(make_qr(order['qris_string']), caption=f"QRIS Demo {rupiah(order['rupiah'])}", width=200)
        if st.button("✅ Simulasi Paid Demo", use_container_width=True, type="primary"):
            new_member = {"id":len(st.session_state.members),"nama":order['nama'],"role":order['role'],"skill":order['skill'],"zona":order['zona'],"hp_hash":order['hp_hash'],"hp_display":mask_data(order['hp']),"vote":1,"downline":0,"status":"Aktif - Voice+QRIS Demo","komitmen":1,"rupiah":order['rupiah'],"referralCode":f"{order['nama'].upper()[:4]}-{len(st.session_state.members):02d}","referredBy":order['referral'],"level":1,"cashbackEarned":0,"payStatus":"Paid - Voice Demo","email_hash":order['email_hash'],"order_id":order['order_id'],"qris_string":order['qris_string']}
            st.session_state.members.append(new_member)
            st.success(f"Paid Demo! Netto {rupiah(order['rupiah']-(11000 if order['role']=='Employee' else 15000)-(4000 if order['role']=='Employee' else 5000))} TITIK!")
            st.session_state.pending_order = None
            st.session_state.payment_status = "PAID_DONE"
            st.balloons()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.payment_status == "PAID_DONE":
        st.markdown('<div class="qris-box"><h3>✅ PAID DEMO!</h3></div>', unsafe_allow_html=True)
        if st.button("Buat QRIS Baru"):
            st.session_state.payment_status = None
            st.rerun()
    else:
        st.markdown('<div class="qris-box"><b>Belum ada QRIS</b></div>', unsafe_allow_html=True)
        st.image(make_qr(f"{OWNER_HP} - {OWNER_NAME} - Voice Ready"), width=160, caption=f"QR {OWNER_NAME}")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="ncr-card ncr-pink">', unsafe_allow_html=True)
st.markdown(f"### LEMBAR 2 - Bursa + Akuntan Netto TITIK! + Voice")
st.line_chart(pd.DataFrame([{"date":"08-26","emp":1,"ent":0,"total":1,"rupiah":315000},{"date":"08-27","emp":1,"ent":1,"total":2,"rupiah":630000},{"date":"08-29","emp":2,"ent":1,"total":3,"rupiah":945000},{"date":"08-31","emp":3,"ent":2,"total":5,"rupiah":1575000},{"date":"09-02","emp":4,"ent":3,"total":7,"rupiah":2205000},{"date":"09-04","emp":6,"ent":5,"total":11,"rupiah":3465000},]), x="date", y=["emp","ent","total","rupiah"])
st.dataframe(pd.DataFrame(st.session_state.members)[['nama','role','vote','payStatus','referredBy','hp_display','order_id']], use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="ncr-card ncr-hijau">', unsafe_allow_html=True)
st.markdown("### LEMBAR 3 - 5 Rak System + Voice")
st.success(f"Auto Nasehat {datetime.now().strftime('%A')}: SOP | ERP | OEE | KPI | Amsal 16:3")
st.markdown('</div>', unsafe_allow_html=True)
st.caption(f"V6.5 Voice Agent AssemblyAI - Owner {OWNER_NAME} - Voice Registration + Voice Bot - Clean for GitHub - Secrets ASSEMBLYAI_API_KEY - Link ?mode=judge&judge=assemblyai&pass=KOMITMEN&dev=1 - $10k Hackathon lablab.ai")
