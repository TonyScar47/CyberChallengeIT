import sys
import os
import re
from scapy.all import *

conf.verb = 0

def scalper_scan(pcap_file):
    print(f"\n" + "="*60)
    print(f"[*] SCALPER V4: Ultimate Strings Extractor - {pcap_file}")
    print("="*60)

    try:
        packets = rdpcap(pcap_file)
    except Exception as e:
        print(f"[!] Errore nel caricamento: {e}")
        return

    # REGEX UNIVERSALE: Cerca qualsiasi parola seguita da { ... } 
    # (Esempio: CCIT{flag_qui}, flag{123}, test{abc})
    universal_flag_pattern = re.compile(r'[a-zA-Z0-9_]+\{.*?\}')
    target_string = "Pwn all the things!!!"

    for i, pkt in enumerate(packets):
        
        # --- ESTRAZIONE "STRINGS-LIKE" ---
        # Prendiamo l'intero pacchetto grezzo e forziamo la decodifica in testo
        # Questo aggira qualsiasi troncamento fatto da Scapy!
        raw_text = bytes(pkt).decode('ascii', errors='ignore')

        # --- CHALLENGE 06 ---
        if target_string in raw_text:
            print(f"\n[🎯] TROVATA LA FRASE TARGET (Pacchetto #{i+1})")
            # Cerchiamo la flag esattamente dentro questo pacchetto grezzo
            flags_near = universal_flag_pattern.findall(raw_text)
            for f in flags_near:
                print(f"[✅] FLAG ESTRATTA: {f}")

        # --- RICERCA FLAG GLOBALE ---
        # Cerchiamo possibili flag in tutto il traffico
        found_flags = universal_flag_pattern.findall(raw_text)
        for f in found_flags:
            # Filtriamo falsi positivi troppo corti (es. if{1})
            if len(f) > 7:
                print(f"[+] [Pkt #{i+1}] Possibile Flag: {f}")

        # --- CHALLENGE 05: COMMENTI ---
        if hasattr(pkt, 'comment') and pkt.comment:
            comment_text = pkt.comment.decode(errors='ignore') if isinstance(pkt.comment, bytes) else pkt.comment
            print(f"[!!!] COMMENTO (Pkt #{i+1}): {comment_text}")

        # --- CHALLENGE 04: DNS ---
        if pkt.haslayer(DNSQR):
            query_name = pkt[DNSQR].qname.decode(errors='ignore')
            if pkt.haslayer(IP) and pkt[IP].src == "192.168.100.3":
                print(f"[DNS] Query da Target: {query_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scalper.py <file.pcapng>")
    else:
        scalper_scan(sys.argv[1])
