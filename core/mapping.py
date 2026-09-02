"""
CORE - Ruang Teduh AI - TAVO MALKHUTKHA
V28.1 AUDIO FIX
Developer: aichaliveret
"""

CORE_IDENTITAS = "Ruang Teduh AI - TAVO MALKHUTKHA"
CORE_VERSION = "V28.1 AUDIO FIX + V2.7 Wellbeing Library"
CORE_WELLBEING = "Kerja max 60km dari rumah"

# === ATURAN UTAMA TERSYSTEMATIS ===
def aturan_utama_tersystematis(pertanyaan, umr="4,900,000"):
    """
    Semua jawaban WAJIB lewat: SOP -> ERP -> OEE -> KPI -> Disempurnakan Alkitab
    + WAJIB Audio No 1
    """
    return {
        "SOP": {
            "ayat": "Kolose 3:23",
            "isi": "Datang, Doa, Kerja seperti untuk Tuhan bukan manusia",
            "action": f"Cek kebersihan & hadapi {pertanyaan} dengan doa"
        },
        "ERP": {
            "versi": "Hati",
            "M1_Manusia": "Keluarga, hati - prioritas",
            "M2_Material": "Waktu, 60km dari rumah, update stok jam 9 pagi",
            "M3_Money": f"UMR Domisili Rp {umr}"
        },
        "OEE": {
            "versi": "Rohani",
            "Availability": "Hadir 100% tepat waktu - jangan sepi",
            "Performance": "1% better tiap hari, tidak mengeluh",
            "Quality": "Hasil memuliakan Tuhan - OEE Mesin 1 target 95%",
            "target": "95%"
        },
        "KPI": {
            "ayat": "Amsal 16:3",
            "isi": "Serahkan perbuatanmu kepada Tuhan, maka terlaksanalah rencanamu",
            "formula": "KPI Iman + KPI Kerja = Improvement Culture"
        }
    }

# === AUDIO CONFIG V28.1 ===
AUDIO_CONFIG = {
    "USE_MUSIC_STRESS": False,
    "BACKGROUND": "Worship Teduh Instrumental - Slow Piano + Nature",
    "MODE": "Klik untuk bunyi, gak auto - Speaker PASTI bunyi asal di-KLIK",
    "FILES": {
        "Ruang1": "ruang1_V28.1_NO_MUSIC.mp3",
        "Ruang2": "ruang2_V28.1_NO_MUSIC.mp3",
        "Ruang3": "ruang3_V28.1_NO_MUSIC.mp3",
        "AturanUtama": "aturan_utama_tersystematis_V28.1.mp3"
    }
}

# === JADWAL NASEHAT MINGGUAN ===
JADWAL = {
    "Senin": "SOP cek kebersihan - Kolose 3:23",
    "Selasa": "ERP update stok jam 9 pagi - M: Manusia, Material, Money",
    "Rabu": "OEE mesin 1 harus 95% - Availability, Performance, Quality",
    "Kamis": "KPI Amsal 16:3 - Serahkan perbuatanmu",
    "Jumat": "Audio Worship Teduh - V28.1 FIX",
    "Sabtu": "Wellbeing Library - Floating Dot Kolom Lo"
}

def cek_email_wajib(email):
    """ATURAN PEMBAYARAN v2.7 - WAJIB email sebelum bayar"""
    import re
    if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Bro, mesti kasih alamat email dulu yang valid ya, biar QR & VA bisa kekirim."
    return True, f"Email terkonfirmasi: {email} - Invoice & Akses akan dikirim kesini."

# Flag doang gak cukup - harus ganti nama file + reboot
DEPLOY_NOTE = """
CRITICAL FIX Streamlit Cloud:
- Flag USE_MUSIC=False doang gak cukup karena cache
- Wajib: Hapus file musik_teduh.mp3
- Wajib: Rename file audio jadi *_V28.1_NO_MUSIC.mp3
- Wajib: Reboot app di dashboard Streamlit Cloud -> Clear cache
"""
