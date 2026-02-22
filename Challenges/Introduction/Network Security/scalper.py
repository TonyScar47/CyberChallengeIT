import sys
import os
import re
from scapy.all import *

# Disabilita i messaggi di log di Scapy per un output pulito
conf.verb = 0

def scalper_scan(pcap_file):
    print(f"\n" + "="*60)
    print(f"[*] SCALPER V3.2: CyberChallenge Solver - {pcap_file}")
    print("="*60)

    try:
        # Caricamento pacchetti
        packets = rdpcap(pcap_file)
    except Exception as e:
        print(f"[!] Errore nel caricamento del file: {e}")
        return

    flag_pattern = re.compile(r'flag\{.*?\}')
    target_string = "Pwn all the things!!!"

    for i, pkt in enumerate(packets):
        # --- CHALLENGE 05: COMMENTI (Filtri 3) ---
        if hasattr(pkt, 'comment') and pkt.comment:
            comment_text = pkt.comment.decode(errors='ignore') if isinstance(pkt.comment, bytes) else pkt.comment
            print(f"[!!!] COMMENTO (Pkt #{i+1}): {comment_text}")

        # --- CHALLENGE 04: DNS (Filtri 2) ---
        if pkt.haslayer(DNSQR):
            query_name = pkt[DNSQR].qname.decode()
            if pkt.haslayer(IP) and pkt[IP].src == "192.168.100.3":
                print(f"[DNS] Query da 192.168.100.3: {query_name}")

        # --- CHALLENGE 06: RICERCA STRINGA E IP (Filtri 4) ---
        # Cerchiamo la stringa "Pwn all the things!!!" nel pacchetto
        if target_string.encode() in bytes(pkt):
            print(f"\n[🎯] TARGET INDIVIDUATO (Pkt #{i+1})")
            if pkt.haslayer(IP):
                src_ip = pkt[IP].src
                dst_ip = pkt[IP].dst
                print(f"[>] Mittente (Source IP): {src_ip}")
                print(f"[>] Destinatario (Dest IP): {dst_ip}")
                print(f"[✅] PROVA QUESTA FLAG: flag{{{src_ip}}}")

        # --- RICERCA FLAG STANDARD (Regex) ---
        raw_pkt_str = str(pkt.show(dump=True))
        found_flags = flag_pattern.findall(raw_pkt_str)
        for f in found_flags:
            print(f"[+] [Pkt #{i+1}] FLAG TROVATA: {f}")

        # --- CHALLENGE 02: METADATI FRAME 4 ---
        if i == 3 and pkt.haslayer(Ether):
            src_mac = pkt[Ether].src
            tcp_len = len(pkt[TCP].payload) if pkt.haslayer(TCP) else 0
            print(f"[*] [PKT 4] MAC: {src_mac} | TCP Len: {tcp_len}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scalper.py <file.pcapng>")
    else:
        scalper_scan(sys.argv[1])
