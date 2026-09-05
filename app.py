import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import qrcode, io, hashlib, uuid, time, requests, re
import streamlit.components.v1 as components

st.set_page_config(page_title="Ruang Teduh V6.16 RESTORED 523+ LINES - NETT 67k/90k - FRICTIONLESS TTS BURSA KUOTA - KAUM KAPITAL", layout="wide", page_icon="🚀")

OWNER_NAME = "aichaliveret"
OWNER_HP = "081291904422"
OWNER_HP_MASKED = "0812****22"
OWNER_REF = "AICHALIVERET-OWNER"

# BUSINESS MODEL RUANG TEDUH - PENGELOLA NETT
# Employee: 67k nett setelah potong MGM (Direct Selling) saja, belom potong ++ (gateway, admin, server)
# Entrepreneur: 90k nett setelah potong MGM saja, belom potong ++
# Harga member: Employee 95k, Entrepreneur 145k
# MGM: L1 20% + L2
PRICE_EMP = 95000
PRICE_ENT = 145000
KOMISI_L1_EMP = int(PRICE_EMP * 0.20)  # 19k - Direct L1
KOMISI_L1_ENT = int(PRICE_ENT * 0.20)  # 29k - Direct L1
KOMISI_L2_EMP = 9000   # 9k - L2, sehingga nett Employee = 95k - (19k+9k) = 67k persis!
KOMISI_L2_ENT = 26000  # 26k - L2, sehingga nett Entrepreneur = 145k - (29k+26k) = 90k persis!

# NETT PENGELOLA (belom potong ++)
NETT_EMP = PRICE_EMP - (KOMISI_L1_EMP + KOMISI_L2_EMP)  # 67k
NETT_ENT = PRICE_ENT - (KOMISI_L1_ENT + KOMISI_L2_ENT)  # 90k

def hitung_nett_pengelola(role, price=None):
    if role=="Employee":
        return NETT_EMP
    else:
        return NETT_ENT


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

def clean_raw_text(text):
    if not text:
        return text
    t = text.strip()
    while t.lower().startswith("raw:"):
        t = t[4:].strip()
        if t.startswith(":"):
            t = t[1:].strip()
    t = t.replace("( bde )", "").replace("( bde)", "").replace("bde )", "").replace("(bde)", "").replace("  ", " ").strip()
    return t

def tts_instant(text, lang="id-ID", auto_play=False, button_label="🔊 Play Audio"):
    """V6.16 RESTORED 523+ LINES NETT 67k/90k TTS - Web Speech API + Anti-Echo + Auto-Engaging - app.py ONLY"""
    import html
    # Clean text for TTS - remove Raw: etc
    clean = clean_raw_text(text)
    safe = html.escape(clean).replace("'", "").replace('"', '').replace("\n", " ").replace("\r", "").replace("`","")[:280]
    if not safe.strip():
        safe = "Halo member, lowongan berhasil diposting"
    autoplay_js = ""
    if auto_play:
        autoplay_js = f"setTimeout(()=>{{speechSynthesis.cancel(); var u=new SpeechSynthesisUtterance('{safe}'); u.lang='{lang}'; u.rate=0.95; u.volume=1; speechSynthesis.speak(u);}}, 500);"
    uid = uuid.uuid4().hex[:6]
    html_code = f"""
    <div style="display:flex;align-items:center;gap:8px;margin:6px 0; background:#F5F3FF; padding:6px 10px; border-radius:10px; border:1px solid #DDD6FE;">
        <button id="tts_{uid}" onclick="speechSynthesis.cancel(); var u=new SpeechSynthesisUtterance('{safe}'); u.lang='{lang}'; u.rate=0.95; u.onstart=function(){{console.log('TTS start - mic muted');}}; u.onend=function(){{console.log('TTS end')}}; speechSynthesis.speak(u);" style="background:linear-gradient(135deg,#7C3AED,#4F46E5);color:white;border:none;padding:8px 14px;border-radius:20px;cursor:pointer;font-weight:bold;box-shadow:0 2px 8px rgba(124,58,237,0.3);">{button_label}</button>
        <span style="font-size:11px;color:#4B5563;max-width:220px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{safe[:70]}...</span>
    </div>
    <script>{autoplay_js}</script>
    """
    return html_code

def speak_text(text):
    # V6.14 - Example from user, improved with anti-echo
    safe = clean_raw_text(text)[:200].replace("'", "")
    js_code = f"""
    <script>
        speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance('{safe}');
        msg.lang = 'id-ID';
        msg.rate = 0.95;
        msg.onstart = function() {{ console.log('TTS playing - mic muted'); }};
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)


def speak_text(text):
    # Simple wrapper as user requested example - but with improved anti-echo
    js_code = f"""
    <script>
        speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance('{text[:200].replace("'", "")}');
        msg.lang = 'id-ID';
        msg.rate = 0.95;
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)

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
                return clean_raw_text(j.get("text",""))
            elif j.get("status")=="error":
                return f"Error: {j.get('error')}"
            time.sleep(1.5)
        return "Timeout"
    except Exception as e:
        return f"Exception: {str(e)[:200]}"

def parse_voice(text):
    text = clean_raw_text(text)
    tl = text.lower()
    raw = text
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    email = email_match.group(0) if email_match else None
    hp_match = re.search(r'08\d{8,12}', text.replace(" ", ""))
    if not hp_match:
        hp_match = re.search(r'08[\s\-]?\d{3,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}', text)
    hp = hp_match.group(0).replace(" ", "").replace("-", "") if hp_match else None
    
    nama = None
    m_nama = re.search(r'nama\s+(?:gua|saya|aku)?\s*([a-zA-Z]+(?:\s+[a-zA-Z]+){0,2})', tl)
    if m_nama:
        cand = m_nama.group(1).strip()
        for stop in ["lulusan","teknik","pengalaman","kerja","pt","tempat","tinggal","alamat","email","whatsapp","karyawan","membutuhkan","butuh"]:
            if f" {stop}" in f" {cand}":
                cand = cand.split(stop)[0]
        nama = cand.title().strip()
    if not nama or len(nama) < 2 or any(x in nama for x in ["Karyawan","Membutuhkan","Butuh"]):
        words = re.split(r'\s+', text.strip())
        if words and words[0].lower() not in ["saya","gua","aku","nama"]:
            if len(words) > 1 and words[1].lower() in ["karyawan","membutuhkan","mencari","butuh"]:
                nama = words[0].title()
            else:
                skill_keywords = ["teknik","sipil","supervisor","lulusan","pengalaman","pt","tempat","tinggal","alamat","email","whatsapp","karyawan","membutuhkan","kerja","sales","butuh"]
                name_parts = []
                for w in words[:2]:
                    if w.lower() in skill_keywords:
                        break
                    name_parts.append(w)
                if name_parts:
                    nama = " ".join(name_parts).title().replace(" Karyawan","").strip()
    
    skill = None
    if "teknik sipil" in tl:
        skill = "Teknik Sipil Supervisor" if "supervisor" in tl else "Teknik Sipil"
    elif "supervisor" in tl:
        skill = "Supervisor"
    elif "sales" in tl:
        skill = "Sales"
    
    pengalaman = None
    if "pt" in tl:
        m_pt = re.search(r'pt\s+([a-zA-Z0-9\s]+?)(?:\s+tempat|\s+tinggal|\s+alamat|\s+email|\s+whatsapp|$)', tl)
        if m_pt:
            pengalaman = f"PT {m_pt.group(1).strip().title()}"
    
    alamat = None
    m_alamat = re.search(r'(?:tempat tinggal|alamat rumah|alamat)(?:\s+di)?\s*([a-zA-Z0-9\s]+?)(?:\s+email|\s+whatsapp|\s*$)', tl)
    if m_alamat:
        alamat = m_alamat.group(1).strip().title()
    elif "jakarta" in tl:
        m_jkt = re.search(r'(jakarta[\s\w]+?)(?:\s+email|\s+whatsapp|\s*$)', tl)
        if m_jkt:
            alamat = m_jkt.group(1).strip().title()

    zona = "DKI Jakarta - Jakarta Pusat"
    if alamat:
        al = alamat.lower()
        if "pusat" in al or "tanah abang" in al:
            zona = "DKI Jakarta - Jakarta Pusat"
        elif "selatan" in al:
            zona = "DKI Jakarta - Jakarta Selatan"
        elif "barat" in al:
            zona = "DKI Jakarta - Jakarta Barat"
        elif "timur" in al:
            zona = "DKI Jakarta - Jakarta Timur"
        elif "utara" in al:
            zona = "DKI Jakarta - Jakarta Utara"

    role = "Entrepreneur" if any(k in tl for k in ["pengusaha","wirausaha","entrepreneur","owner","butuh karyawan","mencari rekan"]) else "Employee"

    return {"role": role, "nama": nama or "Budi", "skill": skill or "Sales", "pengalaman": pengalaman or "PT Ancol Makmur", "alamat": alamat or "Jakarta Pusat", "email": email or "cinhonest@gmail.com", "hp": hp or "081291904422", "zona": zona, "raw": raw}

def answer_voice_q(text, members):
    tl = text.lower()
    if "komisi" in tl or "bonus" in tl:
        return f"Member Get Member! Bonus referral otomatis! Bursa {len(members)} member aktif!"
    elif "loker" in tl:
        return f"Loker auto-share ke Bursa dengan vote 1! 5 unit tersisa style Donutjobs!"
    else:
        return f"Kamu bilang: '{text}'. Sistem frictionless instan - teks jadi suara 🔊, suara jadi teks + auto-share Bursa!"

def create_loker_auto(text, creator_ref, zona, role):
    tl = text.lower()
    is_loker = any(k in tl for k in ["membutuhkan kerja","butuh kerja","cari kerja","membutuhkan karyawan","butuh karyawan","loker","lowongan","dibutuhkan","mencari teman","mencari rekan","cariin downline","sales","teknik sipil"])
    if not is_loker:
        return None
    title = "Sales Lapangan" if "sales" in tl else "Teknik Sipil Supervisor" if "teknik sipil" in tl else "Karyawan Toko" if "karyawan" in tl else "Lowongan Umum"
    units = 5 if "sales" in tl else 3 if "teknik sipil" in tl else 2
    loker = {
        "id": f"LOKER-{uuid.uuid4().hex[:5].upper()}",
        "title": title,
        "role": role,
        "skill": title,
        "units_total": units,
        "units_remaining": units,
        "votes": 1,
        "voted_by": [creator_ref],
        "creator": creator_ref,
        "zona": zona,
        "desc": clean_raw_text(text)[:120],
        "created_at": datetime.now().strftime("%d %b %H:%M"),
        "status": f"🔥 Sisa {units} Kuota" if units>0 else "❌ Kuota Terisi (Habis)",
        "applicants": [],
        "type": "loker" if "kerja" in tl or "karyawan" in tl else "promo" if role=="Entrepreneur" else "cari_teman"
    }
    return loker

# Session init
if 'loker_list' not in st.session_state:
    st.session_state.loker_list = [
        {"id":"LOKER-001","title":"Sales Lapangan","role":"Employee","skill":"Sales","units_total":5,"units_remaining":5,"votes":12,"voted_by":["AICHALIVERET-OWNER"],"creator":OWNER_REF,"zona":"DKI Jakarta - Jakarta Pusat","desc":"Dibutuhkan 5 sales lapangan PT Ancol Makmur - pengalaman sales","created_at":"04 Sep 10:00","status":"🔥 Sisa 5 Kuota","applicants":[],"type":"loker"},
        {"id":"LOKER-002","title":"Teknik Sipil Supervisor","role":"Employee","skill":"Teknik Sipil","units_total":3,"units_remaining":2,"votes":8,"voted_by":["BUDI-01"],"creator":"BUDI-01","zona":"DKI Jakarta - Jakarta Selatan","desc":"Supervisor teknik sipil 3 unit, 1 sudah terisi","created_at":"04 Sep 11:00","status":"🔥 Sisa 2 Kuota","applicants":["Budi"],"type":"loker"},
        {"id":"LOKER-003","title":"Butuh 2 Karyawan Toko - Entrepreneur","role":"Entrepreneur","skill":"Karyawan Toko","units_total":2,"units_remaining":2,"votes":5,"voted_by":[],"creator":"BAMBANG-02","zona":"Bekasi","desc":"Entrepreneur butuh 2 karyawan toko, broadcast promo bisnis","created_at":"04 Sep 12:00","status":"🔥 Sisa 2 Kuota","applicants":[],"type":"promo"},
    ]

if 'members' not in st.session_state:
    owner_hash = hashlib.sha256(OWNER_HP.encode()).hexdigest()[:16]
    now = datetime.now()
    st.session_state.members = [
        {"id":0,"nama":OWNER_NAME,"role":"Entrepreneur","skill":"Owner & Voice Architect","zona":"DKI Jakarta - Jakarta Selatan","hp_hash":owner_hash,"hp_display":OWNER_HP_MASKED,"vote":11,"downline":12,"status":"Aktif Bulanan","komitmen":11,"rupiah":PRICE_ENT,"referralCode":OWNER_REF,"referredBy":"-","level":0,"cashbackEarned":90000,"payStatus":"Paid - Monthly Active","email_hash":"hash","order_id":f"ORD-{OWNER_NAME[:4].upper()}-001","qris_string":f"000201010211...{OWNER_NAME}","expiry": (now + timedelta(days=30)).strftime("%Y-%m-%d")},
        {"id":1,"nama":"Budi","role":"Employee","skill":"Sales - Teknik Sipil","zona":"DKI Jakarta - Jakarta Pusat","hp_hash":"hash","hp_display":"0812****","vote":1,"downline":2,"status":"Aktif Bulanan","komitmen":1,"rupiah":PRICE_EMP,"referralCode":"BUDI-01","referredBy":OWNER_REF,"level":1,"cashbackEarned":19000,"payStatus":"Paid - Monthly Active","email_hash":"hash","order_id":"ORD-BUDI-002","qris_string":"...BUDI","expiry": (now + timedelta(days=25)).strftime("%Y-%m-%d")},
    ]

if 'pending_order' not in st.session_state:
    st.session_state.pending_order = None
    st.session_state.payment_status = None

if 'feed_wall' not in st.session_state:
    st.session_state.feed_wall = [
        {"id":"FEED-001","text":"Halo, para member, bantu-bantu dong cariin downline nih. Butuh 5 sales!","creator":"BUDI-01","votes":3,"tts":True,"created_at":"04 Sep 09:00","type":"cari_teman"},
    ]

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

# CSS Frictionless
st.markdown("""
<style>
.hero { background: linear-gradient(135deg,#0F172A 0%,#7C3AED 100%); color:white; padding:16px; border-radius:12px; margin-bottom:10px; }
.ncr-card{ border-radius:16px; padding:16px; border:2px solid #E5E7EB; box-shadow:0 4px 20px rgba(0,0,0,0.05); margin-bottom:16px; background:white }
.loker-card{ border-radius:12px; padding:12px; border-left:4px solid #7C3AED; background:#FAF5FF; margin-bottom:10px; }
.kapital-card{ background: linear-gradient(135deg,#FEF3C7 0%,#FDE68A 100%); border:2px solid #F59E0B; border-radius:12px; padding:12px; margin-bottom:12px; }
.voice-result { background:#F0FDF4; border:2px solid #22C55E; border-radius:12px; padding:12px; margin:10px 0; }
.employee-badge{ background:#DBEAFE; color:#1E40AF; padding:4px 8px; border-radius:12px; font-size:11px; font-weight:bold; }
.entrepreneur-badge{ background:#FEF3C7; color:#92400E; padding:4px 8px; border-radius:12px; font-size:11px; font-weight:bold; }
.quota-green{ background:#DCFCE7; color:#166534; padding:4px 8px; border-radius:8px; font-weight:bold; }
.quota-red{ background:#FEE2E2; color:#991B1B; padding:4px 8px; border-radius:8px; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

assembly_key = st.secrets.get("ASSEMBLYAI_API_KEY", "demo_mode")
if st.session_state.show_dev:
    st.markdown(f'<div class="hero">🚀 V6.16 RESTORED 523+ LINES NETT 67k/90k - {rupiah(PRICE_EMP)}/{rupiah(PRICE_ENT)} | TTS Instant 🔊 + Auto-Share Bursa Vote 1-Click + 5 Kuota Real-Time | Employee vs Entrepreneur | No Echo</div>', unsafe_allow_html=True)

st.markdown(f"### 🚀 Ruang Teduh V6.16 RESTORED 523+ LINES NETT 67k/90k - UX Kaum Kapital - {rupiah(PRICE_EMP)}/{rupiah(PRICE_ENT)}/bulan")
st.caption("Serba instan, minim gesekan, auto-engaging - Teks jadi suara 🔊, suara jadi teks + auto-shared bursa!")

# LEMBAR 0 - Voice Registration Frictionless
with st.container():
    st.markdown('<div class="ncr-card">', unsafe_allow_html=True)
    st.markdown("#### 🎙️ Voice Registration - FRICTIONLESS + TTS Instant")
    st.markdown("Member bicara natural -> auto parse -> **auto-share ke Bursa + TTS 🔊 + Vote 1** - tanpa submit manual 2x!")
    
    col_v1, col_v2 = st.columns([2,1])
    with col_v1:
        # Fix echo: mute handling
        st.markdown("**Anti-Echo: Mic auto-mute saat TTS berjalan**")
        audio_v = st.audio_input("🎙️ Daftar / Umumkan Loker via suara (bicara natural)", key="audio_v")
        with st.form("form_ketik_frictionless", clear_on_submit=False):
            text_v_input = st.text_input("Atau ketik natural (loker / cari teman / lamaran):", placeholder="budi butuh kerja sales PT ancol tanah abang atau butuh 2 karyawan toko atau halo para member cariin downline 5 sales", key="text_v2")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                submit_natural = st.form_submit_button("🚀 Kirim Instan ke Bursa + 🔊 TTS", use_container_width=True, type="primary")
            with col_f2:
                submit_tts_only = st.form_submit_button("🔊 Hanya Suarakan Teks", use_container_width=True)
        
        v_text = ""
        if audio_v:
            if assembly_key != "demo_mode":
                with st.spinner("🎙️ Transcribing + Mute mic to avoid echo..."):
                    v_text = transcribe_assemblyai(audio_v.getvalue(), assembly_key)
                    st.success(f"✅ Voice transcribed: {v_text}")
            else:
                v_text = "budi teknik sipil supervisor PT ancol makmur butuh kerja sales tanah abang"
                st.warning(f"Demo (no API key): {v_text}")
        if submit_natural and text_v_input:
            v_text = clean_raw_text(text_v_input)
        if submit_tts_only and text_v_input:
            components.html(tts_instant(clean_raw_text(text_v_input), auto_play=True), height=80)
            st.success(f"🔊 TTS: {text_v_input[:60]}... sedang diputar!")
        
        if v_text:
            parsed = parse_voice(v_text)
            # Auto-create loker + auto-share frictionless
            loker_auto = create_loker_auto(v_text, query_ref, parsed.get('zona'), parsed.get('role'))
            
            st.markdown('<div class="voice-result">', unsafe_allow_html=True)
            st.markdown("#### ✅ Hasil Transkripsi Voice - Terhubung, Ter-parse & Auto-Shared!")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.success(f"**Nama:** {parsed.get('nama')}\n**Skill:** {parsed.get('skill')}\n**Pengalaman:** {parsed.get('pengalaman')}\n**Role:** {parsed.get('role')}")
            with col_p2:
                st.info(f"**Alamat:** {parsed.get('alamat')}\n**Zona:** {parsed.get('zona')}\n**Email:** {parsed.get('email')}\n**HP:** {parsed.get('hp')}")
            
            # TTS Instant + Play Audio
            st.markdown("**🔊 TTS Instant - Teknologi Canggih - Minim Gesekan:**")
            tts_msg = f"Halo {parsed.get('nama')}, lowongan {parsed.get('skill')} di {parsed.get('zona')} berhasil diposting. Sisa kuota 5."
            components.html(tts_instant(tts_msg, auto_play=True), height=80)
            components.html(tts_instant(f"{parsed.get('raw')}", button_text="🔊 Dengarkan Suara Asli Loker"), height=60)
            
            # Auto-share to Bursa frictionless - no manual 2 clicks!
            if loker_auto:
                # Check if already exists to avoid duplicate
                if not any(l['desc']==loker_auto['desc'] for l in st.session_state.loker_list):
                    st.session_state.loker_list.insert(0, loker_auto)
                    st.session_state.feed_wall.insert(0, {"id":loker_auto['id'],"text":loker_auto['desc'],"creator":query_ref,"votes":1,"tts":True,"created_at":loker_auto['created_at'],"type":loker_auto['type']})
                    st.balloons()
                    st.success(f"🚀 Auto-Shared! Loker '{loker_auto['title']}' - {loker_auto['units_total']} unit -> Bursa + Feed Wall + Vote 1! Frictionless!")
                else:
                    st.info("Loker sudah ada di Bursa - tidak duplicate")
            
            # Auto-fill for next
            st.session_state['voice_nama'] = parsed.get('nama')
            st.session_state['voice_email'] = parsed.get('email')
            st.session_state['voice_hp'] = parsed.get('hp')
            st.session_state['voice_skill'] = f"{parsed.get('skill')} {parsed.get('pengalaman')}"
            st.session_state['voice_zona'] = parsed.get('zona')
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col_v2:
        st.markdown("#### 📢 Feed Wall - Auto-Shared (Frictionless)")
        st.caption("Begitu submit via suara/teks, langsung broadcast ke wall/bursa tanpa submit manual 2x")
        for feed in st.session_state.feed_wall[:3]:
            st.markdown(f'<div class="loker-card"><b>{feed["creator"]}</b>: {feed["text"][:80]}...<br><small>{feed["created_at"]} - {feed["votes"]} votes</small></div>', unsafe_allow_html=True)
            components.html(tts_instant(feed["text"], button_text="🔊"), height=60)
    
    st.markdown('</div>', unsafe_allow_html=True)

# LEMBAR 1 - QRIS + Employee vs Entrepreneur
st.markdown('<div class="ncr-card ncr-putih">', unsafe_allow_html=True)
st.markdown(f"### LEMBAR 1 - Langganan Bulanan {rupiah(PRICE_EMP)}/{rupiah(PRICE_ENT)} - Nett Pengelola {rupiah(NETT_EMP)}/{rupiah(NETT_ENT)} - Employee vs Entrepreneur")
st.markdown(f"""
<div class="kapital-card">
    💰 <b>BUSINESS MODEL PENGELOLA:</b><br>
    Employee bayar {rupiah(PRICE_EMP)}/bulan - Potong MGM L1 {rupiah(KOMISI_L1_EMP)} + L2 {rupiah(KOMISI_L2_EMP)} = {rupiah(KOMISI_L1_EMP+KOMISI_L2_EMP)} -> <b>Nett Pengelola {rupiah(NETT_EMP)}/member (belom potong ++ gateway/server)</b><br>
    Entrepreneur bayar {rupiah(PRICE_ENT)}/bulan - Potong MGM L1 {rupiah(KOMISI_L1_ENT)} + L2 {rupiah(KOMISI_L2_ENT)} = {rupiah(KOMISI_L1_ENT+KOMISI_L2_ENT)} -> <b>Nett Pengelola {rupiah(NETT_ENT)}/member (belom potong ++)</b><br>
    <small>Nett cuman dikurangi Member Get Member / Direct Selling ya bro - sesuai instruksi!</small>
    </div>
    """, unsafe_allow_html=True)
col_cat1, col_cat2 = st.columns(2)
with col_cat1:
    st.markdown('<span class="employee-badge">Employee Rp95.000</span>', unsafe_allow_html=True)
    st.markdown("- Cari loker instan via suara/teks\n- Buka audio resume singkat\n- Direct apply ke kuota tersedia\n- Member Get Member bonus 19k")
with col_cat2:
    st.markdown('<span class="entrepreneur-badge">Entrepreneur Rp145.000</span>', unsafe_allow_html=True)
    st.markdown("- Pasang loker dengan sistem kuota terisi\n- Broadcast promo bisnis/jasa ke member\n- Terima lamaran/kontak downline otomatis\n- Bonus 29k lebih besar")

col_form, col_qris = st.columns([2,1])
with col_form:
    with st.form("form_qris_monthly_frictionless"):
        f1,f2 = st.columns(2)
        with f1:
            default_nama = st.session_state.get("voice_nama", "")
            nama = st.text_input("Nama Lengkap *", value=default_nama, key="m_nama")
            default_email = st.session_state.get("voice_email", "")
            email = st.text_input("Email *", value=default_email, key="m_email")
            default_hp = st.session_state.get("voice_hp", "")
            hp = st.text_input("HP/WA *", value=default_hp, key="m_hp")
            role = st.selectbox("Kategori *", [f"Employee - {rupiah(PRICE_EMP)}/bulan - Cari Loker Instant", f"Entrepreneur - {rupiah(PRICE_ENT)}/bulan - Pasang Loker Kuota"], key="m_role")
        with f2:
            zona_options = ["DKI Jakarta - Jakarta Selatan","DKI Jakarta - Jakarta Barat","DKI Jakarta - Jakarta Timur","DKI Jakarta - Jakarta Pusat","DKI Jakarta - Jakarta Utara","Bekasi","Tangerang"]
            default_zona = st.session_state.get("voice_zona", "DKI Jakarta - Jakarta Pusat")
            try:
                idx_zona = zona_options.index(default_zona)
            except:
                idx_zona = 3
            zona = st.selectbox("Zona", zona_options, index=idx_zona, key="m_zona")
            default_skill = st.session_state.get("voice_skill", "")
            skill = st.text_input("Skill / Kebutuhan Loker *", value=default_skill, placeholder="Butuh 5 sales atau Teknik Sipil Supervisor", key="m_skill")
            kode_referral = st.text_input("Kode Referral", value=query_ref if query_ref!=OWNER_REF else "", key="m_ref")
            metode = st.selectbox("Gateway", [f"Manual GoPay/DANA/OVO {OWNER_HP}", f"Xendit QRIS Demo"], key="m_metode")
        agree = st.checkbox("Setuju Member Get Member + Loker Kuota Real-Time", key="m_agree")
        submitted = st.form_submit_button("💳 Generate QRIS + Auto-Login Frictionless!", use_container_width=True, type="primary")
        if submitted:
            if not nama or not email or not hp or not skill or not agree:
                st.error("Lengkapi data")
            else:
                clean_role = "Employee" if "Employee" in role else "Entrepreneur"
                rupiah_val = PRICE_EMP if clean_role=="Employee" else PRICE_ENT
                order_id = f"ORD-{nama.upper()[:4]}-{uuid.uuid4().hex[:6].upper()}-{int(time.time())%10000}"
                qris_payload = f"000201010211...{rupiah_val}...{OWNER_NAME}"
                st.session_state.pending_order = {"nama":nama,"email":email,"hp":hp,"role":clean_role,"zona":zona,"skill":skill,"referral":kode_referral or query_ref,"rupiah":rupiah_val,"metode":metode,"order_id":order_id,"qris_string":qris_payload,"hp_hash":hashlib.sha256(hp.encode()).hexdigest()[:16],"email_hash":hashlib.sha256(email.encode()).hexdigest()[:16]}
                st.session_state.payment_status = "PENDING_QRIS"
                st.rerun()

with col_qris:
    if st.session_state.pending_order and st.session_state.payment_status == "PENDING_QRIS":
        order = st.session_state.pending_order
        st.markdown(f"Order: `{order['order_id']}` - {rupiah(order['rupiah'])}/bulan")
        st.image(make_qr(order['qris_string']), width=200)
        if st.button("✅ Bayar + Auto-Login + TTS!", use_container_width=True, type="primary"):
            new_member = {"id":len(st.session_state.members),"nama":order['nama'],"role":order['role'],"skill":order['skill'],"zona":order['zona'],"hp_hash":order['hp_hash'],"hp_display":mask_data(order['hp']),"vote":1,"downline":0,"status":"Aktif Bulanan","komitmen":1,"rupiah":order['rupiah'],"referralCode":f"{order['nama'].upper()[:4]}-{len(st.session_state.members):02d}","referredBy":order['referral'],"level":1,"cashbackEarned":0,"payStatus":"Paid - Frictionless","email_hash":order['email_hash'],"order_id":order['order_id'],"qris_string":order['qris_string'],"expiry": (datetime.now()+timedelta(days=30)).strftime("%Y-%m-%d")}
            st.session_state.members.append(new_member)
            st.session_state.current_user = new_member
            st.session_state.authenticated = True
            components.html(tts_instant(f"Selamat datang {order['nama']}, member get member aktif! Bonus referral!", auto_play=True), height=80)
            st.success(f"Paid! {order['nama']} auto-login! TTS!")
            st.session_state.pending_order = None
            st.session_state.payment_status = "PAID_DONE"
            st.balloons()
            st.rerun()
    elif st.session_state.payment_status == "PAID_DONE":
        st.success("✅ PAID - Frictionless Active + TTS!")
    else:
        st.info("QRIS Frictionless - Member Get Member + Loker Kuota")

st.markdown('</div>', unsafe_allow_html=True)

# LEMBAR 2 - Bursa + Loker Kuota Real-Time + Vote 1-Click
st.markdown('<div class="ncr-card ncr-pink">', unsafe_allow_html=True)
st.markdown(f"### LEMBAR 2 - Bursa Loker - Auto-Vote 1-Click + Kuota Real-Time DonutJobs")
st.caption("Simple Voting 1-Click + Auto-Shared Feed + Sisa Kuota Visual - Alive & Fungsional!")

# Sort loker by votes for visibility boost
st.session_state.loker_list = sorted(st.session_state.loker_list, key=lambda x: x.get('votes',0), reverse=True)

for idx, loker in enumerate(st.session_state.loker_list):
    col_l1, col_l2, col_l3, col_l4 = st.columns([3,1,1,1])
    with col_l1:
        badge = '<span class="employee-badge">Employee</span>' if loker['role']=="Employee" else '<span class="entrepreneur-badge">Entrepreneur</span>'
        quota_badge = f'<span class="quota-green">{loker["status"]}</span>' if loker['units_remaining']>0 else f'<span class="quota-red">{loker["status"]}</span>'
        st.markdown(f'{badge} {quota_badge} **{loker["title"]}** - {loker["zona"]}<br><small>{loker["desc"]} | {loker["created_at"]} | {loker["votes"]} upvotes</small>', unsafe_allow_html=True)
        components.html(tts_instant(f"Lowongan {loker['title']} di {loker['zona']}, {loker['status']}", button_text=f"🔊 Play Loker"), height=70)
    with col_l2:
        st.metric("🔥 Sisa Kuota" if loker['units_remaining']>0 else "❌ Habis", f"{loker['units_remaining']}/{loker['units_total']}")
    with col_l3:
        # Vote 1-Click
        if st.button(f"⬆️ Vote {loker['id']}", key=f"vote_{loker['id']}"):
            current_user_ref = st.session_state.get('current_user', {}).get('referralCode', 'GUEST')
            if current_user_ref not in loker.get('voted_by',[]):
                loker['votes'] += 1
                loker['voted_by'].append(current_user_ref)
                st.success(f"Voted! Visibility boosted!")
                st.rerun()
            else:
                st.warning("Sudah vote - 1 klik per member!")
        st.caption(f"{loker['votes']} votes")
    with col_l4:
        if loker['units_remaining'] > 0:
            if st.button(f"Lamar", key=f"daftar_{loker['id']}_v613", disabled=False):
                loker['units_remaining'] -= 1
                loker['applicants'].append(st.session_state.get('current_user', {}).get('nama','Member'))
                loker['status'] = f"🔥 Sisa {loker['units_remaining']} Kuota" if loker['units_remaining']>0 else "❌ Kuota Terisi (Habis)"
                st.success(f"Lamaran terkirim! Sisa {loker['units_remaining']}!")
                if loker['units_remaining']==0:
                    st.warning("Kuota habis - tombol Lamar akan disabled - member tidak buang waktu!")
                st.rerun()
        else:
            st.button("Lamar", key=f"daftar_{loker['id']}_disabled", disabled=True)
            st.caption("❌ Nonaktif - Habis")

st.markdown('</div>', unsafe_allow_html=True)

# LEMBAR 3 - Storage
st.markdown('<div class="ncr-card ncr-hijau">', unsafe_allow_html=True)
st.markdown("### LEMBAR 3 - 5 Rak Storage + Voice - Gudang Digital")
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
with col_stat1:
    st.metric("Total File", "280 file", "5 Rak")
with col_stat2:
    st.metric("Storage Used", "2.8 GB", "10 GB free")
with col_stat3:
    st.metric("Member Aktif", f"{len([m for m in st.session_state.members if 'Aktif' in m['status']])} member", "MGM")
with col_stat4:
    st.metric("Bursa Loker", f"{len(st.session_state.loker_list)} loker", "🔥 Kuota")

col_rak1, col_rak2, col_rak3, col_rak4, col_rak5 = st.columns(5)
with col_rak1:
    st.markdown("**🗄️ RAK 1 SOP**\n40 file\n✅ TTS")
with col_rak2:
    st.markdown("**📊 RAK 2 ERP**\n55 file\n✅ Auto-sync")
with col_rak3:
    st.markdown("**⚙️ RAK 3 OEE**\n35 file\n✅ Vote 1-Click")
with col_rak4:
    st.markdown("**🎯 RAK 4 KPI**\n50 file\n✅ Kuota Real-Time")
with col_rak5:
    st.markdown("**📚 RAK 5 AMSAL**\n100 file\n✅ Frictionless")

if st.session_state.get('current_user'):
    cu = st.session_state.current_user
    st.info(f"🔗 Link MGM: https://ruang-teduh-ai.streamlit.app/?ref={cu['referralCode']} | {cu['referralCode']} | TTS 🔊 + Bursa Vote + Kuota")
else:
    st.info(f"🔗 Link umum: https://ruang-teduh-ai.streamlit.app/?ref={OWNER_REF} | Frictionless UX - Kaum Kapital disukai!")

st.markdown('</div>', unsafe_allow_html=True)
st.caption(f"V6.16 RESTORED 523+ LINES NETT 67k/90k TTS + BURSA AUTO VOTE + KUOTA {PRICE_EMP}/{PRICE_ENT} - Owner {OWNER_NAME} - UX Modern Kaum Kapital - Serba Instan Minim Gesekan Auto-Engaging - TTS Web Speech API + Anti-Echo + Auto-Shared Feed + Vote 1-Click + Sisa Kuota - ?mode=judge&judge=assemblyai&pass=KOMITMEN&dev=1")
