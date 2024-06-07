import asyncio
from datetime import datetime
import sys

def hari():
    n = datetime.now()
    return n.strftime('%A, %d %B %Y %H:%M:%S')

def read_contacts(file_path):
    contacts = []
    with open(file_path, encoding="utf-8") as file:
        for line in file:
            contacts.append(line.strip())
    return contacts

async def send_telegram_message(api_id, api_hash, phone_number, penerima, pesan, watermark, file_path=None):
    from telethon.sync import TelegramClient
    from telethon.errors.rpcerrorlist import FloodWaitError

    async with TelegramClient('session_name', api_id, api_hash) as client:
        await client.start(phone_number)
        print("Client has been created successfully.")

        for contact in penerima:
            while True:
                try:
                    message_to_send = pesan + ("\n\n" + watermark if watermark else "")
                    if file_path:
                        await client.send_file(contact, file=file_path, caption=message_to_send)
                    else:
                        await client.send_message(contact, message_to_send)
                    print(f"{hari()} -> Pesan terkirim ke {contact}")
                    break  # Jika pesan terkirim berhasil, keluar dari perulangan
                except FloodWaitError as e:
                    print(f"Gagal mengirim pesan ke {contact}: {e}")
                    retry_after = e.seconds
                    print(f"Menunggu {retry_after} detik sebelum mencoba lagi...")
                    while retry_after > 0:
                        print(f"Menunggu {retry_after} detik...", end='\r')
                        await asyncio.sleep(1)
                        retry_after -= 1
                    print("Melanjutkan pengiriman pesan...")
                    continue
                except Exception as e:
                    print(f"Gagal mengirim pesan ke {contact}: {e}")
                    break  # Jika terjadi exception selain FloodWaitError, keluar dari perulangan
        print("Message sent successfully.")

async def main():
    if len(sys.argv) != 8:
        print("Penggunaan: python apk.py <api_id> <api_hash> <phone_number> <watermark> <watermark_text> <tanggal_akhir> <jeda>")
        sys.exit(1)

    api_id, api_hash, phone_number, watermark, watermark_text, tanggal_akhir, jeda = sys.argv[1:]

    api_id = int(api_id)
    jeda = int(jeda)
    tanggal_akhir = datetime.strptime(tanggal_akhir, "%d-%m-%Y %H:%M")

    message_file = 'pesan.txt'
    contacts_file = 'user.txt'
    file_path = None

    with open(message_file, encoding="utf-8") as file:
        message_text = file.read()

    user_contacts = read_contacts(contacts_file)

    jumlah_pesan = int((tanggal_akhir - datetime.now()).total_seconds() / jeda)

    for _ in range(jumlah_pesan):
        await send_telegram_message(api_id, api_hash, phone_number, user_contacts, message_text, watermark_text if watermark == "yes" else None, file_path)
        await asyncio.sleep(jeda)

if __name__ == '__main__':
    asyncio.run(main())
