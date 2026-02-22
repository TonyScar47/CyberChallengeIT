import sys
import os
import re
import gzip
from scapy.all import *

# Disabilita i log fastidiosi
conf.verb = 0

def scalper_scan(pcap_file):
    print(f"\n" + "="*60)
    print(f"[*] SCALPER V5: Ultimate CTF Swiss Army Knife - {pcap_file}")
    print("="*60)

    try:
        packets = rdpcap(pcap_file)
    except Exception as e:
        print(f"[!] Errore nel caricamento: {e}")
        return

    universal_flag_pattern = re.compile(r'[a-zA-Z0-9_]+\{.*?\}')
    target_string_06 = "Pwn all the things!!!"

    for i, pkt in enumerate(packets):
        
        # Estraggo i dati binari grezzi del pacchetto
        raw_bytes = bytes(pkt)
        raw_text = raw_bytes.decode('ascii', errors='ignore')

        # --- NEW: CHALLENGE 08 - ESTRAZIONE FILE COMPRESSI (GZIP/TAR) ---
        # Gzip inizia sempre con i byte magici 1f 8b 08
        if b'\x1f\x8b\x08' in raw_bytes:
            # Trova dove inizia il file compresso
            idx = raw_bytes.find(b'\x1f\x8b\x08')
            gz_data = raw_bytes[idx:]
            try:
                # Decomprime al volo
                decompressed = gzip.decompress(gz_data)
                dec_text = decompressed.decode('ascii', errors='ignore')
                
                print(f"\n[📦] FILE COMPRESSO TROVATO E DECOMPRESSO NEL PACCHETTO #{i+1}")
                # Cerca la flag nel file decompresso
                hidden_flags = universal_flag_pattern.findall(dec_text)
                for hf in hidden_flags:
                    print(f"[✅] FLAG NASCOSTA NEL FILE COMPRESSO: {hf}")
            except Exception as e:
                pass # Se non è un gzip valido, ignora

        # --- CHALLENGE 06 ---
        if target_string_06 in raw_text:
            print(f"\n[🎯] TROVATA LA FRASE TARGET (Pacchetto #{i+1})")
            if pkt.haslayer(IP):
                print(f"[>] IP da usare per la flag: {pkt[IP].src}")
            # Cerca flag vicine
            flags_near = universal_flag_pattern.findall(raw_text)
            for f in flags_near:
                print(f"[+] FLAG: {f}")

        # --- RICERCA FLAG GLOBALE (Challenge 01, 03, ecc.) ---
        found_flags = universal_flag_pattern.findall(raw_text)
        for f in found_flags:
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

        # --- CHALLENGE 02: METADATI FRAME 4 ---
        if i == 3 and pkt.haslayer(Ether):
            src_mac = pkt[Ether].src
            tcp_len = len(pkt[TCP].payload) if pkt.haslayer(TCP) else 0
            print(f"[*] [PKT 4] Hint Challenge 02 -> MAC: {src_mac} | TCP Len: {tcp_len}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scalper.py <file.pcapng>")
    else:
        scalper_scan(sys.argv[1])
