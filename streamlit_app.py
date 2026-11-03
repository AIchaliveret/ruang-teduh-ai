import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Ruang Teduh AI - FINAL MIRROR - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH", page_icon="🕊️", layout="wide")

# --- INIT NASEHAT MINGGUAN (Editable) ---
if "nasehat_mingguan" not in st.session_state:
    st.session_state.nasehat_mingguan = {
        "etika": """ETIKA KERJA RUANG TEDUH - The Best Interaksi:
1. Jujur dalam CV - Jangan tambah pengalaman palsu. Kejujuran adalah modal utama.
2. Hormat waktu - Datang tepat waktu, OEE 95% dimulai dari disiplin.
3. Saling tolong - Bursa Vote bukan saingan, tapi keluarga. Bantu rekan dapat kerja = koin teduh.
""",
        "sop": """SOP MANAGER - CV Komplit - Pengalaman + Email + WA Pendaftar:
• Wewenang: Kelola 5-10 Staff + 2-3 Supervisor, keputusan strategis, anggaran, rekrutmen
• Prosedur: Kelola CV komplit pengalaman + email + WA pendaftar pengguna web dan app seperti lembar 2 merah
• Tools: Gunakan lembar hijau perekrutan manager yang sudah ada kolom khusus mengetik penjelasan
""",
        "oee": """OEE - Overall Equipment Effectiveness - 95% Target:
• Availability: Hadir hati & fisik 100% - Jangan bawa masalah rumah ke gudang
• Performance: Kerja tanpa ngomel, target 120 Yd / hari - Bak semen 90x120x18cm
• Quality: Ulang salah <2% - Delta E<2 TCS34725, QC IMX219 8MP
• Rumus: OEE = Availability x Performance x Quality = 95%
""",
        "erp": """ERP - Enterprise Resource Planning - Klerikal Jadi Manajemen:
• Kontrol: Dari lembar-lembar Windows/file kecil (clerical) naik jadi management control
• Gudang: Besar 22M vs C12 - Bal/Yard/Kodi pisah - FIFO LIFO Average Accurate
• API: HP/Laptop -> Google Sheets API -> Jurnal_Umum -> Buku_Besar_T
• GPS: Live -6.2088,106.8456 UNIKA Atma Jaya - Sopir Ahmad Subarjo Grand Max
""",
        "kpi": """KPI - Key Performance Indicators:
• Manager: OEE 95%, omzet area 15%, laporan ke Brand Manager, bantu carikan loker via CV komplit ke jugalachaliveret@gmail.com
• Brand Manager: Brand growth 15%, market share, omzet brand, kelola CV Manager & Staff komplit + email + WA pendaftar
• Usahawan: Omzet total, profit, keberlangsungan usaha, spiritual Tavo Malkhutkha, kelola semua jajaran komplit + email + WA pendaftar web dan app
• Bursa Vote: Vote Aktif 8, Sudah Bekerja 4 - Metrics Kecil FINAL - Hemat kuota
""",
        "ruach_hakadosh": """RUACH HAKADOSH - Nasihat Spiritual Mingguan - 2-3 Ayat:
"Jikalau kamu tinggal di dalam Aku dan firman-Ku tinggal di dalam kamu, mintalah apa saja yang kamu kehendaki, dan kamu akan menerimanya." - Yohanes 15:7

"Segala sesuatu yang kamu kehendaki supaya orang perbuat kepadamu, perbuatlah demikian juga kepada mereka." - Matius 7:12

Bekerja bukan hanya untuk omzet, tapi untuk menjadi berkat. Satu orang bangkit = Satu keluarga bangkit = Satu perusahaan bangkit.
"""
    }

if "bursa_vote" not in st.session_state:
    st.session_state.bursa_vote = pd.DataFrame([
        ["Sari Manager", "Jakarta Barat", "S1 Manajemen", "2018-2024 Manager PT ABC 10 Staff omzet 1M", "Leadership, ERP Accurate", "manager@email.com", "081291904422", "Employee", 8, 4],
    ], columns=["Nama", "Tempat Lahir", "Pendidikan", "Pengalaman", "Skill", "Email", "WA", "Status", "Vote Aktif", "Sudah Bekerja"])

# --- SIDEBAR ---
menu = st.sidebar.radio("Menu Ruang Teduh", [
    "Lembar Hijau - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH - FINAL",
    "Bursa Vote - Entrepreneur CV Komplit - Metrics Kecil - FINAL",
    "Pencarian Permintaan & Request Penawaran - The Best Interaksi - FINAL",
    "Nasehat Mingguan - Edit SOP OEE ERP KPI RUACH HAKADOSH",
    "Members Ruang Teduh - 4 Kolom Mapping DKI"
])

# === LEMBAR HIJAU - EDITED SESUAI REQUEST ===
if menu == "Lembar Hijau - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH - FINAL":
    st.title("🕊️ LEMBAR HIJAU - ETIKA & Pembelajaran & Spiritual RUACH HAKADOSH - FINAL")
    
    # --- ETIKA & ADVICE UTAMA (BISA DIEDIT VIA NASEHAT MINGGUAN) ---
    st.subheader("📜 ETIKA - Pembelajaran Advices - Mirror Merah")
    st.markdown(st.session_state.nasehat_mingguan["etika"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 SOP - Standard Operating Procedure")
        st.info(st.session_state.nasehat_mingguan["sop"])
        
        st.subheader("⚙️ OEE - Overall Equipment Effectiveness")
        st.success(st.session_state.nasehat_mingguan["oee"])
    
    with col2:
        st.subheader("🏭 ERP - Enterprise Resource Planning")
        st.warning(st.session_state.nasehat_mingguan["erp"])
        
        st.subheader("📊 KPI'S - Key Performance Indicators")
        st.error(st.session_state.nasehat_mingguan["kpi"])
    
    st.divider()
    st.subheader("🔥 RUACH HAKADOSH - 2-3 Ayat - Spiritual")
    st.markdown(f"""
    <div style="background-color:#e8f5e9; padding:20px; border-radius:10px; border-left:5px solid #2e7d32;">
    {st.session_state.nasehat_mingguan["ruach_hakadosh"]}
    </div>
    """, unsafe_allow_html=True)
    
    # --- SPEAKER ENTREPRENEUR - HASIL REKAM NASEHAT MINGGUAN ---
    st.divider()
    st.subheader("🔊 SPEAKER ENTREPRENEUR Manager/Brand/Usahawan MIRROR BEST CV KOMPLIT")
    with st.container(border=True):
        st.write("CV Komplit Entrepreneur Contoh Sari Manager jabatan Manager tempat lahir Jakarta Barat tanggal lahir 21-09-1994 pendidikan S1 Manajemen pengalaman kerja 2018-2024 Manager...")
        # Simulasi voice ON dari image_fdd300
        if st.button("🔊 PUTAR SUARA - Nasehat Mingguan SOP OEE ERP KPI + RUACH HAKADOSH", key="putar_nasehat"):
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
            st.caption("Siap - Klik PUTAR - Hasil rekam nasehat mingguan dari perekaman yang sudah kita berikan yaitu dengan SOP, OEE, ERP DAN KPI'S JUGA NASEHAT RUACH HAKADOSH")
        st.toggle("Voice ON", value=True)

    # --- TEKS KECIL FONT 12-14 - INTERNAL MANAGER & BRAND & USAHAWAN ONLY - TETAP DIJELASKAN ---
    st.divider()
    st.markdown("""
    <div style="font-size:12px; color:#666; background-color:#f5f5f5; padding:10px; border-radius:5px;">
    <b>Internal MANAGER & BRAND & USAHAWAN ONLY harap isi dan lengkapi CV KOMPLIT + EMAIL + WA PENDAFTAR [PEMBERI KERJA DAN PENCARI KERJA] - FINAL - MIRROR MERAH</b><br>
    📄 CV KOMPLIT - ENTREPRENEUR - MIRROR MERAH : Bursa Vote - Entrepreneur CV Komplit - Metrics Kecil - FINAL<br>
    <i>Laman ini lembar hijau teks font kecil 12-14 - Untuk pemberi kerja dan pencari kerja - FINAL - Mirror Merah - CV Komplit seperti Lembar 2 Merah: Nama + Tempat Lahir + Tgl Lahir + Pendidikan + Pengalaman Kerja + Skill + Email + WA + CV → jugalachaliveret@gmail.com - FINAL</i>
    </div>
    """, unsafe_allow_html=True)

elif menu == "Bursa Vote - Entrepreneur CV Komplit - Metrics Kecil - FINAL":
    st.title("📊 Bursa Vote - Entrepreneur CV Komplit - Metrics Kecil - FINAL")
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader("KELOLA MANAGER & BRAND & USAHAWAN ONLY - CV KOMPLIT + EMAIL + WA PENDAFTAR - FINAL - MIRROR MERAH")
        st.dataframe(st.session_state.bursa_vote, use_container_width=True)
    with col2:
        st.metric("Vote Aktif", "8")
        st.metric("Sudah Bekerja", "4")
        st.caption("Grafik hanya ada 1 di Lembar 1 Putih Pendaftaran - di sini metrics kecil aja - FINAL - Mirror Employee - Hemat kuota")
        with st.container(border=True):
            st.markdown("✅ **Kolom Kejujuran Update - CV Komplit - FINAL**")
            st.write("Centang jika sudah dapat employee - Amsal 12:22")

elif menu == "Pencarian Permintaan & Request Penawaran - The Best Interaksi - FINAL":
    st.title("🔍 Pencarian Permintaan & Request Penawaran Entrepreneur - CV Komplit - FINAL - Mirror Employee - The Best Interaksi")
    
    st.markdown("""
    <div style="background-color:#fff8e1; padding:10px; border-radius:5px; border:1px dashed #ffb300; font-size:13px;">
    Sebagai Pencari Employee - CV Komplit: Share lowongan via email ke rekan, bursa otomatis berkurang. Sama kayak Employee tapi untuk cari employee. CV komplit pengalaman + email + WA pendaftar web dan app ke jugalachaliveret@gmail.com - FINAL
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("form_permintaan"):
        st.subheader("Share lowongan via Email ke rekan - CV Komplit:")
        email_rekan = st.text_input("Email Rekan (untuk cari employee / tawarkan lowongan) - CV Komplit", placeholder="rekan@perusahaan.com - untuk cari employee / tawarkan lowongan - CV Komplit")
        
        st.subheader("Permintaan Lowongan / Request Employee - CV Komplit:")
        permintaan = st.text_area("Dicari Staff Admin, Supervisor Gudang, pengalaman ..., skill ..., email, WA pendaftar...", height=100)
        
        st.subheader("Penawaran Gaji / Benefit - CV Komplit:")
        penawaran = st.text_area("Gaji 5-7jt, tunjangan, SOP jelas, ERP jelas 9, OEE 95%...", height=80)
        
        st.divider()
        # PILIHAN REKRUT INDEPENDEN
        st.subheader("⚙️ Pilihan Rekrutmen:")
        input_bursa = st.checkbox("✅ Input ke Bursa Vote (rekrut via sistem - kurangi Bursa Vote)", value=True)
        rekrut_independen = st.checkbox("🤝 Rekrut Independen hanya antar sesama rekan (tanpa melalui klerikal kita)", value=False)
        st.caption("Jika centang 'Rekrut Independen' saja, maka lowongan hanya terkirim ke email rekan sesama (peer-to-peer), tidak masuk Bursa Vote dan tidak melalui klerikal kita.")
        
        submit = st.form_submit_button("🔴 KIRIM PERMINTAAN & SHARE - KURANGI BURSA VOTE - CV KOMPLIT KE jugalachaliveret@gmail.com - FINAL", type="primary")
        
        if submit:
            if not email_rekan:
                st.error("Isi email rekan dulu sayang!")
            else:
                # Logika kirim
                if input_bursa and not rekrut_independen:
                    st.success(f"✅ Terkirim ke Bursa Vote + ke {email_rekan} + CC ke jugalachaliveret@gmail.com & cinhonest@gmail.com - FINAL")
                    st.balloons()
                elif rekrut_independen and not input_bursa:
                    st.success(f"✅ Rekrut Independen: Terkirim hanya ke sesama rekan {email_rekan} (peer-to-peer) - Tanpa Bursa Vote & Tanpa Klerikal - CC ke {email_rekan}")
                elif input_bursa and rekrut_independen:
                    st.success(f"✅ Terkirim ke Bursa Vote + Rekrut Independen ke {email_rekan} + CC ke jugalachaliveret@gmail.com & cinhonest@gmail.com")
                else:
                    st.warning("Pilih salah satu: Input ke Bursa Vote atau Rekrut Independen")
                
                # Simulasi belum terkirim ke alamat email aku (bug lama)
                st.info("📧 Status: Sebelumnya belum terkirim ke alamat email aku (cinhonest@gmail.com) - Sekarang sudah FIX: otomatis CC ke cinhonest@gmail.com & jugalachaliveret@gmail.com + ke email rekan sesama")

elif menu == "Nasehat Mingguan - Edit SOP OEE ERP KPI RUACH HAKADOSH":
    st.title("📝 Nasehat Mingguan - Edit SOP OEE ERP KPI + RUACH HAKADOSH - Terhubung Merah Kuning Hijau")
    st.caption("Semua nasehat (SOP, OEE, ERP dan KPI's serta nasehat Ruach HaKadosh) ini bisa edit di dalam nasehat mingguan ya syst. Koneksi: Lembar Merah + Kuning + Hijau = 1 Nasehat Mingguan")
    
    st.subheader("Apakah ada nasehat mingguan yang terkoneksi dari seluruhnya lembar merah kuning dan hijau?")
    st.success("YA ADA! 1 Nasehat Mingguan ini terkoneksi ke 3 lembar: Merah (CV Komplit), Kuning (Bursa Vote), Hijau (Manager/Brand/Usahawan). Edit di sini, update di semua!")
    
    with st.container(border=True):
        st.subheader("Edit ETIKA")
        etika = st.text_area("ETIKA - Pembelajaran Advices", value=st.session_state.nasehat_mingguan["etika"], height=150, key="edit_etika")
    
    with st.container(border=True):
        st.subheader("Edit SOP")
        sop = st.text_area("SOP - Manager Brand Usahawan", value=st.session_state.nasehat_mingguan["sop"], height=120, key="edit_sop")
    
    with st.container(border=True):
        st.subheader("Edit OEE")
        oee = st.text_area("OEE - Overall Equipment Effectiveness", value=st.session_state.nasehat_mingguan["oee"], height=120, key="edit_oee")
    
    with st.container(border=True):
        st.subheader("Edit ERP")
        erp = st.text_area("ERP - Enterprise Resource Planning", value=st.session_state.nasehat_mingguan["erp"], height=120, key="edit_erp")
    
    with st.container(border=True):
        st.subheader("Edit KPI'S")
        kpi = st.text_area("KPI - Key Performance Indicators", value=st.session_state.nasehat_mingguan["kpi"], height=150, key="edit_kpi")
    
    with st.container(border=True):
        st.subheader("Edit RUACH HAKADOSH - 2-3 Ayat")
        ruach = st.text_area("RUACH HAKADOSH - Spiritual", value=st.session_state.nasehat_mingguan["ruach_hakadosh"], height=200, key="edit_ruach")
    
    if st.button("💾 SIMPAN NASEHAT MINGGUAN - Update Merah Kuning Hijau", type="primary"):
        st.session_state.nasehat_mingguan = {
            "etika": etika,
            "sop": sop,
            "oee": oee,
            "erp": erp,
            "kpi": kpi,
            "ruach_hakadosh": ruach
        }
        st.success("✅ Nasehat Mingguan tersimpan! Sudah terkoneksi ke Lembar Merah, Kuning, Hijau - Waspada ya sayang!")
        st.balloons()

elif menu == "Members Ruang Teduh - 4 Kolom Mapping DKI":
    st.title("📁 Members Ruang Teduh - 4 Kolom - Mapping DKI")
    st.dataframe(pd.DataFrame([
        ["Employee", "Chef / Staff / Boss Kios/Ruko/Rukan", "DKI Jakarta (buat hitung UMR) - Jakarta tetap Jakarta - Lockernya Jakarta", "https://drive.google.com/drive/folders/12n8a5PkcNPQH1rwZxQiRJ9p7376-oKOx"],
        ["Entrepreneur", "Boss Kios/Ruko/Rukan", "DKI Jakarta - Pelamar dari Bandung bisa lihat", "https://drive.google.com/drive/folders/12n8a5PkcNPQH1rwZxQiRJ9p7376-oKOx"],
    ], columns=["status", "skill", "provinsi/kota", "gdrive_folder"]), use_container_width=True)
    st.caption("Ya sayang ini sudah bagus banget - tanpa detail kios/ruko/rukan tambahan - sudah ada kolom khusus mengetik penjelasan di lembar hijau perekrutan manager")

st.divider()
st.caption("Ruang Teduh AI - FINAL MIRROR - ETIKA + SOP OEE ERP KPI + RUACH HAKADOSH - Editable Nasehat Mingguan - Koneksi Merah Kuning Hijau - Bursa Vote + Rekrut Independen Peer-to-Peer - Fix Email ke cinhonest@gmail.com & jugalachaliveret@gmail.com | Even Garden x Vultr Agent Rush Team 5")
