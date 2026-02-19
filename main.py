import requests
import re
from concurrent.futures import ThreadPoolExecutor

# Estetica e Colori (ANSI escape codes)
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def check_url(url, pattern):
    try:
        # Camuffiamo lo script da Firefox su Linux
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}
        response = requests.get(url, headers=headers, timeout=3)
        
        found = []
        # Cerca nel testo e negli headers
        found.extend(pattern.findall(response.text))
        for h_val in response.headers.values():
            found.extend(pattern.findall(h_val))
            
        if found:
            for f in set(found): # set() rimuove i duplicati
                print(f"{GREEN}[+] BINGO su {url}: {f}{RESET}")
            return True
        return False
    except:
        return False

def upgrade_hunt():
    print(f"{YELLOW}=== WEB FLAG HUNTER v2.0 (Pro Edition) ==={RESET}")
    target = input("Incolla il link (es. https://sito.it): ").strip().rstrip('/')
    
    if not target.startswith("http"):
        target = "https://" + target

    pattern = re.compile(r'(flag\{.*?\}|CCIT\{.*?\})', re.IGNORECASE)
    
    # Lista di pagine "sospette" comuni nelle CTF
    common_paths = [
        '',              # Home page
        '/robots.txt', 
        '/sitemap.xml',
        '/.env',         # File di configurazione spesso dimenticati
        '/.git/config',  # Repository Git esposti
        '/admin',
        '/secret',
        '/flag.txt',
        '/config.php'
    ]

    print(f"[*] Scansione intelligente avviata su {len(common_paths)} percorsi...\n")

    # Usiamo i Thread per controllare tutto in parallelo (super veloce)
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(check_url, target + path, pattern) for path in common_paths]
        
    print(f"\n{YELLOW}[*] Scansione completata.{RESET}")

if __name__ == "__main__":
    upgrade_hunt()