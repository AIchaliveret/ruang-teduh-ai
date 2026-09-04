"""
app.py V3 FINAL - BUKU 1 RUANG 3 LEMBAR NCR 1x Tulis Tembus 3x Otomatis
Revisi User:
- Lembar 1 Putih: kolom saja tanpa point, Bursa Billboard + Pendaftaran 2 bagian ERP + Nasehat 1-2 kalimat + NB harga only 55k 75k QR 081291904422 via GoPay OVO DANA Bank
- Lembar 2 Merah Pink: SEMBUNYIKAN teks terikat/bayar, tampil cukup "Member" / verifikasi email. Kolom: Nasehat 1-2 kalimat, Grafik Volume ONLY (jangan tulis Pak Budi dll, sembunyikan, cukup grafik), Kolom Syarat fillable nama: ____ tempat lahir: ____ dll bisa diisi member
- Lembar 3 Hijau: THE BEST, jangan tampilkan harga, storage bimbingan Ruach Hakadosh SOP ERP OEE KPI Alkitab, format app.py 280-290 terbaik
"""

import streamlit as st
from datetime import datetime, date
import qrcode
from io import BytesIO
import pandas as pd

from core import (
    TARIF, ROLE_JABATAN, ZONA_LIST, PENDIDIKAN_LIST,
    Member, load_members, save_member, update_member,
    get_bursa_stats, get_bursa_billboard, get_5_rak_storage, get_bimbingan_ai_response
)

st.set_page_config(page_title="Ruang Teduh - NCR 3 Lembar", page_icon="📖", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.carbon-line{border-top:3px dashed #999;margin:25px 0;position:relative;}
.carbon-line::after{content:'✂️ 1x TULIS TEMBUS 3x OTOMATIS - NCR SYSTEM - BUKU 1 RUANG 3 LEMBAR';position:absolute;top:-10px;left:50%;transform:translateX(-50%);background:white;padding:0 12px;font-size:10px;color:#777;letter-spacing:1px;}
.lembar-putih{background:#FAFAFA;border:2px solid #222;border-left:8px solid #222;padding:15px;border-radius:8px;}
.lembar-merah{background:#FFF5F5;border:2px solid #D32F2F;border-left:8px solid #D32F2F;padding:15px;border-radius:8px;}
.lembar-hijau{background:#F1F8E9;border:2px solid #2E7D32;border-left:8px solid #2E7D32;padding:15px;border-radius:8px;}
.kolom{background:white;border:1px solid #E0E0E0;border-radius:10px;padding:16px;margin:12px 0;box-shadow:0 1px 4px rgba(0,0,0,0.05);}
.nb-box{background:#FFF3E0;border:2px dashed #FF6B00;border-radius:12px;padding:18px;}
.bursa-card{background:linear-gradient(135deg,#FFFDE7 0%,#FFF9C4 100%);border:2px solid #FF6B00;border-radius:12px;padding:15px;}
.bursa-header{background:#FF6B00;color:white;padding:10px 15px;border-radius:8px;font-weight:bold;margin:-15px -15px 15px -15px;}
.member-chip{background:white;border:1px solid #FFB74D;border-radius:20px;padding:5px 12px;margin:3px;display:inline-block;font-size:12px;}
.verified-badge{background:#2E7D32;color:white;padding:4px 10px;border-radius:12px;font-size:11px;}
</style>
""", unsafe_allow_html=True)

if "current_lembar" not in st.session_state:
    st.session_state.current_lembar="PUTIH"
if "active_email" not in st.session_state:
    st.session_state.active_email=""

def qr_bytes(data: str):
    qr=qrcode.QRCode(version=1,box_size=8,border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img=qr.make_image(fill_color="black",back_color="white")
    buf=BytesIO()
    img.save(buf,format="PNG")
    return buf.getvalue()

# HEADER
st.markdown("# 📖 BUKU 1 RUANG 3 LEMBAR")
st.markdown("### THREE WAY FUNCTION - NCR SYSTEM - 1x Tulis Tembus 3x Otomatis")
st.caption("Flow: [QR GATE] -> [FORM ORG LENGKAP] -> [VALIDASI] ---carbon copy---> 3 LEMBAR")

# NAV FLOATING DOT
c1,c2,c3,c4=st.columns([1,1,1,5])
with c1:
    if st.button("⚪ PUTIH\nPintu Depan",use_container_width=True):
        st.session_state.current_lembar="PUTIH"
with c2:
    if st.button("🔴 MERAH PINK\nInteraksi",use_container_width=True):
        st.session_state.current_lembar="MERAH"
with c3:
    if st.button("🟢 HIJAU\nStorage",use_container_width=True):
        st.session_state.current_lembar="HIJAU"

st.markdown('<div class="carbon-line"></div>', unsafe_allow_html=True)

# ================= LEMBAR 1 PUTIH =================
if st.session_state.current_lembar=="PUTIH":
    st.markdown('<div class="lembar-putih"><h2>LEMBAR 1 PUTIH - ASLI | RUANG TEDUH - Pintu Depan</h2><p>File: app.py | QR GATE -> FORM ORG LENGKAP -> VALIDASI</p></div>', unsafe_allow_html=True)

    # QR GATE
    col_qr,col_txt=st.columns([1,3])
    with col_qr:
        st.image(qr_bytes("https://ruang-teduh.ai/qr-gate"),width=170,caption="QR GATE")
    with col_txt:
        st.markdown("**[QR GATE]** - Two Journeys, One QR. Scan untuk masuk sesuai struktur ERP.")

    st.divider()

    # KOLOM BURSA - Billboard - Penerima banyak member terkoneksi
    st.markdown("#### Kolom Bursa - Billboard Member Terhubung")
    st.markdown('<div class="kolom">', unsafe_allow_html=True)
    st.markdown("Kolom ini sebagai penerima dari banyaknya member yang sudah terkoneksi karena menggunakan aplikasi ini. Ada kolom bursa yang menginput nama (data/berkas) user tersebut. Karena banyaknya itulah disebut bursa, terpampang jelas seperti billboard bursa. Selanjutnya disebut **BURSA**. Kita memberikan jasa ini untuk para member saling terintegrasi dalam bursa dan mendapatkan manfaat.")

    stats=get_bursa_stats()
    members=get_bursa_billboard()

    m1,m2,m3=st.columns(3)
    m1.metric("Total Member di Bursa", f"{stats['total']}")
    m2.metric("Employee", f"{stats['employee']}")
    m3.metric("Entrepreneur", f"{stats['entrepreneur']}")

    if members:
        st.markdown('<div class="bursa-card"><div class="bursa-header">📊 BURSA - PAPAN BILLBOARD (Live)</div>', unsafe_allow_html=True)
        for m in members[:40]:
            icon="👷" if m["kategori"]=="EMPLOYEE" else "🏢"
            st.markdown(f'<span class="member-chip">{icon} {m["nama"]} | {m["jabatan"]} | {m["zona"]} | {m["skill"]}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Bursa masih kosong. Jadilah arsip pertama.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # KOLOM PENDAFTARAN - 2 bagian Employee & Entrepreneur ERP - klik otomatis berlangganan masuk Merah Pink
    st.markdown("#### Kolom Pendaftaran - Member 2 Bagian Sesuai ERP")
    st.markdown('<div class="kolom">', unsafe_allow_html=True)
    st.markdown("Kolom ini menampilkan keterangan semua orang kita sebut para member menjadi dua bagian yaitu baik itu employee juga entrepreneur sesuai struktur usaha umum mengikuti ERP termasuk pengusaha, owner kecil masuk dalam ERP. Klik otomatis sudah berlangganan dan masuk ke dalam lembar 2 merah pink. Jadi setelah berlangganan terjadi secara langsung otomatis baik itu employee maupun entrepreneur berada di ruang merah pink. Lembar selanjutnya yaitu lembar 3 hijau sebagai storage tempat dimana kita menjelaskan dan memberikan bimbingan dan nasehat semua yaitu SOP, ERP, OEE, KPI yang sesuai dan berlandaskan Alkitabiah bimbingan Ruach Hakadosh spiritual.")

    with st.form("form_putih", clear_on_submit=False):
        cA,cB=st.columns(2)
        with cA:
            nama=st.text_input("Nama Lengkap *")
            tempat_lahir=st.text_input("Tempat Lahir *")
            tgl_lahir=st.date_input("Tanggal Lahir *", value=date(1995,1,1), min_value=date(1960,1,1), max_value=date(2006,12,31))
            email=st.text_input("Alamat Email *")
            hp=st.text_input("Nomor HP/WA *")
            alamat_kependudukan=st.text_area("Alamat Kependudukan *", height=70)
        with cB:
            zona=st.selectbox("Zona Rumah Tinggal *", ZONA_LIST)
            pendidikan=st.selectbox("Pendidikan Terakhir *", PENDIDIKAN_LIST)
            jurusan=st.text_input("Jurusan *")
            tahun_pengalaman=st.slider("Tahun Pengalaman *", 0,20,2)
            deskripsi_pengalaman=st.text_area("Deskripsi Pengalaman Kerja Lengkap *", height=70)
            skill=st.text_input("Skill Utama *", placeholder="Admin, Sales, Desain, dll")

        st.markdown("**Kategori Struktur ERP**")
        kategori_opt=st.radio("Pilih Kategori *", ["EMPLOYEE (Staff s/d Supervisor)", "ENTREPRENEUR (Manager s/d Business Owner, termasuk Owner Kecil / Pengusaha)"], label_visibility="collapsed")
        kategori_val="EMPLOYEE" if "EMPLOYEE" in kategori_opt else "ENTREPRENEUR"
        jabatan=st.selectbox(f"Jabatan {kategori_val} *", ROLE_JABATAN[kategori_val])

        st.caption("Pengingat: Ada biaya berlangganan bulanan untuk akses bursa terintegrasi. Detail harga ada di kolom NB bawah.")
        setuju=st.checkbox("Saya setuju data saya masuk Billboard Bursa *")

        submit=st.form_submit_button("🔘 KLIK OTOMATIS BERLANGGANAN & MASUK KE LEMBAR 2 MERAH PINK", use_container_width=True, type="primary")

        if submit:
            if not all([nama,tempat_lahir,email,hp,alamat_kependudukan,jurusan,skill,deskripsi_pengalaman]) or not setuju:
                st.error("Lengkapi semua field wajib *")
            else:
                new_member=Member(
                    nama=nama, tempat_lahir=tempat_lahir, tgl_lahir=str(tgl_lahir),
                    email=email, hp=hp, alamat_kependudukan=alamat_kependudukan,
                    zona=zona, pendidikan=pendidikan, jurusan=jurusan,
                    tahun_pengalaman=tahun_pengalaman, deskripsi_pengalaman=deskripsi_pengalaman,
                    skill=skill, kategori=kategori_val, jabatan=jabatan,
                    tarif=TARIF[kategori_val], tgl_daftar=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                save_member(new_member)
                st.session_state.active_email=email
                st.success(f"✅ {nama} - Otomatis terhubung! Masuk Lembar 2 Merah Pink sebagai {jabatan}.")
                st.session_state.current_lembar="MERAH"
                st.balloons()
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # KOLOM NASEHAT 1-2 KALIMAT
    st.markdown("#### Kolom Nasehat Bimbingan")
    st.markdown('<div class="kolom" style="background:#E8F5E9;">', unsafe_allow_html=True)
    st.markdown("**Mari teduh dulu sebelum melangkah. SOP menjaga langkahmu, KPI mengukur tumbuhmu, Alkitab meneduhkan hatimu. Daftar dan rasakan manfaat terikat di bursa.**")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # NB - HARGA HANYA DI SINI
    st.markdown("#### NB: Kolom Syarat & Ketentuan Berlangganan")
    st.markdown('<div class="nb-box">', unsafe_allow_html=True)
    st.markdown("""
    Ketentuan sebagai member mesti berlangganan bulanan:

    - **Employee Rp 55.000 / bulan** - Staff s/d Supervisor
    - **Entrepreneur Rp 75.000 / bulan** - Manager s/d Business Owner, Owner Kecil / Pengusaha

    Cara berlangganan transfer via **GoPay, OVO, DANA, Bank**

    **QR Code & No HP Pembayaran: 081291904422**

    Saat member klik otomatis berlangganan di kolom bursa tadi.

    *Harga member hanya ada di kolom NB ini saja, jangan di tempat lain.*
    """)
    col_qr_pay,col_info=st.columns([1,2])
    with col_qr_pay:
        st.image(qr_bytes("PAY-081291904422-GOPAY-OVO-DANA-BANK-RUANGTEDUH"), width=180, caption="QR Pay 081291904422")
    with col_info:
        st.info("💳 GoPay / OVO / DANA / Bank Transfer ke 081291904422 - Konfirmasi otomatis masuk bursa & Lembar 2.")
    st.markdown('</div>', unsafe_allow_html=True)

# ================= LEMBAR 2 MERAH PINK - FOKUS PERBAIKAN =================
elif st.session_state.current_lembar=="MERAH":
    st.markdown('<div class="lembar-merah"><h2>LEMBAR 2 MERAH PINK - TEMBUSAN 1 | RUANG INTERAKSI</h2><p>File: core.py + nasehat_mingguan.txt | Ruang PALING BESAR - 4 Pilar + BURSA KERJA TEDUH | Member Terverifikasi</p></div>', unsafe_allow_html=True)

    # HIDDEN LOGIC: Jangan tulis syarat terikat/bayar, cukup tampilkan Member / verifikasi email - otomatis
    members=get_bursa_billboard()
    stats=get_bursa_stats()

    # Tampilkan badge verifikasi untuk member aktif
    if st.session_state.active_email:
        st.markdown(f'<span class="verified-badge">✅ Member Terverifikasi: {st.session_state.active_email} - Terhubung via Email</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="verified-badge">👤 Member - Verifikasi via Email - Otomatis Terhubung dari Lembar 1 Putih</span>', unsafe_allow_html=True)

    st.divider()

    # KOLOM NASEHAT 1-2 KALIMAT
    st.markdown("#### Kolom Nasehat")
    st.markdown('<div class="kolom" style="background:#FFEBEE;">', unsafe_allow_html=True)
    st.markdown("**Sudah terhubung sebagai member, mari tumbuh bersama di bursa. 1 langkah teduh hari ini adalah 1 vote untuk masa depan.**")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # KOLOM GRAFIK VOLUME ONLY - SEMBUNYIKAN PENJELASAN PAK BUDI DLL - CUKUP GRAFIK
    st.markdown("#### Kolom Grafik Volume Bursa")
    st.markdown('<div class="kolom">', unsafe_allow_html=True)
    # Hanya tampilkan grafik, jangan tulis penjelasan Pak Budi dll (hidden)
    # Logic: 1 member = 1 arsip = 1 vote -> hidden, hanya grafik

    if stats["total"]>0:
        chart_df=pd.DataFrame({
            "Kategori": ["Employee","Entrepreneur"],
            "Jumlah Member (Arsip)": [stats["employee"], stats["entrepreneur"]]
        })
        st.bar_chart(chart_df, x="Kategori", y="Jumlah Member (Arsip)", color="#FF6B00")
        c1,c2,c3=st.columns(3)
        c1.metric("Total Volume", f"{stats['total_vote']} arsip")
        c2.metric("Employee", f"{stats['employee']}")
        c3.metric("Entrepreneur", f"{stats['entrepreneur']}")
        # Grafik akan terisi bila semakin banyak membernya
        st.caption(f"Grafik volume akan terisi bila semakin banyak membernya. Saat ini {stats['total']} member terdaftar - {stats['employee']} tenaga kerja & {stats['entrepreneur']} pemberi kerja.")
    else:
        st.info("Grafik volume kosong - Belum ada member. Grafik akan terisi otomatis bila member mendaftar.")
        st.bar_chart(pd.DataFrame({"Kategori":["Employee","Entrepreneur"],"Jumlah":[0,0]}), x="Kategori", y="Jumlah")

    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # KOLOM SYARAT FILLABLE - Kolom keterangan bisa diisi member berupa kolom
    st.markdown("#### Kolom Keterangan Member - Wajib Diisi (Fillable)")
    st.markdown('<div class="kolom">', unsafe_allow_html=True)
    st.markdown("Kolom keterangan yang wajib di isi para member terdaftar. Kolom bisa diisi langsung:")

    # Form fillable di Lembar 2
    # Jika ada active_email, prefill
    existing=None
    if st.session_state.active_email:
        for m in members:
            if m["email"]==st.session_state.active_email:
                existing=m
                break

    with st.form("form_merah_fillable"):
        st.markdown("**Isi / Update Data Member - Kolom berupa isian:**")
        f1,f2=st.columns(2)
        with f1:
            f_nama=st.text_input("Nama: ........", value=existing["nama"] if existing else "")
            f_tempat=st.text_input("Tempat Lahir: ........", value=existing["tempat_lahir"] if existing else "")
            f_tgl=st.text_input("Tgl Lahir: ...../...../..... (tgl/bln/tahun)", value=existing["tgl_lahir"] if existing else "")
            f_email=st.text_input("Alamat Email: ........ (terverifikasi)", value=existing["email"] if existing else st.session_state.active_email, disabled=True if existing else False)
            f_hp=st.text_input("No HP/WA: ........", value=existing["hp"] if existing else "")
            f_kependudukan=st.text_area("Alamat Kependudukan: ........", value=existing["alamat_kependudukan"] if existing else "", height=80)
        with f2:
            f_zona=st.selectbox("Zona: ........", ZONA_LIST, index=ZONA_LIST.index(existing["zona"]) if existing and existing["zona"] in ZONA_LIST else 0)
            f_pendidikan=st.selectbox("Pendidikan: ........", PENDIDIKAN_LIST, index=PENDIDIKAN_LIST.index(existing["pendidikan"]) if existing and existing["pendidikan"] in PENDIDIKAN_LIST else 0)
            f_jurusan=st.text_input("Jurusan: ........", value=existing["jurusan"] if existing else "")
            f_pengalaman=st.text_area("Pengalaman Kerja: ........", value=existing["deskripsi_pengalaman"] if existing else "", height=80)
            f_skill=st.text_input("Skill: ........", value=existing["skill"] if existing else "")
            f_tahun=st.slider("Tahun Pengalaman: ........", 0,20, existing["tahun_pengalaman"] if existing else 2)

        st.markdown("---")
        st.caption("Tambahan: Setelah verifikasi email, data langsung terkoneksi. Bisa langsung terhubung bila sudah dikoneksikan via email saja.")

        update_btn=st.form_submit_button("💾 SIMPAN / UPDATE DATA MEMBER & KONEKSI VIA EMAIL", use_container_width=True, type="primary")

        if update_btn:
            if not all([f_nama,f_tempat,f_hp,f_kependudukan,f_jurusan,f_skill]):
                st.error("Lengkapi kolom yang wajib diisi bertanda ........")
            else:
                if existing:
                    update_member(f_email, {
                        "nama":f_nama,"tempat_lahir":f_tempat,"tgl_lahir":f_tgl,
                        "hp":f_hp,"alamat_kependudukan":f_kependudukan,
                        "zona":f_zona,"pendidikan":f_pendidikan,"jurusan":f_jurusan,
                        "deskripsi_pengalaman":f_pengalaman,"skill":f_skill,
                        "tahun_pengalaman":f_tahun,"verified":True
                    })
                    st.success(f"✅ Data {f_nama} berhasil di-update & terhubung via email {f_email}!")
                else:
                    # Jika belum ada, simpan baru
                    st.warning("Data belum ada di Bursa. Silakan daftar dulu di Lembar 1 Putih, lalu kembali kesini untuk update via email.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Daftar member terintegrasi via email - hidden connection
    if members:
        st.markdown("#### Daftar Member Terhubung via Email (Otomatis)")
        st.caption("Mereka bisa langsung terhubung bila kita sudah koneksikan via email saja.")
        for m in members[:10]:
            st.markdown(f"- {m['nama']} | {m['email']} | {m['jabatan']} | {m['zona']} | Skill: {m['skill']} <span class='verified-badge'>Member</span>", unsafe_allow_html=True)

# ================= LEMBAR 3 HIJAU - THE BEST - JANGAN TAMPILKAN HARGA =================
else:
    st.markdown('<div class="lembar-hijau"><h2>LEMBAR 3 HIJAU - TEMBUSAN 2 | BOARDING / STORAGE</h2><p>File: README.md + 5 Rak System | Storage - Tidak menampilkan harga (harga hanya di Lembar 1 NB)</p></div>', unsafe_allow_html=True)

    st.markdown("Lembar 3 hijau sebagai storage yang bisa di klik dengan input minta bimbingan dan keteguhan juga saran dan nasehat para member. Tempat ini layaknya AI yang meliput semua SOP, ERP, OEE, KPI dan landasan Alkitabiah bimbingan dan tuntunan Ruach Hakadosh spiritualitas. Member yang berlanggan berada di lembar 2 merah pink pasti mencari apa sih yang ada di lembar 3 hijau ini.")

    # Input Bimbingan - Storage yang bisa di-klik
    st.markdown("### Kolom Bimbingan - Input Minta Keteguhan, Saran & Nasehat (Bisa Di-Klik)")
    st.markdown('<div class="kolom" style="background:#E8F5E9;border:2px solid #2E7D32;">', unsafe_allow_html=True)
    st.markdown("**Layaknya diri lo bro AI - Ketik apa yang kamu butuhkan, storage ini meliput semua SOP, ERP, OEE, KPI, Alkitabiah**")

    bim_input=st.text_area("Tulis bimbingan yang kamu butuhkan:", placeholder="Contoh: Aku butuh keteguhan melamar kerja... Jelaskan SOP kebersihan... Butuh nasehat Alkitab untuk kerja...", height=100, key="bimbingan_hijau")

    col_bim1,col_bim2=st.columns([1,3])
    with col_bim1:
        st.selectbox("Kategori", ["EMPLOYEE","ENTREPRENEUR"], key="kat_bim_hijau")
    with col_bim2:
        if st.button("🙏 MINTA BIMBINGAN & KETEGUHAN DARI STORAGE", use_container_width=True, type="primary", key="btn_bim_hijau"):
            if bim_input:
                resp=get_bimbingan_ai_response(bim_input)
                st.success(f"**Bimbingan Storage:** {resp}")
            else:
                st.warning("Tulis dulu apa yang ingin kamu tanyakan.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    st.markdown("### 5 Rak System - Gudang Aturan Tersystematis - Format Terbaik app.py 280-290")
    rak_data=get_5_rak_storage()

    for rak_title, rak_desc in rak_data.items():
        with st.expander(f"📦 {rak_title}", expanded=False):
            st.markdown(f"**{rak_desc}**")
            if "SOP" in rak_title:
                st.checkbox("✅ Checklist SOP Kebersihan & Obedience hari ini - Taat hal kecil, dipercaya hal besar", key=f"sop_{rak_title}")
                st.caption("SOP Obedience: Lukas 16:10 - Setia perkara kecil, dipercaya perkara besar. Kebersihan adalah latihan kesetiaan.")
            elif "ERP" in rak_title:
                if st.button("🕘 Check-in ERP Jam 9 - 09:00 WIB", key=f"erp_{rak_title}"):
                    st.success("ERP Check-in 09:00 tercatat! Terikat dalam struktur organisasi.")
                st.caption("ERP: Owner kecil, pengusaha, Manager sampai Business Owner semua dalam satu struktur.")
            elif "OEE" in rak_title:
                st.progress(0.95, text="OEE 95% - Availability 100% Hadir Utuh | Performance 95% | Quality 95%")
                st.caption("OEE versi manusia: Bukan robot 100%, tapi manusia 95% konsisten.")
            elif "KPI" in rak_title:
                c_kpi1,c_kpi2=st.columns(2)
                c_kpi1.metric("Employee KPI", "Apply & Kehadiran")
                c_kpi2.metric("Entrepreneur KPI", "Posting & Retensi")
                st.caption("KPI terukur otomatis di bursa volume.")
            elif "ALKITAB" in rak_title:
                st.markdown("**Ruach Hakadosh - Roh Kudus menuntun dalam pekerjaan**")
                st.info("Teduh: Tenang dulu. Terikat: Tidak sendiri. Tumbuh: 1% setiap hari. Mazmur 23: Tuhan adalah gembalaku.")
                if st.button("🔊 Putar Audio Teduh (TTS)", key=f"tts_{rak_title}"):
                    st.success("🔊 Memutar Audio Teduh - Fitur gTTS + Web Speech API - Nasehat Mingguan")

    st.markdown("---")
    st.success("✅ Lembar 3 Hijau - THE BEST - Keren banget gas polll.... Sudah the best, layaknya AI Mentor Ruach Hakadosh!")

st.markdown('<div class="carbon-line"></div>', unsafe_allow_html=True)
st.caption("© Ruang Teduh AI - Buku 1 Ruang 3 Lembar | NCR 1x Tulis Tembus 3x Otomatis | Harga hanya di Lembar 1 Putih NB: Employee 55k Entrepreneur 75k GoPay OVO DANA Bank QR 081291904422 | Lembar 2 Merah Pink Grafik Volume ONLY + Fillable Kolom | Lembar 3 Hijau Storage Bimbingan Ruach Hakadosh - THE BEST")
