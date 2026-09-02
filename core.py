"""
core.py - OTAK Ruang Teduh | LEMBAR MERAH - TEMBUSAN 1
Three Way NCR - Buku 1 Ruang 3 Lembar
Sesuai struktur organisasi perusahaan real
"""
from datetime import datetime, date
import io

class RuangTeduhCore:
    def __init__(self):
        self.nasehat_path = "nasehat_mingguan.txt"
        self.member_db = {}  # email -> full org data
        self.bursa_kerja = [
            {"id":1, "posted_by":"Budi - Director", "posted_email":"budi@teduh.id", "role_needed":"Supervisor Kebersihan", "level":"Supervisor", "zona":"Jakarta Selatan", "deskripsi":"Lead tim SOP jam 7-9 pagi, cek kebersihan", "tarif":"2.5jt/bulan"},
            {"id":2, "posted_by":"Sari - Business Owner", "posted_email":"sari@teduh.id", "role_needed":"Staff Barista", "level":"Staff", "zona":"Jakarta Pusat", "deskripsi":"Jam 9-17, handle ERP", "tarif":"1.5jt/bulan"},
        ]

    def load_nasehat(self):
        try:
            with open(self.nasehat_path, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip()]
        except:
            return [
                "Teduh itu bukan menghindar, tapi mengelola.",
                "Employee setia = konsisten jam 9 pagi.",
                "Entrepreneur 50rb = ikatan, bukan biaya."
            ]

    def get_nasehat_mingguan(self):
        all_n = self.load_nasehat()
        week = datetime.now().isocalendar()[1]
        return all_n[week % len(all_n)]

    def tts_payload(self, text):
        """Payload untuk gTTS / Web Speech API - saran lu: nasehat bisa dibacakan speaker"""
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang='id', slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp
        except:
            return {"text": text, "voice": "id-ID", "speed": 0.9}

    # === REGISTRASI ORG LENGKAP - SESUAI PERMINTAAN LU TERBARU ===
    def register_org(self, data: dict):
        """
        data wajib: nama, tempat_lahir, tgl_lahir, email, no_hp, zona, pendidikan, jurusan, tahun_pengalaman, pengalaman_detail, main_role, jabatan
        main_role: employee (Staff s/d Supervisor) | entrepreneur (Manager s/d Business Owner)
        """
        email = data["email"]
        tarif = 30000 if data["main_role"] == "employee" else 50000
        
        # Wewenang sesuai jenjang
        if data["main_role"] == "employee":
            wewenang = f"{data['jabatan']} (Employee) - Wewenang: Melamar loker, akses chat, SOP Kebersihan, ERP Jam 9. Level {data['jabatan']} tidak bisa posting loker."
        else:
            wewenang = f"{data['jabatan']} (Entrepreneur) - Wewenang: Posting loker, approve lamaran {data['jabatan']} ke bawah, kelola KPI/OEE, Full 5 Rak SOP/ERP/OEE/KPI/ALKITAB, QRIS VA + Invoice."

        self.member_db[email] = {
            **data,
            "tarif": tarif,
            "wewenang": wewenang,
            "ikatan_score": 0,
            "joined": datetime.now().isoformat(),
            "status": "VALIDASI - TEMBUS 3 LEMBAR"
        }
        return self.member_db[email]

    def post_loker(self, entrepreneur_email, judul, level_butuh, zona, desk, tarif_loker):
        member = self.member_db.get(entrepreneur_email)
        if not member or member["main_role"] != "entrepreneur":
            return False, "Hanya Entrepreneur (Manager s/d Business Owner) yang bisa posting loker - sesuai wewenang pimpinan"
        loker = {
            "id": len(self.bursa_kerja)+1,
            "posted_by": f"{member['nama']} - {member['jabatan']}",
            "posted_email": entrepreneur_email,
            "role_needed": judul,
            "level": level_butuh,
            "zona": zona,
            "deskripsi": desk,
            "tarif": tarif_loker,
            "created": datetime.now().isoformat()
        }
        self.bursa_kerja.append(loker)
        member["ikatan_score"] += 5
        return True, loker

    def apply_loker(self, employee_email, loker_id):
        member = self.member_db.get(employee_email)
        if not member or member["main_role"] != "employee":
            return False, "Hanya Employee (Staff s/d Supervisor) yang bisa melamar - sesuai struktur org"
        member["ikatan_score"] += 10
        return True, f"{member['nama']} ({member['jabatan']}) berhasil melamar loker #{loker_id}. Ikatan +10. Data lengkap (nama, TTL, pendidikan, zona, pengalaman) terkirim ke entrepreneur."

    def get_org_chart(self):
        """Return org chart untuk README & flowchart"""
        return {
            "EMPLOYEE_30K": ["Staff", "Senior Staff", "Supervisor"],
            "ENTREPRENEUR_50K": ["Manager", "General Manager", "Director", "Business Owner - Pimpinan Utama"]
        }

core = RuangTeduhCore()
