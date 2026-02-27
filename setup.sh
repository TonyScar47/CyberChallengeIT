#!/bin/bash

# ==============================================================================
# ARCH LINUX AUTOMATION SETUP FOR CYBERCHALLENGE
# ------------------------------------------------------------------------------
# IDEMPOTENT SCRIPT: Safe to run multiple times.
# STRICT MODE: The script will abort immediately if any command fails.
# ==============================================================================

# Stop script on error (Safety First!)
set -e

# Define Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "---  STARTING AUTOMATION: IDEMPOTENT SETUP ---"

# 1. System Update
echo "---  Step 1: Updating System (Safe Update)... ---"
sudo pacman -Syu --noconfirm

# 1.5. Core Documentation (Guaranteed Installation)
echo "---  Step 1.5: Installing Core Documentation (man pages)... ---"
sudo pacman -S --needed --noconfirm man-db man-pages

# 2. Install Tools by CyberChallenge Macro-Categories
echo "---  Step 2: Installing Tools by CTF Categories... ---"

# --- BASE SYSTEM & DEV ---
echo "[*] Installing Base & Dev tools..."
sudo pacman -S --needed --noconfirm git base-devel code python python-pip fastfetch virtualbox-guest-utils docker-compose

# --- WEB SECURITY ---
# ffuf: Fast web fuzzer for directory discovery
# sqlmap: Automatic SQL injection and database takeover tool
echo "[*] Installing Web Security tools..."
sudo pacman -S --needed --noconfirm ffuf sqlmap

# --- NETWORK SECURITY ---
# nmap: Network exploration tool and security / port scanner
# wireshark-qt: Network protocol analyzer
# tcpdump: Command-line packet analyzer
# bind: DNS utilities (contains 'dig' and 'host')
# openbsd-netcat: The "Swiss army knife" for networking (nc)
echo "[*] Installing Network Security tools..."
sudo pacman -S --needed --noconfirm nmap wireshark-qt tcpdump bind openbsd-netcat

# --- CRYPTOGRAPHY ---
# john: John the Ripper (password cracker)
# hashcat: Advanced password recovery utility
echo "[*] Installing Cryptography tools..."
sudo pacman -S --needed --noconfirm john hashcat

# --- SOFTWARE SECURITY (Pwn & Reverse Engineering) ---
# gdb: The GNU Debugger (essential for Binary Exploitation)
# strace / ltrace: Trace system calls and library calls
# radare2: Advanced command-line reverse engineering framework
# binwalk: Tool for searching binary images for embedded files/signatures
echo "[*] Installing Software Security tools..."
sudo pacman -S --needed --noconfirm gdb strace ltrace radare2 binwalk

# --- HARDWARE SECURITY ---
# minicom: Serial communication program (used to interface with hardware via UART)
# flashrom: Utility for reading/writing/verifying flash ROM chips
echo "[*] Installing Hardware Security tools..."
sudo pacman -S --needed --noconfirm minicom flashrom

# --- CRYPTOGRAPHY PROTOCOLS ---
# Usually analyzed theoretically or via custom Python scripts (pycryptodome).
# Left empty for future custom additions. 

# Setup Wireshark permissions
# Add user to wireshark group to allow packet capturing without root
echo "---  Configuring Wireshark Permissions... ---"
sudo usermod -aG wireshark $USER

# --- Man page color configuration ---
MAN_COLORS="
# Man colors configuration
export LESS_TERMCAP_mb=$'\e[1;31m'
export LESS_TERMCAP_md=$'\e[1;36m'
export LESS_TERMCAP_me=$'\e[0m'
export LESS_TERMCAP_se=$'\e[0m'
export LESS_TERMCAP_so=$'\e[01;44;33m'
export LESS_TERMCAP_ue=$'\e[0m'
export LESS_TERMCAP_us=$'\e[1;32m'"

if ! grep -q "LESS_TERMCAP_mb" ~/.bashrc; then
    echo "$MAN_COLORS" >> ~/.bashrc
    echo "Man page colors configured."
fi

# --- Virtual Environment Setup for Python CTF Tools ---
echo "---  Step 3: Setting up Python Virtual Environment... ---"
if [ ! -d "venv" ]; then
    python -m venv venv
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

# Install python modules inside the venv
# Added 'pwntools' (Software Sec) and 'pycryptodome' (Cryptography)
echo "---  Installing Python tools in venv... ---"
./venv/bin/pip install --upgrade pip
./venv/bin/pip install exrex rstr requests scapy pwntools pycryptodome

# 4. Global Git Configuration
echo "---  Step 4: Configuring Global Git Settings... ---"
git config --global credential.helper store

# 5. Clean Cache
echo "---  Step 5: Cleaning Package Cache... ---"
sudo pacman -Sc --noconfirm

# 6. Final Success Message
echo ""
echo "----------------------------------------------------------------"
echo -e "${GREEN}  ACCESS GRANTED. SYSTEM READY.${NC}"
echo -e "${GREEN}  ALL TOOLS INSTALLED SUCCESSFULLY.${NC}"
echo -e "${GREEN}  GLHF (Good Luck Have Fun) & HAPPY HACKING! 💀${NC}"
echo "----------------------------------------------------------------"

# Show System Info
fastfetch

echo ""
echo " PYTHON VENV REMINDER:"
echo "To use your tools (like pwntools), run: source venv/bin/activate"
echo "then run: deactivate"
