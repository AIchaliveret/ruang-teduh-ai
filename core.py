# core.py - V28.2 AUTO FIX - Otak System Ruang Teduh
import random
from pathlib import Path

AUDIO_CONFIG = {
    "USE_MUSIC": False,
    "USE_MUSIC_STRESS": False,
    "FORCE_VOICE_ONLY": True,
    "MODE": "V28.2_AUTO - Voice Only Tanpa Musik Stress",
    "FILES": {
        "Ruang1": "ruang1_V28.1_NO_MUSIC.mp3",
        "ATURAN_UTAMA": "aturan_utama_voice_only.mp3"
    }
}
SOP_CONFIG = {"ayat": "Kolose 3:23", "flow": "Datang -> Doa -> Kerja -> Evaluasi", "aturan": "Kerja max 60km dari rumah - jaga keluarga, jaga hati"}
ERP_CONFIG = {"Manusia": "keluarga, hati", "Material": "waktu, 60km dari rumah", "Money": "UMR Domisili Rp 10.000.000", "Machine": "Mesin 1 OEE 95%", "Method": "SOP terdokumentasi"}
OEE_CONFIG = {"Availability": "Hadir 100%", "Performance": "Tidak mengeluh, 1% better tiap hari", "Quality": "Hasil kerja memuliakan Tuhan", "Target": "95%"}
KPI_CONFIG = {"ayat": "Amsal 16:3", "indikator": ["Kehadiran", "Kebersihan", "Ketepatan SOP", "OEE", "Wellbeing"]}

def get_audio_aturan_utama():
    # paksa voice only, gak pernah panggil file stress
    return AUDIO_CONFIG["FILES"]["ATURAN_UTAMA"] if Path(AUDIO_CONFIG["FILES"]["ATURAN_UTAMA"]).exists() else AUDIO_CONFIG["FILES"]["Ruang1"]

def get_suara_teduh_lengkap():
    return f"{SOP_CONFIG['ayat']} - {SOP_CONFIG['flow']}. ERP: Manusia={ERP_CONFIG['Manusia']}, Material={ERP_CONFIG['Material']}. OEE: {OEE_CONFIG['Availability']}, {OEE_CONFIG['Performance']}. KPI: {', '.join(KPI_CONFIG['indikator'])}. {KPI_CONFIG['ayat']}"

def auto_generate_all():
    # ini yang bikin otomatis kayak v2.7
    return {
        "sop": SOP_CONFIG,
        "erp": ERP_CONFIG,
        "oee": OEE_CONFIG,
        "kpi": KPI_CONFIG,
        "nasehat": get_suara_teduh_lengkap(),
        "audio": get_audio_aturan_utama()
}
