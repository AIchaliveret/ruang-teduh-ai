"""
core.py V3 - Final NCR System
- Sembunyikan logika terikat/bayar, tampilkan "Member" + verifikasi email saja
- 1 member = 1 arsip = 1 vote (hidden logic, hanya grafik volume)
- Kolom isian fillable untuk Lembar 2
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict
from datetime import datetime

TARIF = {"EMPLOYEE": 55000, "ENTREPRENEUR": 75000}

ROLE_JABATAN = {
    "EMPLOYEE": ["Staff", "Senior Staff", "Supervisor"],
    "ENTREPRENEUR": ["Manager", "GM", "Director", "Business Owner", "Owner Kecil / Pengusaha"]
}

ZONA_LIST = ["Jakarta Pusat","Jakarta Utara","Jakarta Barat","Jakarta Timur","Jakarta Selatan","Bogor","Depok","Tangerang","Bekasi"]
PENDIDIKAN_LIST = ["SMA/SMK","D3","S1","S2","S3"]

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
    verified: bool = True  # verifikasi email - tampil sebagai "Member"

    def to_dict(self):
        return asdict(self)

def load_members() -> List[Dict]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_member(member: Member):
    members = load_members()
    members.append(member.to_dict())
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(members,f,indent=2,ensure_ascii=False)
    return members

def update_member(email: str, updates: Dict):
    members = load_members()
    for m in members:
        if m["email"]==email:
            m.update(updates)
            m["verified"]=True
            break
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(members,f,indent=2,ensure_ascii=False)

def get_bursa_stats():
    members = load_members()
    total=len(members)
    emp=len([m for m in members if m.get("kategori")=="EMPLOYEE"])
    ent=len([m for m in members if m.get("kategori")=="ENTREPRENEUR"])
    return {"total":total,"employee":emp,"entrepreneur":ent,"total_vote":total}

def get_bursa_billboard():
    members=load_members()
    return sorted(members,key=lambda x:x.get("tgl_daftar",""),reverse=True)

def get_5_rak_storage():
    return {
        "RAK 1 - SOP Kebersihan & Obedience": "SOP Obedience - Setia hal kecil, dipercaya hal besar. Checklist kebersihan harian wajib Staff-Supervisor, dicek Pimpinan.",
        "RAK 2 - ERP Jam 9": "ERP - Struktur usaha umum, owner kecil masuk ERP. Check-in 09:00 WIB wajib semua jenjang, Supervisor & Manager monitoring.",
        "RAK 3 - OEE 95%": "OEE 95% - Availability 100% Hadir utuh, Performance 95%, Quality 95%. Target diri konsisten, bukan sempurna.",
        "RAK 4 - KPI Performance": "KPI - Employee: apply & kehadiran. Entrepreneur: posting & retensi. Semua terukur otomatis di bursa volume.",
        "RAK 5 - ALKITAB & Ruach Hakadosh": "Fondasi Teduh, Terikat, Tumbuh. Bimbingan Ruach Hakadosh - Roh Kudus menuntun dalam pekerjaan."
    }

def get_bimbingan_ai_response(q: str):
    ql=q.lower()
    if "bimbang" in ql or "kerja" in ql:
        return "Teduh dulu. 1 arsip = 1 kesempatan. Tetap di bursa, Ruach Hakadosh buka jalan."
    if "sop" in ql:
        return "SOP menjaga langkahmu tetap bersih dan taat. Lakukan hari ini."
    if "erp" in ql:
        return "ERP mengikat kita dalam satu struktur. Jam 9 adalah komitmen bersama."
    if "oee" in ql:
        return "OEE 95% - Hadir utuh 100%, kerja 95%, hasil 95%."
    if "kpi" in ql:
        return "KPI mengukur tumbuhmu. 1 vote hari ini adalah benih esok."
    return "Di Storage ini, SOP, ERP, OEE, KPI dan Alkitab menuntunmu. Teduh, Terikat, Tumbuh."
