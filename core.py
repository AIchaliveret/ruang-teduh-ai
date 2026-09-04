"""
core.py - Otak Ruang Teduh AI - Three Way NCR + Billboard Bursa + Volume Grafik
Update: Support kolom syarat lengkap + Ruach Hakadosh bimbingan
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict
from datetime import datetime

TARIF = {
    "EMPLOYEE": 55000,
    "ENTREPRENEUR": 75000
}

ROLE_JABATAN = {
    "EMPLOYEE": ["Staff", "Senior Staff", "Supervisor"],
    "ENTREPRENEUR": ["Manager", "GM", "Director", "Business Owner", "Owner Kecil / Pengusaha"]
}

ZONA_LIST = [
    "Jakarta Pusat", "Jakarta Utara", "Jakarta Barat", "Jakarta Timur",
    "Jakarta Selatan", "Bogor", "Depok", "Tangerang", "Bekasi"
]

PENDIDIKAN_LIST = ["SMA/SMK", "D3", "S1", "S2", "S3"]

# Field wajib sesuai point 3 lembar 2 merah pink + tambahan sistematis
FIELD_WAJIB = [
    "Nama Lengkap",
    "Tempat & Tanggal Lahir",
    "Alamat Email",
    "Nomor HP/WA",
    "Alamat Kependudukan (KTP/Domisili)",
    "Zona Rumah Tinggal",
    "Pendidikan Terakhir + Jurusan",
    "Tahun Pengalaman (0-20th)",
    "Deskripsi Pengalaman Kerja Lengkap",
    "Skill Utama (3 skill)",
    "Kategori (Employee / Entrepreneur)",
    "Jabatan Sesuai Struktur ERP",
    "Foto Profil (opsional)",
    "CV/Portofolio Link (opsional)",
    "Akun LinkedIn / Sosmed (opsional)"
]

DATA_FILE = "data_member.json"

@dataclass
class Member:
    nama: str
    tempat_lahir: str
    tgl_lahir: str
    email: str
    hp: str
    alamat_kependudukan: str
    zona: str
    pendidikan: str
    jurusan: str
    tahun_pengalaman: int
    deskripsi_pengalaman: str
    skill: str
    kategori: str
    jabatan: str
    tarif: int
    tgl_daftar: str
    ikatan_score: int = 10
    foto: str = ""
    cv_link: str = ""

    def to_dict(self):
        return asdict(self)

def load_members() -> List[Dict]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_member(member: Member):
    members = load_members()
    members.append(member.to_dict())
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(members, f, indent=2, ensure_ascii=False)
    return members

def get_bursa_billboard():
    members = load_members()
    return sorted(members, key=lambda x: x.get("tgl_daftar", ""), reverse=True)

def get_bursa_stats():
    members = load_members()
    total = len(members)
    employee = len([m for m in members if m.get("kategori") == "EMPLOYEE"])
    entrepreneur = len([m for m in members if m.get("kategori") == "ENTREPRENEUR"])
    # 1 member = 1 arsip = 1 vote
    total_vote = total
    return {
        "total": total,
        "employee": employee,
        "entrepreneur": entrepreneur,
        "total_vote": total_vote,
        "volume_grafik": {"Employee": employee, "Entrepreneur": entrepreneur}
    }

def get_5_rak_storage():
    return {
        "RAK 1 - SOP Kebersihan & Obedience": "SOP Obedience - Latihan kesetiaan pada hal kecil. Checklist kebersihan area kerja harian, wajib untuk Staff-Supervisor, dicek Pimpinan. Taat = dipercaya hal besar.",
        "RAK 2 - ERP Jam 9": "ERP - Enterprise Resource Planning versi manusia. Check-in 09:00 WIB wajib semua jenjang. Supervisor & Manager monitoring. ERP mengikat pengusaha, owner kecil, sampai Business Owner dalam satu struktur.",
        "RAK 3 - OEE 95%": "Overall Equipment Effectiveness versi manusia: Availability 100% (Hadir utuh), Performance 95% (Kerja optimal), Quality 95% (Hasil bermutu). Target diri 95% hadir utuh, bukan 100% sempurna.",
        "RAK 4 - KPI Performance": "Employee KPI: Jumlah apply loker, kehadiran, SOP. Entrepreneur KPI: Jumlah posting loker, approve lamaran, retensi employee. Semua terukur di bursa.",
        "RAK 5 - ALKITAB & Ruach Hakadosh": "Fondasi Teduh, Terikat, Tumbuh. Bukan sekadar co-working, tapi co-growing. Bimbingan Ruach Hakadosh - Roh Kudus yang menuntun dalam pekerjaan, bukan hanya teori."
    }

def get_bimbingan_ai_response(pertanyaan: str, member_kategori: str = "EMPLOYEE"):
    """Lembar 3 Hijau - Storage sebagai AI Mentor Ruach Hakadosh"""
    q = pertanyaan.lower()
    # Template bimbingan 1-2 kalimat + SOP/ERP/OEE/KPI/Alkitab
    if "sudah bayar" in q or "terikat" in q or "bimbang" in q:
        return "Tetap teduh dulu, keterikatanmu di bursa adalah bukti komitmen. SOP ingatkan: setia hal kecil, ERP ingatkan: jam 9 tepat adalah hormat. (Pengkhotbah 9:10)"
    if "kerja" in q or "lamar" in q:
        return "Bursa mencatat 1 arsip = 1 vote = 1 kesempatan. Employee melamar, Entrepreneur membuka pintu. Terus apply, skor ikatan naik, Ruach Hakadosh buka jalan. (Kolose 3:23)"
    if "sop" in q:
        return "SOP bukan beban, tapi pagar yang menjaga mutu. Bersihkan areamu hari ini, maka besok kepercayaan ditambahkan."
    if "erp" in q:
        return "ERP adalah keteraturan ilahi dalam organisasi. Owner kecil sampai Business Owner semua terikat dalam struktur yang sama. Check-in 09:00 adalah ibadah tepat waktu."
    if "oee" in q:
        return "OEE 95% - Jangan kejar 100% sempurna, kejar 95% konsisten hadir utuh. Availability 100%, Performance 95%, Quality 95%."
    if "kpi" in q:
        return "KPI bukan untuk menghakimi, tapi untuk melihat pertumbuhan. 1 lamaran = 1 benih. Tabur terus, tuai akan datang."
    # Default bimbingan ajakan
    return "Di Ruang Teduh, kita tidak jalan sendiri. Teduh dulu, terikat dalam bursa, lalu tumbuh bersama. SOP, ERP, OEE, KPI dan Alkitab menuntunmu. Tanyakan lagi, aku di sini sebagai storage bimbinganmu."
