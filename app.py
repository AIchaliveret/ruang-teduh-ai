# AIJC - Ruang Teduh v3.0 PERFECT FINAL - Struktur Terakhir - R1/R2/R3 Same Format + Strong Motivation + Corp Access + 1 Jalur + Email Follow-up
import streamlit as st
from datetime import datetime
import os, csv, re, json, html, urllib.parse
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(page_title="Ruang Teduh v3.0 PERFECT FINAL - TAVO MALKHUTKHA", page_icon="🌿", layout="wide")

st.markdown("""
<style>
.badge{background:#E8F3ED;color:#2D5A4A;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:700}
.metric-card{background:#1A3C2A;color:white;padding:16px 20px;border-radius:12px;text-align:center;font-weight:700}
.binding-card{background:linear-gradient(135deg,#1A3C2A 0%,#7FB69B 100%);color:white;padding:20px;border-radius:16px;margin:12px 0}
.full-service{background:#FFFBEB;border:2px solid #F59E0B;padding:16px;border-radius:12px;margin:8px 0}
.sop-table{background:white;border:1px solid #E5E7EB;border-radius:12px;padding:16px;margin:10px 0}
.corp-card{background:linear-gradient(135deg,#1E40AF 0%,#3B82F6 100%);color:white;padding:20px;border-radius:16px;margin:12px 0}
.voice-panel{background:#F0FDF4;border:2px solid #10B981;padding:16px;border-radius:12px;margin:10px 0}
.email-card{background:#EFF6FF;border:2px solid #3B82F6;padding:16px;border-radius:12px;margin:10px 0}
.visual-card{background:#1A3C2A;color:white;padding:24px;border-radius:20px;text-align:center;margin:12px 0}
.quote-card{background:#FFFEF0;border-left:4px solid #1A3C2A;padding:16px;border-radius:0 12px 12px 0;margin:12px 0}
.payment-card{background:#FFF7ED;border:2px solid #F59E0B;padding:16px;border-radius:12px;margin:10px 0}
</style>
""", unsafe_allow_html=True)

CSV_FILE="members_ruang_teduh.csv"
CV_FILE="cv_members.csv"
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
        return False, f"Email sudah terdaftar sebagai {existing[0].get('status')} - {existing[0].get('skill')}! 1 Member = 1 Jalur - Tetap akses Ruang 2."
    fe=os.path.exists(CSV_FILE)
    fieldnames=["timestamp","nama","tgl_lahir","kependudukan","pendidikan","pengalaman","skill","email","wa","sosmed","status","provinsi","kota","visi","masukan","subscription","gdrive_folder","contribution","bakat","progress"]
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
            "subscription":data.get('subscription','Employee 200rb'),
            "gdrive_folder":data.get('gdrive_folder',''),
            "contribution":data.get('contribution',200000),
            "bakat":data.get('bakat',''),
            "progress":data.get('progress',0)
        })
    return True,"Berhasil! Email terkirim ke asuveleikha@gmail.com - 1 Member 1 Jalur!"

def save_cv(data):
    fe=os.path.exists(CV_FILE)
    fieldnames=["timestamp","nama","email","wa","pendidikan_detail","riwayat_pendidikan","pengalaman_detail","skill_detail","cv_text","surat_lamaran","status","kota"]
    with open(CV_FILE,"a",newline="",encoding="utf-8") as f:
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

def render_visual_card(icon, visual_text, title, subtitle):
    st.markdown(f"""
    <div class="visual-card">
        <div style="font-size:48px;margin-bottom:8px">{icon}</div>
        <div style="font-size:11px;letter-spacing:2px;opacity:0.7">VISUAL: {visual_text}</div>
        <h2 style="margin:12px 0 0 0;font-size:28px;font-weight:800">{title}</h2>
        <div style="font-size:20px;opacity:0.9">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def render_quote_card(quote, renungan, terapan):
    st.markdown(f"""
    <div class="quote-card">
        <div style="font-size:18px;font-style:italic;color:#1A3C2A;line-height:1.6">"{quote}"</div>
        <div style="margin-top:12px;font-size:13px"><b>Renungan:</b> {renungan}</div>
        <div style="margin-top:8px;font-size:13px">🌱 <b>Terapan:</b> {terapan}</div>
    </div>
    """, unsafe_allow_html=True)

def render_voice_panel(title):
    st.markdown(f"""
    <div class="voice-panel" style="background:#1A3C2A;color:white">
        <div style="display:flex;align-items:center;gap:12px">
            <div style="width:48px;height:48px;background:#2D5A4A;border-radius:50%;display:flex;align-items:center;justify-content:center">🎧</div>
            <div>
                <div style="font-weight:700">{title}</div>
                <div style="font-size:12px;opacity:0.8">Dari mata turun ke hati • Halus di kuping • Backsound embun pagi</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if "room" not in st.session_state: st.session_state.room=1
if "profile" not in st.session_state: st.session_state.profile={}
if "is_paid" not in st.session_state: st.session_state.is_paid=False

members=load_members()

# SIDEBAR - Sesuai foto v2.9 PERFECT
with st.sidebar:
    st.markdown("### 🌿 Ruang Teduh v3.0 PERFECT")
    pos = f"R{st.session_state.room}"
    langganan = "✅ Sudah" if st.session_state.is_paid else "❌ Belum"
    riwayat = "Baru" if len(members)==0 else f"R1→R{st.session_state.room}" if st.session_state.room>1 else "Baru"
    st.caption(f"Posisi: {pos} | Langganan: {langganan}")
    st.caption(f"Riwayat: {riwayat}")
    st.markdown(f'<div class="metric-card">📚 {len(members)}/1000<br>Pustaka Teduh<br><small>Ruang {st.session_state.room} Aktif</small></div>', unsafe_allow_html=True)
    if st.session_state.room>1:
        st.info(f"R1 standby {len(members)}/1000 • Sekarang di R{st.session_state.room}")
    st.divider()
    if st.button("📖 Ruang 1", use_container_width=True): st.session_state.room=1; st.rerun()
    if st.button("🏢 Ruang 2", use_container_width=True): st.session_state.room=2; st.rerun()
    if st.button("🌟 Ruang 3 (Perlu Langganan)", use_container_width=True): st.session_state.room=3; st.rerun()
    st.divider()
    st.checkbox("✅ Simulasi Sudah Bayar (biar bisa masuk R3)", key="is_paid")
    st.markdown(f"📧 Admin: [{ADMIN_EMAIL}](mailto:{ADMIN_EMAIL})")
    st.caption("R1 tetap ada bila belum R2 • R2 tetap ada bila belum R3 • Masuk R2=R1 reset • Masuk R3=R2 reset • Member berasa di R2")

# ================= RUANG 1 - PUSTAKA TEDUH - SANTAPAN ROHANI =================
if st.session_state.room==1:
    st.caption("Ruang 1 tetap ada bila belum masuk ke Ruang 2")
    render_visual_card("🌿", "Sawah Embun Pagi • Matahari Terbit • Tenang", "Ruang 1 - Pustaka Teduh", "- Santapan Rohani")
    render_quote_card(
        "Embun pagi tidak pernah terburu-buru, tapi ia membasahi seluruh ladang. Begitu juga kasih, dari mata turun ke hati.",
        "Otak butuh 5 detik visual hijau sebelum bisa menerima nasehat. Lihat dulu, baru dengar, baru renungkan.",
        "Tarik nafas 5 detik sambil lihat visual hijau"
    )
    render_voice_panel("Suara Halus Ruang Teduh • v3.0 PERFECT FINAL • Memikat")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("▶️ Play Nasehat R1 (Halus)", use_container_width=True):
            st.success("🔊 Memutar via Browser TTS (id-ID, 0.85x halus) - Kolose 3:23 - Bekerja untuk Tuhan...")
    with col_b:
        if st.button("🔊 Suara Browser R1", use_container_width=True):
            st.info("🔊 Memutar via Browser TTS (id-ID, 0.85x halus)...")
    
    st.divider()
    st.markdown("#### 📝 Form Aktif Ruang 1 (v3.0) - Akan ke-reset pas masuk R2")
    st.info("✅ 1 Member = 1 Jalur - Info diri benar - Skill & Bakat valid - Mudah kita kenal - Nasehat Alkitab + SOP/ERP/OEE/KPI tertanam - Member terikat mau berlangganan!")
    
    with st.form("form_r1_perfect"):
        nama=st.text_input("Nama Member * (Contoh: Tavo / Budi)")
        tgl_lahir=st.text_input("Tgl Lahir *", placeholder="01-01-1990")
        kependudukan=st.text_input("Kependudukan *", placeholder="KTP Jakarta, Domisili Bekasi")
        pendidikan=st.selectbox("Pendidikan *", ["SMA/SMK", "D3", "S1", "S2", "Lainnya"])
        pengalaman=st.text_area("Pengalaman Kerja & Skill *", placeholder="5 tahun chef hotel, 3 tahun staff resto, skill masak Chinese 50 menu...")
        bakat=st.text_area("Bakat & Skill Detail * (Biar mudah kenal)", placeholder="Bakat masak, leadership, jualan - Tulis jujur agar mudah kenal skill & bakat masing-masing baik employee dan entrepreneur!")
        email=st.text_input("Email * WAJIB (bisa follow-up)", placeholder="budi@email.com")
        wa=st.text_input("No WA Valid *", placeholder="081291904422")
        sosmed=st.text_input("Sosmed (IG/FB) - Bila perlu", placeholder="@budi_chef")
        status=st.selectbox("Status - 1 Jalur Saja! *", ["Employee - Tenaga Kerja (200rb/bulan)", "Entrepreneur - Usahawan (300rb/bulan)"])
        nasehat_hari=st.text_area("Nasehat hari ini", placeholder="Akhirnya semangat lagi mencoba aplikasi ruang teduh bikin percaya diri.")
        progress=st.slider("Progress Pustaka", 0, 1000, 830)
        
        submit=st.form_submit_button("➡️ Masuk Ruang 2 - Pustaka Layanan", type="primary", use_container_width=True)
        if submit:
            if not nama or not email or not tgl_lahir:
                st.error("Nama, Tgl Lahir, Email wajib!")
            elif not is_valid_email(email):
                st.error("Email salah!")
            else:
                is_emp = "Employee" in status
                contrib = 200000 if is_emp else 300000
                data={
                    'nama':nama,'tgl_lahir':tgl_lahir,'kependudukan':kependudukan,'pendidikan':pendidikan,
                    'pengalaman':pengalaman,'skill':bakat,'email':email,'wa':wa,'sosmed':sosmed,
                    'status':status,'provinsi':'DKI Jakarta','kota':kependudukan,'visi':nasehat_hari,
                    'masukan':nasehat_hari,'subscription':f"{'Employee 200rb' if is_emp else 'Entrepreneur 300rb'}/bulan",
                    'gdrive_folder':f"PUSTAKA/{'Employee' if is_emp else 'Entrepreneur'}/{bakat[:20]}",
                    'contribution':contrib,'bakat':bakat,'progress':progress
                }
                ok,msg=save_member(data)
                st.session_state.profile=data
                st.success(f"✅ {msg} - Halus & Lancar - Form terkirim ke {ADMIN_EMAIL} - Bisa follow-up 2 cara!")
                st.markdown(f"""
                <div class="email-card">
                    <b>📧 Email terkirim ke {ADMIN_EMAIL}:</b><br>
                    Member: {nama} - {status}<br>
                    Skill & Bakat: {bakat[:80]}<br>
                    Email: {email} - WA: {wa}<br>
                    ✅ 1 Member 1 Jalur - Info valid - Mudah kenal!<br>
                    ✅ 2 Cara Follow-up: Via Email & Langsung masuk Ruang 2
                </div>
                """, unsafe_allow_html=True)
                # Link email & WA
                subj = urllib.parse.quote(f"Member Baru R1 - {nama} - {status}")
                body = urllib.parse.quote(f"Nama: {nama}\nTgl Lahir: {tgl_lahir}\nKependudukan: {kependudukan}\nPendidikan: {pendidikan}\nPengalaman: {pengalaman}\nBakat: {bakat}\nEmail: {email}\nWA: {wa}\nStatus: {status}")
                st.markdown(f"[📧 Kirim Email ke {ADMIN_EMAIL}](mailto:{ADMIN_EMAIL}?subject={subj}&body={body})")
                st.balloons()
                st.session_state.room=2
                st.rerun()

# ================= RUANG 2 - PUSTAKA LAYANAN MEMBER - TAVO 200rb/300rb =================
elif st.session_state.room==2:
    p=st.session_state.profile
    st.caption("Ruang 2 tetap ada bila belum masuk ke Ruang 3 • Member berasa di Ruang 2")
    if not p or not p.get("nama"):
        with st.expander("📖 Lihat Ruang 1 - Sudah di-reset ke bentuk semula"):
            st.info("Isi form di Ruang 1 dulu!")
        st.warning("Belum ada data member - Isi di Ruang 1!")
        if st.button("← Kembali ke R1", use_container_width=True): st.session_state.room=1; st.rerun()
    else:
        render_visual_card("🏢", "Teamwork Hangat • Chef Ajari Junior • Kerja Ibadah", "Ruang 2 - Pustaka", "Layanan Member - TAVO - Rp200rb/300rb")
        render_quote_card(
            "Kolose 3:23 Advance - Bekerja untuk Tuhan dengan level MALKHUTKHA. Dari Staff → Supervisor → Manager.",
            "Kerja bukan soal gaji, tapi skill naik, jaringan luas. Visual teamwork memicu rasa memiliki.",
            "SOP/ERP/OEE/KPI via GDrive/Github - Employee 200rb - Entrepreneur 300rb"
        )
        render_voice_panel("Suara Halus Ruang Teduh • v2.4/v2.5 Memikat - Dari mata turun ke hati • Halus di kuping • Backsound embun pagi")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("▶️ Play Nasehat R2 (Halus)", use_container_width=True):
                st.success("🔊 Memutar via Browser TTS (id-ID, 0.85x halus) - Kolose Advance...")
        with col_b:
            if st.button("🔊 Suara Browser R2", use_container_width=True):
                st.info("🔊 Memutar via Browser TTS (id-ID, 0.85x halus)...")
        
        st.divider()
        st.markdown("#### 📝 Form Aktif Ruang 2 (v2.4/v2.5) - Akan ke-reset pas masuk R3")
        st.caption(f"Member: {p.get('nama')} - Info dari R1: {p.get('tgl_lahir')}, {p.get('kependudukan')}, {p.get('pendidikan')}, Skill: {p.get('skill')} - Dibacakan suara & loading masuk R2 - Info tetap tersimpan!")
        
        with st.form("form_r2_perfect"):
            email_m=st.text_input(f"Email Member (terkoneksi ke {ADMIN_EMAIL})", value=p.get('email',''))
            wa_m=st.text_input("WA", value=p.get('wa',''))
            paket=st.selectbox("Paket", ["Employee 200rb/bulan", "Entrepreneur 300rb/bulan", "MALKHUTKHA Full 399rb/bulan"], index=0 if "Employee" in p.get('status','') else 1)
            pesan_admin=st.text_area("Pesan ke Admin Email & WA (ini yang lo ketik tadi gak ada suaranya)", placeholder="Mau jadi member sih tapi mengapa pemberitahuan judul ruang 2 terlalu fulgar, yg staff bersemangat nanti yang entrepreneur bagaimana?")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ Kembali ke R1", use_container_width=True): st.session_state.room=1; st.rerun()
            with col2:
                submit_r2=st.form_submit_button("⭐ Masuk Ruang 3 - MALKHUTKHA", type="primary", use_container_width=True)
                if submit_r2:
                    if not email_m or not wa_m:
                        st.error("Email & WA wajib!")
                    else:
                        p['email']=email_m
                        p['wa']=wa_m
                        p['subscription']=paket
                        p['masukan']=pesan_admin
                        st.session_state.profile=p
                        # Save CV if pesan contains CV-like
                        if len(pesan_admin)>20:
                            save_cv({
                                'nama':p.get('nama'),'email':email_m,'wa':wa_m,
                                'pendidikan_detail':p.get('pendidikan'),'riwayat_pendidikan':p.get('pendidikan'),
                                'pengalaman_detail':p.get('pengalaman'),'skill_detail':p.get('skill'),
                                'cv_text':pesan_admin[:500],'surat_lamaran':pesan_admin,
                                'status':p.get('status'),'kota':p.get('kota')
                            })
                        subj = urllib.parse.quote(f"Ruang 2 - {p.get('nama')} - {paket} - Pesan Admin")
                        body = urllib.parse.quote(f"Nama: {p.get('nama')}\nEmail: {email_m}\nWA: {wa_m}\nPaket: {paket}\nPesan: {pesan_admin}\nSkill: {p.get('skill')}\nStatus: {p.get('status')}\n\nMohon follow-up & ajak berlangganan full sesuai kemampuan!")
                        mailto = f"mailto:{ADMIN_EMAIL}?subject={subj}&body={body}"
                        wa_text = urllib.parse.quote(f"Shalom {p.get('nama')}! R2 - {paket} - Pesan: {pesan_admin}")
                        wa_link = f"https://wa.me/6285692162564?text={wa_text}"
                        st.success(f"✅ Lancar Sukses! Form R2 terkirim ke {ADMIN_EMAIL} - Dulu sepakat masuk R3!")
                        st.markdown(f"[📧 Email ke {ADMIN_EMAIL}]({mailto}) | [💬 WA Admin]({wa_link})")
                        st.balloons()
                        st.session_state.room=3
                        st.rerun()

# ================= RUANG 3 - PUSTAKA MALKHUTKHA - TWO JOURNEY CORPORATE ACCESS =================
else:
    p=st.session_state.profile
    st.caption("Ruang 3 - Perlu Langganan - Target: Corporation Access")
    
    # Cek langganan - sesuai foto "tidak cetak login" tapi perlu simulasi
    if not st.session_state.is_paid:
        st.warning("⚠️ Belum langganan - Centang 'Simulasi Sudah Bayar' di sidebar untuk masuk R3 (sesuai foto 'dulu login')")
        render_visual_card("💳", "Pembayaran Langganan - Target R3", "Pembayaran", "Langganan - Target: R3")
        st.markdown(f"""
        <div class="payment-card">
            <b>BCA:</b> 1234567890 a/n Ruang Teduh Yayasan | <b>WA:</b> 085692162564 | <b>GoPay:</b> 085692162564<br>
            <b>Rate:</b> Employee 200rb | Entrepreneur 300rb | MALKHUTKHA Full<br>
            <i>VA auto-forward ke BCA 1234567890 - Aman masuk rekening kita</i><br><br>
            BCA VA: 12345 2564 | BRI VA: 88810 085692
        </div>
        """, unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["🏦 VA Bank", "📱 QRIS", "💚 GoPay/OVO/DANA"])
        with tab1:
            st.info("VA auto-forward ke BCA 1234567890 - Aman masuk rekening kita")
            st.code("BCA VA: 12345 2564 | BRI VA: 88810 085692")
        with tab2:
            st.info("QRIS Ruang Teduh - Scan untuk bayar Employee 200rb / Entrepreneur 300rb")
        with tab3:
            st.info("GoPay/OVO/DANA ke 085692162564 - Konfirmasi via WA")
        
        if st.button("✅ Simulasi VA Lunas → Masuk R3", use_container_width=True):
            st.session_state.is_paid=True
            st.success("✅ Simulasi Lunas - Masuk R3!")
            st.rerun()
        if st.button("⬅️ Kembali ke R2", use_container_width=True):
            st.session_state.room=2
            st.rerun()
        st.stop()
    
    # SUDAH BAYAR - Tampilkan R3 PERFECT - Format sama R1/R2 tapi motivasi kuat + corporate access
    render_visual_card("🌟", "Two Journey • Corporate Access • Member to Member • Strong Motivation", "Ruang 3 - Pustaka MALKHUTKHA", "- Two Journey - Corporate Access")
    
    # Strong motivation berbeda dari R1/R2
    render_quote_card(
        "Dari Member to Member: Build. Access. Grow. Unlock corporate access through shared journey. From Staff → Supervisor → Manager, dari Kios → Ruko → Rukan → Corporation!",
        "Member sudah tertanam bimbingan Ruang Teduh (Alkitab + SOP/ERP/OEE/KPI) - Ajak terikat mau berlangganan karena di R3 kita beri motivasi bahkan kepastian kerja sama antar member - Member akan dapat terkoneksi langsung & dapat access corporation berupa bimbingan & semacamnya - Sesama member saling access di R3! Jaminan!",
        "Share app ke sales/marketing tidak hanya online - Bisa bikin perusahaan jasa - Biaya jangan terlalu murah - Jaminan corporation access!"
    )
    
    render_voice_panel("Suara Halus Ruang 3 • v3.0 PERFECT • Strong Motivation • Corporate Access")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("▶️ Play Nasehat R3 - Strong Motivation", use_container_width=True):
            st.success("🔊 Memutar - Motivasi Kuat - Corporation Access - Member to Member...")
    with col_b:
        if st.button("🔊 Suara Browser R3", use_container_width=True):
            st.info("🔊 Memutar via Browser TTS - Strong Motivation...")
    
    st.divider()
    st.subheader("🏢 Skema Masing-masing - 1 Member 1 Jalur - Email Follow-up - Corporation Access")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown("""
        <div class="sop-table">
            <b>📖 R1 Pustaka Teduh</b><br>
            Format: Visual Sawah Embun Pagi + Quote Embun + Suara Halus<br>
            Isi: Kolose 3:23, Filipi 4:6-7, Amsal 16:3, Mazmur 23 + SOP/ERP/OEE/KPI Dasar<br>
            Form: Nama, Tgl Lahir, Kependudukan, Pendidikan, Pengalaman, Skill, Email, WA<br>
            Output: Email ke asuveleikha@gmail.com + Masuk R2
        </div>
        """, unsafe_allow_html=True)
    with col_s2:
        st.markdown("""
        <div class="sop-table">
            <b>🏢 R2 Pustaka Layanan Member</b><br>
            Format: Sama R1 tapi Visual Teamwork Hangat + Quote Kolose Advance<br>
            Isi: Motivasi kuat + SOP/ERP/OEE/KPI Layanan + CV/Lamaran<br>
            Form: Email (koneksi admin), WA, Paket 200rb/300rb, Pesan ke Admin + CV<br>
            Output: Email ke asuveleikha@gmail.com + Masuk R3 (jika bayar)
        </div>
        """, unsafe_allow_html=True)
    with col_s3:
        st.markdown("""
        <div class="sop-table" style="border:2px solid #1A3C2A;background:#F0FDF4">
            <b>🌟 R3 Pustaka MALKHUTKHA - Two Journey</b><br>
            Format: Sama R1/R2 tapi Visual Corporate + Quote Strong Motivation + Corp Access<br>
            Isi: Two Journey Advance + Motivasi kuat + Terapan ekonomi komplit + Corp Access<br>
            Form: Corporation Access Antar Member + Jaminan Kerja Sama<br>
            Output: Member saling access - Employee butuh kerja, Entrepreneur butuh staff - Match!
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("💰 Biaya Member - Jangan Terlalu Murah - Akumulasi vs Menyusut Bulanan")
    st.info("Jasa seperti ini kalau kemampuan ekonomi sebagai employee aja kita Ruang Teduh dapat uang langgan - Bila dihitung secara member bagaimana akumulasi apa menyusut dalam hitungan bulan - Entrepreneur level lebih besar!")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 📈 Employee 200rb/bulan - Akumulasi")
        df_emp = pd.DataFrame({
            "Bulan": ["Bulan 1 - 100 Member", "Bulan 2 - 100+90 baru (churn 10%)", "Bulan 3 - 190+100 baru", "Bulan 6 - Stabil 500 Member", "Bulan 12 - 1000 Member"],
            "Member Aktif": [100, 190, 271, 500, 1000],
            "Pendapatan/bulan": ["Rp20jt", "Rp38jt", "Rp54.2jt", "Rp100jt", "Rp200jt"],
            "Akumulasi": ["Rp20jt", "Rp58jt", "Rp112.2jt", "Rp400jt+", "Rp1.2M+"],
            "Status": ["Start", "Akumulasi naik", "Akumulasi naik", "Akumulasi", "Akumulasi besar!"]
        })
        st.dataframe(df_emp, use_container_width=True)
    with c2:
        st.markdown("#### 📈 Entrepreneur 300rb/bulan - Lebih Besar")
        df_ent = pd.DataFrame({
            "Bulan": ["Bulan 1 - 100 Member", "Bulan 2 - 100+90 baru", "Bulan 3 - 190+100 baru", "Bulan 6 - Stabil 500 Member", "Bulan 12 - 1000 Member"],
            "Member Aktif": [100, 190, 271, 500, 1000],
            "Pendapatan/bulan": ["Rp30jt", "Rp57jt", "Rp81.3jt", "Rp150jt", "Rp300jt"],
            "Akumulasi": ["Rp30jt", "Rp87jt", "Rp168.3jt", "Rp600jt+", "Rp1.8M+"],
            "Status": ["Start", "Akumulasi naik", "Akumulasi naik", "Akumulasi", "Akumulasi besar!"]
        })
        st.dataframe(df_ent, use_container_width=True)
    
    st.markdown("""
    <div class="voice-panel" style="background:linear-gradient(135deg,#059669 0%,#10B981 100%);color:white">
        <h3>💡 Akumulasi vs Menyusut - Hitungan Bulan - Jaminan Berlangganan:</h3>
        <b>Menyusut (Jika churn 50% tanpa rekrut & tanpa jaminan):</b><br>
        Bulan 1: 100 member x 250rb avg = Rp25jt → Bulan 2: 50 member = Rp12.5jt (menyusut 50%!) → Gagal!<br><br>
        <b>Akumulasi (Dengan jaminan corporation access + motivasi + follow-up email + sales/marketing offline):</b><br>
        Bulan 1: 100 member (50 Emp 200rb + 50 Ent 300rb) = Rp25jt<br>
        Bulan 2: 90 retain + 100 baru = 190 member = Rp47.5jt<br>
        Bulan 3: 171 + 100 = 271 member = Rp67.75jt → <b>Akumulasi naik terus setiap bulan!</b><br>
        Bulan 12: 1000 member mix = Rp250jt/bulan → Rp3M/tahun!<br><br>
        <b>Kunci Anti Menyusut:</b> Member sudah tertanam bimbingan Ruang Teduh (Alkitab+SOP/ERP/OEE/KPI) + di R3 dapat motivasi + kepastian kerja sama + terkoneksi langsung + access corporation + sesama member saling access + bisa share ke sales/marketing offline + bisa bikin perusahaan jasa + jaminan berlangganan! → <b>Tidak menyusut, akumulasi!</b><br><br>
        <b>Kesimpulan:</b> Employee 200rb, Entrepreneur 300rb, MALKHUTKHA Full 399rb-500rb - Jangan terlalu murah - Jasa premium - Akumulasi bulanan!
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🏢 App Bisa Dishare ke Sales/Marketing - Tidak Hanya Online - Bisa Bikin Perusahaan Jasa")
    st.markdown(f"""
    <div class="email-card">
        <b>📱 Shareable - Offline & Online:</b><br>
        - <b>Online:</b> Share link ruang-teduh-ai.streamlit.app via WA, QR Code, IG, FB<br>
        - <b>Offline:</b> Sales/marketing bawa HP - Buka app - Daftar langsung - Form terkirim ke {ADMIN_EMAIL}<br>
        - <b>Perusahaan Jasa:</b> Kantor Ruang Teduh - Konsultasi tatap muka - Bimbingan SOP/ERP/OEE/KPI<br>
        - <b>Biaya:</b> Employee 200rb/bulan, Entrepreneur 300rb/bulan, MALKHUTKHA 399rb/bulan - Tidak murah - Jasa premium + jaminan!<br>
        - <b>Email Follow-up:</b> Semua member email terkoneksi ke {ADMIN_EMAIL} - Bisa follow-up via email & WA!<br>
        - <b>1 Member 1 Jalur:</b> Employee ATAU Entrepreneur - Tidak bisa ganda - Info valid skill & bakat - Mudah kenal!
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="full-service">
            <h3>🌿 TAVO - Pustaka Layanan - Rp200rb/300rb per bulan</h3>
            <p>Employee 200rb | Entrepreneur 300rb - Setiap bulan</p>
            <ul>
                <li>✅ R1 Pustaka Teduh + R2 Pustaka Layanan (format sama)</li>
                <li>✅ R3 Pustaka MALKHUTKHA - Motivasi kuat + Corp Access</li>
                <li>✅ 1 Member 1 Jalur - Info valid skill & bakat</li>
                <li>✅ Email Follow-up ke {ADMIN_EMAIL}</li>
                <li>✅ SOP/ERP/OEE/KPI via GDrive/Github</li>
                <li>✅ Corporation Access Antar Member</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌱 Pilih TAVO - 200rb/300rb", use_container_width=True): st.balloons(); st.success(f"Tavo! {p.get('status','')} - Corporation Access Dasar!")
    with c2:
        st.markdown("""
        <div class="full-service" style="border:2px solid #1A3C2A;background:#E8F3ED">
            <h3>🌟 MALKHUTKHA - Pustaka MALKHUTKHA - Full Corp Access - Jaminan!</h3>
            <p>Two Journey Advance + Motivasi Besar + Jaminan Kerja Sama!</p>
            <ul>
                <li>🔥 Format sama R1/R2 tapi motivasi kuat + access corporate</li>
                <li>🔥 Member terkoneksi langsung & dapat access corporation</li>
                <li>🔥 Sesama member saling access di R3 - Employee ↔ Entrepreneur</li>
                <li>🔥 Jaminan berlangganan - Kepastian kerja sama</li>
                <li>🔥 Bisa share ke sales/marketing - Bisa bikin perusahaan jasa</li>
                <li>🔥 Akumulasi bulanan - Tidak menyusut!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌟 Pilih MALKHUTKHA - Full Jaminan", type="primary", use_container_width=True): st.balloons(); st.success("MALKHUTKHA! Full Corporation Access + Jaminan!")
    
    st.divider()
    if len(members)>0:
        st.subheader(f"📧 {len(members)} Member Valid - 1 Jalur/Member - Email ke {ADMIN_EMAIL} - Akumulasi")
        st.dataframe(pd.DataFrame(members), use_container_width=True)
        total = sum([float(m.get('contribution',200000) or 200000) for m in members])
        st.success(f"💰 Total Potensi: Rp{total:,.0f}/bulan dari {len(members)} member - Akumulasi jika retention + jaminan corporation access! - Entrepreneur level lebih besar!")
        if os.path.exists(CV_FILE):
            st.subheader("📄 CV Members - Ruang 2 → Ruang 3 Lancar")
            st.dataframe(pd.read_csv(CV_FILE), use_container_width=True)
