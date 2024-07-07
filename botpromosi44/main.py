import subprocess
from datetime import datetime

# Fungsi untuk membaca API ID, API Hash, dan nomor dari token.txt
def baca_token():
    try:
        with open('token.txt', 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            api_id = None
            api_hash = None
            phone_number = None

            for line in lines:
                if line.startswith("api_id:"):
                    api_id = line.split("api_id:")[1].strip()
                elif line.startswith("api_hash:"):
                    api_hash = line.split("api_hash:")[1].strip()
                elif line.startswith("phone_number:"):
                    phone_number = line.split("phone_number:")[1].strip()

            if not api_id or not api_hash or not phone_number:
                raise ValueError("Isi file token tidak lengkap atau tidak valid.")
            return api_id, api_hash, phone_number

    except Exception as e:
        print(f"Error membaca token: {e}")
        return None, None, None

# Fungsi untuk menjalankan Jaseb Basic
def jalankan_jaseb_basic(api_id, api_hash, phone_number, watermark, watermark_text, tanggal_akhir, jeda):
    print("Menjalankan Jaseb Basic...")
    cmd = ["python3", "apk.py", api_id, api_hash, phone_number, watermark, watermark_text, tanggal_akhir.strftime("%d-%m-%Y %H:%M"), str(jeda)]
    subprocess.run(cmd)
    print("Jaseb Basic selesai.")

# Fungsi untuk menjalankan Jaseb Forward
def jalankan_jaseb_forward(api_id, api_hash, phone_number, tanggal_akhir, jeda):
    print("Menjalankan Jaseb Forward...")
    cmd = ["python3", "bot.py", api_id, api_hash, phone_number, tanggal_akhir.strftime("%d-%m-%Y %H:%M"), str(jeda)]
    subprocess.run(cmd)
    print("Jaseb Forward selesai.")

# Script utama
def main():
    api_id, api_hash, phone_number = baca_token()
    if not api_id or not api_hash or not phone_number:
        print("Tidak bisa membaca API ID, API Hash, atau Nomor.")
        return

    pilihan = input("Pilih mode: \n1. Jaseb Basic\n2. Jaseb Forward\nMasukkan pilihan (1/2): ")
    if pilihan not in ['1', '2']:
        print("Pilihan tidak valid.")
        return

    if pilihan == '1':
        watermark_pilihan = input("Gunakan watermark? (y/n): ").lower()
        watermark = "yes" if watermark_pilihan == 'y' else "no"
        watermark_text = "**JASEB OTOMATIS BY @ZYREIJASEB**"
    else:
        watermark = "no"
        watermark_text = ""

    tanggal_akhir_str = input("Masukkan tanggal dan jam berakhir (format: DD-MM-YYYY HH:MM): ")
    try:
        tanggal_akhir = datetime.strptime(tanggal_akhir_str, "%d-%m-%Y %H:%M")
    except ValueError:
        print("Format tanggal atau jam tidak valid.")
        return

    jeda_str = input("Masukkan jeda pengiriman pesan dalam detik: ")
    try:
        jeda = int(jeda_str)
    except ValueError:
        print("Jeda harus berupa angka.")
        return

    if pilihan == '1':
        jalankan_jaseb_basic(api_id, api_hash, phone_number, watermark, watermark_text, tanggal_akhir, jeda)
    elif pilihan == '2':
        jalankan_jaseb_forward(api_id, api_hash, phone_number, tanggal_akhir, jeda)

if __name__ == "__main__":
    main()
