#!/bin/bash

#Se hai problemi con il git da VSCode, vai sui tre pallini su VSCode
#(a destra di View in alto a sinistra) e apri il terminale. E scrivi prima
#"git pull origin main --rebase" e poi "git push origin main" e stai apposto.
#Tutto questo nel terminale di VSCode

echo "--- STARTING AUTOMATION ---"

#Update package repositories
sudo pacman -Sy

#Install essential programs
sudo pacman -S --noconfirm git base-devel code python python-pip nmap

#NICEEEE
echo "--- VM is up do date and ready for action! ---"