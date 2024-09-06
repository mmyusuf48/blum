import argparse
import requests
import time
import datetime
from colorama import init, Fore, Style

init(autoreset=True)

start_time = datetime.datetime.now()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Blum BOT')
    parser.add_argument('--task', type=str, choices=['y', 'n'], help='Cek and Claim Task (y/n)')
    parser.add_argument('--reff', type=str, choices=['y', 'n'], help='Apakah ingin claim ref? (y/n, default n)')
    args = parser.parse_args()

    if args.task is None:
        task_input = input("Apakah Anda ingin cek dan claim task? (y/n, default n): ").strip().lower()
        args.task = task_input if task_input in ['y', 'n'] else 'n'

    if args.reff is None:
        reff_input = input("Apakah ingin claim ref? (y/n, default n): ").strip().lower()
        args.reff = reff_input if reff_input in ['y', 'n'] else 'n'

    return args

def get_new_token(query_id):
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://telegram.blum.codes",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    }
    data = {"query": query_id}
    url = "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"

    for attempt in range(3):
        print(f"\r{Fore.YELLOW+Style.BRIGHT}Mendapatkan token...", end="", flush=True)
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['token']['refresh']
        else:
            print(f"\r{Fore.RED+Style.BRIGHT}Gagal mendapatkan token, percobaan {attempt + 1}", flush=True)
    
    print(f"\r{Fore.RED+Style.BRIGHT}Gagal mendapatkan token setelah 3 percobaan.", flush=True)
    return None

def get_user_info(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.get('https://gateway.blum.codes/v1/user/me', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"{Fore.RED+Style.BRIGHT}Gagal mendapatkan informasi user")
        return None

def get_balance(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    for attempt in range(3):
        try:
            response = requests.get('https://game-domain.blum.codes/api/v1/user/balance', headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"\r{Fore.RED+Style.BRIGHT}Gagal mendapatkan saldo, percobaan {attempt + 1}", flush=True)
        except Exception as e:
            print(f"\r{Fore.RED+Style.BRIGHT}Error: {str(e)}", flush=True)
    print(f"\r{Fore.RED+Style.BRIGHT}Gagal mendapatkan saldo setelah 3 percobaan.", flush=True)
    return None

def claim_balance(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'content-length': '0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = requests.post('https://game-domain.blum.codes/api/v1/farming/claim', headers=headers)
        return response.json()
    except Exception as e:
        print(f"{Fore.RED+Style.BRIGHT}Gagal mengklaim saldo karena error: {e}")
    return None

def start_farming(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'content-length': '0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = requests.post('https://game-domain.blum.codes/api/v1/farming/start', headers=headers)
        return response.json()
    except Exception as e:
        print(f"{Fore.RED+Style.BRIGHT}Gagal memulai farming karena error: {e}")
    return None

def check_daily_reward(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'content-length': '0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    try:
        response = requests.post('https://game-domain.blum.codes/api/v1/daily-reward?offset=-420', headers=headers, timeout=10)
        return response.json() if response.status_code != 400 else response.text
    except requests.exceptions.Timeout:
        print(f"\r{Fore.RED+Style.BRIGHT}Gagal claim daily: Timeout")
    except requests.exceptions.RequestException as e:
        print(f"\r{Fore.RED+Style.BRIGHT}Error: {str(e)}")
    return None

def main():
    args = parse_arguments()
    cek_task_enable = args.task
    claim_ref_enable = args.reff

    with open('tgwebapp.txt', 'r') as file:
        query_ids = file.read().splitlines()

    while True:
        try:
            for index, query_id in enumerate(query_ids, start=1):
                token = get_new_token(query_id)
                if not token:
                    continue

                user_info = get_user_info(token)
                if not user_info:
                    continue

                print(f"{Fore.BLUE+Style.BRIGHT}\n====[{Fore.WHITE+Style.BRIGHT}Akun ke-{index} {user_info['username']}{Fore.BLUE+Style.BRIGHT}]====")  

                balance_info = get_balance(token)
                if not balance_info:
                    print(f"{Fore.RED+Style.BRIGHT}Gagal mendapatkan informasi balance")
                    continue

                available_balance = balance_info['availableBalance']
                balance = f"{float(available_balance):,.0f}".replace(",", ".")
                print(f"{Fore.YELLOW+Style.BRIGHT}[ Balance ]: {balance}")
                print(f"{Fore.MAGENTA+Style.BRIGHT}[ Tiket Game ]: {balance_info['playPasses']}")

                farming_info = balance_info.get('farming')
                if farming_info:
                    end_time_ms = farming_info['endTime']
                    end_time = datetime.datetime.fromtimestamp(end_time_ms / 1000.0, datetime.timezone.utc)
                    current_time = datetime.datetime.now(datetime.timezone.utc)
                    time_difference = end_time - current_time
                    hours_remaining = int(time_difference.total_seconds() // 3600)
                    minutes_remaining = int((time_difference.total_seconds() % 3600) // 60)
                    farming_balance = farming_info['balance']
                    farming_balance_formatted = f"{float(farming_balance):,.0f}".replace(",", ".")
                    print(f"{Fore.RED+Style.BRIGHT}[ Claim Balance ] : {hours_remaining} jam {minutes_remaining} menit | Balance: {farming_balance_formatted}")

                    if hours_remaining < 0:
                        print(f"{Fore.GREEN+Style.BRIGHT}[ Claim Balance ] : Claiming balance...")
                        claim_response = claim_balance(token)
                        if claim_response:
                            print(f"{Fore.GREEN+Style.BRIGHT}[ Claim Balance ] : Claimed: {claim_response['availableBalance']}")
                            print(f"{Fore.GREEN+Style.BRIGHT}[ Claim Balance ] : Starting farming...")
                            start_response = start_farming(token)
                            if start_response:
                                print(f"{Fore.GREEN+Style.BRIGHT}[ Claim Balance ] : Farming started.")
                            else:
                                print(f"{Fore.RED+Style.BRIGHT}[ Claim Balance ] : Gagal start farming")
                        else:
                            print(f"{Fore.RED+Style.BRIGHT}[ Claim Balance ] : Gagal claim")
                else:
                    print(f"{Fore.RED+Style.BRIGHT}[ Claim Balance ] : Gagal mendapatkan informasi farming")
                    print(f"{Fore.GREEN+Style.BRIGHT}[ Claim Balance ] : Claiming balance...")
                    claim_response = claim_balance(token)
                    if claim_response:
                        print(f"{Fore.GREEN+Style.BRIGHT}[ Claim Balance ] : Claimed")
                        print(f"{Fore.GREEN+Style.BRIGHT}[ Claim Balance ] : Starting farming...")
                        start_response = start_farming(token)
                        if start_response:
                            print(f"{Fore.GREEN+Style.BRIGHT}[ Claim Balance ] : Farming started.")
                        else:
                            print(f"{Fore.RED+Style.BRIGHT}[ Claim Balance ] : Gagal start farming")
                    else:
                        print(f"{Fore.RED+Style.BRIGHT}[ Claim Balance ] : Gagal claim")

                print(f"{Fore.CYAN+Style.BRIGHT}[ Daily Reward ] : Checking daily reward...")
                daily_reward_response = check_daily_reward(token)
                if daily_reward_response is None:
                    print(f"{Fore.RED+Style.BRIGHT}[ Daily Reward ] : Gagal cek hadiah harian")
                else:
                    if daily_reward_response == 'same day':
                        print(f"{Fore.CYAN+Style.BRIGHT}[ Daily Reward ] : Hadiah harian sudah diklaim hari ini")
                    elif daily_reward_response == 'OK':
                        print(f"{Fore.CYAN+Style.BRIGHT}[ Daily Reward ] : Hadiah harian berhasil diklaim!")
                    else:
                        print(f"{Fore.RED+Style.BRIGHT}[ Daily Reward ] : Gagal cek hadiah harian. {daily_reward_response}")

            print(f"\n{Fore.GREEN+Style.BRIGHT}========={Fore.WHITE+Style.BRIGHT}Semua akun berhasil di proses{Fore.GREEN+Style.BRIGHT}=========")
            print(f"\n{Fore.GREEN+Style.BRIGHT}Refreshing token...")

            waktu_tunggu = 1800  # 30 menit dalam detik
            for detik in range(waktu_tunggu, 0, -1):
                print(f"\r{Fore.CYAN}Menunggu waktu claim berikutnya dalam {Fore.WHITE}{detik // 60} menit {detik % 60} detik", end="", flush=True)
                time.sleep(1)
            print("\nWaktu claim berikutnya telah tiba!")

        except KeyboardInterrupt:
            print(f"\n{Fore.RED+Style.BRIGHT}Proses dihentikan paksa oleh anda!")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
