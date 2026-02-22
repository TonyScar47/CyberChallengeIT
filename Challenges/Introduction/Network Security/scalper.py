import sys
import os
import re
from scapy.all import *

conf.verb = 0

def scalper_scan(pcap_file):
    print(f"\n" + "="*60)
    print(f"[*] SCALPER V3: CyberChallenge Hunter Mode - {pcap_file}")
    print("="*60)

    try:
        packets = rdpcap(pcap_file)
    except Exception as e:
        print(f"[!] Errore: {e}")
        return

    # Pattern per le flag classiche
    flag_pattern = re.compile(r'flag\{.*?\}')
    # Pattern specifico per la sfida Network 06
    target_string = "Pwn all the things!!!"

    for i, pkt in enumerate(packets):
        # --- CHALLENGE 05: COMMENTI ---
        if hasattr(pkt, 'comment') and pkt.comment:
            comment_text = pkt.comment.decode(errors='ignore') if isinstance(pkt.comment, bytes) else pkt.comment
            print(f"[!!!] COMMENTO (Pkt #{i+1}): {comment_text}")

        # --- CHALLENGE 04: DNS ---
        if pkt.haslayer(DNSQR):
            query_name = pkt[DNSQR].qname.decode()
            if pkt.haslayer(IP) and pkt[IP].src == "192.168.100.3":
                print(f"[DNS] Da 192.168.100.3: {query_name}")

        # --- CHALLENGE 06: RICERCA STRINGA SPECIFICA ---
        # Estraiamo i dati grezzi in modo più aggressivo
        raw_data = bytes(pkt)
        if target_string.encode() in raw_data:
            print(f"[FOUND] Stringa 'Pwn all the things!!!' nel pacchetto #{i+1}")
            print(f"[>>>] FLAG PER NETWORK 06: flag{{{target_string}}}")

        # --- RICERCA FLAG CLASSICHE ---
        raw_str = str(pkt.show(dump=True))
        found_flags = flag_pattern.findall(raw_str)
        for f in found_flags:
            print(f"[+] [Pkt #{i+1}] FLAG TROVATA: {f}")

        # --- CHALLENGE 02: METADATI ---
        if i == 3 and pkt.haslayer(Ether):
            print(f"[*] [PKT 4] MAC: {pkt[Ether].src} | TCP Len: {len(pkt[TCP].payload) if pkt.haslayer(TCP) else 0}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scalper.py <file.pcapng>")
    else:
        scalper_scan(sys.argv[1])
