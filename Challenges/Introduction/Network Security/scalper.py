import sys
import os
import re
import binascii
from scapy.all import *

# Disabilita i messaggi di log non necessari di Scapy
conf.verb = 0

def check_base64(string):
    """Tenta di decodificare possibili flag in Base64"""
    try:
        # Cerca pattern che sembrano base64 (almeno 10 caratteri)
        potential = re.findall(r'[A-Za-z0-9+/]{10,}={0,2}', string)
        for p in potential:
            decoded = binascii.a2b_base64(p).decode('utf-8', errors='ignore')
            if "flag{" in decoded:
                return f"[FOUND B64] {decoded}"
    except:
        pass
    return None

def beast_mode_resolver(pcap_file):
    print(f"\n" + "="*50)
    print(f"[*] ATTACK MODE ON: Analizzando {pcap_file}")
    print("="*50)

    try:
        packets = rdpcap(pcap_file)
    except Exception as e:
        print(f"[!] Errore nel caricamento del file: {e}")
        return

    flag_pattern = re.compile(r'flag\{.*?\}')
    
    for i, pkt in enumerate(packets):
        # 1. Estrazione dati grezzi dal pacchetto
        # Proviamo a dumpare tutto il contenuto in formato stringa
        raw_content = str(pkt.show(dump=True))
        
        # 2. Ricerca Flag in chiaro (Regex)
        flags = flag_pattern.findall(raw_content)
        for f in flags:
            print(f"[+] [PKT {i+1}] FLAG TROVATA: {f}")

        # 3. Analisi Payload Raw (per Base64 e DNS)
        if pkt.haslayer(Raw):
            payload = pkt[Raw].load.decode(errors='ignore')
            
            # Controllo Base64
            b64_res = check_base64(payload)
            if b64_res:
                print(f"[+] [PKT {i+1}] {b64_res}")

        # 4. Caso speciale: DNS (Data Exfiltration)
        if pkt.haslayer(DNSQR):
            query = pkt[DNSQR].qname.decode()
            if "flag" in query:
                print(f"[!] [DNS] Query sospetta rilevata: {query}")

        # 5. Logica specifica per metadati (come Challenge 02)
        # Se non troviamo flag nel testo, proviamo a ricostruire il formato MAC/LEN
        if i == 3 and not flags: # Controllo il frame 4
            if pkt.haslayer(Ether) and pkt.haslayer(TCP):
                src_mac = pkt[Ether].src
                tcp_len = len(pkt[TCP].payload)
                print(f"[*] [HINT] Possibile flag formato metadati: flag{{{src_mac}/{tcp_len}}}")

if __name__ == "__main__":
    # Controlla se l'utente ha passato il file da terminale
    if len(sys.argv) < 2:
        print("\n[!] Errore: Nessun file specificato.")
        print("Uso corretto: python cyber_solver.py nome_sfida.pcapng")
    else:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            beast_mode_resolver(file_path)
        else:
            print(f"[!] Errore: Il file '{file_path}' non esiste nella cartella corrente.")
