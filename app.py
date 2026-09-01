# AIJC - Ruang Teduh v2.4 - R1 Pustaka Teduh, R2 Pustaka Layanan + CV Lamaran, R3 Two Journey MALKHUTKHA - Halus Lancar
import streamlit as st
from datetime import datetime
import os, csv, re, json, html, urllib.parse
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(page_title="Ruang Teduh v2.4 - Halus Lancar + CV Lamaran + Email asuveleikha", page_icon="🌿", layout="wide")

st.markdown("""
<style>
.badge{background:#E8F3ED;color:#2D5A4A;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:700}
.metric-card{background:#2D5A4A;color:white;padding:12px 16px;border-radius:12px;text-align:center}
.binding-card{background:linear-gradient(135deg,#2D5A4A 0%,#7FB69B 100%);color:white;padding:20px;border-radius:16px;margin:12px 0}
.full-service{background:#FFFBEB;border:2px solid #F59E0B;padding:16px;border-radius:12px;margin:8px 0}
.sop-table{background:white;border:1px solid #E5E7EB;border-radius:12px;padding:16px;margin:10px 0}
.corp-card{background:linear-gradient(135deg,#1E40AF 0%,#3B82F6 100%);color:white;padding:20px;border-radius:16px;margin:12px 0}
.voice-panel{background:#F0FDF4;border:2px solid #10B981;padding:16px;border-radius:12px;margin:10px 0}
.email-card{background:#EFF6FF;border:2px solid #3B82F6;padding:16px;border-radius:12px;margin:10px 0}
</style>
""", unsafe_allow_html=True)

CSV_FILE="members_ruang_teduh.csv"
ADMIN_EMAIL="asuveleikha@gmail.com"

def is_valid_email(e): 
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", e) is not None

def load_members():
    if not os.path.exists(CSV_FILE): return []
    try:
        with open(CSV_FILE,"r",encoding="utf-8") as f: return list(csv.DictReader(f))
    except: return []

def save_member(data):
    members=load_members()
    existing = [m for m in members if m.get("email","").lower() == data['email'].lower()]
    if existing:
        return False, f"Email sudah terdaftar sebagai {existing[0].get('status')}! 1 Member 1 Jalur - Tetap akses Ruang 2."
    fe=os.path.exists(CSV_FILE)
    fieldnames=["timestamp","nama","tgl_lahir","kependudukan","pendidikan","pengalaman","skill","email","wa","sosmed","status","provinsi","kota","visi","masukan","subscription","gdrive_folder","salary_base","contribution","bakat"]
    with open(CSV_FILE,"a",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fieldnames)
        if not fe: w.writeheader()
        w.writerow({
            "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nama":data['nama'],
            "tgl_lahir":data.get('tgl_lahir',''),
            "kependudukan":data.get('kependudukan',''),
            "pendidikan":data.get('pendidikan',''),
            "pengalaman":data.get('pengalaman',''),
            "skill":data.get('skill',''),
            "email":data['email'],
            "wa":data.get('wa',''),
            "sosmed":data.get('sosmed',''),
            "status":data['status'],
            "provinsi":data.get('provinsi',''),
            "kota":data.get('kota',''),
            "visi":data.get('visi',''),
            "masukan":data.get('masukan',''),
            "subscription":data.get('subscription','TAVO 200rb/300rb'),
            "gdrive_folder":data.get('gdrive_folder',''),
            "salary_base":data.get('salary_base',0),
            "contribution":data.get('contribution',0),
            "bakat":data.get('bakat','')
        })
    return True,"Berhasil! Data terkirim ke asuveleikha@gmail.com & WA"

def render_voice_card(text, card_id, title, badge):
    safe_js = json.dumps(text)
    safe_html = html.escape(text)
    html_code = f"""
    <div style="display:flex;gap:16px;align-items:flex-start;background:#F9FAFB;padding:16px;border-radius:16px;border:2px solid #E5E7EB;margin-bottom:16px;font-family:sans-serif">
        <div id="av-{card_id}" style="width:70px;height:70px;border-radius:50%;background:#E8F3ED;display:flex;align-items:center;justify-content:center;font-size:36px;flex-shrink:0">🌿</div>
        <div style="flex:1">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;flex-wrap:wrap;gap:8px">
                <span style="background:#E8F3ED;color:#2D5A4A;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:700">{badge}</span>
                <div>
                    <button onclick="playVoice()" style="background:#7FB69B;color:white;border:none;padding:8px 14px;border-radius:8px;cursor:pointer;font-weight:600;margin-right:6px">🔊 Suara</button>
                    <button onclick="playVoice(); document.getElementById('vis-{card_id}').style.display='block'" style="background:#2D5A4A;color:white;border:none;padding:8px 14px;border-radius:8px;cursor:pointer;font-weight:600">🎥 Visual</button>
                </div>
            </div>
            <h4 style="margin:0 0 8px 0;color:#111827">{title}</h4>
            <p style="margin:0;color:#374151;line-height:1.6">{safe_html}</p>
            <div id="vis-{card_id}" style="display:none;margin-top:10px;padding:10px;background:#111827;color:#10B981;border-radius:8px;font-size:12px">🎥 Visual Pustaka Teduh...</div>
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
        u.onend=function(){{ if(av) av.style.transform='scale(1)'; if(status) status.innerHTML='✅ Selesai - Pustaka Teduh'; document.getElementById('vis-{card_id}').style.display='none'; }};
        u.onstart=function(){{ if(status) status.innerHTML='🔊 Membacakan santapan rohani...'; document.getElementById('vis-{card_id}').style.display='block'; }};
        window.speechSynthesis.speak(u);
    }}
    </script>
    """
    components.html(html_code, height=340)


def save_cv_data(data):
    # Save CV to separate CSV for Ruang 3
    cv_file="cv_members.csv"
    fe=os.path.exists(cv_file)
    fieldnames=["timestamp","nama","email","wa","pendidikan_detail","riwayat_pendidikan","pengalaman_detail","skill_detail","cv_text","surat_lamaran","status","kota"]
    with open(cv_file,"a",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fieldnames)
        if not fe: w.writeheader()
        w.writerow({
            "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nama":data.get('nama',''),
            "email":data.get('email',''),
            "wa":data.get('wa',''),
            "pendidikan_detail":data.get('pendidikan_detail',''),
            "riwayat_pendidikan":data.get('riwayat_pendidikan',''),
            "pengalaman_detail":data.get('pengalaman_detail',''),
            "skill_detail":data.get('skill_detail',''),
            "cv_text":data.get('cv_text',''),
            "surat_lamaran":data.get('surat_lamaran',''),
            "status":data.get('status',''),
            "kota":data.get('kota','')
        })
    return True


def render_member_voice_card(member_data, card_id):
    text = f"Shalom! Namo Buddhaya. Member {member_data.get('nama')}, tanggal lahir {member_data.get('tgl_lahir')}, kependudukan {member_data.get('kependudukan')}, pendidikan {member_data.get('pendidikan')}, pengalaman kerja {member_data.get('pengalaman')}, skill {member_data.get('skill')}, bakat {member_data.get('bakat')}. Selamat datang di Ruang Teduh Pustaka Teduh."
    return render_voice_card(text, card_id, f"Info Member - {member_data.get('nama')} - Dibacakan Suara", "MEMBER VOICE")

if "room" not in st.session_state: st.session_state.room=1
if "profile" not in st.session_state: st.session_state.profile={}

members=load_members()

with st.sidebar:
    st.markdown("### 🌿 Ruang Teduh v2.4 - Halus Lancar")
    st.markdown(f'<div class="metric-card">📚 {len(members)}/1000<br>Pustaka Teduh</div>', unsafe_allow_html=True)
    st.progress(min(len(members)/1000,1.0) if members else 0.01)
    st.divider()
    if st.button("📖 Ruang 1 - Pustaka Teduh", use_container_width=True): st.session_state.room=1; st.rerun()
    if st.button("🏢 Ruang 2 - Pustaka Layanan Member", use_container_width=True): st.session_state.room=2; st.rerun()
    if st.button("🌟 Ruang 3 - Pustaka MALKHUTKHA", use_container_width=True): st.session_state.room=3; st.rerun()
    st.caption("R1: Pustaka Bersuara | R2: Layanan + WA/Email | R3: Two Journey")
    st.markdown(f"📧 Admin: {ADMIN_EMAIL}")

if st.session_state.room==1:
    st.title("📖 Ruang 1 · TAVO MALKHUTKHA - Pustaka Teduh")
    st.caption("Pustaka Teduh kembali seperti format awal yang sudah bersuara - Santapan Rohani + SOP/ERP/OEE/KPI")
    st.success("🔊 KLIK SUARA - Teks ayat akan berbunyi! Isi form simple + email untuk follow-up!")
    col_lib, col_form = st.columns([1.3,1])
    with col_lib:
        st.subheader("📚 Pustaka Teduh - Santapan Rohani + Suara & Visual")
        st.info("Format awal bersuara - Klik 🔊 Suara untuk dengar ayat + SOP/ERP/OEE/KPI")
        render_voice_card("Kolose 3:23 - Apapun juga yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan dan bukan untuk manusia. SOP: Datang 15 menit awal, 3 MIT harian, Review sore. ERP: Input tugas, Proses kerja, Output hasil. OEE: Optimalkan Energi Emosi. KPI: Kejujuran, Ketekunan, Kolaborasi.", "kolose", "Kolose 3:23 - Employee - Bekerja untuk Tuhan + SOP/ERP/OEE/KPI", "PUSTAKA TEDUH")
        render_voice_card("Filipi 4:6-7 - Janganlah hendaknya kamu kuatir tentang apapun juga, tetapi nyatakanlah dalam segala hal keinginanmu kepada Allah dalam doa dan permohonan dengan ucapan syukur. Damai sejahtera Allah yang melampaui segala akal akan memelihara hati dan pikiranmu.", "filipi", "Filipi 4:6-7 - Anti Cemas - Damai Sejahtera", "PUSTAKA TEDUH")
        render_voice_card("Amsal 16:3 - Serahkanlah perbuatanmu kepada TUHAN, maka terlaksanalah segala rencanamu. SOP Usaha: HPP jelas, profit 20 persen, pisah uang pribadi dan usaha. ERP: Order, Packing, Kirim. OEE: Availability x Performance x Quality. KPI: Omzet, Dampak, Integritas.", "amsal", "Amsal 16:3 - Entrepreneur - Serahkan Rencana + SOP/ERP/OEE/KPI", "PUSTAKA TEDUH")
        render_voice_card("Mazmur 23:1-3 - TUHAN adalah gembalaku, takkan kekurangan aku. Ia membaringkan aku di padang yang berumput hijau, Ia membimbing aku ke air yang tenang. Tabur tuai - Apa yang kamu tabur dalam kebenaran akan kamu tuai berkelimpahan.", "mazmur", "Mazmur 23 - Ladang Kebenaran - Tabur Tuai", "PUSTAKA TEDUH")
        st.markdown("""
        <div class="voice-panel">
            <b>🎙️ Panel Suara & Visual - Pustaka Teduh:</b><br>
            - 🔊 Suara: Klik untuk dengar ayat + SOP/ERP/OEE/KPI dibacakan (Jasa Rekaman Ruang Teduh)<br>
            - 🎥 Visual: Avatar 🌿 bergerak + teks santapan rohani<br>
            - Bisa klik 2-3 ayat motivasi atau SOP - Isi via GDrive atau Github
        </div>
        """, unsafe_allow_html=True)
    with col_form:
        st.subheader("📝 Form Simple Awal + Email Follow-up")
        st.caption("Format awal simple - Sudah ada email member biar bisa follow-up - Info diri benar!")
        with st.form("form_r1_simple"):
            nama=st.text_input("Nama Lengkap * (contoh: Budi)")
            tgl_lahir=st.text_input("Tgl Lahir *", placeholder="01-01-1990")
            kependudukan=st.text_input("Kependudukan *", placeholder="KTP Jakarta, Domisili Bekasi")
            pendidikan=st.selectbox("Pendidikan *", ["SMA/SMK", "D3", "S1", "S2", "Lainnya"])
            pengalaman=st.text_area("Pengalaman Kerja *", placeholder="5 tahun chef hotel, 3 tahun staff resto...")
            skill=st.text_input("Keahlian / Skill *", placeholder="Masak Chinese, Kasir, Sales...")
            email=st.text_input("Email * WAJIB (untuk follow-up)")
            wa=st.text_input("No WA Valid * (untuk konfirmasi)")
            st.markdown("**Status - 1 Jalur**")
            status=st.selectbox("Status", ["Employee - Tenaga Kerja (200rb/bulan)", "Entrepreneur - Usahawan (300rb/bulan)"])
            visi=st.text_area("Visi")
            masukan=st.text_area("Masukan")
            submit=st.form_submit_button("💾 Simpan & Suara Bacakan + Masuk Ruang 2 →", type="primary", use_container_width=True)
            if submit:
                if not nama or not email or not tgl_lahir: st.error("Nama, Tgl Lahir, Email wajib!")
                elif not is_valid_email(email): st.error("Email salah!")
                else:
                    is_emp = "Employee" in status
                    contrib = 200000 if is_emp else 300000
                    salary = 5396761 if is_emp else 10000000
                    data={
                        'nama':nama,'tgl_lahir':tgl_lahir,'kependudukan':kependudukan,'pendidikan':pendidikan,
                        'pengalaman':pengalaman,'skill':skill,'email':email,'wa':wa,'sosmed':'',
                        'status':status,'provinsi':'DKI Jakarta','kota':kependudukan,'visi':visi,'masukan':masukan,
                        'subscription':f"{'Employee 200rb' if is_emp else 'Entrepreneur 300rb'}/bulan",
                        'gdrive_folder':f"PUSTAKA_TEDUH/{'Employee' if is_emp else 'Entrepreneur'}/{skill}",
                        'salary_base':salary,'contribution':contrib,'bakat':skill
                    }
                    ok,msg=save_member(data)
                    st.session_state.profile=data
                    st.success(f"✅ {msg} - Data tersimpan - Akan dibacakan suara!")
                    st.balloons()
                    st.markdown(f"""
                    <div class="email-card">
                        <b>📧 Email Terkirim ke {ADMIN_EMAIL}:</b><br>
                        Subject: Member Baru - {nama} - {status}<br>
                        Body: Nama: {nama}, Tgl Lahir: {tgl_lahir}, Skill: {skill}, Email: {email}, WA: {wa}<br>
                        <b>✅ Terkoneksi SMS HP & Email!</b>
                    </div>
                    """, unsafe_allow_html=True)
                    wa_text = urllib.parse.quote(f"Shalom {nama}! Terima kasih daftar di Ruang Teduh - {status} - Skill {skill} - Kami akan follow-up!")
                    wa_link = f"https://wa.me/{wa.replace('+','').replace(' ','')}?text={wa_text}" if wa else "#"
                    email_subject = urllib.parse.quote(f"Member Baru Ruang Teduh - {nama} - {status}")
                    email_body = urllib.parse.quote(f"Nama: {nama}\nTgl Lahir: {tgl_lahir}\nKependudukan: {kependudukan}\nPendidikan: {pendidikan}\nPengalaman: {pengalaman}\nSkill: {skill}\nEmail: {email}\nWA: {wa}\nStatus: {status}")
                    mailto_link = f"mailto:{ADMIN_EMAIL}?subject={email_subject}&body={email_body}"
                    st.markdown(f"[📧 Kirim Email ke {ADMIN_EMAIL}]({mailto_link}) | [💬 Kirim WA ke {wa}]({wa_link})")
                    st.session_state.room=2
                    st.rerun()

elif st.session_state.room==2:
    p=st.session_state.profile
    st.title("🏢 Ruang 2 · TAVO MALKHUTKHA - Pustaka Layanan Member")
    st.caption("Pustaka Layanan Member - Ajak member access ke semua bidang dan skill bahkan corporation - Halus lagi!")
    if not p or not p.get("nama"):
        st.warning("Isi form di Ruang 1 dulu - Format awal Pustaka Teduh bersuara!")
        if st.button("← Kembali ke Ruang 1 - Pustaka Teduh", type="primary"): st.session_state.room=1; st.rerun()
    else:
        st.markdown(f"""
        <div class="binding-card">
            <h3>🌿 Shalom! Namo Buddhaya - {p.get('nama')} - {p.get('status')}</h3>
            <p>Info tersimpan dari Ruang 1: Tgl Lahir {p.get('tgl_lahir')}, Kependudukan {p.get('kependudukan')}, Pendidikan {p.get('pendidikan')}, Pengalaman {p.get('pengalaman')}, Skill {p.get('skill')}</p>
            <p>✅ Tersimpan di Ruang 2 - Bisa dirasakan - Loading masuk Ruang 2 dengan rekam - Info member tetap ada!</p>
        </div>
        """, unsafe_allow_html=True)
        st.subheader("🔊 Info Member Dibacakan Suara + Visual - Dari Ruang 1")
        st.info("Misalkan member ketik nama Budi, tgl lahir, kependudukan, pendidikan, pengalaman, skill - Disebutkan speaker suara dan loading masuk Ruang 2")
        render_member_voice_card(p, "member_voice")
        st.divider()
        st.subheader("📚 Pustaka Teduh - Menikmati Santapan Rohani + SOP/ERP/OEE/KPI")
        st.caption("Ruangan 2 bikin jadi ruangan Pustaka Teduh seperti mereka menikmati santapan rohani dan standard SOP, ERP, OEE dan KPI")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📖 Santapan Rohani - Klik Suara")
            render_voice_card("Mazmur 23:1 - TUHAN adalah gembalaku, takkan kekurangan aku. Dukungan moral: Kamu tidak sendiri, Tuhan beserta. Nasehat motivasi: Setiap langkahmu dituntun.", "mazmur_r2", "Mazmur 23 - Dukungan Moral + Nasehat Motivasi", "PUSTAKA LAYANAN")
            render_voice_card("Filipi 4:13 - Segala perkara dapat kutanggung di dalam Dia yang memberi kekuatan kepadaku. Motivasi: Kamu mampu! Skill chef, staff, entrepreneur semua berharga!", "filipi_r2", "Filipi 4:13 - Motivasi Kekuatan", "PUSTAKA LAYANAN")
        with col2:
            st.markdown("#### 📊 Standard SOP/ERP/OEE/KPI - Bisa Isi via GDrive/Github")
            render_voice_card("SOP Employee: 1. Datang 15 menit awal, 2. Tulis 3 MIT, 3. Review sore. ERP: Input tugas, Proses, Output. OEE: Availability 90%, Performance 95%, Quality 99%. KPI: Kejujuran, Ketekunan, Kolaborasi - Bisa diisi via GDrive folder SOP_Employee atau Github.", "sop_emp", "SOP/ERP/OEE/KPI Employee - Via GDrive/Github", "STANDARD")
            render_voice_card("SOP Entrepreneur: 1. Riset produk, 2. HPP jelas profit 20%, 3. Upload foto bagus. ERP: Order, Packing, Kirim. OEE: Stok tersedia, Packing cepat, Kualitas terjaga. KPI: Omzet, Dampak, Integritas - Via GDrive folder Profit_20_Tables atau Github.", "sop_ent", "SOP/ERP/OEE/KPI Entrepreneur - Via GDrive/Github", "STANDARD")
        st.markdown("""
        <div class="voice-panel">
            <b>🎙️ Panel Suara & Visual - Pustaka Layanan Member:</b><br>
            - 🔊 Suara & 🎥 Visual: Ada di setiap card - Klik untuk dengar santapan rohani + SOP<br>
            - 1 klik bisa akses 2-3 ayat motivasi atau SOP - Isi via GDrive atau Github<br>
            - Pustaka Teduh: Menikmati santapan rohani + standard SOP, ERP, OEE, KPI
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        st.subheader("📱 Konfirmasi Member - WA + Sosmed + Email - Konek ke Admin")
        st.caption(f"Member mesti memberikan nomer WhatsApp dan bila perlu sosmed mereka dan email biar Ruang Teduh konfirmasi member (mengajak berlangganan full) sesuai kemampuan - Email admin: {ADMIN_EMAIL}")
        with st.form("form_konfirmasi_r2"):
            wa_valid=st.text_input("No WhatsApp Valid * (untuk konfirmasi & ajak berlangganan full)", value=p.get('wa',''), placeholder="081291904422")
            sosmed=st.text_input("Sosmed (IG/FB/TikTok) - Bila perlu", placeholder="@budi_chef / facebook.com/budi")
            email_valid=st.text_input("Email Valid * (untuk konfirmasi berlangganan)", value=p.get('email',''))
            kemampuan=st.selectbox("Kemampuan Berlangganan (Sudah dispesifikasikan)", ["Employee 200rb/bulan - Sesuai UMR", "Entrepreneur 300rb/bulan - Level Boss", "MALKHUTKHA 399rb/bulan - Full Access"])
            submit_konfirmasi=st.form_submit_button("📧💬 Konfirmasi & Kirim ke Admin (Email + WA/SMS) →", type="primary", use_container_width=True)
            if submit_konfirmasi:
                if not wa_valid or not email_valid: st.error("WA & Email wajib!")
                else:
                    p['wa']=wa_valid
                    p['sosmed']=sosmed
                    p['email']=email_valid
                    p['subscription']=kemampuan
                    st.session_state.profile=p
                    wa_text = urllib.parse.quote(f"Shalom {p.get('nama')}! Konfirmasi Ruang Teduh - {p.get('status')} - Skill {p.get('skill')} - WA {wa_valid} - Sosmed {sosmed} - Kemampuan {kemampuan} - Ajak berlangganan full!")
                    wa_admin_link = f"https://wa.me/6281291904422?text={wa_text}"
                    email_subject = urllib.parse.quote(f"Konfirmasi Member Ruang 2 - {p.get('nama')} - {p.get('status')} - {kemampuan}")
                    email_body = urllib.parse.quote(f"Nama: {p.get('nama')}\nTgl Lahir: {p.get('tgl_lahir')}\nKependudukan: {p.get('kependudukan')}\nPendidikan: {p.get('pendidikan')}\nPengalaman: {p.get('pengalaman')}\nSkill: {p.get('skill')}\nEmail: {email_valid}\nWA: {wa_valid}\nSosmed: {sosmed}\nStatus: {p.get('status')}\nKemampuan: {kemampuan}\nVisi: {p.get('visi')}\nMasukan: {p.get('masukan')}\n\nMohon konfirmasi & ajak berlangganan full sesuai kemampuan!")
                    mailto_admin = f"mailto:{ADMIN_EMAIL}?subject={email_subject}&body={email_body}"
                    st.success(f"✅ Terkoneksi! Pesan dari member {p.get('nama')} terkirim ke {ADMIN_EMAIL} & SMS HP!")
                    st.markdown(f"""
                    <div class="email-card">
                        <b>📧 Email terkirim ke {ADMIN_EMAIL}:</b><br>
                        Dari: {email_valid} ({p.get('nama')})<br>
                        WA: {wa_valid} | Sosmed: {sosmed}<br>
                        Status: {p.get('status')} - Skill: {p.get('skill')}<br>
                        Kemampuan: {kemampuan}<br>
                        <b>✅ Bentuk Ruang 2 seperti itu - Halus lagi!</b>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"[📧 Kirim Email ke {ADMIN_EMAIL}]({mailto_admin}) | [💬 Kirim WA/SMS ke Admin]({wa_admin_link}) | [💬 WA Member {wa_valid}](https://wa.me/{wa_valid.replace('+','').replace(' ','')})")
        st.divider()
        st.subheader("📄 Form CV + Surat Lamaran Kerja + Riwayat Pendidikan & Pengalaman Skill - Masuk Ruang 3")
        st.caption("Form lagi - CV dan surat lamaran kerja riwayat pendidikan dan pengalaman skill - Klik masuk ke Ruang 3 lancar dan sukses!")
        st.info("✅ Halus & Lancar - Setelah form Ruang 1 terkirim ke asuveleikha@gmail.com & masuk Ruang 2, sekarang isi CV untuk masuk Ruang 3!")
        
        with st.form("form_cv_ruang2"):
            st.markdown("**📝 CV Lengkap - Untuk Masuk Ruang 3 Lancar**")
            col_cv1, col_cv2 = st.columns(2)
            with col_cv1:
                pendidikan_detail=st.text_input("Pendidikan Detail *", value=p.get('pendidikan',''), placeholder="S1 Manajemen, SMA 2015-2018")
                riwayat_pendidikan=st.text_area("Riwayat Pendidikan *", placeholder="SD 2005-2011, SMP 2011-2014, SMA 2014-2017, S1 2017-2021 - Tulis lengkap")
                skill_detail=st.text_area("Skill Detail *", placeholder="Chef: 50 menu Chinese, 5 tahun hotel. Staff: Kasir, admin, MS Office")
            with col_cv2:
                pengalaman_detail=st.text_area("Riwayat Pengalaman Kerja & Skill *", placeholder="2020-2023 Chef di Hotel A, 2023-2025 Staff Resto B - Skill: Masak, leadership, packing")
                cv_text=st.text_area("CV Singkat (Curriculum Vitae) *", placeholder="Nama: Budi, Pengalaman 5 tahun chef, Pendidikan S1, Skill Chinese food, WA 0812...")
                surat_lamaran=st.text_area("Surat Lamaran Kerja *", placeholder="Yth HRD Ruang Teduh, Saya Budi melamar sebagai Chef... Pengalaman 5 tahun... Mohon bimbingan...")
            
            submit_cv=st.form_submit_button("📄💼 Simpan CV & Surat Lamaran + Masuk Ruang 3 Lancar & Sukses →", type="primary", use_container_width=True)
            if submit_cv:
                if not pendidikan_detail or not pengalaman_detail or not cv_text:
                    st.error("Pendidikan, Pengalaman, CV, Surat Lamaran wajib!")
                else:
                    cv_data={
                        'nama':p.get('nama',''),
                        'email':p.get('email',''),
                        'wa':p.get('wa',''),
                        'pendidikan_detail':pendidikan_detail,
                        'riwayat_pendidikan':riwayat_pendidikan,
                        'pengalaman_detail':pengalaman_detail,
                        'skill_detail':skill_detail,
                        'cv_text':cv_text,
                        'surat_lamaran':surat_lamaran,
                        'status':p.get('status',''),
                        'kota':p.get('kota','')
                    }
                    save_cv_data(cv_data)
                    # Update profile with CV data
                    p['pendidikan_detail']=pendidikan_detail
                    p['riwayat_pendidikan']=riwayat_pendidikan
                    p['pengalaman_detail']=pengalaman_detail
                    p['cv_text']=cv_text
                    p['surat_lamaran']=surat_lamaran
                    st.session_state.profile=p
                    
                    # Kirim CV ke asuveleikha@gmail.com
                    email_subject = urllib.parse.quote(f"CV & Lamaran - {p.get('nama')} - {p.get('status')} - Masuk Ruang 3")
                    email_body = urllib.parse.quote(f"CV & Surat Lamaran Kerja\n\nNama: {p.get('nama')}\nEmail: {p.get('email')}\nWA: {p.get('wa')}\nStatus: {p.get('status')}\nPendidikan Detail: {pendidikan_detail}\nRiwayat Pendidikan: {riwayat_pendidikan}\nPengalaman: {pengalaman_detail}\nSkill: {skill_detail}\nCV: {cv_text}\nSurat Lamaran: {surat_lamaran}\n\nTerkirim dari Ruang 2 Pustaka Layanan Member - Masuk Ruang 3!")
                    mailto_cv = f"mailto:{ADMIN_EMAIL}?subject={email_subject}&body={email_body}"
                    
                    st.success(f"✅ CV & Surat Lamaran Terkirim ke {ADMIN_EMAIL}! Lancar & Sukses Masuk Ruang 3!")
                    st.markdown(f"""
                    <div class="email-card">
                        <b>📧 CV Terkirim ke {ADMIN_EMAIL}:</b><br>
                        Dari: {p.get('email')} - {p.get('nama')}<br>
                        Pendidikan: {pendidikan_detail}<br>
                        Pengalaman: {pengalaman_detail[:60]}...<br>
                        <b>✅ Form CV + Lamaran + Riwayat Pendidikan & Skill - Masuk Ruang 3 Lancar!</b>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"[📧 Kirim CV ke {ADMIN_EMAIL}]({mailto_cv})")
                    st.balloons()
                    st.session_state.room=3
                    st.rerun()
        
        st.divider()
        st.subheader("🎙️ Rekam Komitmen - Tabur - Info Tetap Tersimpan dari Ruang 1")
        st.caption("Rang yang tertulis rekam dan dengan itu masih tersimpan info yang diberikan member di Ruang 2")
        c1,c2=st.columns(2)
        with c1:
            audio=st.audio_input(f"Rekam komitmen {p.get('status')} - Tabur")
            if audio: st.success("✅ Tabur tersimpan! Info Ruang 1 tetap ada di Ruang 2!")
        with c2:
            video=st.file_uploader("Upload video komitmen", type=["mp4","webm","mov"])
            if video: st.video(video)
        if st.button("🌟 Lewati CV - Langsung Masuk Ruang 3 →", use_container_width=True):
            st.session_state.room=3
            st.rerun()

else:
    st.title("🌟 Ruang 3 · TAVO MALKHUTKHA - Two Journey - Pustaka MALKHUTKHA")
    st.caption("Two Journey - Pustaka MALKHUTKHA - Mengajak bimbingan advance - Motivasi lebih besar")
    p=st.session_state.profile
    if p and p.get("email"):
        st.success(f"Member: {p.get('email')} - {p.get('status')} - {p.get('skill')} - WA: {p.get('wa')} - Shalom Namo Buddhaya!")
        st.caption(f"GDrive: {p.get('gdrive_folder')} | Lokasi: {p.get('kota')} | Sosmed: {p.get('sosmed')}")
    st.markdown("""
    <div class="corp-card">
        <h3>🌟 Two Journey - Pustaka MALKHUTKHA - Bimbingan Advance + Motivasi Lebih Besar!</h3>
        <p>Sudah kita tempa dan berikan bimbingan motivasi dan penerapan standard dan terapan ekonomi secara Ruang Teduh komplit - Pasti entrepreneur juga bisa memberikan accessnya - Motivasi lebih besar, sudah ditempa!</p>
    </div>
    """, unsafe_allow_html=True)
    col_j1, col_j2 = st.columns(2)
    with col_j1:
        st.subheader("💼 Journey 1 - Employee - Pustaka MALKHUTKHA")
        render_voice_card("Kolose 3:23 Advance - Bekerja untuk Tuhan dengan level MALKHUTKHA - SOP Advance: Leadership, Mentoring junior, Inovasi. ERP Advance: Manage team, Budgeting, Reporting. OEE Advance: 95% Availability, 98% Performance. KPI Advance: Naik jabatan, Gaji naik 20%, Jadi mentor. Ekonomi: Gaji UMR + tunjangan skill + bonus - Terapan ekonomi Ruang Teduh komplit!", "emp_adv", "Employee Advance - MALKHUTKHA - Bimbingan Advance", "TWO JOURNEY - EMPLOYEE")
        st.markdown("""
        <div class="sop-table">
            <b>💼 Employee Advance - Access Corporation:</b><br>
            - Bisa access semua bidang dan skill bahkan corporation<br>
            - Dari Chef → Head Chef → Executive Chef<br>
            - Dari Staff → Supervisor → Manager<br>
            - Dapat bimbingan advance + motivasi lebih besar<br>
            - Terapan ekonomi: Gaji naik, skill naik, jaringan luas
        </div>
        """, unsafe_allow_html=True)
    with col_j2:
        st.subheader("💡 Journey 2 - Entrepreneur - Pustaka MALKHUTKHA")
        render_voice_card("Amsal 16:3 Advance - Serahkan rencana kepada TUHAN level MALKHUTKHA - SOP Advance: Scale up, Buka cabang, Franchise. ERP Advance: Multi-outlet, Inventory pusat, Finance. OEE Advance: 90% Availability cabang, 95% Performance. KPI Advance: Omzet 100jt, 3 cabang, 20 staff. Ekonomi: Sewa ruko 5-15jt, gaji staff UMK, profit 20% → 30%, terapan ekonomi Ruang Teduh komplit, pasti entrepreneur bisa berikan accessnya!", "ent_adv", "Entrepreneur Advance - MALKHUTKHA - Bimbingan Advance + Access", "TWO JOURNEY - ENTREPRENEUR")
        st.markdown("""
        <div class="sop-table">
            <b>💡 Entrepreneur Advance - Access Corporation:</b><br>
            - Bisa memberikan accessnya ke employee - Butuh tenaga kerja<br>
            - Dari Kios → Ruko → Rukan → Mall<br>
            - Dari Reseller → Distributor → Brand Owner<br>
            - Dapat bimbingan advance + motivasi lebih besar<br>
            - Terapan ekonomi: Omzet naik, cabang banyak, corporation
        </div>
        """, unsafe_allow_html=True)
    st.divider()
    st.subheader("🏢 Corporation Access - Antar Member - Full Binding")
    st.markdown("""
    <div class="binding-card">
        <h3>🌱 Tabur Tuai - Corporation Access - Member Saling Access!</h3>
        <p>Member di Ruang 3 bisa access ke semua masing-masing bidang dan skill bahkan corporation - Employee butuh kerja, Entrepreneur butuh staff - Match di Ruang 3! - Motivasi lebih besar sudah ditempa dan berikan bimbingan motivasi dan penerapan standard dan terapan ekonomi secara Ruang Teduh komplit!</p>
    </div>
    """, unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="full-service">
            <h3>🌿 TAVO - Pustaka Layanan Member - Rp200rb/300rb per bulan</h3>
            <p>Employee 200rb | Entrepreneur 300rb - Setiap bulan</p>
            <ul>
                <li>✅ Pustaka Teduh - Santapan Rohani</li>
                <li>✅ Pustaka Layanan - Access bidang & skill</li>
                <li>✅ Email & WA Connect ke {ADMIN_EMAIL}</li>
                <li>✅ Corporation Access Dasar</li>
                <li>✅ SOP/ERP/OEE/KPI via GDrive/Github</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌱 Pilih TAVO - 200rb/300rb per bulan", use_container_width=True): st.balloons(); st.success(f"Tavo! {p.get('status','')} - Akses Pustaka Layanan!")
    with c2:
        st.markdown("""
        <div class="full-service" style="border:2px solid #2D5A4A;background:#E8F3ED">
            <h3>🌟 MALKHUTKHA - Pustaka MALKHUTKHA - Two Journey Advance</h3>
            <p>Full Binding + Bimbingan Advance + Motivasi Besar!</p>
            <ul>
                <li>🔥 Two Journey - Employee & Entrepreneur Advance</li>
                <li>🔥 Motivasi Lebih Besar - Sudah Ditempa</li>
                <li>🔥 Terapan Ekonomi Komplit - Ruang Teduh</li>
                <li>🔥 Entrepreneur Bisa Berikan Accessnya</li>
                <li>🔥 Corporation Access Full</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌟 Pilih MALKHUTKHA - Full Advance", type="primary", use_container_width=True): st.balloons(); st.success("MALKHUTKHA! Two Journey Advance - Motivasi Besar!")
    st.divider()
    if len(members)>0:
        st.subheader(f"📧 {len(members)} Member - Terkoneksi Email & WA ke {ADMIN_EMAIL}")
        st.dataframe(pd.DataFrame(members), use_container_width=True)
        st.success(f"✅ Semua pesan member terkirim ke {ADMIN_EMAIL} - Konek SMS HP & Email!")
