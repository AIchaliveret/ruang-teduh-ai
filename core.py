# core.py - Otak System Ruang Teduh AI V28.1
# Flow: SOP -> ERP -> OEE -> KPI Tersystematis
# Ruang Teduh AI - Tavo Malkhutkha

AUDIO_CONFIG = {
    "USE_MUSIC": False,
    "USE_MUSIC_STRESS": False,
    "MODE": "V28.1_NO_MUSIC - Worship Teduh Slow Piano + Nature - Klik untuk bunyi",
    "FILES": {
        "Ruang1": "ruang1_V28.1_NO_MUSIC.mp3",
        "Ruang2": "ruang2_V28.1_NO_MUSIC.mp3",
        "Ruang3": "ruang3_V28.1_NO_MUSIC.mp3"
    }
}

SOP_CONFIG = {
    "ayat": "Kolose 3:23 - Apapun juga yang kamu perbuat, perbuatlah dengan segenap hatimu seperti untuk Tuhan",
    "cek_kebersihan": "Senin pagi cek kebersihan Ruang Teduh",
    "flow": "Datang -> Doa -> Kerja -> Evaluasi"
}

ERP_CONFIG = {
    "Manusia": "Employee wellbeing max 60km dari rumah",
    "Material": "Stok & alat - Update Selasa jam 9 pagi",
    "Money": "UMR Rp 4,900,000 - Transparan",
    "Machine": "Mesin 1 target OEE 95%",
    "Method": "SOP terdokumentasi"
}

OEE_CONFIG = {
    "Availability": "100% - Hadir & siap",
    "Performance": "1% better setiap hari",
    "Quality": "Zero defect mindset",
    "Target": "Rabu cek OEE mesin 1 95%"
}

KPI_CONFIG = {
    "ayat": "Amsal 16:3 - Serahkanlah perbuatanmu kepada TUHAN, maka terlaksanalah segala rencanamu",
    "indikator": ["Kehadiran", "Kebersihan", "Ketepatan SOP", "OEE", "Wellbeing"]
}

QRIS_CONFIG = {
    "QRIS": "QRIS Ruang Teduh",
    "VA_BCA": "VA BCA - Ruang Teduh",
    "VA_Mandiri": "VA Mandiri - Ruang Teduh",
    "VA_BRI": "VA BRI - Ruang Teduh"
}

SYSTEM_FLOW = ["SOP", "ERP", "OEE", "KPI"]

def cek_email_wajib(email):
    if not email or "@" not in email or "." not in email:
        return False, "Bro, mesti kasih alamat email dulu yang valid ya"
    return True, f"Email terkonfirmasi: {email}"

def load_fondasi():
    return "Kolom1_Fondasi.pdf - Fondasi Ruang Teduh"

def get_system_status():
    return {
        "flow": " -> ".join(SYSTEM_FLOW),
        "audio": AUDIO_CONFIG["MODE"],
        "sop": SOP_CONFIG,
        "erp": ERP_CONFIG,
        "oee": OEE_CONFIG,
        "kpi": KPI_CONFIG
}
