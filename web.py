import requests
import re

def hunt_for_flag(url):
    # Aggiungiamo un controllo per assicurarci che l'URL inizi con http:// o https://
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    print(f"\n[*] Inizio la scansione automatica su: {url}")
    
    # La Regex: Cerca pattern come flag{...} o CCIT{...}
    pattern = re.compile(r'(flag\{.*?\}|CCIT\{.*?\})', re.IGNORECASE)
    
    try:
        # Effettuiamo la richiesta GET al server
        response = requests.get(url, timeout=5)
        trovata = False
        
        # 1. Caccia nel codice sorgente (HTML)
        matches_html = pattern.findall(response.text)
        if matches_html:
            print(f"[+] BINGO! Trovata nel sorgente HTML: {matches_html[0]}")
            trovata = True
            
        # 2. Caccia negli HTTP Headers
        for header, value in response.headers.items():
            matches_header = pattern.findall(value)
            if matches_header:
                print(f"[+] BINGO! Trovata nell'Header '{header}': {matches_header[0]}")
                trovata = True
                
        # 3. Caccia nei Cookie
        for cookie in response.cookies:
            matches_cookie = pattern.findall(cookie.value)
            if matches_cookie:
                print(f"[+] BINGO! Trovata nel Cookie '{cookie.name}': {matches_cookie[0]}")
                trovata = True

        if not trovata:
            print("[-] Non trovata nei posti standard. Provo su /robots.txt...")
            rob_resp = requests.get(url.rstrip('/') + "/robots.txt", timeout=5)
            if rob_resp.status_code == 200:
                rob_matches = pattern.findall(rob_resp.text)
                if rob_matches:
                    print(f"[+] BINGO! Trovata in robots.txt: {rob_matches[0]}")
                else:
                    print("[-] Niente da fare, non è nemmeno in robots.txt.")
            else:
                print("[-] Il file robots.txt non esiste su questo server.")
                    
    except requests.exceptions.RequestException as e:
        print(f"[-] Errore di connessione. Verifica che il link sia corretto: {e}")

# --- LA PARTE INTERATTIVA ---
print("=========================================")
print("   WEB FLAG HUNTER - CyberChallenge      ")
print("=========================================")

# Il programma si ferma e aspetta il tuo Ctrl+V
bersaglio = input("Inserisci il link della challenge (e premi Invio): ").strip()

# Lanciamo l'attacco passando il link che hai appena incollato
hunt_for_flag(bersaglio)
