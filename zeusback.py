import os
import sys
import time
import subprocess
import importlib.util
import signal
import requests
import re
import urllib.parse
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
import validators

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_package_installed(package):
    return importlib.util.find_spec(package) is not None

def install_package(package):
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print(f"{Fore.GREEN}[+] {Fore.WHITE}{package} {Fore.GREEN}successfully deployed!")
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}[!] Critical failure installing {package}!")

def check_and_install_packages(packages):
    for package in packages:
        if is_package_installed(package):
            print(f"{Fore.GREEN}[+] {Fore.WHITE}{package} {Fore.GREEN}already armed!")
        else:
            print(f"{Fore.YELLOW}[!] {package} missing. Deploying payload...") 
            install_package(package)

def load_config():
    return ["colorama", "requests", "validators"]

def handle_interrupt(signal, frame):
    print(f"\n{Fore.RED}[!] MISSION ABORTED!")
    sys.exit(0)

def get_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

def fetch_status_code(url):
    try:
        head_response = requests.head(url, timeout=5)
        return url, head_response.status_code
    except requests.exceptions.Timeout:
        return url, "TIMEOUT"
    except requests.exceptions.RequestException as e:
        return url, "TARGET LOST"

def fetch_and_filter_wayback_info(domain):
    hits = 0
    urls_to_save = []
    start_time = time.time()
    print(f"{Fore.MAGENTA}🌀 ZEUSBACK INITIATED {Fore.WHITE}|| {Fore.CYAN}TARGET: {Fore.WHITE}{domain}")
    time.sleep(2)
    print(f"{Fore.YELLOW}\n[⚡] DEPLOYING ZEUS SCAN...\n")

    base_url = "https://web.archive.org/cdx/search/cdx"
    
    params = {
        'url': f"*.{domain}/*",
        'collapse': 'urlkey',
        'output': 'text',
        'fl': 'original'
    }

    file_extensions_regex = r'\.xls|\.xml|\.xlsx|\.json|\.pdf|\.sli|\.doc|\.docx|\.pptx|\.txt|\.zip|\.tar|\.gz|\.tgz|\.bak|\.7z|\.rar|\.log|\.cache|\.secret|\.db|\.backup|\.yml|\.gz|\.config|\.csv|\.yaml|\.md|\.md5|\.exe|\.dll|\.bin|\.ini|\.bat|\.sh|\.deb|\.rpm|\.iso|\.img|\.apk|\.msi|\.dmg|\.tmp|\.crt|\.pem|\.key|\.pub|\.asc'
    
    try:
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            urls = response.text.splitlines()
            filtered_urls = [url.strip() for url in urls if re.search(file_extensions_regex, url)]
            
            if filtered_urls:
                with ThreadPoolExecutor() as executor:
                    futures = {executor.submit(fetch_status_code, url): url for url in filtered_urls}
                    
                    for idx, future in enumerate(as_completed(futures), start=1):
                        url, status_code = future.result()
                        encoded_url = urllib.parse.quote(url, safe=':/')
                        
                        index_str = f"[{idx:02}]" 
                        
                        if "TIMEOUT" in str(status_code) or "TARGET LOST" in str(status_code):
                            print(f"{Fore.RED}☠️ {index_str} {Fore.WHITE}{url} {Fore.YELLOW}>> {Fore.RED}{status_code}")
                        else:
                            print(f"{Fore.GREEN}🔥 {index_str} {Fore.WHITE}{url} {Fore.YELLOW}>> {Fore.CYAN}{status_code}")
                        print(f"{Fore.MAGENTA}└─ {Fore.BLUE}ARCHIVE: {Fore.WHITE}https://web.archive.org/web/*/{encoded_url}")
                        print()
                        hits += 1
                        urls_to_save.append(url)
            else:
                print(f"{Fore.RED}[!] TARGET CLEAN - NO VULNERABILITIES FOUND\n")
        else:
            print(f"{Fore.RED}[!] CONNECTION TERMINATED - TARGET FIGHTING BACK!\n")
    except Exception as e:
        print(f"{Fore.RED}[!] SYSTEM FAILURE: {e}")
    
    end_time = time.time()
    time_taken = end_time - start_time
    print(f"{Fore.YELLOW}[⌛] OPERATION COMPLETED IN {time_taken:.2f}s")
    time.sleep(1)
    print(f"{Fore.CYAN}[🎯] TOTAL HITS: {hits}")

    if hits > 0:
        save_urls = input(f"{Fore.WHITE}\n[?] SAVE FINDINGS TO WAR ROOM? (Y/N): ").strip().lower()
        if save_urls == 'y':
            with open("zeus_report.txt", "w") as f:
                for url in urls_to_save:
                    f.write(url + "\n")
            print(f"{Fore.GREEN}[💾] DATA ARCHIVED: zeus_report.txt")
        else:
            print(f"{Fore.RED}[🗑️] MISSION DATA PURGED")

def validate_url(url):
    if validators.url(url):
        return True
    else:
        print(f"{Fore.RED}[!] INVALID TARGET COORDINATES!")
        return False

def Banner():
    print(rf"""
    {Fore.RED}███████╗███████╗███████╗██╗   ██╗███████╗██████╗  ██████╗ █████╗ ██╗  ██╗
    {Fore.RED}╚══███╔╝██╔════╝╚══███╔╝██║   ██║██╔════╝██╔══██╗██╔════╝██╔══██╗██║ ██╔╝
    {Fore.YELLOW}  ███╔╝ █████╗    ███╔╝ ██║   ██║█████╗  ██████╔╝██║     ███████║█████╔╝ 
    {Fore.YELLOW} ███╔╝  ██╔══╝   ███╔╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗██║     ██╔══██║██╔═██╗ 
    {Fore.GREEN}███████╗███████╗███████╗ ╚████╔╝ ███████╗██║  ██║╚██████╗██║  ██║██║  ██╗
    {Fore.GREEN}╚══════╝╚══════╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝
    {Fore.WHITE}                           [ {Fore.RED}ZeUs BaCk v2.0 {Fore.WHITE}]                          
    """)

    created_by_text = f"{Fore.WHITE}CODED BY {Fore.RED}ZeUsVuLn {Fore.WHITE}| {Fore.GREEN}GAZA SECURITY"
    print(" " * 10 + created_by_text)
    print("\n" + " " * 12 + f"{Fore.YELLOW}⚡ POWERED BY THE DARK WEB ARCHIVES ⚡\n")

def main():
    signal.signal(signal.SIGINT, handle_interrupt)
    
    clear_screen()
    print(f"{Fore.BLUE}[🔍] SCANNING FOR CYBER WEAPONS...\n")
    
    required_packages = load_config()
    check_and_install_packages(required_packages)

    time.sleep(3)

    clear_screen()
    Banner()
    
    while True:
        url = input(f"{Fore.WHITE}[🎯] ENTER TARGET URL ({Fore.RED}e.g. https://high-value-target.com{Fore.WHITE}): ")
        if validate_url(url):
            break
        input(f"{Fore.YELLOW}[⚠️] PRESS ENTER TO RE-ENGAGE...")
        clear_screen()
        Banner()

    print(f"{Fore.YELLOW}\n[⚡] INITIALIZING CYBER ATTACK VECTORS...")
    time.sleep(3)
    clear_screen()

    domain = get_domain(url)
    fetch_and_filter_wayback_info(domain)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Fore.RED}\n[!] CYBER ATTACK ABORTED!")
