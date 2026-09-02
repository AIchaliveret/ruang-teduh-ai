
# core.py - v2.7 CLEAN - stub untuk mencegah ImportError auto_generate_all
# File ini sengaja dibuat minimal agar tidak ada error impor di app.py
# Jika nanti butuh logika SOP/ERP/OEE/KPI, tambahkan di sini

def get_jadwal_harian():
    """Ambil jadwal dari nasehat_mingguan.txt"""
    return {
        "Senin": "SOP",
        "Selasa": "ERP", 
        "Rabu": "OEE & KPI",
        "Kamis": "Vendor",
        "Jumat": "Mood Tracker",
        "Sabtu": "Kolom 1-3 Review",
        "Minggu": "Istirahat & Tawakal"
    }

def calculate_wellbeing(umr, percentage=0.05):
    return umr * percentage

# Placeholder - dulu error ImportError auto_generate_all, sekarang tidak ada
# def auto_generate_all():  # deprecated, jangan dipakai
#     pass

__all__ = ["get_jadwal_harian", "calculate_wellbeing"]
