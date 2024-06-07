import asyncio
from datetime import datetime
import sys
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError

def get_forward_chat_ids(filename):
    """Fungsi untuk membaca chat ID dari file."""
    with open(filename, 'r', encoding='utf-8') as file:
        chat_ids = [line.strip() for line in file]
    return chat_ids

async def validate_chat_ids(client, chat_ids):
    """Fungsi untuk memvalidasi chat ID yang akan digunakan."""
    valid_chat_ids = []
    for chat_id in chat_ids:
        try:
            entity = await client.get_entity(chat_id)
            valid_chat_ids.append(entity)
            print(f"Chat ID {chat_id} valid: {entity.title}")
        except Exception as e:
            print(f"Chat ID {chat_id} tidak valid: {e}")
    return valid_chat_ids

async def forward_message_to_groups(client, message, valid_chat_ids):
    """Fungsi untuk meneruskan pesan ke grup yang valid."""
    for chat_id in valid_chat_ids:
        try:
            await client.forward_messages(chat_id, message)
            print(f"Pesan berhasil diteruskan ke {chat_id.title} pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except FloodWaitError as e:
            print(f"FloodWaitError: {e}. Menunggu {e.seconds} detik...")
            await asyncio.sleep(e.seconds)
            await client.forward_messages(chat_id, message)  # Coba lagi setelah menunggu
        except Exception as e:
            print(f"Pesan gagal diteruskan ke {chat_id.title}: {e}")

async def main():
    if len(sys.argv) != 6:
        print("Penggunaan: python bot.py <api_id> <api_hash> <phone_number> <tanggal_akhir> <jeda>")
        sys.exit(1)

    api_id, api_hash, phone_number, tanggal_akhir_str, jeda_str = sys.argv[1:]

    api_id = int(api_id)
    jeda = int(jeda_str)
    tanggal_akhir = datetime.strptime(tanggal_akhir_str, "%d-%m-%Y %H:%M")

    client = TelegramClient('session_name', api_id, api_hash)

    async with client:
        await client.start(phone_number)
        print("Client telah berhasil dimulai.")

        valid_chat_ids = await validate_chat_ids(client, get_forward_chat_ids('user.txt'))
        if not valid_chat_ids:
            print("Tidak ada chat ID yang valid ditemukan. Keluar...")
            return

        print("Bot siap menerima pesan untuk diteruskan...")

        while datetime.now() < tanggal_akhir:
            try:
                messages = await client.get_messages('@JenderalKolonel', limit=1)
                if messages:
                    await forward_message_to_groups(client, messages, valid_chat_ids)
                print("Semua pesan berhasil diteruskan, menunggu untuk mengulang...")
                await asyncio.sleep(jeda)
            except FloodWaitError as e:
                print(f"FloodWaitError: {e}. Menunggu {e.seconds} detik...")
                await asyncio.sleep(e.seconds)

if __name__ == "__main__":
    asyncio.run(main())
