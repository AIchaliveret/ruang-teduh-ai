
import streamlit as st
import pandas as pd

st.set_page_config(page_title="V11 FOUR WAYS FUNCTION - aichaliveret", layout="wide")
OWNER="aichaliveret"
QR="081291904422"
ref=st.query_params.get("ref", OWNER)
if isinstance(ref, list):
    ref=ref[0]
if "db" not in st.session_state:
    st.session_state.db=[{"nama":"Tuan Cin","email":"cinhonest@gmail.com","jabatan":"Manager","kota":"Jakarta Pusat","skill":"Anggaran Auto CAD","kategori":"Entrepreneur"}]

st.markdown(f"<div style='background:black;color:#00ff00;padding:8px;'><marquee>FOUR WAYS FUNCTION - 1x Tulis Tembus 4x Otomatis - Owner {OWNER} 40k/55k TITIK! - Lembar1 Purchasing PO -> Lembar2 Gudang QC BAQC -> Lembar3 Admin BA Penerimaan -> Lembar4 Finance Payment Direct Selling - QR {QR} - Ref {ref}</marquee></div>", unsafe_allow_html=True)
st.title("📖 FOUR WAYS FUNCTION - 1x Tulis Tembus 4x Otomatis")
st.caption("Three Way: PO+Surat Jalan (Vendor) -> Gudang QC BAQC -> Admin Invoice+BA Penerimaan | Four Way: + Finance BAQC+Invoice Payment | Mapping ke 4 Lembar NCR Ruang Teduh")
st.info("Origin: Purchasing menerima PO + Surat Jalan Invoice Vendor -> Gudang Procurement QC BAQC -> Admin Invoice + BA Penerimaan -> Wingman tambah Finance terima BAQC + Invoice amankan posisi purchasing + bayar = FOUR WAYS FUNCTION - Sekarang tersystematis + Excel + Flowchart + Single Database + Otomatis terkoneksi!")

tab1,tab2,tab3,tab4,tab5 = st.tabs(["⚪ PUTIH L1 - Purchasing PO","🔴 MERAH L2 - Gudang QC BAQC","🟢 HIJAU L3 - Admin BA","🔵 BIRU L4 - Finance Payment Direct Selling","📊 Flowchart + Excel"])

with tab1:
    st.header("Lembar 1 PUTIH - Purchasing - QR GATE + PO + Surat Jalan Invoice Vendor")
    st.write("Fungsi Purchasing sebagai penerima PO dan surat jalan (invoice) dari vendor")
    st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={QR}", width=180)
    c1,c2,c3=st.columns(3)
    c1.metric("Total Member di Bursa", len(st.session_state.db))
    emp=len([m for m in st.session_state.db if m["kategori"]=="Employee"])
    ent=len([m for m in st.session_state.db if m["kategori"]=="Entrepreneur"])
    c2.metric("Employee (Tenaga Kerja)", emp)
    c3.metric("Entrepreneur (Pemberi Kerja)", ent)
    st.write("Kolom ini sebagai penerima dari banyaknya member yang sudah terkoneksi... disebut BURSA... billboard bursa")
    with st.form("form_four"):
        nama=st.text_input("Nama Lengkap *")
        tempat=st.text_input("Tempat Lahir *")
        tgl=st.text_input("Tanggal Lahir *", value="1995/01/01")
        email=st.text_input("Alamat Email *")
        hp=st.text_input("Nomor HP/WA *")
        kategori=st.radio("Kategori ERP", ["EMPLOYEE (Staff s/d Supervisor)","ENTREPRENEUR (Manager s/d Business Owner, termasuk Owner Kecil)"])
        ref_code=st.text_input("Kode Referral", value=ref)
        st.checkbox("Saya setuju data saya masuk Billboard Bursa *")
        submit=st.form_submit_button("🔴 KLIK OTOMATIS - SIMPAN BERKAS DATABASE - OTOMATIS KE GUDANG QC + ADMIN + FINANCE - 1x Tulis Tembus 4x!", use_container_width=True, type="primary")
        if submit and nama:
            st.session_state.db.append({"nama":nama,"email":email,"jabatan":"Staff","kota":"Jakarta Pusat","skill":"Admin","kategori":"Entrepreneur" if "ENTREPRENEUR" in kategori else "Employee"})
            st.success(f"{nama} disimpan sebagai PO+Surat Jalan Vendor -> Otomatis ke Gudang QC BAQC -> Admin BA Penerimaan -> Finance Payment! Single DB!")
            st.rerun()
    st.markdown(f"NB: Employee 55k -> Netto {OWNER} 40k TITIK! Entrepreneur 75k -> Netto 55k TITIK! QR {QR} Harga hanya di NB ini saja")

with tab2:
    st.header("Lembar 2 MERAH PINK - Gudang Procurement QC - BAQC Berita Acara QC")
    st.write("Fungsi: Gudang menerima barang, QC, buat BAQC")
    st.success("👤 Member - Verifikasi via Email - Otomatis Terhubung dari Lembar 1 Putih (Purchasing PO)")
    st.write("Grafik volume akan terisi bila semakin banyak membernya. Saat ini 1 member terdaftar - 0 tenaga kerja & 1 pemberi kerja.")
    df=pd.DataFrame([{"Kategori":"Employee","Jumlah":emp},{"Kategori":"Entrepreneur","Jumlah":ent}])
    st.bar_chart(df.set_index("Kategori"))
    st.write("Daftar Member Terhubung via Email Otomatis - Dari Single Database Purchasing PO")
    for m in st.session_state.db:
        st.write(f"- {m['nama']} | {m['email']} | BAQC OK")

with tab3:
    st.header("Lembar 3 HIJAU - Admin BA Penerimaan - 5 Rak System + Bimbingan Ruach Hakadosh")
    st.write("Fungsi: Admin membuat invoice dan BA Penerimaan")
    st.write("Lembar 3 hijau sebagai storage yang bisa di klik dengan input minta bimbingan dan keteguhan juga saran dan nasehat para member. Tempat ini layaknya AI yang meliput semua SOP, ERP, OEE, KPI dan landasan Alkitabiah bimbingan Ruach Hakadosh spiritualitas.")
    with st.expander("📦 RAK 1 - SOP Kebersihan & Obedience"):
        st.write("SOP Purchasing PO, SOP Gudang QC BAQC, SOP Admin BA Penerimaan")
    with st.expander("📦 RAK 2 - ERP Jam 9"):
        st.write("ERP Keuangan Netto 40k/55k TITIK!")
    with st.expander("📦 RAK 3 - OEE 95%"):
        st.write("Availability 100%")
    with st.expander("📦 RAK 4 - KPI Performance"):
        st.write("KPI 40k/55k")
    with st.expander("📦 RAK 5 - ALKITAB & Ruach Hakadosh"):
        st.write("Amsal 16:3")

with tab4:
    st.header("Lembar 4 BIRU - Finance Payment - Tim & Paket - Direct Selling Upline/Downline")
    st.write("Fungsi: Finance menerima BAQC dan invoice untuk mengamankan posisi purchasing dan melakukan pembayaran + Direct Selling Reward")
    st.markdown(f"""
    <div style="border:3px solid #3b82f6;padding:15px;background:#eff6ff;border-radius:15px;">
    <b>Paket Freemium 3/3 anggota - Slot penuh. Upgrade untuk anggota lebih banyak (segera).</b><br><br>
    <b>Model Share Upline/Downline:</b> A share link ?ref={OWNER} -> B tekan -> B jadi downline A (L1) -> A dapat L1 11k/15k + Gratis! -> B share ke C -> C jadi downline B (L1) dan downline A (L2) -> A dapat L2 4k/5k<br><br>
    My Upline: {OWNER}<br>
    L1: Employee 11k*3=33k+Gratis Entrepreneur 15k*3=45k+Gratis<br>
    L2: Employee 4k*9=36k Entrepreneur 5k*9=45k<br>
    Total: 69k+Gratis+Billboard Top! 90k+Gratis+Billboard Top!<br>
    Gross = Emp*55k + Ent*75k | L1 = Emp*11k + Ent*15k | L2 = Emp*4k + Ent*5k | Netto Founder {OWNER} = Emp*40k + Ent*55k TITIK!<br>
    Auto Bayar: Bayar 55k/75k ke QR {QR} -> Potong L1 -> L2 -> Sisa 40k/55k TITIK! ke Founder {OWNER}! Flow Klaim->Pending->Approved->Paid!
    </div>
    """, unsafe_allow_html=True)
    base_url=f"https://komitmen-growth.emergent.host/?ref={OWNER}"
    st.text_input("Link Referral Upline", value=base_url)
    emp_n=st.number_input("Employee baru (Downline)", 0,100,1, key="emp4")
    ent_n=st.number_input("Entrepreneur baru (Downline)",0,100,1, key="ent4")
    gross=emp_n*55000+ent_n*75000
    l1=emp_n*11000+ent_n*15000
    l2=emp_n*4000+ent_n*5000
    netto=gross-l1-l2
    st.metric(f"Netto Founder {OWNER} TITIK! (Finance Payment)", f"Rp{netto:,} = {emp_n}*40k + {ent_n}*55k")
    st.write("Daftar Downline Otomatis dari Link Share")
    for m in st.session_state.db:
        st.write(f"- {m['nama']} | L1 Downline dari {OWNER} | Cashback 11k/15k")

with tab5:
    st.header("📊 Flowchart + Excel - FOUR WAYS FUNCTION Tersystematis Otomatis Terkoneksi")
    st.write("Flow: Lembar 1 PUTIH Purchasing PO -> Lembar 2 MERAH PINK Gudang QC BAQC -> Lembar 3 HIJAU Admin BA Penerimaan Storage -> Lembar 4 BIRU Finance Payment Direct Selling -> Finance Payment + Single Database Central")
    st.image("/mnt/data/gallery/four_ways_function_flowchart.webp")
    st.markdown("**Excel Direct Selling Member Get Member Reward:**")
    df_excel=pd.DataFrame({
        "Kategori":["Employee","Entrepreneur"],
        "Gross":[55000,75000],
        "Potong L1":[11000,15000],
        "Potong L2":[4000,5000],
        "Netto Founder aichaliveret TITIK!":[40000,55000],
        "L1*3":[33000,45000],
        "L2*9":[36000,45000],
        "Total Cashback 12":[69000,90000]
    })
    st.dataframe(df_excel, use_container_width=True)
    st.write("Download Excel untuk tabel lengkap")

st.divider()
st.caption(f"V11 FOUR WAYS FUNCTION - 1x Tulis Tembus 4x Otomatis - Purchasing PO -> Gudang QC BAQC -> Admin BA Penerimaan -> Finance Payment Direct Selling - Owner {OWNER} 40k/55k TITIK! QR {QR} - Single DB")
