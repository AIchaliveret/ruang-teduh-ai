# core.py - Otak System Ruang Teduh AI V28.2 VOICE ONLY FIX
# Flow: SOP -> ERP -> OEE -> KPI Tersystematis

AUDIO_CONFIG = {
    "USE_MUSIC": False,
    "USE_MUSIC_STRESS": False,
    "FORCE_VOICE_ONLY": True, # KUNCI UTAMA - paksa tanpa musik stress
    "MODE": "V28.2_VOICE_ONLY - Worship Teduh Voice + Nasehat Sistematis",
    "FILES": {
        "Ruang1": "ruang1_V28.1_NO_MUSIC.mp3",
        "Ruang2": "ruang2_V28.1_NO_MUSIC.mp3",
        "Ruang3": "ruang3_V28.1_NO_MUSIC.mp3",
        "ATURAN_UTAMA": "aturan_utama_voice_only.mp3" # ini yang harusnya diputar
    }
}

SOP_CONFIG = {
    "ayat": "Kolose 3:23",
    "flow": "Datang -> Doa -> Kerja -> Evaluasi",
    "aturan": "Kerja max 60km dari rumah - jaga keluarga, jaga hati"
}
ERP_CONFIG = {
    "Manusia": "Employee wellbeing max 60km",
    "Material": "Update Selasa 9 pagi",
    "Money": "UMR Rp 4.900.000 Transparan",
    "Machine": "Mesin 1 target OEE 95%",
    "Method": "SOP terdokumentasi"
}
OEE_CONFIG = {"Availability": "100%", "Performance": "1% better", "Quality": "Zero defect", "Target": "95%"}
KPI_CONFIG = {"ayat": "Amsal 16:3", "indikator": ["Kehadiran", "Kebersihan", "Ketepatan SOP", "OEE", "Wellbeing"]}
QRIS_CONFIG = {"QRIS": "QRIS Ruang Teduh", "VA_BCA": "VA BCA", "VA_Mandiri": "VA Mandiri", "VA_BRI": "VA BRI"}

def cek_email_wajib(email):
    if not email or "@" not in email or "." not in email:
        return False, "Bro, mesti kasih alamat email dulu yang valid ya"
    return True, f"Email terkonfirmasi: {email}"

def load_fondasi():
    return "Kolom1_Fondasi.pdf"

# FIX UTAMA BIAR GAK MUNCUL MUSIK STRESS LAGI
def get_audio_aturan_utama():
    # Selalu paksa Voice Only, bukan musik
    if AUDIO_CONFIG["FORCE_VOICE_ONLY"]:
        return AUDIO_CONFIG["FILES"]["ATURAN_UTAMA"]
    return AUDIO_CONFIG["FILES"]["Ruang1"]

def get_suara_teduh_lengkap():
    # Ini yang lu mau: nasehat + prosedur aturan tersystematis (indikator kerja)
    indikator = ", ".join(KPI_CONFIG["indikator"])
    return f"""
    {SOP_CONFIG['ayat']}. 
    Aturan Ruang Teduh: {SOP_CONFIG['aturan']}.
    Flow kerja: {SOP_CONFIG['flow']}.
    Indikator kerja hari ini: {indikator}.
    {KPI_CONFIG['ayat']}.
    """

def get_system_status():
    return {"flow": "SOP -> ERP -> OEE -> KPI", "mode": AUDIO_CONFIG["MODE"], "force_voice": True}
