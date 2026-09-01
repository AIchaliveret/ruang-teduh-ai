# AIJC - Ruang Teduh v2.2 - FIXED RATE: Employee 200rb, Entrepreneur 300rb - Keterikatan Member
import streamlit as st
from datetime import datetime
import os, csv, re, json, html
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(page_title="Ruang Teduh v2.2 - 200rb & 300rb - Keterikatan", page_icon="🌿", layout="wide")

st.markdown("""
<style>
.badge{background:#E8F3ED;color:#2D5A4A;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:700}
.badge-emp{background:#DBEAFE;color:#1E40AF}
.badge-ent{background:#FEF3C7;color:#92400E}
.metric-card{background:#2D5A4A;color:white;padding:12px 16px;border-radius:12px;text-align:center}
.binding-card{background:linear-gradient(135deg,#2D5A4A 0%,#7FB69B 100%);color:white;padding:20px;border-radius:16px;margin:12px 0}
.full-service{background:#FFFBEB;border:2px solid #F59E0B;padding:16px;border-radius:12px;margin:8px 0}
.sop-table{background:white;border:1px solid #E5E7EB;border-radius:12px;padding:16px;margin:10px 0}
.corp-card{background:linear-gradient(135deg,#1E40AF 0%,#3B82F6 100%);color:white;padding:20px;border-radius:16px;margin:12px 0}
.profit-card{background:linear-gradient(135deg,#059669 0%,#10B981 100%);color:white;padding:20px;border-radius:16px;margin:12px 0}
</style>
""", unsafe_allow_html=True)

CSV_FILE="members_ruang_teduh.csv"

def is_valid_email(e): 
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", e) is not None

def load_members():
    if not os.path.exists(CSV_FILE): return []
    try:
        with open(CSV_FILE,"r",encoding="utf-8") as f: return list(csv.DictReader(f))
    except: return []

def save_member(data):
    members=load_members()
    # 1 member 1 jalur - cek email sudah ada, tidak boleh ganti jalur
    existing = [m for m in members if m.get("email","").lower() == data['email'].lower()]
    if existing:
        return False, f"Email sudah terdaftar sebagai {existing[0].get('status')} - {existing[0].get('skill')}! 1 Member = 1 Jalur - Tidak bisa ganti jalur. Tetap masuk Ruang 2."
    fe=os.path.exists(CSV_FILE)
    fieldnames=["timestamp","nama","email","status","skill","skill_detail","provinsi","kota","visi","masukan","subscription","gdrive_folder","salary_base","contribution_5pct","bakat","phone"]
    with open(CSV_FILE,"a",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fieldnames)
        if not fe: w.writeheader()
        w.writerow({
            "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nama":data['nama'],
            "email":data['email'],
            "status":data['status'],
            "skill":data['skill'],
            "skill_detail":data['skill_detail'],
            "provinsi":data['provinsi'],
            "kota":data['kota'],
            "visi":data['visi'],
            "masukan":data['masukan'],
            "subscription":data.get('subscription','TAVO'),
            "gdrive_folder":data.get('gdrive_folder',''),
            "salary_base":data.get('salary_base',0),
            "contribution_5pct":data.get('contribution_5pct',0),
            "bakat":data.get('bakat',''),
            "phone":data.get('phone','')
        })
    return True,"Berhasil! Email follow-up akan dikirim."

def render_voice_card(text, card_id, title, badge):
    safe_js = json.dumps(text)
    safe_html = html.escape(text)
    html_code = f"""
    <div style="display:flex;gap:16px;align-items:flex-start;background:#F9FAFB;padding:16px;border-radius:16px;border:2px solid #E5E7EB;margin-bottom:16px;font-family:sans-serif">
        <div id="av-{card_id}" style="width:70px;height:70px;border-radius:50%;background:#E8F3ED;display:flex;align-items:center;justify-content:center;font-size:36px;flex-shrink:0">🌿</div>
        <div style="flex:1">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;flex-wrap:wrap;gap:8px">
                <span style="background:#E8F3ED;color:#2D5A4A;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:700">{badge}</span>
                <button onclick="playVoice()" style="background:#7FB69B;color:white;border:none;padding:10px 18px;border-radius:10px;cursor:pointer;font-weight:700">🔊 Suara</button>
            </div>
            <h4 style="margin:0 0 8px 0;color:#111827">{title}</h4>
            <p style="margin:0;color:#374151;line-height:1.6">{safe_html}</p>
            <div id="status-{card_id}" style="margin-top:8px;font-size:12px;color:#7FB69B"></div>
        </div>
    </div>
    <script>
    function playVoice(){{
        window.speechSynthesis.cancel();
        let av=document.getElementById('av-{card_id}');
        let status=document.getElementById('status-{card_id}');
        if(av) av.style.transform='scale(1.1)';
        let text={safe_js};
        let u=new SpeechSynthesisUtterance(text);
        u.lang='id-ID'; u.rate=0.9;
        u.onend=function(){{ if(av) av.style.transform='scale(1)'; if(status) status.innerHTML='✅ Selesai - Jasa Ruang Teduh'; }};
        window.speechSynthesis.speak(u);
    }}
    </script>
    """
    components.html(html_code, height=320)

if "room" not in st.session_state: st.session_state.room=1
if "profile" not in st.session_state: st.session_state.profile={}

members=load_members()

with st.sidebar:
    st.markdown("### 🌿 Ruang Teduh v2.1")
    st.markdown(f'<div class="metric-card">📚 {len(members)}/1000<br>1 Jalur/Member</div>', unsafe_allow_html=True)
    st.progress(min(len(members)/1000,1.0) if members else 0.01)
    st.divider()
    if st.button("📚 Ruang 1 - Daftar Valid", use_container_width=True): st.session_state.room=1; st.rerun()
    if st.button("🎥 Ruang 2 - 200rb/300rb", use_container_width=True): st.session_state.room=2; st.rerun()
    if st.button("🌟 Ruang 3 - Corp Access", use_container_width=True): st.session_state.room=3; st.rerun()
    st.caption("Skema: 1 Member = 1 Jalur | Employee 200rb | Entrepreneur 300rb")

if st.session_state.room==1:
    st.title("📚 Ruang 1 · Pendaftaran Valid - 1 Member 1 Jalur")
    st.info("✅ Member harus info diri dengan benar - Skill & Bakat - Employee/Entrepreneur - Mudah kita kenali! Nasehat Alkitab + SOP/ERP/OEE/KPI sudah tertanam - Bimbingan Ruang Teduh!")
    
    col_lib, col_form = st.columns([1.2,1])
    with col_lib:
        st.subheader("📖 Nasehat + Ayat Motivasi + SOP/ERP/OEE/KPI")
        render_voice_card("Kolose 3:23 - Bekerja dengan segenap hati seperti untuk Tuhan. SOP: Datang 15 menit awal. ERP: Input tugas→Proses→Output. OEE: Optimalkan Energi. KPI: Kejujuran, Ketekunan.", "kolose", "Employee - Kolose 3:23 + SOP/ERP/OEE/KPI", "EMPLOYEE + KPI")
        render_voice_card("Amsal 16:3 - Serahkan perbuatanmu kepada TUHAN. SOP Usaha: HPP jelas, profit 20%. ERP: Order→Packing→Kirim. OEE: Availability x Performance. KPI: Omzet, Dampak, Integritas.", "amsal", "Entrepreneur - Amsal 16:3 + SOP/ERP/OEE/KPI", "ENTREPRENEUR + KPI")
        st.markdown("""
        <div class="sop-table">
            <b>🌱 Bimbingan Tertanam Ruang Teduh:</b><br>
            - <b>Alkitab:</b> Kolose 3:23, Amsal 16:3, Filipi 4:6-7, Mazmur 23<br>
            - <b>SOP:</b> Standar Operasional Prosedur kerja & usaha<br>
            - <b>ERP:</b> Enterprise Resource Planning - alur kerja<br>
            - <b>OEE:</b> Overall Equipment Effectiveness - efisiensi<br>
            - <b>KPI:</b> Key Performance Indicator - target terukur<br>
            → Member sudah tertanam bimbingan & terikat mau berlangganan!
        </div>
        """, unsafe_allow_html=True)
    
    with col_form:
        st.subheader("📝 Form Valid - 1 Jalur/Member + Email Follow-up")
        with st.form("form_v21"):
            nama=st.text_input("Nama Lengkap Valid *")
            email=st.text_input("Email Valid * (untuk follow-up)")
            phone=st.text_input("No HP/WA Valid * (untuk sales/marketing share)")
            
            st.markdown("**🔀 Status - 1 Jalur Saja! * (Tidak bisa ganti!)**")
            status=st.selectbox("Status", ["Employee - Tenaga Kerja", "Entrepreneur - Usahawan"], help="1 Member = 1 Jalur - Pilih sekali seumur hidup!")
            
            if "Employee" in status:
                skill=st.selectbox("Skill Employee", ["Chef / Koki", "Staff Resto/Cafe", "Staff Admin", "Staff Sales", "Waiter", "Cleaning", "Driver", "Barista", "Lainnya"])
                bakat=st.text_area("Bakat & Skill Detail *", placeholder="Contoh: Bakat masak Chinese, 5 tahun chef hotel, bisa 50 menu. Jujur tulis agar mudah kita kenali bakat masing-masing!")
                skill_detail=st.text_input("Pengalaman (tahun & tempat)")
            else:
                skill=st.selectbox("Skill Entrepreneur", ["Pedagang Online", "Boss Kios", "Boss Ruko", "Boss Rukan", "Reseller/Dropship", "Owner Warung/Cafe", "Owner Toko", "Lainnya"])
                bakat=st.text_area("Bakat & Usaha Detail *", placeholder="Contoh: Bakat jualan, punya kios sembako 3x3m di Bekasi, omzet 20jt/bln, butuh 1 staff. Tulis jelas!")
                skill_detail=st.text_input("Omzet & Lokasi Usaha")
            
            st.markdown("**📍 Lokasi Valid (untuk UMR & Follow-up)**")
            provinsi=st.selectbox("Provinsi", ["DKI Jakarta", "Jawa Barat", "Jawa Timur", "Jawa Tengah", "Banten", "Bali", "Sumatera Utara", "Lainnya"])
            kota=st.text_input("Kota/Kabupaten Valid *", placeholder="Kota Bekasi - untuk hitung UMR/UMP/UMK")
            
            visi=st.text_area("Visi Pribadi/Karir/Usaha")
            masukan=st.text_area("Masukan & Kebutuhan Bimbingan *", placeholder="Butuh bimbingan apa? Gaji? Vendor? Sewa ruko?")
            
            # Fixed Rate - Keterikatan Member (dari 5% dikonversi ke fixed)
            st.markdown("**💰 Biaya Berlangganan - Keterikatan Member (Fixed Rate)**")
            st.caption("Dari hitungan 5% UMR (Rp109k-269k) kita bulatkan jadi keterikatan fixed - Jangan terlalu murah!")
            if "Employee" in status:
                salary_base=st.number_input("Gaji/Upah Regional Anda (Rp/bulan) - Info saja", value=5396761, step=100000, help="UMR Jakarta 5.396.761, Jabar 2.191.232 - Untuk data valid")
                contrib = 200000  # Fixed rate Employee
                st.success(f"✅ Employee Rate: Rp{contrib:,}/bulan - Keterikatan Member (dari 5% UMR dibulatkan)")
            else:
                salary_base=st.number_input("Omzet/Profit Usaha (Rp/bulan) - Info saja", value=10000000, step=500000, help="Entrepreneur lebih besar")
                contrib = 300000  # Fixed rate Entrepreneur
                st.success(f"✅ Entrepreneur Rate: Rp{contrib:,}/bulan - Keterikatan Member - Level lebih besar!")
            
            subscription=st.selectbox("Paket", [f"TAVO - Rp{contrib:,}/bulan - Employee 200rb / Entrepreneur 300rb (Keterikatan)", "MALKHUTKHA - Rp399k/bulan Full Corporation Access"])
            
            submit=st.form_submit_button("🌟 Daftar Valid & Masuk Ruang 2 →", type="primary", use_container_width=True)
            if submit:
                if not nama or not email or not phone or not bakat: st.error("Nama, Email, HP, Bakat wajib valid!")
                elif not is_valid_email(email): st.error("Email salah!")
                else:
                    gdrive = f"TAVO_MALKHUTKHA/{'01_EMPLOYEE' if 'Employee' in status else '02_ENTREPRENEUR'}/{skill.replace(' ', '_')}"
                    data={'nama':nama,'email':email,'phone':phone,'status':status,'skill':skill,'skill_detail':skill_detail,'bakat':bakat,'provinsi':provinsi,'kota':kota,'visi':visi,'masukan':masukan,'subscription':subscription,'gdrive_folder':gdrive,'salary_base':salary_base,'contribution_5pct':contrib}
                    ok,msg=save_member(data)
                    st.session_state.profile=data
                    if ok:
                        st.success(f"✅ Valid! {nama} - {status} - Email follow-up akan dikirim ke {email}!")
                    else:
                        st.warning(msg)
                    st.balloons()
                    st.session_state.room=2
                    st.rerun()

elif st.session_state.room==2:
    p=st.session_state.profile
    st.title("🎥 Ruang 2 · Dual Jalur + 5% + Email Follow-up")
    st.caption("1 Member 1 Jalur - Info Valid - Skill & Bakat Terdata - SOP/ERP/OEE/KPI Tertanam")
    
    if not p or not p.get("nama"):
        st.warning("Isi form valid di Ruang 1 dulu!")
        if st.button("← Ruang 1", type="primary"): st.session_state.room=1; st.rerun()
    else:
        is_emp = "Employee" in p.get('status','')
        st.markdown(f"""
        <div class="binding-card">
            <h3>🌿 Shalom! Namo Buddhaya - {p.get('nama')} - {p.get('status')}</h3>
            <p>Skill: {p.get('skill')} | Bakat: {p.get('bakat')[:60]}... | Lokasi: {p.get('kota')}, {p.get('provinsi')} | HP: {p.get('phone')}</p>
            <p>Gaji/Omzet: Rp{p.get('salary_base',0):,.0f} → Kontribusi 5%: Rp{p.get('contribution_5pct',0):,.0f}/bulan | Folder: {p.get('gdrive_folder')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # SKEMA 1 JALUR
        st.subheader("🔀 Skema - Masing-masing 1 Jalur")
        st.info("✅ Setiap member hanya 1 jalur - Employee atau Entrepreneur - Tidak bisa ganda - Email follow-up nanti dari email bisa kita follow-up - Info diri benar agar mudah kenal skill & bakat!")
        
        if is_emp:
            st.markdown("#### 💼 Employee - Gaji Wajar UMR/UMP/UMK + Bakat")
            umr_data = {
                "Wilayah": ["DKI Jakarta", "Jabar UMP", "Bekasi UMK", "Bogor Kota", "Depok"],
                "UMR 2025": ["Rp5.396.761", "Rp2.191.232", "Rp5.690.753", "Rp5.126.897", "Rp5.195.720"],
                "5% Kontribusi": ["Rp269.838", "Rp109.562", "Rp284.538", "Rp256.345", "Rp259.786"]
            }
            st.dataframe(pd.DataFrame(umr_data), use_container_width=True)
            st.success(f"💰 Anda: {p.get('skill')} - {p.get('bakat')} - Gaji Rp{p.get('salary_base',0):,.0f} → Kontribusi 5% = Rp{p.get('contribution_5pct',0):,.0f}/bulan - Jasa Ruang Teduh!")
        else:
            st.markdown("#### 💡 Entrepreneur - Profit 20% + Butuh Tenaga Kerja + Gaji Lebih Besar")
            ent_data = {
                "Usaha": ["Kios 3x3m", "Ruko 4x12m", "Rukan", "Online Reseller"],
                "Sewa/bulan": ["Rp1-2jt", "Rp5-15jt", "Rp10-25jt", "Rp0 (online)"],
                "Butuh Staff": ["1 staff", "2-3 staff", "3-5 staff", "1 admin"],
                "Gaji Staff (UMK)": ["Rp5.4jt", "Rp10.8jt", "Rp16.2jt", "Rp5.4jt"],
                "Omzet Contoh": ["Rp10jt", "Rp30jt", "Rp50jt", "Rp20jt"],
                "5% Kontribusi": ["Rp500k", "Rp1.5jt", "Rp2.5jt", "Rp1jt"]
            }
            st.dataframe(pd.DataFrame(ent_data), use_container_width=True)
            st.success(f"💰 Anda: {p.get('skill')} - Omzet Rp{p.get('salary_base',0):,.0f} → Kontribusi 5% = Rp{p.get('contribution_5pct',0):,.0f}/bulan - Level entrepreneur lebih besar!")
        
        st.divider()
        st.subheader("📧 Email Follow-up + Corporation Access")
        st.markdown("""
        <div class="sop-table">
            <b>📧 Prosedur Email Follow-up:</b><br>
            1. Member daftar valid di Ruang 1 → Data masuk CSV Github (1 member 1 jalur)<br>
            2. Sistem kirim email otomatis ke member: 'Shalom! Bimbingan Ruang Teduh - SOP/ERP/OEE/KPI'<br>
            3. Tim Ruang Teduh follow-up via email & WA dari data phone valid<br>
            4. Member di Ruang 2 dapat motivasi & cara berlangganan sesuai kemampuan<br>
            5. Di Ruang 3: Member dapat akses corporation - bimbingan, kerja sama antar member, saling access!<br>
            6. <b>Jaminan:</b> Berlangganan = Dapat kepastian kerja sama & akses corporation!
        </div>
        """, unsafe_allow_html=True)
        
        # SIMULASI EMAIL FOLLOW-UP
        st.markdown("#### ✉️ Simulasi Email Follow-up (Nanti Otomatis)")
        email_template = f"""
        Subject: Shalom {p.get('nama')}! Bimbingan Ruang Teduh - {p.get('status')} - {p.get('skill')}
        
        Shalom! Namo Buddhaya {p.get('nama')},
        
        Terima kasih sudah daftar valid sebagai {p.get('status')} - {p.get('skill')} - Bakat: {p.get('bakat')}.
        
        Bimbingan Anda sudah tertanam di Ruang Teduh:
        - Ayat: {'Kolose 3:23' if is_emp else 'Amsal 16:3'} + SOP/ERP/OEE/KPI
        - Lokasi: {p.get('kota')}, {p.get('provinsi')} - Gaji/Omzet: Rp{p.get('salary_base',0):,.0f}
        - Kontribusi 5%: Rp{p.get('contribution_5pct',0):,.0f}/bulan
        
        Next: Masuk Ruang 3 untuk akses corporation & antar member!
        
        Salam,
        Tim Ruang Teduh AIJC
        """
        st.text_area("Template Email Follow-up", value=email_template, height=200)
        
        st.divider()
        st.subheader("🎙️ Rekam Komitmen - Tabur")
        c1,c2=st.columns(2)
        with c1:
            audio=st.audio_input(f"Rekam komitmen {p.get('status')}")
            if audio: st.success("✅ Tabur tersimpan!")
        with c2:
            video=st.file_uploader("Upload video", type=["mp4","webm","mov"])
            if video: st.video(video)
        
        if st.button("🌟 Masuk Ruang 3 - Corporation Access →", type="primary", use_container_width=True):
            st.session_state.room=3
            st.rerun()

else:
    st.title("🌟 Ruang 3 · Full Binding - Corporation Access & Jaminan Berlangganan")
    p=st.session_state.profile
    if p and p.get("email"):
        st.success(f"Member: {p.get('email')} - {p.get('status')} - {p.get('skill')} - Valid - Shalom Namo Buddhaya!")
    
    st.markdown("""
    <div class="corp-card">
        <h3>🏢 Corporation Access - Ruang Teduh - Jaminan Berlangganan!</h3>
        <p>Member sudah tertanam bimbingan Ruang Teduh (Alkitab + SOP/ERP/OEE/KPI) - Ajak terikat mau berlangganan karena di Ruang 3 kita beri motivasi bahkan kepastian kerja sama antar member - Member akan dapat terkoneksi langsung & dapat access corporation berupa bimbingan & semacamnya - Sesama member akan dapat saling access di Ruang 3! Makanya mereka mesti berlangganan. Jaminan!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # PERHITUNGAN FIXED RATE - KETERIKATAN MEMBER
    st.subheader("💰 Biaya Member - Keterikatan Berlangganan - Fixed Rate!")
    st.info("Dari penjelasan persentase 5% (Rp109k-269k) kita alihkan langsung jadi keterikatan member berupa berlangganan fixed rate - Employee 200rb, Entrepreneur 300rb - Jangan terlalu murah!")
    
    col_calc1, col_calc2 = st.columns(2)
    with col_calc1:
        st.markdown("#### 📈 Employee - Rp200rb/bulan (Fixed)")
        calc_emp = {
            "Skenario": ["100 Employee x 200rb", "500 Employee x 200rb", "1000 Employee x 200rb", "Dasar: 5% UMR Jakarta 5.39jt = 269rb → bulat 200rb"],
            "Per Member": ["Rp200.000", "Rp200.000", "Rp200.000", "Rp200.000 (dari 5% = 109k-269k)"],
            "Akumulasi/bulan": ["Rp20.000.000", "Rp100.000.000", "Rp200.000.000", "Wajar - Tidak murah!"],
            "Catatan": ["100 x 200k", "500 x 200k", "1000 x 200k", "Keterikatan member"]
        }
        st.dataframe(pd.DataFrame(calc_emp), use_container_width=True)
    
    with col_calc2:
        st.markdown("#### 📈 Entrepreneur - Rp300rb/bulan (Fixed - Lebih Besar)")
        calc_ent = {
            "Skenario": ["100 Entrepreneur x 300rb", "500 Entrepreneur x 300rb", "1000 Entrepreneur x 300rb", "1000 Mix (500 Emp + 500 Ent)"],
            "Per Member": ["Rp300.000", "Rp300.000", "Rp300.000", "200rb & 300rb"],
            "Akumulasi/bulan": ["Rp30.000.000", "Rp150.000.000", "Rp300.000.000", "Rp250.000.000 (100jt+150jt)"],
            "Catatan": ["Level boss", "Kios/Ruko/Rukan", "Omzet lebih besar", "Total mix"]
        }
        st.dataframe(pd.DataFrame(calc_ent), use_container_width=True)
    
    st.markdown("""
    <div class="profit-card">
        <h3>💡 Fixed Rate 200rb & 300rb - Akumulasi vs Menyusut:</h3>
        <b>Dari 5% (109k-500k) → Fixed Rate Keterikatan:</b><br>
        - Employee: 5% UMR (109k-269k) → <b>Fixed Rp200rb/bulan</b> (tengah-tengah, tidak murah!)<br>
        - Entrepreneur: 5% Omzet (500k-2.5jt) → <b>Fixed Rp300rb/bulan</b> (lebih besar, level boss!)<br><br>
        <b>Akumulasi (Retention 90%):</b><br>
        - Bulan 1: 100 member (50 Emp 200rb + 50 Ent 300rb) = 10jt + 15jt = Rp25jt<br>
        - Bulan 2: 90 + 100 baru = 190 member = Rp47.5jt<br>
        - Bulan 3: 171 + 100 = 271 member = Rp67.75jt → <b>Akumulasi naik terus!</b><br><br>
        <b>Menyusut (Churn 50%):</b><br>
        - Bulan 1: 100 member = Rp25jt<br>
        - Bulan 2: 50 member = Rp12.5jt → <b>Menyusut!</b><br>
        - Solusi: Jaminan corporation access + antar member + email follow-up + sales offline!<br><br>
        <b>Kesimpulan:</b> Employee 200rb, Entrepreneur 300rb - Fixed Rate Keterikatan - Wajar, tidak murah, jasa premium + SOP + corporation!
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🏢 App Bisa Dishare ke Sales/Marketing - Offline + Online - Jasa Perusahaan")
    st.markdown("""
    <div class="sop-table">
        <b>📱 App Share - Tidak Hanya Online:</b><br>
        - <b>Sales/Marketing:</b> Bisa share link ruang-teduh-ai.streamlit.app via WA, QR Code, brosur<br>
        - <b>Offline:</b> Bisa bikin perusahaan jasa - Kantor Ruang Teduh - Konsultasi tatap muka<br>
        - <b>Jasa:</b> Bimbingan Employee (UMR) & Entrepreneur (sewa ruko, vendor, profit 20%)<br>
        - <b>Biaya:</b> 5% dari gaji/omzet - Wajar - Jangan murah - Jasa premium!<br>
        - <b>Garansi:</b> Member berlangganan = Dapat akses corporation & antar member!
    </div>
    """, unsafe_allow_html=True)
    
    c1,c2=st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="full-service">
            <h3>🌿 TAVO - Fixed Rate Keterikatan</h3>
            <p>Employee: Rp200rb/bln | Entrepreneur: Rp300rb/bln (dari 5% → fixed rate keterikatan)</p>
            <p>Member: Rp{p.get('contribution_5pct', 200000):,.0f}/bulan - {p.get('status','')}</p>
            <ul>
                <li>✅ 12 Folder GDrive</li>
                <li>✅ SOP/ERP/OEE/KPI</li>
                <li>✅ Email Follow-up</li>
                <li>✅ Corporation Access Dasar</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌱 Pilih TAVO - 200rb/300rb", use_container_width=True): st.balloons(); st.success(f"Tavo! {p.get('status','')} - Rp{p.get('contribution_5pct',0):,.0f}/bulan - Keterikatan!")
    with c2:
        st.markdown("""
        <div class="full-service" style="border:2px solid #2D5A4A;background:#E8F3ED">
            <h3>🌟 MALKHUTKHA - Full Corp Access</h3>
            <p>Full Binding + Jaminan Kerja Sama!</p>
            <ul>
                <li>🔥 Akses Corporation Antar Member</li>
                <li>🔥 Kepastian Kerja Sama</li>
                <li>🔥 Share ke Sales/Marketing Offline</li>
                <li>🔥 Jaminan Berlangganan</li>
                <li>🔥 Bisa Jadi Perusahaan Jasa</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌟 MALKHUTKHA - Full Access", type="primary", use_container_width=True): st.balloons(); st.success("MALKHUTKHA! Full Corporation Access!")
    
    st.divider()
    if len(members)>0:
        st.subheader(f"📧 {len(members)} Member Valid - 1 Jalur/Member - Bisa Email Follow-up")
        st.dataframe(pd.DataFrame(members), use_container_width=True)
        total_contrib = sum([float(m.get('contribution_5pct',0) or 0) for m in members])
        st.success(f"💰 Total Potensi Kontribusi 5%: Rp{total_contrib:,.0f}/bulan dari {len(members)} member - Akumulasi jika retention bagus!")
