# 🏆 CyberChallenge Attack/Defense Cheatsheet

Questo documento contiene i passaggi fondamentali da eseguire nei primi 15-30 minuti di una gara Attack/Defense.

## 🟢 Fase 0: Connessione e Setup Rete
Appena viene dato il via alla gara, la prima cosa è stabilire e verificare la connessione alla VPN.

- **Avviare la VPN:**
  
  ```bash
  sudo wg-quick up /percorso_del_file_configurazione.conf
  ```
  
- **Verificare la connessione e il proprio IP:**
      
  ```bash
  sudo wg             # Mostra lo stato di WireGuard
  ip addr show        # Trova il tuo IP assegnato sulla rete di gara
  ```
  
- **Testare la raggiungibilità del Game Server:**
  
  ```bash
  ping 10.60.5.1
  ```

## 🔑 Fase 1: Accesso e Persistenza
Evitare di inserire la password decine di volte ti farà risparmiare tempo prezioso.

- **Generare la chiave SSH (se non l'hai già fatto sul tuo PC locale):**
  
  ```bash
  ssh-keygen
  cat file       #copia tutta la riga
  ```
  
- **Accedere alla VulnBox (Terminale di Gara):**
      
  ```bash
  ssh root@<Indirizzo_IP_Ufficiale_VulnBox>
  ```
  
- **Autorizzare la propria chiave SSH sulla VulnBox:**
  
  ```bash
  # Sulla VulnBox
  mkdir -p ~/.ssh
  nano .ssh/authorized_keys 
  # Incolla la tua chiave pubblica, poi premi: Ctrl+X, Y, Invio
  ```
  
- **Pulizia (!IN CASO DI ERRORI):**
  
  ```bash
  rm "/percorso_indicato_dalle_istruzioni" 
  ```

## 🛡️ Fase 2: Backup e Discovery (IMPORTANTE)
Prima di toccare *qualsiasi* cosa, fai un backup dei servizi vergini. Se "rompi" un servizio cercando di patcharlo, perderai punti SLA (Service Level Agreement).

- **Individuare i servizi in esecuzione:**
  
  ```bash
  # Controlla quali container Docker stanno girando e su quali porte
  docker ps
  ```
  
- **Backup dei servizi vergini:**
  
  ```bash
  # Identifica la cartella dove si trovano i sorgenti dei servizi (es. /opt, /var/www, ecc.)
  tar -czvf /root/backup_servizi_vergini.tar.gz /percorso/sorgenti/servizi
  ```
  
- **Scaricare i sorgenti in locale (sul tuo PC Arch):**
  
  ```bash
  scp root@<Indirizzo_IP_Ufficiale_VulnBox>:/root/backup_servizi_vergini.tar.gz .
  ```

## Exploit Template

```python
#!/usr/bin/env python3

from exploitfarm import *
import requests
from pwn import *

SERVICE = "<service>"
PORT = 0000
DEBUG = False

HOST = get_host()
store = Store()
req = session(random_agent=False, user_agent="checker")


def get_ids():
    team_id = HOST.split(".")[2]
    flag_ids = requests.get(
        f"http://10.10.0.1:8081/flagIds?service={SERVICE}&team={team_id}"
    ).json()[SERVICE][team_id]

    if DEBUG:
        print(flag_ids)

    return flag_ids


def attack(flag_id):
    # You can start pwning here (change Service and Port)
    # Use "req"!!
    pass


if __name__ == "__main__":
    flag_ids = get_ids()

    for round, f in flag_ids.items():
        if not store.get(f"{HOST}_{round}"):
            attack(f)
            store.set(f"{HOST}_{round}", True)
```

## Digger

[work in progress]
