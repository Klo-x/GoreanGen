import os
import subprocess
from colorama import Fore
import requests
import random
import threading
from rgbprint import *

banner = f'''
      ________                                     ________               
     /  _____/  ___________   ____ _____    ____  /  _____/  ____   ____  
    /   \  ___ /  _ \_  __ \_/ __ \\__   \  /    \/   \  ____/ __ \ /    \\ 
    \    \_\  (  <_> )  | \/\  ___/ / __ \|   |  \    \_\  \  ___/|   |  \\ 
     \______  /\____/|__|    \___  >____  /___|  /\______  /\___  >___|  /
            \/                   \/     \/     \/        \/     \/     \/  v1.4 | Made By If0n
'''

def generate():
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWYYZ"
    numbers = "0123456789"

    amount = int(input(f"{Fore.CYAN}> How many to Generate ---( {Fore.RED}"))
    upper, lower, nums = True, True, True
    all_chars = ""

    if upper:
        all_chars += uppercase
    if lower:
        all_chars += lowercase
    if nums:
        all_chars += numbers

    count = 0
    length = 16

    n = open('nitros.txt', 'w+')
    for x in range(amount):
        code = "".join(random.sample(all_chars, length))
        n.write(code + "\n")
        count += 1
        print(f"{Fore.RED}{code}{Fore.CYAN} | Code Written ({Fore.RED}nitros.txt{Fore.CYAN}){Fore.RED} - x{count}{Fore.CYAN}/{Fore.RED}{amount}{Fore.CYAN}")
    n.close()

def check(nitros, proxies, index):
    nitro = nitros[index]
    proxy = random.choice(proxies)  # Randomly select a proxy for each nitro
    ProxyParam = {"http://": proxy, "https://": proxy}
    checkurl = requests.get(f"https://discordapp.com/api/v6/entitlements/gift-codes/{nitro}", proxies=ProxyParam, timeout=3)

    count = index + 1
    if checkurl.status_code == 200:
        print(f"{Fore.CYAN}[+] {Fore.GREEN}{nitro}{Fore.CYAN} | Valid Code{Fore.RED} - x{count}{Fore.CYAN}/{Fore.RED}{len(nitros)}")
    else:
        print(f"{Fore.CYAN}[+] {Fore.RED}{nitro}{Fore.CYAN} | Invalid Code{Fore.RED} - x{count}{Fore.CYAN}/{Fore.RED}{len(nitros)}")

def scrape_proxies():
    input(f"{Fore.CYAN}> Press ENTER To Scrape HTTP Proxies")
    url = requests.get("https://api.openproxylist.xyz/http.txt")
    url_result = url.text
    line_count = 0
    with open('proxies.txt', 'w') as proxy_scrape_list:
        proxy_scrape_list.write(url_result)
        with open('proxies.txt') as file:
            for line in file:
                if line != "\n":
                    line_count += 1
        print(f"{Fore.CYAN}[+] Scraped {Fore.RED}{line_count}{Fore.CYAN} Proxies ({Fore.RED}proxies.txt{Fore.CYAN})")
        input(f"{Fore.CYAN}> Press ENTER To Start Checking")

def main():

    gradient_print(
            f"{banner}\n",
            start_color=Color.dark_blue,
            end_color=Color.ghost_white
    )

    while True:
        gen_or_check = input(f"{Fore.CYAN}> Generate or Check? (g/c)---( {Fore.RED}")

        if gen_or_check == "g":
            generate_thread = threading.Thread(target=generate)
            generate_thread.start()
            generate_thread.join()
        elif gen_or_check == "c":
            nitros = open("nitros.txt", "r").read().split("\n")[:-1]
            proxies = open("proxies.txt", "r").read().split("\n")[:-1]

            scrape_proxies_thread = threading.Thread(target=scrape_proxies)
            scrape_proxies_thread.start()
            scrape_proxies_thread.join()

            check_threads = []
            for i in range(len(nitros)):
                thread = threading.Thread(target=check, args=(nitros, proxies, i))
                check_threads.append(thread)
                thread.start()

            for thread in check_threads:
                thread.join()

if __name__ == "__main__":
    main()
