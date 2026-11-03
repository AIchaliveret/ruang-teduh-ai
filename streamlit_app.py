import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="SAAS.SCM.SYSTEM V4 - Fashion Garment Market Control", page_icon="🧵", layout="wide", initial_sidebar_state="expanded")

# CSS ala blueprint dark + yellow
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Geist+Mono:wght@400;700&display=swap');
.main { background:#0a0f1a; }
h1,h2,h3 { font-family:'Instrument Serif', serif; }
code, .mono { font-family:'Geist Mono', monospace; }
.yellow { color:#ffde59; }
.card { background:#faf8f2; border:1px solid #1a2332; border-radius:12px; padding:16px; color:#0a0f1a; }
</style>
""", unsafe_allow_html=True)

if 'vendors' not in st.session_state:
    st.session_state.vendors = [
        {"nama":"PT Sinar Kainindo","kategori":"Kain Katun Mori Primis","email":"sales@sinarkain.co.id","phone":"0812-1234-5678","saldo":12500000,"notes":"Langganan sejak 2019, kualitas Mori Primis 90cm 6kg/25kodi bagus, tempo 14 hari, pernah telat 2 hari Jan 2026. Top: Mori Primis 90cm.","alamat":"Tanah Abang Blok A Lt.3 No.12, Jakarta"},
        {"nama":"Toko Kimia Makmur Pekalongan","kategori":"Kimia Naptol Reactive","email":"kimia.makmur.pkl@gmail.com","phone":"0823-9876-5432","saldo":8750000,"notes":"Supplier AS-G AS-BS AS-BO, Nitrit, Fast Red B, Fast Blue B. Harga stabil, perlu cek stok AS-G 75-300gr.","alamat":"Jl. Jetayu No.45 Pekalongan"},
        {"nama":"UD Siongkah Jaya","kategori":"Lilin Gondorukem","email":"siongkah.jaya@yahoo.com","phone":"0857-1111-2222","saldo":3200000,"notes":"Parafin 60% 52-56C, Micro 20%, Siongkah 15%, Beeswax 5%. Campuran sesuai spec bak semen 90x120x18cm.","alamat":"Jl. Raya Batik No.88, Pekalongan"},
    ]

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/892/892458.png", width=60)
    st.title("SAAS.SCM.V3")
    st.caption("Prototype Fashion Garment Market Control
Autonomous + Accurate")
    menu = st.radio("Navigasi", [
        "Dashboard Accurate",
        "Master Bahan Baku (Bal-Balan)",
        "FIFO / LIFO / Average",
        "Vendor & Supplier Notes (Accurate Style)",
        "PO / SQR / BAPO / Surat Jalan",
        "Keuangan - Buku Besar + Kwitansi + Invoice + ESC/POS",
        "Gudang C12 + GC Kepala Gudang",
        "Transport GPS Live -6.2088,106.8456",
        "Ruang Teduh Loker + Ruach Ha Kadosh",
        "Marketing Digital Links",
        "Director - Statistik Demand Planner Market Control",
        "Live HTML Full V4"
    ])
    st.divider()
    st.info("📶 WiFi: super-infrared.local\n192.168.4.1 laptop\n192.168.4.22 HP meta.aichaliveret\n✉️ Email terdaftar teregistrasi")
    st.success("Repo: AIchaliveret/saas_scm_fashion_market_v3\nBranch: main")

if menu == "Dashboard Accurate":
    st.title("SAAS.SCM.SYSTEM V4 - Prototype Fashion Garment Market Control V3.5")
    st.markdown("**ERP Garment Autonomous + Accurate System + Vendor Notes + GPS + Ruang Teduh** - saingi Accurate software akuntansi")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Persediaan Yards", "12,450 Yd", "+320")
    c2.metric("Nilai FIFO", "Rp 186,750,000", "-2.1%")
    c3.metric("PO Pending", "8 PO", "BAPO Waiting GC")
    c4.metric("Sales Hari Ini Tanah Abang+ITC+IG", "47 Kodi", "+12%")
    st.markdown("### RQS 6 Factors - Zero Blast Radius + Future of Work")
    colA, colB = st.columns(2)
    with colA:
        st.markdown("""
        **1. Forwarding Hybrid 3PL:** Jakarta-only bottleneck → Bandung/Semarang/Surabaya hub

        **2. SCM Integration:** Bal-balan → Gudang C12 → Potong 180/200/240/270/300/340cm → Kodi 20pcs → WIP 1x2x3x cetak

        **3. Demand Planner:** #OOTDJakarta scanner + Kwitansi Tanah Abang OCR → AI.Meta generate insights

        """)
    with colB:
        st.markdown("""
        **4. Benefit:** Tenaga kerja tetap inti, autonomous helps not replaces, operator Bak1 60-70°C Bak2 15-20°C + es

        **5. Need:** Market Intelligence IG/FB/WA/TikTok/Shopee + ITC grocery retail

        **6. Marketing:** Direktur Business Owner Aku Bald Lead control via super-infrared.local

        """)
    st.divider()
    df = pd.DataFrame({"size":[180,200,240,270,300,340],"kodi":[12,18,22,15,9,6],"m_tot":[43.2,72,105.6,81,54,40.8]})
    st.bar_chart(df, x="size", y="kodi")

elif menu == "Master Bahan Baku (Bal-Balan)":
    st.header("Persediaan Bahan Baku Batik Keseluruhan")
    st.caption("Kain katun yards bal-balan + pewarna reactive + kimia naptol AS-G AS-BS AS-BO + nitrit air keras soda api soda abu emping kuweh lilin parafin siongkah")
    data = [
        ["Mori Primis 90cm 6kg/25 kodi","Kain","Yd",450,"PT Sinar Kainindo","Bal"],
        ["Reactive Blue 300gr/25L","Pewarna","L",25,"Kimia Makmur","Drum"],
        ["Reactive Pink 150gr","Pewarna","L",18,"Kimia Makmur","Drum"],
        ["Naptol AS-G 75-300gr","Kimia","Kg",32,"Kimia Makmur","Sak"],
        ["Naptol AS-BS","Kimia","Kg",18,"Kimia Makmur","Sak"],
        ["Naptol AS-BO","Kimia","Kg",15,"Kimia Makmur","Sak"],
        ["Fast Red B / Fast Blue B","Diazo","Kg",12,"Kimia Makmur","Sak"],
        ["NaNO2 Nitrit 3kg","Aux","Kg",24,"Kimia Makmur","Sak"],
        ["HCl Air Keras 8L","Aux","L",40,"Kimia Makmur","Jerigen"],
        ["NaOH Soda Api 6L","Aux","L",36,"Kimia Makmur","Jerigen"],
        ["Garam 10kg","Aux","Kg",100,"UD Garam","Sak"],
        ["Soda Ash Na2CO3 / Soda Abu Emping Kueh","Aux","Kg",60,"UD Kimia","Sak"],
        ["Lilin Parafin 60% 52-56C + Micro 20% + Gondorukem Siongkah 15% + Beeswax 5%","Lilin","Kg",85,"UD Siongkah Jaya","Bal"],
    ]
    df = pd.DataFrame(data, columns=["Nama Bahan","Kategori","Satuan","Stok","Vendor","Kemasan"])
    st.dataframe(df, use_container_width=True)
    st.info("Formula: 1 Yd=0.9144M | 1 Kodi=20pcs | Kodi Real=FLOOR(Total M / (cm/100) /20) | Input ke Buku Besar otomatis")

elif menu == "FIFO / LIFO / Average":
    st.header("Buku Besar + FIFO / LIFO / Average - Saingi Accurate")
    st.caption("Pembukuan penuh nggak syst? IYA - kayak Accurate System")
    method = st.selectbox("Metode", ["FIFO","LIFO","Average Weighted"])
    tx = pd.DataFrame([
        ["2026-10-20","Masuk","Mori Primis","100 Yd","10,000","1,000,000"],
        ["2026-10-25","Masuk","Mori Primis","50 Yd","12,000","600,000"],
        ["2026-10-28","Keluar","Potong 200cm","120 Yd","-","-"],
    ], columns=["Tanggal","Jenis","Item","Qty","Harga/Yd","Total"])
    st.table(tx)
    if method=="FIFO":
        st.success("FIFO: Jual 120 Yd = 100 Yd @10k + 20 Yd @12k = Rp 1,240,000 | Sisa 30 Yd @12k = Rp 360,000")
    elif method=="LIFO":
        st.warning("LIFO: Jual 120 Yd = 50 Yd @12k + 70 Yd @10k = Rp 1,300,000 | Sisa 30 Yd @10k = Rp 300,000")
    else:
        st.info("Average Weighted: Avg = (1,000,000+600,000)/150 = 10,666.7 | HPP = 120*10,666.7 = Rp 1,280,000 | Sisa 30*10,666.7 = Rp 320,000")

elif menu == "Vendor & Supplier Notes (Accurate Style)":
    st.header("Vendor Notes - Lembar Halaman Untuk Vendor")
    st.caption("Sudah disediakan lembar halaman untuk vendor agar memudahkan business utama mencatat dan merekam para vendor suppliernya dalam saas.scm.system yang nb sebagai pembukuan akuntansi juga saingi Accurate")
    for i, v in enumerate(st.session_state.vendors):
        with st.expander(f"{v['nama']} - {v['kategori']} | Hutang: Rp {v['saldo']:,}"):
            c1,c2 = st.columns([2,1])
            with c1:
                st.text(f"Alamat: {v['alamat']}
Email terdaftar: {v['email']}
Phone: {v['phone']}")
                notes = st.text_area(f"Notes lembar halaman {v['nama']}", value=v['notes'], key=f"notes_{i}", height=100)
                if st.button(f"Simpan Notes {v['nama']}", key=f"save_{i}"):
                    st.session_state.vendors[i]['notes']=notes
                    st.success("Notes tersimpan ke Buku Besar Vendor!")
            with c2:
                st.metric("Saldo Hutang", f"Rp {v['saldo']:,}")
                st.button(f"Kirim Email Bukti Bayar ke {v['email']}", key=f"email_{i}")
                st.button(f"Lihat Buku Besar", key=f"ledger_{i}")

elif menu == "PO / SQR / BAPO / Surat Jalan":
    st.header("SQR + PO + BAPO + Surat Jalan + GC Kepala Gudang")
    st.markdown("**SQR** - Supplier Quotation Request | **PO** - Purchase Order | **BAPO** - Berita Acara PO | **GC** - General Check Kepala Gudang")
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("PO-2026-001 - Mori Primis 25 Kodi")
        st.write("Vendor: PT Sinar Kainindo | Tgl: 2026-10-28 | Status: Approved | Total: Rp 15,000,000")
        st.checkbox("GC Mr. Soesendi Lim - QC Visual IMX219 8MP OK", value=True)
        st.checkbox("GC Mister Aliang - TCS34725 L*a*b* Delta E <2 OK", value=True)
        st.checkbox("HX711 5kg LOCK buzzer 75gr Timbang OK")
    with col2:
        st.subheader("Surat Jalan SJ-2026-088")
        st.write("Sopir: Ahmad Subarjo - Grand Max B1234ABC 5-8 Bal 800Kg | Phone: 0812-xxxx (aktif di kwitansi)")
        st.write("Sopir: Rian Hidayat - L300 Pick Up 10-15 Bal 1.5 Ton")
        st.write("Sopir: M Faisal - Truk Engkel CDD/CDE 25-40 Bal 2.5-4 Ton")
        st.write("Sopir: Dedi Kurniawan - Fuso/CDD Long 80-120 Bal 7-12 Ton")
        st.info("Logistik Transportasi - Forwarding Hybrid Jakarta → Bandung/Semarang/Surabaya")

elif menu == "Keuangan - Buku Besar + Kwitansi + Invoice + ESC/POS":
    st.header("Keuangan Lengkap - Buku Besar + Kwitansi Pelunasan Kas Manual + Invoice + Driver Printer")
    j = pd.DataFrame([
        ["2026-10-28","Persediaan - Mori Primis","Debet","15,000,000",""],
        ["2026-10-28","Kas / Hutang Usaha","Kredit","","15,000,000"],
        ["2026-10-29","Kas","Debet","5,000,000","Pelunasan KWT-001"],
        ["2026-10-29","Hutang Usaha - Sinar Kainindo","Kredit","","5,000,000"],
    ], columns=["Tanggal","Akun","D/K","Debet","Kredit"])
    st.dataframe(j, use_container_width=True)
    c1,c2 = st.columns(2)
    with c1:
        st.subheader("Kwitansi Pelunasan Teregistrasi - Kas Manual ke Vendor")
        st.write("No: KWT-2026-001 | Vendor: PT Sinar Kainindo | Jumlah: Rp 5,000,000 | Metode: Kas | Status: Lunas")
        st.file_uploader("Upload Bukti Kas Manual")
    with c2:
        st.subheader("Invoice + Driver Printer ESC/POS")
        st.write("Invoice Tanah Abang: INV-TA-2026-012 | 25 Kodi @200cm | Total Rp 7,500,000")
        st.code("ESC/POS Driver: 58mm Thermal + A4 PDF\nLOGO SUPER SECURE SYST v3.0\nEmail: bukti ke vendor & pelanggan")
        if st.button("Simulate Print Invoice"):
            st.success("Printed via ESC/POS driver - PDF preview generated!")

elif menu == "Gudang C12 + GC Kepala Gudang":
    st.header("Gudang C12 - GC Kepala Gudang Approval")
    st.map(pd.DataFrame({"lat":[-6.2088],"lon":[106.8456]}))
    st.info("Gudang C12 - Ketel Uap Tabung 500L 2 Ruang 2.5 bar 90kg/jam 88% kayu 100kg→70kg→50kg | Trafo Isolasi 500VA SELV 6-12V auto OFF 17:00/19:00 | Safety MCB 6A RCD 30mA MOV 275V Thermal Fuse 72°C IP54")
    st.dataframe(pd.DataFrame([["Rak A1","Mori Primis","45 Kodi","QR-001"],["Rak A2","Reactive Blue","25 L","QR-002"],["Rak B1","Naptol AS-G","32 Kg","QR-003"]], columns=["Rak","Item","Stok","QR"]))

elif menu == "Transport GPS Live -6.2088,106.8456":
    st.header("Transportasi Terhubung GPS atau Google Maps")
    st.caption("Perjalanan selama pengantaran transport logistik terbaca dan terpantau jelas - GPS Live atau cukup Google Maps")
    c1,c2 = st.columns([2,1])
    with c1:
        st.map(pd.DataFrame({"lat":[-6.2088,-6.21,-6.19,-6.22],"lon":[106.8456,106.86,106.84,106.83]}))
        st.markdown("""
        **Live Tracking:**
        - Ahmad Subarjo Grand Max 5-8 Bal 800Kg - On the way to Gudang C12 12km ETA 25min - Phone aktif di kwitansi
        - Rian Hidayat L300 10-15 Bal 1.5 Ton - Delivered to Business Owner Gudang
        - M Faisal Truk Engkel 25-40 Bal 2.5-4 Ton - Return
        - Dedi Kurniawan Fuso 80-120 Bal 7-12 Ton - To Pekalongan ITC
        """)
    with c2:
        st.subheader("Google Maps vs GPS")
        st.radio("Pilih", ["Google Maps Embed (cukup)", "GPS Module ESP32 + Phone GPS (live)"])
        st.success("Keduanya bisa! Google Maps cukup untuk juri, GPS ESP32 untuk real tracking.")
        st.info("Turbine Francis Faraday ε=-dΦ/dt Generator 1000W×4 | Thermal Battery 500L ATS <15s | IPAL 3-stage | Cerobong 12M SS304 Cyclone+Scrubber")

elif menu == "Ruang Teduh Loker + Ruach Ha Kadosh":
    st.header("Ruang Teduh Loker + Ruach Ha Kadosh - Spiritual Kelestarian Lingkungan Kerja Lebih Baik")
    st.caption("Perekrutan SDM - Vultr Agent Rush Future of Work + Zero Blast Radius | Better Improvement | Ruach Ha Kadosh spiritualitas utama")
    st.markdown("""
    **Kenapa Ruang Teduh?** Juri Lablab.ai hackathon Vultr Agent Rush menetapkan perekrutan SDM - kita gunakan Ruang Teduh Loker kita
    
    - **Repo Ruang Teduh:** ruang-teduh-ai, ruang-teduh-perpustakaan-dki, aichaliveret-vercel-ready, silver-broccoli-aichaliveret-scm
    - **Zero Blast Radius:** Seleksi kandidat CV parsing in isolated sandbox - docker rm -f safe, verifiable output
    - **Future of Work:** Jadwal wawancara Playwright browser automation sandbox + calendar, orientasi karyawan baru checklist safety SOP IPAL cerobong
    - **Ruach Ha Kadosh:** Spiritualitas utama kelestarian - Ruach Ha Kadosh sebagai better improvement lingkungan kerja lebih baik, wellbeing AI for Future of Work Kerja max 60km dari rumah, Building in public Elohim is
    - **Pelatihan SDM:** Checklist pelatihan skill batik canting 3-6 bulan, koperasi setempat, BPJS Ketenagakerjaan Jamsostek + pensiun - bisa menyusul bila pengusaha koperasi siap menerima prototype
    """)
    st.link_button("Buka ruang-teduh-ai GitHub", "https://github.com/AIchaliveret/ruang-teduh-ai")
    st.link_button("Buka Ruang Teduh Perpustakaan DKI", "https://github.com/AIchaliveret/ruang-teduh-perpustakaan-dki")

elif menu == "Marketing Digital Links":
    st.header("Laman Link URL Marketing Digital Instagram dan Media Sosial Lain")
    st.caption("Sediakan laman penyediaan tempat link url marketing digital instagram dan media sosial lain")
    st.markdown("""
    **Instagram:** @cinhonest - Even Garden - AI Chaliveret

    **Facebook:** even.garden.637384 - Even Garden

    **Threads:** @cinhonest

    **TikTok:** @cinhonest (prototype)

    **Shopee:** Sari Batik Store

    **BlueSky / X:** @aichaliveret

    **LinkedIn:** AIchaliveret

    **GitHub:** AIchaliveret/saas_scm_fashion_market_v3
    """)
    c1,c2,c3 = st.columns(3)
    c1.link_button("Instagram @cinhonest", "https://instagram.com/cinhonest")
    c2.link_button("GitHub Repo V3", "https://github.com/AIchaliveret/saas_scm_fashion_market_v3")
    c3.link_button("Facebook Even Garden", "https://facebook.com/even.garden.637384")
    st.info("Market Int. Tanah Abang Kwitansi + ITC + Grocery Retail - ai.meta generate insights untuk Director")

elif menu == "Director - Statistik Demand Planner Market Control":
    st.header("Direktur Business Owner - Statistik Penjualan Menyeluruh - Survey Market - Demand Planner Market Control")
    st.caption("Bagaimana caranya agar direktur business owner bisa menerima statistik penjualan secara menyeluruh sebagai survey market atau masukan langsung dari pihak penjual berdasarkan data pembelian actual dan adanya permintaan sebagai data masukan demand planner market control berupa grafik dan hitungan terakumulasi atas penjualan aktual dan permintaan - hukum permintaan berbanding survey market control ala syst meta.ai")
    c1,c2,c3 = st.columns(3)
    c1.metric("Penjualan Aktual Bulan Ini", "342 Kodi", "+18% vs last month")
    c2.metric("Permintaan Request", "410 Kodi", "Gap 68 Kodi")
    c3.metric("Hukum Permintaan", "Surplus Demand 19.8%", "Need produksi +25 Kodi")
    df_sales = pd.DataFrame({
        "Market":["Tanah Abang","ITC Pekalongan","IG Online","Shopee","TikTok","Grosir Solo/Jogja"],
        "Actual":[120,75,68,45,20,14],
        "Permintaan":[145,90,85,60,30,20]
    })
    st.bar_chart(df_sales, x="Market", y=["Actual","Permintaan"])
    st.line_chart(pd.DataFrame({"Penjualan":[20,35,47,60,78,95,120],"Permintaan":[25,40,60,80,100,125,145]}))
    st.success("AI.Meta Generate: Motif Parang Kusumo Blue Reactive naik 23% di Tanah Abang, stok Naptol AS-G critical (32kg → need 50kg), rekomendasi produksi 25 kodi 200cm | Buyer internasional Amerika Afrika China Thailand Vietnam request Mega Mendung")

elif menu == "Live HTML Full V4":
    st.header("SAAS SCM V4 Full HTML - Accurate + Vendor Notes + GPS")
    html_path = "saas_scm_prototype_fashion_garment_market_control.html"
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=800, scrolling=True)
    else:
        st.warning(f"File {html_path} belum ada di repo, upload file V4 dari /mnt/data/saas_scm_prototype_fashion_garment_market_control.html")
        st.info("Upload file HTML V4 yang syst bikin tadi ke repo root")

st.divider()
st.caption("SAAS.SCM.SYSTEM V3.5 - Vultr Agent Rush - Zero Blast Radius: sandbox-code - browser automation Playwright - verifiable output - security moment PC817 5kVrms + 1N4007 + BC337 - Future of Work: SDM Recruitment Ruang Teduh + Ruach Ha Kadosh | Team 7: Aku Bald Lead, Mr Soesendi Lim Tech Analyst, Mister Aliang Field Ops, Mister Budi, Mister Sandy | License Hak Cipta Kemenkominfo SUPER SECURE SYST v3.0 | Even Garden x Cerebral Valley x Vultr | meta.aichaliveret | super-infrared.local")
