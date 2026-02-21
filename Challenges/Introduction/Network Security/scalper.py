from scapy.all import *
import re
import binascii
import os

# Creiamo una cartella per i file estratti
if not os.path.exists("extracted_files"):
    os.makedirs("extracted_files")

def extract_http_payload(packet):
    """Estrae e salva file dai payload HTTP"""
    try:
        if packet.haslayer(Raw) and packet.haslayer(TCP):
            load = packet[Raw].load
            if b"Content-Type" in load:
                # Proviamo a salvare il payload in un file
                filename = f"extracted_files/payload_pkt_{packet.summary()[:20]}.bin"
                with open(filename, "wb") as f:
                    f.write(load)
                return f"[!] File estratto salvato come: {filename}"
    except:
        pass
    return None

def check_base64(string):
    """Tenta di decodificare possibili flag in Base64"""
    try:
        # Cerca pattern che sembrano base64 (A-Za-z0-9+/=)
        potential = re.findall(r'[A-Za-z0-9+/]{10,}={0,2}', string)
        for p in potential:
            decoded = binascii.a2b_base64(p).decode('utf-8', errors='ignore')
            if "flag{" in decoded:
                return f"[FOUND B64] {decoded}"
    except:
        pass
    return None

def beast_mode_resolver(pcap_file):
    print(f"\n=== [ATTACK MODE ON] Analizzando: {pcap_file} ===")
    packets = rdpcap(pcap_file)
    flag_pattern = re.compile(r'flag\{.*?\}')

    for i, pkt in enumerate(packets):
        # 1. Analisi Testuale Profonda
        raw_content = str(pkt.show(dump=True))
        
        # Cerca flag in chiaro
        flags = flag_pattern.findall(raw_content)
        for f in flags:
            print(f"[*] [PKT {i}] FLAG TROVATA: {f}")

        # 2. Cerca Base64 nel payload
        if pkt.haslayer(Raw):
            b64_res = check_base64(pkt[Raw].load.decode(errors='ignore'))
            if b64_res:
                print(f"[+] [PKT {i}] {b64_res}")

        # 3. Analisi DNS (spesso usata per infiltrare flag)
        if pkt.haslayer(DNSQR):
            query = pkt[DNSQR].qname.decode()
            if "flag" in query:
                print(f"[!] [DNS] Query sospetta: {query}")

        # 4. Estrazione file (Carving)
        extraction = extract_http_payload(pkt)
        if extraction:
            print(extraction)

# Eseguiamo il mostro
for f in ['nw-intro01.pcap', 'nw-intro02.pcap', 'nw-intro03.pcapng']:
    if os.path.exists(f):
        beast_mode_resolver(f)
