# core/mapping.py
# Logika Ruang Teduh - Kerja Dekat Rumah max 60km

TETANGGA_DEKAT = {
  "Kab. Bandung": ["Kota Bandung", "Kab. Bandung Barat", "Sumedang", "Garut"],
  "Kota Bandung": ["Kab. Bandung", "Cimahi", "Kab. Bandung Barat"],
  "Kab. Badung": ["Kota Denpasar", "Gianyar", "Tabanan"],
  "Jakarta Selatan": ["Jakarta Pusat", "Jakarta Barat", "Jakarta Timur", "Depok"],
}

def cari_loker_dekat(domisili, semua_loker):
  lokasi_boleh = [domisili] + TETANGGA_DEKAT.get(domisili, [])
  return [l for l in semua_loker if l.get('lokasi') in lokasi_boleh]
