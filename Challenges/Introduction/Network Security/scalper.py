import sys
import os
import re
from scapy.all import *

# Disabilita i messaggi di log di Scapy per un output pulito
conf.verb = 0

def scalper_scan(pcap_file):
    print(f"\n" + "="*60)
    print(f"[*] SCALPER V2: Analisi Omnicomprensiva di {pcap_file}")
    print("="*60)

    try:
        # Leggiamo i pacchetti
        packets = rdpcap(pcap_file)
    except Exception as e:
        print(f"[!] Errore nel caricamento del file: {e}")
        return

    flag_pattern = re.compile(r'flag\{.*?\}')

    for i, pkt in enumerate(packets):
        # --- 1. CHALLENGE 05: COMMENTI ---
        # Cerchiamo nei metadati del pacchetto (pcapng)
        if hasattr(pkt, 'comment') and pkt.comment:
            comment_text = pkt.comment.decode(errors='ignore') if isinstance(pkt.comment, bytes) else pkt.comment
            print(f"[!!!] FLAG/INFO TROVATA NEI COMMENTI (Pkt #{i+1}): {comment_text}")

        # --- 2. CHALLENGE 04: FILTRI DNS & IP ---
        if pkt.haslayer(DNSQR):
            query_name = pkt[DNSQR].qname.decode()
            # Se la richiesta viene dall'IP specifico della sfida
            if pkt.haslayer(IP) and pkt[IP].src == "192.168.100.3":
                print(f"[DNS] Richiesta da 192.168.100.3: {query_name}")
            elif "flag" in query_name.lower():
                print(f"[DNS] Query sospetta trovata: {query_name}")

        # --- 3. CHALLENGE 01/03: RICERCA TESTUALE ---
        # Converte il pacchetto in stringa per trovare flag{...}
        raw_pkt = str(pkt.show(dump=True))
        found_flags = flag_pattern.findall(raw_pkt)
        for f in found_flags:
            print(f"[+] [Pkt #{i+1}] FLAG TROVATA NEL TESTO: {f}")

        # --- 4. CHALLENGE 02: METADATI FRAME 4 ---
        if i == 3: # Frame 4
            if pkt.haslayer(Ether):
                src_mac = pkt[Ether].src
                tcp_len = len(pkt[TCP].payload) if pkt.haslayer(TCP) else 0
                print(f"[*] [PKT 4] MAC: {src_mac} | TCP Len: {tcp_len}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scalper.py <file.pcapng>")
    else:
        scalper_scan(sys.argv[1])
