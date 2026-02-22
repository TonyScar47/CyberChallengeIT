import sys
import os
import re
import gzip
import subprocess
from scapy.all import *

conf.verb = 0

def scalper_scan(pcap_file, keylog_file=None):
    print(f"\n" + "="*60)
    print(f"[*] SCALPER V6: TLS Decryptor Edition - {pcap_file}")
    print("="*60)

    universal_flag_pattern = re.compile(r'[a-zA-Z0-9_]+\{.*?\}')

    # --- NEW: CHALLENGE 09 - DECIFRATURA TLS CON TSHARK ---
    if keylog_file and os.path.exists(keylog_file):
        print(f"[🔐] File chiavi TLS rilevato ({keylog_file}). Inizio decifratura profonda...")
        try:
            # Chiamiamo TShark chiedendogli di decifrare il traffico e stampare tutto in chiaro
            cmd = [
                'tshark', 
                '-r', pcap_file, 
                '-o', f'tls.keylog_file:{keylog_file}', 
                '-V' # Verbose: stampa tutto il contenuto decifrato
            ]
            
            # Eseguiamo il comando e catturiamo l'output
            result = subprocess.run(cmd, capture_output=True, text=True, errors='ignore')
            decrypted_text = result.stdout

            # Cerchiamo la flag in tutto il testo decifrato
            hidden_flags = universal_flag_pattern.findall(decrypted_text)
            if hidden_flags:
                print(f"\n[🎯] TRAFFICO DECIFRATO! TROVATE POSSIBILI FLAG:")
                for f in set(hidden_flags):
                    if len(f) > 7:
                        print(f"[✅] FLAG ESTRATTA DAL TLS: {f}")
                return # Se troviamo la flag nel traffico decifrato, fermiamo lo script
            else:
                print("[!] Decifratura completata ma nessuna flag trovata.")

        except FileNotFoundError:
            print("[!] ERRORE: TShark non è installato. Usa 'sudo pacman -S wireshark-cli'")
            return
        except Exception as e:
            print(f"[!] Errore durante la decifratura: {e}")

    # --- RESTO DELLO SCRIPT (Per le sfide dalla 01 alla 08) ---
    print("\n[*] Avvio scansione pacchetti standard (Scapy)...")
    try:
        packets = rdpcap(pcap_file)
    except Exception as e:
        print(f"[!] Errore caricamento Scapy: {e}")
        return

    for i, pkt in enumerate(packets):
        raw_bytes = bytes(pkt)
        raw_text = raw_bytes.decode('ascii', errors='ignore')

        # Controllo Gzip (Sfida 08)
        if b'\x1f\x8b\x08' in raw_bytes:
            idx = raw_bytes.find(b'\x1f\x8b\x08')
            try:
                dec_text = gzip.decompress(raw_bytes[idx:]).decode('ascii', errors='ignore')
                for hf in universal_flag_pattern.findall(dec_text):
                    print(f"[✅] FLAG GZIP (Pkt #{i+1}): {hf}")
            except: pass

        # Ricerca standard
        for f in universal_flag_pattern.findall(raw_text):
            if len(f) > 7: print(f"[+] POSSIBILE FLAG (Pkt #{i+1}): {f}")

        # Commenti (Sfida 05)
        if hasattr(pkt, 'comment') and pkt.comment:
            print(f"[!!!] COMMENTO (Pkt #{i+1}): {pkt.comment.decode(errors='ignore') if isinstance(pkt.comment, bytes) else pkt.comment}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso standard: python scalper.py <file.pcapng>")
        print("Uso con TLS : python scalper.py <file.pcapng> <tls-keys.txt>")
    else:
        pcap = sys.argv[1]
        keys = sys.argv[2] if len(sys.argv) > 2 else None
        
        # Auto-detect file chiavi se l'utente si dimentica di passarlo
        if not keys and os.path.exists("tls-keys.txt"):
            keys = "tls-keys.txt"
            
        scalper_scan(pcap, keys)
