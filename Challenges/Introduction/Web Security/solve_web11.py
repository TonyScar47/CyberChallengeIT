import requests
import json
import sys

# ==========================================
# CTF Web Challenge: CSRF Token Automation
# Versione Debug-Ready
# ==========================================

BASE_URL = "http://web-11.challs.olicyber.it"

def solve_challenge():
    print("[*] Inizializzazione della Sessione...")
    session = requests.Session()
    
    # 1. Fase di Login
    login_url = f"{BASE_URL}/login"
    credentials = {"username": "admin", "password": "admin"}
    
    try:
        response = session.post(login_url, json=credentials)
        response.raise_for_status()
        
        # Debug della risposta di Login
        login_data = response.json()
        print(f"[DEBUG] Login response:\n{json.dumps(login_data, indent=4)}")
        
        current_token = login_data.get("token")
        
        if not current_token:
            print("[-] Errore: Token CSRF non trovato.")
            sys.exit(1)
            
        print("[+] Login effettuato. Token iniziale acquisito.")
        
    except requests.exceptions.RequestException as e:
        print(f"[-] Errore di connessione: {e}")
        sys.exit(1)

    # 2. Fase di Estrazione della Flag
    flag = ""
    piece_url = f"{BASE_URL}/flag_piece"
    
    for i in range(4):
        print(f"\n[*] Recupero il frammento {i}...")
        
        params = {"index": i, "token": current_token}
        
        try:
            res = session.get(piece_url, params=params)
            res.raise_for_status()
            
            # --- DEBUGGING ATTIVO ---
            # Questo ti permette di vedere esattamente cosa restituisce il server
            # ad ogni passo del loop
            piece_data = res.json()
            print(f"[DEBUG] Risposta frammento {i}:\n{json.dumps(piece_data, indent=4)}")
            # ------------------------
            
            # Aggiungiamo il pezzo alla flag
            flag += piece_data.get("flag_piece", "")
            
            # Aggiorniamo il token per la prossima iterazione
            current_token = piece_data.get("token")
            
        except requests.exceptions.RequestException as e:
            print(f"[-] Errore durante il recupero del frammento {i}: {e}")
            sys.exit(1)

    print(f"\n[+] Operazione completata!")
    print(f"[!] La flag è: {flag}")

if __name__ == "__main__":
    solve_challenge()
