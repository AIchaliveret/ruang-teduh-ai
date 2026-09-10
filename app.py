"""
RUANG TEDUH V6.16 FINAL - 523+ LINES - FINAL CV KOMPLIT + GRAFIK DI PUTIH AJA + KUNING STORAGE ROLLING 7 HARI
================================================================================
FINAL SESUAI PERMINTAAN BRO - GAS LANGSUNG EDIT - ISTIRAHAT JAM 4 LANJUT INFRAMERAH LABLAB.AI KOMPETISI:
- Lembar 2 Merah Employee: Tambahkan kolom isi pengalaman dan isi alamat email whatsapp pendaftar pengguna web dan app - CV komplit
- Lembar 3 Hijau Entrepreneur: Tambahkan CV komplit seperti lembar 2 merah lengkapi dengan alamat email whatsapp pendaftar pengguna web dan app - CV komplit mirror merah
- Lembar 4 Kuning: Sebagai storage ruang teduh nasehat mingguan kita akan edit setiap minggu dan nasehat rolling setiap harinya - Final - Storage library aja tanpa grafik
- Grafik: Hanya di lembar 1 putih pendaftaran - 1 aja - Hemat kuota & tenaga clerical
- CV: Nama + Tempat Lahir + Tgl Lahir + Pendidikan + Pengalaman Kerja + Skill (di bawah pengalaman) + Alamat Email + Nomor Whatsapp = CV → asuveleikha@gmail.com
- 523+ Lines, Nett 67K/90, Gratis Tidak Berbayar, No Pricing 95K/145K, Voice All
================================================================================
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import date, datetime
import json
import os
import urllib.parse

st.set_page_config(page_title="Ruang Teduh V6.16 FINAL - CV Komplit + Grafik di Putih + Kuning Storage Rolling", page_icon="📗", layout="wide", initial_sidebar_state="collapsed")

# SESSION - FINAL
if "member_data" not in st.session_state:
    st.session_state.member_data = {}
if "bursa_total" not in st.session_state:
    st.session_state.bursa_total = 12
if "bursa_aktif" not in st.session_state:
    st.session_state.bursa_aktif = 8
if "bursa_kerja" not in st.session_state:
    st.session_state.bursa_kerja = 4
if "bursa_hist" not in st.session_state:
    st.session_state.bursa_hist = [
        {"jam": "08:00", "vote": 2, "kerja": 0, "total": 2},
        {"jam": "09:00", "vote": 5, "kerja": 1, "total": 6},
        {"jam": "10:00", "vote": 8, "kerja": 2, "total": 10},
        {"jam": "11:00", "vote": 8, "kerja": 4, "total": 12},
    ]
if "bursa_log" not in st.session_state:
    st.session_state.bursa_log = []
if "jujur" not in st.session_state:
    st.session_state.jujur = False

def add_login_bursa():
    st.session_state.bursa_total += 1
    st.session_state.bursa_aktif += 1
    now = datetime.now().strftime("%H:%M")
    st.session_state.bursa_hist.append({"jam": now, "vote": st.session_state.bursa_aktif, "kerja": st.session_state.bursa_kerja, "total": st.session_state.bursa_total})
    if len(st.session_state.bursa_hist) > 12:
        st.session_state.bursa_hist = st.session_state.bursa_hist[-12:]

def kurang_bursa_share(email, alasan="share email"):
    if st.session_state.bursa_aktif > 0:
        st.session_state.bursa_aktif -= 1
        st.session_state.bursa_kerja += 1
        now = datetime.now().strftime("%H:%M")
        st.session_state.bursa_hist.append({"jam": now, "vote": st.session_state.bursa_aktif, "kerja": st.session_state.bursa_kerja, "total": st.session_state.bursa_total})
        st.session_state.bursa_log.append({"waktu": now, "ke": email, "oleh": st.session_state.member_data.get("nama","-"), "alasan": alasan})
        if len(st.session_state.bursa_hist) > 12:
            st.session_state.bursa_hist = st.session_state.bursa_hist[-12:]

def kurang_bursa_jujur(email, alasan="kejujuran"):
    kurang_bursa_share(email, alasan)

def load_nasehat_mingguan():
    for p in ["nasehat_mingguan.txt", "/mnt/data/nasehat_mingguan.txt"]:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()
            except:
                pass
    return """Senin: SOP - Cek Kebersihan, kerapian ruang, alat kerja bersih - Ruach Ha Kadosh - Storage Library
Selasa: ERP - Jam 9 Tepat, input data harian, laporan akurat - Tavo Malkhutkha - Storage Library
Rabu: OEE 95% - Availability x Performance x Quality = 95% target efisiensi - Storage Library
Kamis: KPI - Evaluasi kinerja mingguan Employee & Entrepreneur & Bursa - Storage Library
Jumat: Alkitab - Ruach Ha Kadosh - Kolose 3:23 Kerja untuk Tuhan, Amsal 12:22 Kejujuran - Storage Library
Sabtu: Bursa - Share info loker via email ke rekan, bursa otomatis berkurang - Storage Library
Minggu: Istirahat & Refleksi - Kolom Kejujuran Update, Bursa Berkurang, Sudah Bekerja Bertambah - Storage Library
"""

def save_nasehat_mingguan(text):
    try:
        with open("nasehat_mingguan.txt", "w", encoding="utf-8") as f:
            f.write(text)
        return True
    except:
        return False

def parse_nasehat_7_hari(text):
    hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    result = {}
    lines = text.strip().split("\n")
    for hari in hari_list:
        result[hari] = ""
    current_hari = None
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            continue
        found = False
        for hari in hari_list:
            if line_strip.lower().startswith(hari.lower() + ":") or line_strip.lower().startswith(hari.lower() + " "):
                result[hari] = line_strip
                current_hari = hari
                found = True
                break
        if not found and current_hari:
            result[current_hari] += " " + line_strip
    for hari in hari_list:
        if not result[hari]:
            result[hari] = f"{hari}: Nasehat {hari} - Ruang Teduh V6.16 FINAL Storage"
    return result

def tts_voice_all(text, role, key_id):
    clean = text.replace('"','').replace("'","").replace("\n"," ").strip()[:280]
    if not clean:
        clean = "Halo selamat datang di Ruang Teduh V6.16 FINAL"
    js_txt = json.dumps(clean)
    if role == "emp":
        rate = "0.9"; bg = "#FFEBEE"; border = "#FF5252"; label = "EMPLOYEE Staff/Supervisor THE BEST CV KOMPLIT"; icon = "👨‍💼"
    elif role == "ent":
        rate = "1.05"; bg = "#E8F5E9"; border = "#4CAF50"; label = "ENTREPRENEUR Manager/Brand/Usahawan MIRROR BEST CV KOMPLIT"; icon = "🚀"
    else:
        rate = "1.0"; bg = "#FFF9C4"; border = "#FBC02D"; label = "RUANG TEDUH STORAGE LIBRARY ROLLING 7 HARI"; icon = "📜"
    html = f"""
    <div style="background:{bg}; border:2px solid {border}; border-radius:12px; padding:12px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <div style="font-weight:800; font-size:11px;">{icon} SPEAKER {label}</div>
            <div style="font-size:8px; background:white; padding:3px 8px; border-radius:12px; border:1px solid {border};">🔊 Voice ON</div>
        </div>
        <div style="background:white; border-radius:8px; padding:8px; font-size:11px; max-height:60px; overflow:auto; border:1px dashed #ccc; margin-bottom:8px;">{clean[:170]}...</div>
        <div style="display:flex; gap:6px;">
            <button onclick="speak_{key_id}()" style="flex:1; background:{border}; color:white; border:none; padding:10px; border-radius:8px; font-weight:800; cursor:pointer;">🔊 PUTAR SUARA</button>
            <button onclick="window.speechSynthesis.cancel()" style="background:#212121; color:white; border:none; padding:10px 14px; border-radius:8px;">⏹️</button>
        </div>
        <div id="st_{key_id}" style="font-size:9px; text-align:center; margin-top:6px; color:#666;">Siap - Klik PUTAR</div>
    </div>
    <script>
        function speak_{key_id}(){{
            if('speechSynthesis' in window){{
                window.speechSynthesis.cancel();
                var u = new SpeechSynthesisUtterance({js_txt});
                u.rate={rate}; u.lang='id-ID';
                u.onstart=function(){{document.getElementById('st_{key_id}').innerHTML='🔊 Berbicara...';}};
                u.onend=function(){{document.getElementById('st_{key_id}').innerHTML='✅ Selesai';}};
                window.speechSynthesis.speak(u);
            }}
        }}
    </script>
    """
    components.html(html, height=185)

def generate_cv_text(md):
    return f"""CV KOMPLIT - RUANG TEDUH V6.16 FINAL - {md.get('nama','')} - {md.get('jabatan','')}
========================================
Nama Lengkap: {md.get('nama','')}
Tempat Lahir: {md.get('tempat','')}
Tanggal Lahir: {md.get('tgl','')}
Umur: {md.get('umur','')} tahun
Pendidikan: {md.get('pendidikan','')}
Pengalaman Kerja: {md.get('pengalaman','')}
Skill: {md.get('skill','')}
Alamat Email: {md.get('email','')} (pendaftar pengguna web dan app)
Nomor WhatsApp: {md.get('wa','')} (pendaftar pengguna web dan app)
Jabatan Dilamar: {md.get('jabatan','')}
Bursa: Total {st.session_state.bursa_total} | Aktif {st.session_state.bursa_aktif} | Kerja {st.session_state.bursa_kerja}
========================================
CV Komplit - Nama + Tempat Lahir + Tgl Lahir + Pendidikan + Pengalaman Kerja + Skill + Email + Whatsapp = CV
Kirim ke: asuveleikha@gmail.com untuk dibantu carikan loker manual
Tavo Malkhutkha - Ruach Ha Kadosh - Gratis Tidak Berbayar - FINAL
"""

def generate_mailto_link(md):
    subject = f"CV KOMPLIT - {md.get('nama','')} - {md.get('jabatan','')} - Ruang Teduh V6.16 FINAL"
    body = generate_cv_text(md)
    subject_enc = urllib.parse.quote(subject)
    body_enc = urllib.parse.quote(body)
    return f"mailto:asuveleikha@gmail.com?subject={subject_enc}&body={body_enc}"

def render_grafik_bursa():
    hist = st.session_state.bursa_hist
    if not hist:
        return
    max_v = max([h["vote"] for h in hist] + [h["kerja"] for h in hist] + [1])
    html_g = '<div style="display:flex; gap:8px; align-items:end; height:90px; background:white; border:1px solid #E0E0E0; border-radius:12px; padding:12px;">'
    for h in hist:
        v_h = int(h["vote"] / max_v * 65)
        k_h = int(h["kerja"] / max_v * 65)
        html_g += f'<div style="flex:1; text-align:center;"><div style="display:flex; gap:3px; justify-content:center; align-items:end; height:70px;"><div style="width:45%; background:#FF5252; height:{v_h}px; border-radius:4px;"></div><div style="width:45%; background:#4CAF50; height:{k_h}px; border-radius:4px;"></div></div><div style="font-size:8px; margin-top:5px; font-weight:700;">{h["jam"]}</div></div>'
    html_g += '</div><div style="font-size:9px; color:#666; margin-top:6px;">🔴 Merah = Vote Bursa Aktif (belum bekerja) | 🟢 Hijau = Sudah Bekerja (via share email + kejujuran) - Grafik hanya di Lembar 1 Putih Pendaftaran</div>'
    st.markdown(html_g, unsafe_allow_html=True)

st.markdown("""
<style>
.lembar{border-radius:14px; padding:20px; margin-bottom:16px; border-left:4px dashed #bbb; background:white; box-shadow:2px 2px 8px rgba(0,0,0,0.06);}
.lembar-putih{border-top:5px solid #424242;}
.lembar-merah{background:#FFEBEE; border-top:5px solid #FF5252;}
.lembar-hijau{background:#E8F5E9; border-top:5px solid #4CAF50;}
.lembar-kuning{background:linear-gradient(135deg, #FFFDE7, #FFF9C4); border-top:5px solid #FBC02D;}
.kotak-cv{background:white; border:2px solid #424242; border-radius:12px; padding:14px; margin:10px 0;}
.kotak-cv-komplit{background:#E3F2FD; border:3px solid #1565C0; border-radius:12px; padding:16px; margin:12px 0;}
.kotak-jujur{background:#E8F5E9; border:2px solid #4CAF50; border-radius:12px; padding:12px; margin:10px 0;}
.kotak-share{background:#FFF3E0; border:2px dashed #FF9800; border-radius:12px; padding:12px; margin:10px 0;}
.kotak-wewenang{background:white; border:1px solid #E0E0E0; border-radius:12px; padding:14px; margin:10px 0;}
.kotak-sop{background:white; border:2px solid #FF5252; border-radius:12px; padding:12px; margin:8px 0;}
.kotak-erp{background:white; border:2px solid #2196F3; border-radius:12px; padding:12px; margin:8px 0;}
.kotak-oee{background:white; border:2px solid #FF9800; border-radius:12px; padding:12px; margin:8px 0;}
.kotak-kpi{background:white; border:2px solid #9C27B0; border-radius:12px; padding:12px; margin:8px 0;}
.kotak-alkitab{background:linear-gradient(135deg, #FFF9C4, #FFEB3B); border:2px solid #F57F17; border-radius:12px; padding:14px; margin:8px 0;}
.kotak-nasehat-hari{background:white; border:2px solid #4CAF50; border-radius:12px; padding:12px; margin:8px 0;}
.kotak-nasehat-hari-active{background:#E8F5E9; border:3px solid #2E7D32; border-radius:12px; padding:14px; margin:8px 0; box-shadow:2px 2px 8px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:8px 0 12px 0;">
    <div style="font-size:10px; letter-spacing:2px; color:#888; font-weight:700;">TAVO MALKHUTKHA • RUACH HA KADOSH • V6.16 FINAL • 523+ LINES • GRATIS • CV KOMPLIT PENGALAMAN + EMAIL + WA → asuveleikha@gmail.com</div>
    <div style="font-size:20px; font-weight:900;">📗 BUKU 4 LEMBAR - FINAL - CV KOMPLIT + GRAFIK DI PUTIH + KUNING STORAGE ROLLING 7 HARI</div>
    <div style="font-size:10px; background:#1565C0; color:white; display:inline-block; padding:4px 12px; border-radius:20px; font-weight:800;">Lembar 2 Merah CV Komplit Pengalaman + Email + WA | Lembar 3 Hijau CV Komplit Mirror Merah | Lembar 4 Kuning Storage + Nasehat Rolling 7 Hari | Grafik Hanya di Putih</div>
</div>
""", unsafe_allow_html=True)

# BURSA DASHBOARD TOP - HANYA METRICS, TANPA GRAFIK BESAR - GRAFIK HANYA DI PUTIH
c1,c2,c3,c4 = st.columns(4)
c1.metric("TOTAL LOGIN", st.session_state.bursa_total)
c2.metric("BURSA AKTIF VOTE", st.session_state.bursa_aktif)
c3.metric("SUDAH BEKERJA", st.session_state.bursa_kerja)
persen = int(st.session_state.bursa_kerja/st.session_state.bursa_total*100) if st.session_state.bursa_total else 0
c4.metric("KONVERSI", f"{persen}%")
st.caption("📊 Metrics Bursa - Grafik Volume hanya di Lembar 1 Putih Pendaftaran saja (FINAL) - Lembar 2 & 3 CV Komplit + Metrics Kecil - Lembar 4 Kuning Storage Library Tanpa Grafik")

tab1, tab2, tab3, tab4 = st.tabs(["📄 PUTIH - FORM LOKER CV + GRAFIK", "🔴 MERAH - EMPLOYEE CV KOMPLIT + EMAIL + WA", "🟢 HIJAU - ENTREPRENEUR CV KOMPLIT + EMAIL + WA", "📜 KUNING - STORAGE RUANG TEDUH + ROLLING NASEHAT 7 HARI - FINAL"])

# TAB 1 PUTIH - FORM LOKER CV + GRAFIK - GRAFIK HANYA DI SINI - FINAL
with tab1:
    st.markdown('<div class="lembar lembar-putih"><b>LEMBAR 1 - FORM LOKER + JABATAN - CV KOMPLIT + GRAFIK BURSA VOLUME - GRAFIK HANYA DI SINI - FINAL</b><br/><small>CV Komplit = Nama + Tempat Lahir + Tgl Lahir + Pendidikan + Pengalaman Kerja + Skill + Email + WA → asuveleikha@gmail.com | Grafik Hanya di Putih Pendaftaran</small></div>', unsafe_allow_html=True)
    
    st.markdown("#### 📈 Grafik Volume Nilai Orang Banyak Login Dalam Bursa - Hanya di Lembar 1 Putih Pendaftaran - FINAL")
    render_grafik_bursa()
    st.divider()
    
    with st.form("form_loker_cv_final"):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Lengkap * - CV Komplit", placeholder="Budi Setia - CV")
        with col2:
            jabatan = st.selectbox("Jabatan / Posisi * - CV", ["Staff", "Supervisor", "Manager", "Brand Manager", "Usahawan / Entrepreneur"])
        col3, col4 = st.columns(2)
        with col3:
            tempat = st.text_input("Tempat Lahir * - CV", placeholder="Jakarta Barat")
        with col4:
            tgl = st.date_input("Tgl Lahir * - CV", value=date(1994,9,21))
        pendidikan = st.text_input("Pendidikan * - CV", placeholder="S1 - sarjana akuntansi universitas trisakti")
        pengalaman = st.text_area("Pengalaman Kerja * - CV Komplit", placeholder="2020-2023 Auditor PT XYZ, handle laporan keuangan, ERP Accurate, audit 10 cabang...", height=85)
        skill = st.text_area("Skill * - CV Komplit - Di bawah pengalaman kerja", placeholder="akuntansi dan auditor berbasis komputerisasi dan soft ware erp accurate, Excel advanced, leadership...", height=85)
        col5, col6 = st.columns(2)
        with col5:
            email = st.text_input("Alamat Email * - CV Komplit - Pendaftar Pengguna Web dan App", placeholder="cinhonest@gmail.com")
        with col6:
            wa = st.text_input("Nomor WhatsApp * - CV Komplit - Pendaftar Pengguna Web dan App", placeholder="081291904422")
        submit = st.form_submit_button("✅ SIMPAN CV KOMPLIT & MASUK BURSA + KIRIM KE asuveleikha@gmail.com - FINAL - GRATIS", type="primary", use_container_width=True)
        if submit:
            if not nama or not tempat or not email or not wa or not pengalaman:
                st.error("Lengkapi * bro - wajib isi CV komplit - pengalaman + email + WA pendaftar")
            else:
                is_emp = jabatan in ["Staff", "Supervisor"]
                st.session_state.member_data = {
                    "nama": nama, "jabatan": jabatan, "is_emp": is_emp, "is_ent": not is_emp,
                    "tempat": tempat, "tgl": tgl.strftime("%d-%m-%Y"), "umur": date.today().year - tgl.year,
                    "email": email, "wa": wa, "pendidikan": pendidikan,
                    "pengalaman": pengalaman, "skill": skill
                }
                add_login_bursa()
                st.success(f"✅ CV KOMPLIT {nama} ({jabatan}) masuk Bursa! Total: {st.session_state.bursa_total} | Aktif: {st.session_state.bursa_aktif} | CV ke asuveleikha@gmail.com - FINAL")
                st.balloons()
                md = st.session_state.member_data
                cv_text = generate_cv_text(md)
                st.code(cv_text, language="text")
                mailto = generate_mailto_link(md)
                st.link_button("📧 KLIK UNTUK KIRIM CV KOMPLIT KE asuveleikha@gmail.com - FINAL", mailto, type="primary", use_container_width=True)

# TAB 2 MERAH - EMPLOYEE CV KOMPLIT + EMAIL + WA - FINAL
with tab2:
    st.markdown('<div class="lembar lembar-merah"><b>LEMBAR 2 - RUANG INTERAKSI - EMPLOYEE ONLY (Staff & Supervisor) - THE BEST - CV KOMPLIT + PENGALAMAN + EMAIL + WA PENDAFTAR - FINAL</b></div>', unsafe_allow_html=True)
    if not st.session_state.member_data:
        st.warning("Isi Putih dulu - Form Loker CV Komplit - Gratis - FINAL")
        md = {"nama": "Contoh Budi Setia", "jabatan": "Staff", "tempat": "Jakarta Barat", "tgl": "21-09-1994", "umur": 31, "email": "contoh@email.com - pendaftar web app", "wa": "081291904422 - pendaftar web app", "pendidikan": "S1 Akuntansi Trisakti", "pengalaman": "2020-2023 Auditor PT XYZ - handle laporan keuangan 10 cabang - pengalaman kerja", "skill": "akuntansi, ERP Accurate, Excel advanced - skill di bawah pengalaman"}
    else:
        md = st.session_state.member_data
        if not md.get("is_emp"):
            st.info(f"Info: Anda {md['nama']} jabatan {md['jabatan']} = Entrepreneur. Lembar ini untuk Employee Staff/Supervisor, tapi tetap tampil mirror CV komplit (tidak blank) - FINAL")

    st.markdown(f'<div style="background:#FFCDD2; padding:8px; border-radius:8px; font-size:11px; font-weight:700;">✅ CV KOMPLIT: {md["nama"]} | {md["jabatan"]} | Employee - Pengalaman + Email + WA Pendaftar Web dan App = CV → asuveleikha@gmail.com - FINAL</div>', unsafe_allow_html=True)
    
    col_kiri, col_kanan = st.columns([1.2, 0.8])
    with col_kiri:
        st.markdown("### 👤 KELOLA STAFF & SUPERVISOR ONLY - CV KOMPLIT + EMAIL + WA PENDAFTAR - FINAL")
        st.markdown(f"""
        <div class="kotak-cv-komplit">
            <b>📄 CV KOMPLIT - CURRICULUM VITAE - EMPLOYEE - FINAL:</b><br/>
            <b>Nama Lengkap:</b> {md['nama']}<br/>
            <b>Tempat Lahir:</b> {md['tempat']}<br/>
            <b>Tanggal Lahir:</b> {md['tgl']} ({md['umur']} th)<br/>
            <b>Pendidikan:</b> {md['pendidikan']}<br/>
            <b>Pengalaman Kerja (kolom isi pengalaman):</b> {md['pengalaman']}<br/>
            <b>Skill (di bawah pengalaman kerja):</b> {md['skill']}<br/>
            <b>Alamat Email (pendaftar pengguna web dan app):</b> {md['email']}<br/>
            <b>Nomor WhatsApp (pendaftar pengguna web dan app):</b> {md['wa']}<br/>
            <b>Jabatan:</b> {md['jabatan']}<br/>
            <b>Status:</b> CV Komplit = Nama + Tempat Lahir + Tgl Lahir + Pendidikan + Pengalaman Kerja + Skill + Email + WA = CV → asuveleikha@gmail.com - FINAL
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🔴 Wewenang & Tanggung Jawab Employee Per Jajaran - FINAL")
        st.markdown("""
        <div class="kotak-wewenang">
            <b>STAFF - Pelaksana Lapangan - CV Komplit:</b><br/>
            • Wewenang: Pelaksana SOP kebersihan Senin, input ERP jam 9 tepat, OEE Availability 95%, kelola CV komplit pengalaman + email + WA pendaftar<br/>
            • Tanggung Jawab: Kehadiran, kerapian ruang, laporan harian, kejujuran update, input CV lengkap pengalaman + email + WA pendaftar web dan app
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="kotak-wewenang">
            <b>SUPERVISOR - Pengawas Staff - CV Komplit:</b><br/>
            • Wewenang: Awasi 3-5 Staff, validasi ERP jam 9, OEE Performance, laporan ke Manager, validasi CV komplit Staff (pengalaman + email + WA pendaftar)<br/>
            • Tanggung Jawab: Hasil Staff, disiplin tim, training SOP, bantu carikan loker via CV ke asuveleikha@gmail.com, kelola CV komplit
        </div>
        """, unsafe_allow_html=True)

        tts_voice_all(f"CV Komplit Employee {md['nama']} jabatan {md['jabatan']} tempat lahir {md['tempat']} tanggal lahir {md['tgl']} pendidikan {md['pendidikan']} pengalaman kerja {md['pengalaman']} skill {md['skill']} alamat email {md['email']} pendaftar pengguna web dan app nomor whatsapp {md['wa']} pendaftar pengguna web dan app Bursa aktif {st.session_state.bursa_aktif} Kirim ke asuveleikha at gmail dot com Final", "emp", "emp_cv_komplit_final")

        cv_text = generate_cv_text(md)
        mailto = generate_mailto_link(md)
        st.link_button("📧 KIRIM CV KOMPLIT INI KE asuveleikha@gmail.com - BANTU CARIKAN LOKER MANUAL - FINAL", mailto, type="primary", use_container_width=True)
        with st.expander("📄 Lihat Text CV Komplit Lengkap Employee (Copy manual) - FINAL"):
            st.code(cv_text, language="text")

    with col_kanan:
        st.markdown("### 📊 Bursa Vote - Employee CV Komplit - Metrics Kecil - FINAL")
        st.metric("Vote Aktif", st.session_state.bursa_aktif)
        st.metric("Sudah Bekerja", st.session_state.bursa_kerja)
        st.caption("Grafik hanya ada 1 di Lembar 1 Putih Pendaftaran - di sini metrics kecil aja - FINAL - Hemat kuota")
        st.markdown('<div class="kotak-jujur"><b>✅ Kolom Kejujuran Update - CV Komplit</b><br/>Centang jika sudah diterima kerja - Amsal 12:22 - FINAL</div>', unsafe_allow_html=True)
        if st.session_state.member_data:
            jujur_emp = st.checkbox("✅ Sudah Diterima Kerja (Jujur) - CV Komplit", key="jujur_emp_final")
            if jujur_emp and not st.session_state.jujur:
                st.session_state.jujur = True
                kurang_bursa_jujur(md['email'], "Jujur Employee CV Komplit FINAL")
                st.success("Terima kasih jujur! Bursa -1 - FINAL")
                st.balloons()

    st.divider()
    st.markdown("### 🔍 Pencarian Permintaan & Request Penawaran Employee - CV Komplit - FINAL - The Best Interaksi")
    st.markdown('<div class="kotak-share"><b>Sebagai Pencari Kerja - CV Komplit:</b> Share ke rekan via email, bursa otomatis berkurang - CV komplit pengalaman + email + WA pendaftar ke asuveleikha@gmail.com untuk bantu carikan loker manual - FINAL</div>', unsafe_allow_html=True)
    with st.form("share_emp_final"):
        email_t = st.text_input("Share via Email ke teman/rekan - CV Komplit:", placeholder="teman@email.com - untuk cari kerja / tawarkan jasa - CV komplit", key="share_emp_final_input")
        permintaan = st.text_area("Permintaan Lowongan / Request Employee - CV Komplit:", placeholder="Dicari Staff Admin, Supervisor Gudang, pengalaman..., skill..., email, WA pendaftar...", height=80)
        penawaran = st.text_area("Penawaran Gaji / Benefit - CV Komplit:", placeholder="Gaji 5-7jt, tunjangan, SOP jelas, ERP jam 9, OEE 95%...", height=60)
        btn = st.form_submit_button("📧 KIRIM & SHARE - KURANGI BURSA VOTE - CV KOMPLIT KE asuveleikha@gmail.com - FINAL", type="primary")
        if btn and "@" in email_t:
            kurang_bursa_share(email_t, "Employee share CV Komplit FINAL")
            st.success(f"Shared ke {email_t}! Bursa: {st.session_state.bursa_aktif} - CV komplit tetap ke asuveleikha@gmail.com - FINAL")

# TAB 3 HIJAU - ENTREPRENEUR CV KOMPLIT + EMAIL + WA - FINAL - MIRROR MERAH
with tab3:
    st.markdown('<div class="lembar lembar-hijau"><b>LEMBAR 3 - RUANG BOARDING - ENTREPRENEUR ONLY (Manager, Brand Manager, Usahawan) - MIRROR BEST - CV KOMPLIT + PENGALAMAN + EMAIL + WA PENDAFTAR - FINAL</b></div>', unsafe_allow_html=True)
    if not st.session_state.member_data:
        st.warning("Isi Putih dulu - Form Loker CV Komplit - Gratis - FINAL")
        md = {"nama": "Contoh Sari Manager", "jabatan": "Manager", "tempat": "Jakarta Barat", "tgl": "21-09-1994", "umur": 31, "email": "manager@email.com - pendaftar web app", "wa": "081291904422 - pendaftar web app", "pendidikan": "S1 Manajemen", "pengalaman": "2018-2024 Manager PT ABC - kelola 10 Staff, omzet 1M - pengalaman kerja", "skill": "Leadership, ERP Accurate, Strategy - skill di bawah pengalaman"}
    else:
        md = st.session_state.member_data
        if not md.get("is_ent"):
            st.info(f"Info: Anda {md['nama']} jabatan {md['jabatan']} = Staff/Supervisor. Lembar ini untuk Entrepreneur Manager/Brand/Usahawan, tapi tetap tampil mirror CV komplit (tidak blank) - FINAL")

    st.markdown(f'<div style="background:#C8E6C9; padding:8px; border-radius:8px; font-size:11px; font-weight:700;">✅ CV KOMPLIT: {md["nama"]} | {md["jabatan"]} | Entrepreneur Mirror Merah - Pengalaman + Email + WA Pendaftar Web dan App = CV → asuveleikha@gmail.com - FINAL</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:white; border:1px solid #A5D6A7; border-radius:12px; padding:12px; margin:10px 0; font-size:11px;">
        <b>🟢 KETERANGAN KEBERADAAN - MANAGE & SELEVELNYA - CV KOMPLIT - FINAL:</b><br/>
        • Manager, Brand Manager, Usahawan - Wewenang & Tanggung Jawab beda dengan Staff Supervisor - CV komplit pengalaman kerja + email + WA pendaftar pengguna web dan app seperti lembar 2 merah - Mirror Merah - Final
    </div>
    """, unsafe_allow_html=True)

    col_kiri_h, col_kanan_h = st.columns([1.2, 0.8])
    with col_kiri_h:
        st.markdown("### 🚀 KELOLA MANAGER & BRAND & USAHAWAN ONLY - CV KOMPLIT + EMAIL + WA PENDAFTAR - FINAL - MIRROR MERAH")
        st.markdown(f"""
        <div class="kotak-cv-komplit">
            <b>📄 CV KOMPLIT - CURRICULUM VITAE - ENTREPRENEUR - MIRROR MERAH - FINAL:</b><br/>
            <b>Nama Lengkap:</b> {md['nama']}<br/>
            <b>Tempat Lahir:</b> {md['tempat']}<br/>
            <b>Tanggal Lahir:</b> {md['tgl']} ({md['umur']} th)<br/>
            <b>Pendidikan:</b> {md['pendidikan']}<br/>
            <b>Pengalaman Kerja (kolom isi pengalaman):</b> {md['pengalaman']}<br/>
            <b>Skill (di bawah pengalaman kerja):</b> {md['skill']}<br/>
            <b>Alamat Email (pendaftar pengguna web dan app):</b> {md['email']}<br/>
            <b>Nomor WhatsApp (pendaftar pengguna web dan app):</b> {md['wa']}<br/>
            <b>Jabatan:</b> {md['jabatan']} (Manager/Brand Manager/Usahawan)<br/>
            <b>Status:</b> CV Komplit seperti Lembar 2 Merah - Nama + Tempat Lahir + Tgl Lahir + Pendidikan + Pengalaman Kerja + Skill + Email + WA = CV → asuveleikha@gmail.com - FINAL
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🟢 Wewenang & Tanggung Jawab Entrepreneur Per Jajaran - CV Komplit - FINAL - Mirror Merah")
        st.markdown("""
        <div class="kotak-wewenang" style="border-color:#4CAF50; background:#F1F8E9;">
            <b>MANAGER - CV Komplit - Pengalaman + Email + WA Pendaftar:</b><br/>
            • Wewenang: Kelola 5-10 Staff + 2-3 Supervisor, keputusan strategis, anggaran, rekrutmen, kelola CV komplit pengalaman + email + WA pendaftar pengguna web dan app seperti lembar 2 merah<br/>
            • Tanggung Jawab: OEE 95%, omzet area, laporan ke Brand Manager, bantu carikan loker via CV komplit ke asuveleikha@gmail.com, kelola CV komplit pendaftar
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="kotak-wewenang" style="border-color:#4CAF50; background:#F1F8E9;">
            <b>BRAND MANAGER - CV Komplit:</b><br/>
            • Wewenang: Kelola brand, strategi marketing, koordinasi Manager, budget marketing, kelola CV komplit pengalaman + email + WA pendaftar web dan app<br/>
            • Tanggung Jawab: Brand growth 15%, market share, omzet brand, CV Manager & Staff komplit pengalaman + email + WA pendaftar
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="kotak-wewenang" style="border-color:#4CAF50; background:#F1F8E9;">
            <b>USAHAWAN - CV Komplit - Pengalaman + Email + WA Pendaftar:</b><br/>
            • Wewenang: Keputusan tertinggi, visi misi, investasi, fondasi Alkitab, kelola CV komplit semua jajaran pengalaman + email + WA pendaftar pengguna web dan app<br/>
            • Tanggung Jawab: Omzet total, profit, keberlangsungan usaha, spiritual Tavo Malkhutkha, CV semua jajaran komplit pengalaman + email + WA pendaftar web dan app
        </div>
        """, unsafe_allow_html=True)

        tts_voice_all(f"CV Komplit Entrepreneur {md['nama']} jabatan {md['jabatan']} tempat lahir {md['tempat']} tanggal lahir {md['tgl']} pendidikan {md['pendidikan']} pengalaman kerja {md['pengalaman']} skill {md['skill']} alamat email {md['email']} pendaftar pengguna web dan app nomor whatsapp {md['wa']} pendaftar pengguna web dan app Mirror Merah Bursa aktif {st.session_state.bursa_aktif} Kirim ke asuveleikha at gmail Final", "ent", "ent_cv_komplit_final")

        cv_text = generate_cv_text(md)
        mailto = generate_mailto_link(md)
        st.link_button("📧 KIRIM CV KOMPLIT INI KE asuveleikha@gmail.com - BANTU CARIKAN LOKER / EMPLOYEE MANUAL - FINAL", mailto, type="primary", use_container_width=True)
        with st.expander("📄 Lihat Text CV Komplit Lengkap Entrepreneur (Copy manual) - FINAL - Mirror Merah"):
            st.code(cv_text, language="text")

    with col_kanan_h:
        st.markdown("### 📊 Bursa Vote - Entrepreneur CV Komplit - Metrics Kecil - FINAL")
        st.metric("Vote Aktif", st.session_state.bursa_aktif)
        st.metric("Sudah Bekerja", st.session_state.bursa_kerja)
        st.caption("Grafik hanya ada 1 di Lembar 1 Putih Pendaftaran - di sini metrics kecil aja - FINAL - Mirror Employee - Hemat kuota")
        st.markdown('<div class="kotak-jujur"><b>✅ Kolom Kejujuran Update - CV Komplit - FINAL</b><br/>Centang jika sudah dapat employee - Amsal 12:22</div>', unsafe_allow_html=True)
        if st.session_state.member_data:
            jujur_ent = st.checkbox("✅ Sudah Dapat Employee (Jujur) - CV Komplit - FINAL", key="jujur_ent_final")
            if jujur_ent and not st.session_state.jujur:
                st.session_state.jujur = True
                kurang_bursa_jujur(md['email'], "Jujur Entrepreneur CV Komplit FINAL")
                st.success("Terima kasih jujur! Bursa -1 - FINAL")

    st.divider()
    st.markdown("### 🔍 Pencarian Permintaan & Request Penawaran Entrepreneur - CV Komplit - FINAL - Mirror Employee - The Best Interaksi")
    st.markdown('<div class="kotak-share"><b>Sebagai Pencari Employee - CV Komplit:</b> Share lowongan via email ke rekan, bursa otomatis berkurang - Sama kayak Employee tapi untuk cari employee - CV komplit pengalaman + email + WA pendaftar web dan app ke asuveleikha@gmail.com - FINAL</div>', unsafe_allow_html=True)
    with st.form("share_ent_final"):
        email_r = st.text_input("Share lowongan via Email ke rekan - CV Komplit:", placeholder="rekan@perusahaan.com - untuk cari employee / tawarkan lowongan - CV komplit", key="share_ent_final_input")
        permintaan = st.text_area("Permintaan Lowongan / Request Employee - CV Komplit:", placeholder="Dicari Staff Admin, Supervisor Gudang, pengalaman..., skill..., email, WA pendaftar...", height=80)
        penawaran = st.text_area("Penawaran Gaji / Benefit - CV Komplit:", placeholder="Gaji 5-7jt, tunjangan, SOP jelas, ERP jam 9, OEE 95%...", height=60)
        btn = st.form_submit_button("📧 KIRIM PERMINTAAN & SHARE - KURANGI BURSA VOTE - CV KOMPLIT KE asuveleikha@gmail.com - FINAL", type="primary")
        if btn and "@" in email_r:
            kurang_bursa_share(email_r, f"Entrepreneur {md['jabatan']} cari employee CV Komplit FINAL")
            st.success(f"Terkirim ke {email_r}! Bursa: {st.session_state.bursa_aktif} - CV komplit tetap ke asuveleikha@gmail.com - FINAL")

# TAB 4 KUNING - RUANG TEDUH - STORAGE LIBRARY + ROLLING NASEHAT 7 HARI - FINAL - TANPA GRAFIK
with tab4:
    st.markdown('<div class="lembar lembar-kuning"><b>LEMBAR 4 - RUANG TEDUH - SOP, ERP, OEE, KPI + RUACH HA KADOSH (ALKITAB) - STORAGE RUANG TEDUH NASEHAT MINGGUAN EDIT SETIAP MINGGU + ROLLING SETIAP HARINYA - FINAL - TANPA GRAFIK</b><br/><small>Final - Lembar 4 Kuning sebagai storage ruang teduh nasehat mingguan kita akan edit setiap minggu dan nasehat rolling setiap harinya - Grafik hanya di lembar 1 putih pendaftaran - Storage library aja</small></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="kotak-alkitab">
        <b>🕊️ TAVO MALKHUTKHA - RUACH HA KADOSH - Fondasi Spiritual Ruang Teduh - Storage Ruang Teduh - Nasehat Mingguan Edit Setiap Minggu + Rolling Setiap Harinya - FINAL - Tanpa Grafik</b><br/>
        "Datanglah KerajaanMu, Jadilah KehendakMu di bumi seperti di Sorga" - Matius 6:10<br/>
        Lembar 4 Kuning sebagai storage ruang teduh nasehat mingguan kita akan edit setiap minggu dan nasehat rolling setiap harinya - Final - Storage library aja tanpa grafik - Grafik hanya di lembar 1 putih pendaftaran
    </div>
    """, unsafe_allow_html=True)
    tts_voice_all("Ruang Teduh Lembar 4 Kuning Storage Ruang Teduh Nasehat Mingguan Edit Setiap Minggu Rolling Setiap Harinya Final Tanpa Grafik Grafik Hanya di Lembar 1 Putih Pendaftaran", "spirit", "kuning_storage_final")

    col_sop, col_erp = st.columns(2)
    with col_sop:
        st.markdown("#### 📜 SOP - Standard Operating Procedure - Storage Library - FINAL")
        st.markdown("""
        <div class="kotak-sop">
            <b>SOP Loker CV Komplit (Putih):</b> Nama + Tempat Lahir + Tgl Lahir + Pendidikan + Pengalaman Kerja + Skill (di bawah pengalaman) + Alamat Email + Nomor Whatsapp = CV → asuveleikha@gmail.com - CV komplit pendaftar pengguna web dan app - Storage library - FINAL<br/>
            <b>SOP Employee Merah:</b> Staff & Supervisor - CV komplit pengalaman + email + WA pendaftar pengguna web dan app seperti lembar 2 merah - Wewenang & Tanggung Jawab Staff Supervisor - Voice ON - Storage - FINAL<br/>
            <b>SOP Entrepreneur Hijau:</b> Manager, Brand Manager, Usahawan - CV komplit seperti lembar 2 merah lengkapi dengan alamat email whatsapp pendaftar pengguna web dan app - Mirror Merah - Wewenang Manager Brand Usahawan - Voice ON - Storage - FINAL<br/>
            <b>SOP Bursa:</b> 1 Login = 1 Vote, Grafik Volume Nilai Orang Banyak Login - Grafik hanya di lembar 1 putih pendaftaran - FINAL - Storage library
        </div>
        """, unsafe_allow_html=True)
        tts_voice_all("SOP Loker CV Komplit Nama Tempat Lahir Tanggal Lahir Pendidikan Pengalaman Kerja Skill di bawah pengalaman Email Whatsapp pendaftar pengguna web dan app CV kirim ke asuveleikha at gmail Final Storage", "spirit", "sop_final")

        st.markdown("#### ⚙️ OEE 95% - Storage Library - FINAL - Tanpa Grafik")
        st.markdown("""
        <div class="kotak-oee">
            <b>OEE = Availability x Performance x Quality = 95% Target - Storage Library - Tanpa Grafik - FINAL:</b><br/>
            • Availability 95%: Kehadiran tepat waktu, jam 9 tepat ERP, Total Login 12 - Storage library - FINAL<br/>
            • Performance 95%: Kecepatan kerja sesuai SOP, Bursa Aktif 8 vote - Storage library - FINAL<br/>
            • Quality 95%: Hasil kerja sesuai KPI, kejujuran update, Sudah Bekerja 4 via share email + kejujuran, zero error - CV komplit pengalaman + email + WA pendaftar membantu Quality - Storage library - FINAL<br/>
            • Grafik: Hanya di lembar 1 putih pendaftaran - FINAL - Storage library aja tanpa grafik di kuning
        </div>
        """, unsafe_allow_html=True)
        tts_voice_all("OEE 95 persen Storage Library Tanpa Grafik Grafik Hanya di Lembar 1 Putih Pendaftaran Final", "spirit", "oee_final")

    with col_erp:
        st.markdown("#### 🏢 ERP - Jam 9 Tepat - Storage Library - FINAL")
        st.markdown("""
        <div class="kotak-erp">
            <b>ERP Input Harian Jam 9 Tepat - Storage Library - FINAL - Tanpa Grafik:</b><br/>
            • Data CV komplit Nama Tempat Tgl Pendidikan Pengalaman Skill Email WA pendaftar pengguna web dan app, Bursa Total Aktif Kerja, Share Log, Kejujuran - Input jam 9 tepat setiap hari - Storage library - CV ke asuveleikha@gmail.com - FINAL<br/>
            • ERP Kelola: Staff, Supervisor, Manager, Brand Manager, Usahawan - CV komplit pengalaman + email + WA pendaftar - Storage - FINAL<br/>
            • ERP Storage: 5 Rak System - Rak 1 SOP (Fondasi Merah), Rak 2 ERP (Pengelolaan Biru), Rak 3 OEE (Efisiensi Orange 95%), Rak 4 KPI (Evaluasi Ungu), Rak 5 Alkitab (Spiritual Kuning Emas Permanen) - Storage 5 Rak - Tanpa grafik - FINAL - Grafik hanya di Putih<br/>
            • ERP Bursa: Total Login 12, Aktif Vote 8, Sudah Bekerja 4, Konversi 33% - Grafik hanya di lembar 1 putih pendaftaran - FINAL
        </div>
        """, unsafe_allow_html=True)
        tts_voice_all("ERP Jam 9 tepat Storage 5 Rak SOP ERP OEE KPI Alkitab Tanpa Grafik di Kuning Grafik Hanya di Putih Final", "spirit", "erp_final")

        st.markdown("#### 📈 KPI - Storage Library - FINAL - Tanpa Grafik")
        st.markdown("""
        <div class="kotak-kpi">
            <b>KPI Employee & Entrepreneur - Storage Library - CV Komplit - FINAL - Tanpa Grafik:</b><br/>
            • Staff: Kehadiran 100%, SOP 100%, ERP jam 9 tepat, OEE 95%, kejujuran update, CV komplit pengalaman + email + WA pendaftar<br/>
            • Supervisor: Tim Staff OEE 95%, laporan tepat waktu, zero error ERP, training Staff baru, CV komplit<br/>
            • Manager: Tim 5-10 Staff + 2-3 Supervisor OEE 95%, omzet area 100%, CV komplit pengalaman + email + WA pendaftar pengguna web dan app<br/>
            • Brand Manager: Brand growth 15%, market share, omzet brand, CV komplit<br/>
            • Usahawan: Omzet total, profit, keberlangsungan usaha, spiritual foundation Tavo Malkhutkha, CV komplit semua jajaran<br/>
            • KPI Bursa: Total Login 12, Vote Aktif 8, Sudah Bekerja 4, Konversi 33% - Grafik hanya di lembar 1 putih pendaftaran - FINAL<br/>
            • KPI Spiritual: Ruach Ha Kadosh, Tavo Malkhutkha, kejujuran Amsal 12:22 - Storage library - FINAL
        </div>
        """, unsafe_allow_html=True)
        tts_voice_all("KPI Employee Entrepreneur Bursa Spiritual Storage Library Tanpa Grafik Grafik Hanya di Putih Final", "spirit", "kpi_final")

    st.divider()
    st.markdown("#### 📖 Alkitab - Ruach Ha Kadosh - Storage Library - FINAL - Tanpa Grafik - Voice All")
    st.markdown("""
    <div class="kotak-alkitab">
        <b>📖 ALKITAB - RUACH HA KADOSH (Roh Kudus) - Landasan Ruang Teduh - Storage Library - FINAL - Tanpa Grafik:</b><br/><br/>
        <b>1. Kejujuran:</b> Amsal 12:22 "Bibir dusta adalah kekejian bagi TUHAN" - Kolom Kejujuran Update di Merah & Hijau CV Komplit - Bursa berkurang - Storage - FINAL<br/>
        <b>2. Kerja Keras:</b> Kolose 3:23 "Apapun juga yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan" - SOP, ERP jam 9, OEE 95% - Storage - FINAL<br/>
        <b>3. Berbagi:</b> Kisah 2:44-45 "Segala kepunyaan mereka adalah kepunyaan bersama" - Share info loker via email ke rekan - CV komplit pengalaman + email + WA pendaftar - Bursa berkurang - Storage - FINAL<br/>
        <b>4. Tavo Malkhutkha:</b> Matius 6:33 & Matius 6:10 "Datanglah KerajaanMu" - Fondasi spiritual - Storage library - Tanpa grafik - FINAL<br/>
        <b>5. 5 Rak Storage Hijau Permanen - FINAL:</b> SOP Merah, ERP Biru, OEE Orange 95%, KPI Ungu, Alkitab Kuning Emas - Storage library aja tanpa grafik - Grafik hanya di lembar 1 putih pendaftaran - FINAL - Bener bro storage library aja<br/>
        <b>6. Employee & Entrepreneur Tidak Berbayar Gratis Mirror Best CV Komplit - FINAL:</b> Merah = Hijau - CV Komplit = Nama + Tempat Lahir + Tgl Lahir + Pendidikan + Pengalaman Kerja + Skill + Email + WA (pendaftar pengguna web dan app) → asuveleikha@gmail.com - Storage - FINAL
    </div>
    """, unsafe_allow_html=True)
    tts_voice_all("Alkitab Ruach Ha Kadosh Storage Library Final Tanpa Grafik Grafik Hanya di Putih CV Komplit Pengalaman Email Whatsapp Pendaftar", "spirit", "alkitab_final")

    st.divider()
    st.markdown("#### 📅 Nasehat Mingguan - Storage Ruang Teduh - Edit Setiap Minggu + Rolling Setiap Harinya - FINAL - Bisa Diedit - Kerjaan Klerikal Banyak")
    st.markdown("**Final - Lembar 4 Kuning sebagai storage ruang teduh nasehat mingguan kita akan edit setiap minggu dan nasehat rolling setiap harinya - Final - Jangan bikin blank lagi - Sudah bagus the best**")
    
    nasehat_raw = load_nasehat_mingguan()
    nasehat_7 = parse_nasehat_7_hari(nasehat_raw)
    
    hari_ini_map = {0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"}
    hari_ini_idx = datetime.now().weekday()
    hari_ini = hari_ini_map.get(hari_ini_idx, "Senin")
    
    st.info(f"📅 Hari ini: **{hari_ini}** - Rolling nasehat harian - 1 minggu full - Edit setiap minggu - Bisa diedit - Kerjaan klerikal banyak - FINAL - The best")
    
    cols = st.columns(7)
    hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    for i, hari in enumerate(hari_list):
        with cols[i]:
            is_today = (hari == hari_ini)
            box_class = "kotak-nasehat-hari-active" if is_today else "kotak-nasehat-hari"
            icon = "🔥 HARI INI" if is_today else "📅"
            st.markdown(f'<div class="{box_class}"><b>{icon} {hari}</b><br/><small>{nasehat_7.get(hari,"")[:90]}...</small></div>', unsafe_allow_html=True)
    
    st.markdown(f"##### 🔥 Nasehat Hari Ini - {hari_ini} - Rolling - FINAL")
    st.markdown(f'<div class="kotak-nasehat-hari-active"><b>📅 {hari_ini} - HARI INI - FINAL:</b><br/>{nasehat_7.get(hari_ini,"")}</div>', unsafe_allow_html=True)
    tts_voice_all(f"Nasehat hari ini {hari_ini} {nasehat_7.get(hari_ini,'')} Rolling setiap hari selama 1 minggu full Edit setiap minggu Bisa diedit Kerjaan klerikal banyak Sudah bagus the best Final", "spirit", "nasehat_hari_ini_final")
    
    st.markdown("##### 📚 Semua Nasehat 1 Minggu Full - Rolling Setiap Harinya - FINAL - Bisa Diedit")
    for hari in hari_list:
        is_today = (hari == hari_ini)
        label = f"🔥 {hari} (HARI INI - FINAL)" if is_today else f"📅 {hari} - FINAL"
        st.markdown(f'<div class="{"kotak-nasehat-hari-active" if is_today else "kotak-nasehat-hari"}"><b>{label}:</b> {nasehat_7.get(hari,"")}</div>', unsafe_allow_html=True)
    
    tts_voice_all("Nasehat mingguan rolling setiap hari Senin Selasa Rabu Kamis Jumat Sabtu Minggu Edit setiap minggu Bisa diedit Kerjaan klerikal banyak Sudah bagus the best Final", "spirit", "nasehat_rolling_final")
    
    st.divider()
    st.markdown("**✏️ Edit Nasehat Mingguan - Storage Ruang Teduh - Edit Setiap Minggu + Rolling Setiap Harinya - FINAL - Bisa Diedit:**")
    st.markdown("Format: Tulis per baris dengan format Hari: Nasehat - Contoh: Senin: SOP - Cek Kebersihan - Ruach Ha Kadosh - Storage Library")
    new_nasehat = st.text_area("Edit nasehat mingguan 7 hari - Rolling - Edit Setiap Minggu - Bisa Diedit - FINAL:", value=nasehat_raw, height=220, key="edit_nasehat_final_rolling")
    if st.button("💾 SIMPAN NASEHAT ROLLING 7 HARI - EDIT SETIAP MINGGU - ROLLING SETIAP HARI - FINAL - Bisa Diedit - Kerjaan Klerikal Banyak", type="primary", use_container_width=True):
        if save_nasehat_mingguan(new_nasehat):
            st.success("✅ Nasehat rolling 7 hari tersimpan - nasehat_mingguan.txt - Edit setiap minggu + Rolling setiap hari - FINAL - Bisa diedit - The best - Jangan bikin blank lagi - FINAL")
            st.balloons()
        else:
            st.error("Gagal simpan - copy manual ke GitHub nasehat_mingguan.txt - FINAL")
    
    st.markdown("---")
    st.markdown("**📊 Storage Library - 5 Rak System - Tanpa Grafik - Grafik Hanya di Lembar 1 Putih Pendaftaran - FINAL:**")
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.markdown('<div style="background:white; border:2px solid #FF5252; border-radius:10px; padding:10px; text-align:center;"><div style="font-size:22px;">📜</div><div style="font-size:10px; font-weight:800;">SOP</div><div style="font-size:8px;">Storage FINAL</div></div>', unsafe_allow_html=True)
    c2.markdown('<div style="background:white; border:2px solid #2196F3; border-radius:10px; padding:10px; text-align:center;"><div style="font-size:22px;">🏢</div><div style="font-size:10px; font-weight:800;">ERP</div><div style="font-size:8px;">Jam 9 FINAL</div></div>', unsafe_allow_html=True)
    c3.markdown('<div style="background:white; border:2px solid #FF9800; border-radius:10px; padding:10px; text-align:center;"><div style="font-size:22px;">⚙️</div><div style="font-size:10px; font-weight:800;">OEE 95%</div><div style="font-size:8px;">Tanpa Grafik FINAL</div></div>', unsafe_allow_html=True)
    c4.markdown('<div style="background:white; border:2px solid #9C27B0; border-radius:10px; padding:10px; text-align:center;"><div style="font-size:22px;">📈</div><div style="font-size:10px; font-weight:800;">KPI</div><div style="font-size:8px;">Storage FINAL</div></div>', unsafe_allow_html=True)
    c5.markdown('<div style="background:#FFF9C4; border:2px solid #F57F17; border-radius:10px; padding:10px; text-align:center;"><div style="font-size:22px;">📖</div><div style="font-size:10px; font-weight:800;">ALKITAB</div><div style="font-size:8px;">Library FINAL</div></div>', unsafe_allow_html=True)
    st.markdown(f"**Bursa:** Total: {st.session_state.bursa_total} | Aktif: {st.session_state.bursa_aktif} | Kerja: {st.session_state.bursa_kerja} | Grafik hanya di Lembar 1 Putih Pendaftaran - FINAL - Kuning Storage Library aja tanpa grafik - FINAL - Bener bro?")

# FOOTER FINAL
st.markdown(f"""
<div style="background:white; border-radius:12px; padding:12px; border:1px solid #eee; text-align:center; font-size:9px; margin-top:14px;">
<div style="background:#1565C0; color:white; display:inline-block; padding:5px 14px; border-radius:20px; font-weight:800;">📗 V6.16 FINAL • CV Komplit Pengalaman + Email + WA Pendaftar • Grafik Hanya di Putih • Kuning Storage + Rolling 7 Hari Edit Mingguan • FINAL • Gratis • Jam 4 Lanjut Infra Merah Lablab.ai</div>
<div style="margin-top:6px;">Total: {st.session_state.bursa_total} | Aktif: {st.session_state.bursa_aktif} | Kerja: {st.session_state.bursa_kerja} | Lembar 2 Merah CV Komplit Pengalaman + Email + WA Pendaftar - Lembar 3 Hijau CV Komplit Mirror Merah - Lembar 4 Kuning Storage Ruang Teduh Nasehat Mingguan Edit Setiap Minggu + Rolling Setiap Hari - Grafik Hanya di Lembar 1 Putih - FINAL</div>
</div>
""", unsafe_allow_html=True)
